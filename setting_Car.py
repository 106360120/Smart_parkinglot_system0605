# -- coding:UTF-8 --<code>
import time
from setting_Manage import ParkManage

class Car():
    """一個關於車的類"""
    def __init__(self,car_number,reserved_time,User_uid,order_number):
        super(Car, self).__init__()
        self.car_number=car_number
        #self.car_owner=car_owner
        #self.contact_way=contact_way
        self.balance=0
        self.entrance_time = 0
        self.exit_time = 0
        self.should_leave_time = 0
        self.reserved_time = reserved_time
        self.User_uid = User_uid
        self.order_number = order_number


    def __setitem__(self, key, value):
        self.__dict__[key]=value

    def slot_card(self):
        """根據時間計費"""
        print(self.entrance_time)
        print(self.exit_time)
        park_time = self.exit_time - self.entrance_time
        #park_time=time.mktime(time.strptime(self.exit_time)) - time.mktime(
         #   time.strptime(self.entrance_time))
        d=park_time//86400
        h=(park_time-d*86400)//3600
        m=((park_time-d*86400)-h*3600)//60
        s=park_time-d*86400-h*3600-m*60
        P_time="%.0f時%.0f分%.0f秒"%(h,m,s)
        if s > 0:
            m=m+1
            s=0
            if m > 0:
                h=h+1
                m=0
                if h>=8:
                    d=d+1
                    h=0
        else:
            s=0
        consumption = d*240 + h*30
        a = []
        self.balance -= consumption
        a.append(self.balance)
        a.append(consumption)
        a.append(park_time)
        return a
        
        print("車牌號為:%s\n停車時長:%s\n本次消費:%.2f元\n卡里餘額:%.2f元\n" % (self.car_number,P_time, self.pay, self.balance))

    def __str__(self): 
        '''將汽車資訊顯示成字串'''
        return "%s %s " %(self.car_number,self.entrance_time)
