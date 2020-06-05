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
    print(entrance_plate)
    reservation_plate = data_action.firebase_Read_Reserved_Car(entrance_plate) #reservation_time
    print(reservation_plate)
    GPIO.output(19,GPIO.LOW)
    if entrance_plate == reservation_plate:
        GPIO.output(13,GPIO.HIGH) #entrance_gate open
        lcd_car_in(entrance_plate)
        
        car = Car(entrance_plate , data_action.firebase_Read_Reserved_time(entrance_plate))
        #time.sleep(1)
        GPIO.output(13,GPIO.LOW) #entrance_gate close
        data_action.firebase_Car_Enter_Add_and_Update(entrance_plate,'rJm10FH2PoYCE4iKuMfwD8LECBf106051242')
        parkmanage.add_car(car) 
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
    reservation_plate = data_action.firebase_Read_Reserved_Car(exit_plate) #reservation_time
    print(reservation_plate)
    
    GPIO.output(20,GPIO.LOW)
    #print(parkmanage.car_list)
    
    for car in parkmanage.car_list:
        
        if car.car_number == exit_plate:
            
            
            #time = data_action.get_paid_time(exit_plate)
            GPIO.output(16,GPIO.HIGH) #exit_gate open
            lcd_car_out(exit_plate)
            #flag = parkmanage.check_ten_minute(car,time)
            
            #if flag:
                #open the door
            GPIO.output(16,GPIO.LOW) #exit_gate close
            data_action.firebase_Car_Exit_and_Update(exit_plate,'rJm10FH2PoYCE4iKuMfwD8LECBf106051242')
            parkmanage.delete_car(car)
            read_remain_place = data_action.check_remain_place()
            now_place = data_action.remain_place_sub(read_remain_place)
            #show_remain_place(int(now_place))
            #sleep(3)
            
            
            print("Car out complete")
            
            
            break
            
        else:
            print("未找到車牌號為%s的車輛" % (exit_plate))
    #data_action.check_user_paid(str(exit_plate))#bug1
    
    
    
    
    #should_exit_time = check_user_paid time - get_reserved_time
    
    #if should_exit_time > 10min:
     #count_again(True)
    #else
      #count_again(False)
    #data_action.firebase_Car_Exit_and_Update(plate,exit_time)
    #print("Car out complete")



def main():
    # 建立 2 個子執行緒
    parkmanage = ParkManage()
    while True:
        #if 訂單完成 ==True
        #print(GPIO.input(shot))
        #data_action.on_snapshot()
        Carin = GPIO.input(21)
        Carout = GPIO.input(26)
        print(Carin)
        print(Carout)
        if GPIO.event_detected(21):
            if data_action.firebase_Read_Using_Car() == False:
                if data_action.firebase_Read_Order_complete() == False:
                    Carin_job(parkmanage)
            # 執行該子執行緒
            #  thread1 = threading.Thread(target=Carin_job, name='T1')
            #             thread1.start()
            #             thread1.join()
                     
        else:
            Carin = GPIO.input(21)
            
        if GPIO.event_detected(26):
            if data_action.firebase_Read_Using_Car() == True:
                Carout_job(parkmanage)
            # 執行該子執行緒
            #thread2 = threading.Thread(target=Carout_job, name='T2')
            #thread2.start()
            #thread2.join()
        
                    
        else:
            Carout = GPIO.input(26)
    
    
        #else:
            #print("no car")
            #time.sleep(1) 
            #GPIO.cleanup()
        #parkmanage=ParkManage()
        
    
            #recognize_and_indicate(picture_path)
                
    
            #make_photo()
            
    
    
    
    
            # 指定var接受使用者輸入的指令
            #var = int(input('Enter 1 – 9: '))
            #寫入使用的輸入的指令Var
            #writeNumber(var)
            #print ('RPI: Hi Arduino, I sent you ', var)
            #接收Arduino回傳的訊息
            #number = readNumber()
            #print(GPIO.input(shot))

                #print (' Hey Arduino, I received a digit ', number)
        
                
                #35行新增拍照程式,現在先固定照片
                
                #make_photo()
                #car_number=recognize_and_indicate(picture_path)
                
                #for plate in reservation_plate:
                    
                     #if plate == car_number:        
                        #check_error_list=[]
                
                #if check_car_number(car_number):
                    #car_owner=input("請輸入車主姓名:")
                    #contact_way=input("請輸入車主聯絡方式:")
                    #if check_contact_way(contact_way):
                        #check_error_list=[car_number,car_owner,contact_way]
                        #for info in check_error_list:    #判斷輸入資訊的完整性
                            #if info=='':
                                #print("輸入資訊不全")
                                #break
                        #else:
                            #car = Car(car_number, car_owner, contact_way)
                            #parkmanage.add_car(car)
                    #else:
                        #print("手機號無效")
                #else:
                    #print("車牌號不合法")
                
    '''
            if choice=='2':
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
                print("歡迎下次使用！！！")
                exit()
            elif choice=='8':
                parkmanage.info() #menu
               
            else:
                print("請輸入正確的選項")
    '''
if __name__ == '__main__':
    
    #main()
    '''
    車牌經由辨識取得
    '''
    parkmanage = ParkManage()
    Carin_job(parkmanage)
    
    Carout_job(parkmanage)
    

        



        
