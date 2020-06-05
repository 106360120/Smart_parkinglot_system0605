# -- coding:UTF-8 --<code>
import time
import datetime
from firebase_action import firebase_action as data_action

class ParkManage(object):
    """建立一個關於停車的類"""
    def __init__(self,max_car=3,):  #定義最大停車輛數
        self.max_car=max_car
        self.car_list = []
        self.cur_car=len(self.car_list)


    def info(self):
        """ #顯示系統功能資訊"""
        print("""
        —————————————————————————
        |***歡迎進入車輛管理系統***|
        —————————————————————————    
{1}                                    
{2}           1)新增車輛資訊{3}{2}
{0}                                  
{2}           2)查詢車輛資訊{3}{2}
{0}
{2}           3)顯示車輛資訊{3}{2}
{0}
{2}           4)編輯車輛資訊{3}{2}
{0}
{2}           5)刪除車輛資訊{3}{2}
{0}
{2}           6)統計車輛資訊{3}{2}
{0}
{2}              7)退出系統{3}{2}
{1}
        """.format("-"*40,"="*40,"|"," "*16))

    def add_car(self,car):
        """#新增車輛資訊"""
        entrance_time = time.time() #計時開始
        car["entrance_time"]=entrance_time
        
        entrance_time_2 = datetime.datetime.now().replace(tzinfo=None)
        reserved_time  = car.reserved_time.replace(tzinfo=None)
        delay_time = (entrance_time_2 - reserved_time).seconds
        car["order"] = data_action.firebase_Read_Reserved_Car_Order(car.car_number)
        print(car.order)
        car.balance = data_action.firebase_Read_Users_Balance(car.order)
        
        for Car in self.car_list:
            if Car.car_number == car.car_number or delay_time>1800:
                print("車牌號資訊有誤，重新輸入")
                break
        else:
            if delay_time > 900:
                car.balance -= 30 #1hr fee
            data_action.firebase_Car_Enter_Add_and_Update(car.car_number,car.order) #modify database
            self.car_list.append(car)
            print("車牌號為%s的車入庫成功" %car.car_number)

    def search_By_Number(self):
        """#按車牌號查詢"""
        car_number=input("請輸入你您要查詢的車牌號：")
        for car in self.car_list:
            if car.car_number==car_number:
                print(car)
                break
        else:
            print("未找到車牌號為%s的車輛" %car_number)


    def searchCar(self):
        """#查詢車輛資訊"""
        self.search_By_Number()



    def display(self):
        """#顯示車車輛資訊"""
        if len(self.car_list)!=0:
            for car in self.car_list:
                print(car)
        else:
            print("車庫為空")

    def change_Carinfo(self):
        """#修改車輛資訊"""
        car_number = input("請輸入你您要查詢的車牌號：")
        for car in self.car_list:
            if car.car_number == car_number:
                index=self.car_list.index(car)
                change=int(input("(修改資訊的序號:\n車主0,\n聯絡方式1)\n輸入你要修改的資訊序號："))
                if change==0:
                    new_info=input("輸入新的資訊：")
                    self.car_list[index].car_owner=new_info
                    print("車主名修改成功")
                    break
                elif change==1:
                    new_info=input("輸入新的資訊：")
                    self.car_list[index].contact_way=new_info
                    print("聯絡方式修改成功")
                    break
        else:
            print("未找到車牌號為%s的車輛" % car_number)
    '''
    def check_ten_minute(self,car,should_leave_time):
        exit_time=time.ctime()  #計時結束
        car["exit_time"]=exit_time
        #print (int((should_leave_time - exit_time).seconds))
        ex_time = datetime.datetime.now()
        print(ex_time)
        print(should_leave_time)
        naive1 = ex_time.replace(tzinfo=None)
        naive2 = should_leave_time.replace(tzinfo=None)
        print(naive1)
        print(naive2)
        
        delay_time = (naive2 - naive1).seconds
        
        print(delay_time)
        
        if  delay_time > 600:
            print('繳費時間超過')
            data_action.count_again(True)
            # send message to user !!
            return False
        else:
            print('go')
            return True
    '''
    def delete_car(self,car):
        """刪除車輛資訊"""
        exit_time=time.time()  #計時結束
        car["exit_time"]=exit_time
        rest_money = car.slot_card()
        print(car.order)
        data_action.firebase_Change_Users_Balance(car.order,rest_money)#modify database
        self.car_list.remove(car)
        print("車牌號為%s的車成功刪除"%car.car_number)


    def statistics(self):
        """統計車輛資訊"""
        sedan_car_number=0
        for car in self.car_list:
            if car.car_number!=' ':
                sedan_car_number+=1
        else:
            print("小汽車：%s\n"
                  %(sedan_car_number))
        rest_space = self.max_car-sedan_car_number
        print("剩餘車位%s" %rest_space)
