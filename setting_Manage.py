# -- coding:UTF-8 --<code>
import time
import datetime
from firebase_action import firebase_action as data_action
from auto_recognize import lcd_car_out
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
{2}              7)手動繳費{3}{2}
{0}
{2}              8)退出系統{3}{2}
{1}
        """.format("-"*40,"="*40,"|"," "*16))
 
    def add_car(self,car):
        """#新增車輛資訊"""
        entrance_time = time.time() #計時開始
        car["entrance_time"]=entrance_time
        
        entrance_time_2 = datetime.datetime.now().replace(tzinfo=None)
        reserved_time  = car.reserved_time.replace(tzinfo=None)
        delay_time = (entrance_time_2 - reserved_time).seconds
        car["User_uid"] = data_action.firebase_Read_Reserved_User_uid(car.car_number)
        print(car.User_uid)
        car.balance = data_action.firebase_Read_Users_Balance(car.User_uid)
        
        for Car in self.car_list:
            if Car.car_number == car.car_number: 
                print("車牌號資訊有誤，重新輸入")
                break
            if delay_time > 30:
                data_action.firebase_Car_Overtime_thirty()
        else:
            
            data_action.firebase_Car_Enter_Add_and_Update(car.car_number,car.User_uid,car.order_number) #modify database
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
        car_number = input("請輸入您要查詢的車牌號：")
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
        money_data = car.slot_card()
        rest_money = money_data[0]
        pay = money_data[1]
        total_time = money_data[2]
        print(car.User_uid)
        data_action.firebase_Change_Users_Balance_Time(car.User_uid,car.order_number,rest_money,pay,total_time)#modify database
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
    
    def pay_by_staff(self):
        """手動繳費"""
        car_number = input("請輸入您要的車牌號碼：")
        for car in self.car_list:
            if car.car_number == car_number:
                exit_time=time.time()  #計時結束
                car["exit_time"]=exit_time
                money_data = car.slot_card()
                print(money_data)
                rest_money = money_data[0]
                pay = money_data[1]
                total_time = money_data[2]
                print("應付金額：",pay)
                input_pay = eval(input("請輸入繳費金額："))
                if input_pay == pay:
                    print("謝謝光臨！")
                    lcd_car_out(car_number)
                    #data_action.firebase_Car_Exit_and_Update(car_number,car.User_uid,car.order_number)
                    self.car_list.remove(car)
                    print("車牌號為%s的車成功刪除"%car.car_number)
                else:
                    print("Money Not correct!")
#if __name__ == '__main__':
    
