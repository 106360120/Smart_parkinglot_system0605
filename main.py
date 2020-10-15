# -- coding:UTF-8 --<code>
from setting_Car import Car
from setting_Manage import ParkManage

from firebase_action import firebase_action as data_action
from lcd_library import my_lcd as lcd

from time import sleep

import re
import cv2
import sys
import RPi.GPIO as GPIO
import smbus
import time
import threading
import queue
from take_picture import make_photo
from auto_recognize import entrance_recognize_and_indicate
from auto_recognize import exit_recognize_and_indicate
from auto_recognize import lcd_car_in
from auto_recognize import lcd_car_out
from auto_recognize import show_remain_place
# 設定樹莓派I2C的總線
bus = smbus.SMBus(1)

# 設定Arduino 的I2C位置
address = 0x04
#設定樹莓派gpio腳位

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(26, GPIO.IN)
GPIO.setup(13, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(19, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(20, GPIO.OUT,initial=GPIO.LOW)
#GPIO.setup(21,GPIO.IN,initial=GPIO.LOW)
#GPIO.setup(26,GPIO.IN,initial=GPIO.LOW)
GPIO.add_event_detect(21, GPIO.RISING)
GPIO.add_event_detect(26, GPIO.RISING)
GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(shot, GPIO.IN)

# 傳送訊息
def writeNumber(value):
    bus.write_byte(address, value)
    return -1

# 讀取訊息
def readNumber():
    number = bus.read_byte(address)
    return number

def check_car_number(car_number):    #判斷車牌號是否合法
    #pattern = re.compile(u'[\u4e00-\u9fa5]?')
    pattern1 = re.compile(u'[A-Z]+')
    pattern2 = re.compile(u'[0-9]+')

    #match = pattern.search(car_number)
    match1 = pattern1.search(car_number)
    match2 = pattern2.search(car_number)
    if match1 and match2:
        return True
    else:
        return False
def check_contact_way(contact_way):   #判斷手機號是否合法
    pattern = re.compile(u'0[1|2|3|4|5|6|7|8|9]\d{8}$')

    match = pattern.search(contact_way)
    if match:
        return True
    else:
        return False

#entrance_time= ' 2020/05/08,12:30'
# 子執行緒的工作函數
def Carin_job(parkmanage):   
    print("Car in action")
    #lock = threading.lock()
    #lock.acquire()
    make_photo(10)
    GPIO.output(19,GPIO.HIGH)
    picture_path = "/home/pi/pytest/final_project/ea7the.jpg"
    entrance_plate = entrance_recognize_and_indicate(picture_path)
    
    reservation_plate = data_action.firebase_Read_Reserved_Car_licence(entrance_plate) #reservation_time
    
    GPIO.output(19,GPIO.LOW)
    
    if entrance_plate == reservation_plate[0] and reservation_plate[1] == True:
        GPIO.output(13,GPIO.HIGH) #entrance_gate open
        lcd_car_in(entrance_plate)
        User_uid = data_action.firebase_Read_Reserved_User_uid(entrance_plate)
        order_number = data_action.firebase_Read_Reserved_Car_Order_Number(entrance_plate)
        car = Car(entrance_plate , data_action.firebase_Read_Reserved_time(entrance_plate),User_uid,order_number)
        
        #time.sleep(1)
        GPIO.output(13,GPIO.LOW) #entrance_gate close
        data_action.firebase_Car_Enter_Add_and_Update(entrance_plate,User_uid,order_number)
        parkmanage.add_car(car)
        read_remain_place = data_action.check_remain_place()
        now_place = data_action.remain_place_sub(read_remain_place)
        print("Car in complete")

    else:
        print("You can't go in")
    
def Carout_job(parkmanage):
    print("Car out action")
    #global A,lock
    #lock.acquire()
    make_photo(10)
    GPIO.output(20,GPIO.HIGH)
    picture_path = "/home/pi/pytest/final_project/ea7the.jpg"
    exit_plate = exit_recognize_and_indicate(picture_path)
    reservation_plate = data_action.firebase_Read_Reserved_Car_licence(exit_plate) #reservation_time
    print(reservation_plate)
    
    GPIO.output(20,GPIO.LOW)
    #print(parkmanage.car_list)
    
    for car in parkmanage.car_list:
        
        if car.car_number == exit_plate:
            
            
            #time = data_action.get_paid_time(exit_plate)
            GPIO.output(16,GPIO.HIGH) #exit_gate open
            lcd_car_out(exit_plate)

            GPIO.output(16,GPIO.LOW) #exit_gate close
            data_action.firebase_Car_Exit_and_Update(exit_plate,car.User_uid,car.order_number)
            parkmanage.delete_car(car)
            read_remain_place = data_action.check_remain_place()
            now_place = data_action.remain_place_add(read_remain_place)
            #show_remain_place(int(now_place))
            #sleep(3)
            
            
            print("Car out complete")
            
            
            break
            
        else:
            print("未找到車牌號為%s的車輛" % (exit_plate))
            
def Carin_job_YA(parkmanage):   
    print("Car in action")
    #lock = threading.lock()
    #lock.acquire()
    tic = time.clock()
    make_photo(10)
    GPIO.output(19,GPIO.HIGH)
    picture_path = "/home/pi/pytest/final_project/5978YA.jpg"
    entrance_plate = entrance_recognize_and_indicate(picture_path)
    print(entrance_plate)
    
    reservation_plate = data_action.firebase_Read_Reserved_Car_licence(entrance_plate) #reservation_time
    
    GPIO.output(19,GPIO.LOW)
    
    if entrance_plate == reservation_plate[0] and reservation_plate[1] == True:
        GPIO.output(13,GPIO.HIGH) #entrance_gate open
        lcd_car_in(entrance_plate)
        User_uid = data_action.firebase_Read_Reserved_User_uid(entrance_plate)
        order_number = data_action.firebase_Read_Reserved_Car_Order_Number(entrance_plate)
        car = Car(entrance_plate , data_action.firebase_Read_Reserved_time(entrance_plate),User_uid,order_number)
        
        #time.sleep(1)
        GPIO.output(13,GPIO.LOW) #entrance_gate close
        data_action.firebase_Car_Enter_Add_and_Update(entrance_plate,User_uid,order_number)
        parkmanage.add_car(car)
        read_remain_place = data_action.check_remain_place()
        now_place = data_action.remain_place_sub(read_remain_place)
        print("Car in complete")
        toc = time.clock()
    
        print(toc-tic)
    else:
        print("You can't go in")
    
def Carout_job_YA(parkmanage):
    print("Car out action")
    #global A,lock
    #lock.acquire()
    make_photo(10)
    GPIO.output(20,GPIO.HIGH)
    picture_path = "/home/pi/pytest/final_project/5978YA.jpg"
    exit_plate = exit_recognize_and_indicate(picture_path)
    reservation_plate = data_action.firebase_Read_Reserved_Car_licence(exit_plate) #reservation_time
    print(reservation_plate)
    
    GPIO.output(20,GPIO.LOW)
    #print(parkmanage.car_list)
    
    for car in parkmanage.car_list:
        
        if car.car_number == exit_plate:
            
            
            #time = data_action.get_paid_time(exit_plate)
            GPIO.output(16,GPIO.HIGH) #exit_gate open
            lcd_car_out(exit_plate)

            GPIO.output(16,GPIO.LOW) #exit_gate close
            data_action.firebase_Car_Exit_and_Update(exit_plate,car.User_uid,car.order_number)
            parkmanage.delete_car(car)
            read_remain_place = data_action.check_remain_place()
            now_place = data_action.remain_place_add(read_remain_place)
            #show_remain_place(int(now_place))
            #sleep(3)
            
            
            print("Car out complete")
            
            
            break
            
        else:
            print("未找到車牌號為%s的車輛" % (exit_plate))
            

def hand_control(parkmanage):
    while True:
        parkmanage.info()
        choice=input("請輸入你要的功能:")
        if choice=='1':
            check_error_list=[]
            car_number=input("請輸入車牌號:")
            if check_car_number(car_number):
                Carin_job(parkmanage)
                print("Welcome")
                '''
                car_owner=input("請輸入車主姓名:")
                contact_way=input("請輸入車主聯絡方式:")
                order_number=str("admin")
                if check_contact_way(contact_way):
                    check_error_list=[car_number,car_owner,contact_way]
                    for info in check_error_list:    #判斷輸入資訊的完整性
                        if info=='':
                            print("輸入資訊不全")
                            break
                    else:
                        car = Car(car_number, car_owner, contact_way, order_number)
                        parkmanage.add_car(car)
                else:
                    print("手機號無效")
                '''
            else:
                print("車牌號不合法")

        elif choice=='2':
            parkmanage.searchCar()
        elif choice =='3':
            parkmanage.display()
        elif choice=='4':
            parkmanage.change_Carinfo()
        elif choice=='5':
            car_number = input("輸入您要刪除的車輛的車牌號：")
            for car in parkmanage.car_list:
                if car.car_number == car_number:
                    parkmanage.delete_car(car)
                    break
            else:
                print("未找到車牌號為%s的車輛" % (car_number))

        elif choice=='6':
            parkmanage.statistics()
        elif choice=='7':
            parkmanage.pay_by_staff()
            GPIO.output(16,GPIO.HIGH) #exit_gate open
            time.sleep(3)

            GPIO.output(16,GPIO.LOW) #exit_gate close
            
            #read_remain_place = data_action.check_remain_place()
            #now_place = data_action.remain_place_add(read_remain_place)
        elif choice=='8':
            print("歡迎下次使用！！！")
            break
        else:
            print("請輸入正確的選項")
            
def entrance_exit(parkmanage):           
    while True:
        #print(GPIO.input(shot))
        #data_action.on_snapshot()
        try:
            Carin = GPIO.input(21)
            Carout = GPIO.input(26)
            print(Carin,' ',Carout)
            #print(Carout) 
                
            if GPIO.event_detected(21):
                    
                print(data_action.firebase_Read_Reservating_Car())
                if data_action.firebase_Read_Reservating_Car() == True:
                        #if data_action.firebase_Read_Order_complete() == False:
                    #try:
                    Carin_job(parkmanage)
                       
            if GPIO.event_detected(26):
                    
                if data_action.firebase_Read_Using_Car() == True:
                    #try:
                    Carout_job(parkmanage)
        except KeyboardInterrupt:
            break
def entrance_exit_YA(parkmanage):           
    while True:
        #print(GPIO.input(shot))
        #data_action.on_snapshot()

        try:
            Carin = GPIO.input(21)
            Carout = GPIO.input(26)
            print(Carin,' ',Carout)
            #print(Carout) 
                
            if GPIO.event_detected(21):
                    
                print(data_action.firebase_Read_Reservating_Car())
                if data_action.firebase_Read_Reservating_Car() == True:
                        #if data_action.firebase_Read_Order_complete() == False:
                    #try:
                    Carin_job_YA(parkmanage)
                       
            if GPIO.event_detected(26):
                    
                if data_action.firebase_Read_Using_Car() == True:
                    #try:
                    Carout_job_YA(parkmanage)
        except KeyboardInterrupt:
            break
def main():
    # 建立 2 個子執行緒
    parkmanage = ParkManage()
    
    while True:
    
        mode = input("Mode:")
        if mode =='1':
            mode = '0'
            thread1 = threading.Thread(target=entrance_exit(parkmanage), name='T1')
            thread1.start()
            thread1.join()
            
        if mode =='2':
            mode = '0'
            thread2 = threading.Thread(target=hand_control(parkmanage), name='T2')
            thread2.start()
            thread2.join()
        if mode =='3':
            mode = '0'
            entrance_exit_YA(parkmanage)
        if mode =='4':
            mode = '0'
            remain_place = data_action.check_remain_place()
            reserved_car = data_action.firebase_Read_ParkingGridData()
            show_remain_place(remain_place,reserved_car)
        
                
            
    
if __name__ == '__main__':
    #GPIO.output(20,GPIO.HIGH)
    #time.sleep(1)
    #GPIO.output(20,GPIO.LOW)
    main()
    '''
    車牌經由辨識取得
    '''
    #parkmanage = ParkManage()
    #Carin_job(parkmanage)
    #Carout_job(parkmanage)
    

        



        
