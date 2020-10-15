import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime as dt
import time
import threading

cred = credentials.Certificate("car-project-b45b3-firebase-adminsdk-41ei0-555cf34e12.json")#('test-6a8a7-firebase-adminsdk-tgspq-f9a1230d6b.json')#
firebase_admin.initialize_app(cred)

db = firestore.client()
#讀取停車場預約的車輛數
def firebase_Read_ParkingGridData():
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid')
    docs = list(doc_ref.stream())
    
    '''
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    '''
    print('number of documents in collection: {}'.format(len(docs)))
    
    return len(docs)


def firebase_Read_Reservating_Car():
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').where(u'reservating', u'==', True).stream()
    #plate = []
    for doc in doc_ref:
        print("car information: {}".format(doc.to_dict()))

        if doc.to_dict()['reservating'] == True :
            return True
       
    
def firebase_Read_Using_Car():
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').where(u'using', u'==', True).stream()
    for doc in doc_ref:
        print("car information: {}".format(doc.to_dict()))
            
        if doc.to_dict()['using'] == True :
            return True

        #print(u'{} => {}'.format(doc.id, doc.to_dict()))
        #print(doc.to_dict()['預約中'])
        #if doc.to_dict()['使用中'] == True :
            #parking_dict_data[doc.id] = doc.to_dict()
            #return True
        #if doc.to_dict()['使用中'] == False :
            #parking_dict_data[doc.id] = doc.to_dict()
            #return False

    
    
def firebase_Read_Reserved_Car_licence(plate):
    parking_data = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate))
    parking_dict_data = {} #建立空辭典
    
    '''
    parking_data是一個  Generator object 也是一個 Iterator，帶有 __iter__ 和 __next__ attributes。
    可和外部進行雙向溝通，可以傳出也可以傳入值。
    '''
    try:
        parking_data = parking_data.get()
        #print("car information: {}".format(parking_data.to_dict()))
        read_reserved_car = parking_data.to_dict()['預約車牌']
        read_status = parking_data.to_dict()['reservating']
        a = []
        a.append(read_reserved_car)
        a.append(read_status)
        return a
    except:
        print('error')
    #print(read_reserved_car)
        
    
    '''
    print(parking_data)
    
    i = 0;
    for doc in parking_data:
        print(i)
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        print(doc.to_dict()['預約中'])
        if doc.to_dict()['預約中'] == True or doc.to_dict()['使用中'] == True :
            parking_dict_data[doc.to_dict()['預約車牌']] = doc.id
        i=i+1
        
            
    return parking_dict_data
    
def firebase_Read_Order_complete():
    parking_data = db.collection('users').document('rJm10FH2PoYCE4iKuMfwD8LECBf1').collection('record').document('rJm10FH2PoYCE4iKuMfwD8LECBf106020343')
    parking_dict_data = {} #建立空辭典
   
    try:
        parking_data = parking_data.get()
        #print("car information: {}".format(parking_data.to_dict()))
        read_order_complete = parking_data.to_dict()['訂單完成']
    except:
        print('error')
    return read_order_complete
    '''
def firebase_Read_Reserved_User_uid(plate):
    parking_data = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate))
    parking_dict_data = {} #建立空辭典
    
    '''
    parking_data是一個  Generator object 也是一個 Iterator，帶有 __iter__ 和 __next__ attributes。
    可和外部進行雙向溝通，可以傳出也可以傳入值。
    '''
    try:
        parking_data = parking_data.get()
        #print("car information: {}".format(parking_data.to_dict()))
        read_reserved_User_uid = parking_data.to_dict()['User_uid']
    except:
        print('error')
   
    return read_reserved_User_uid

def firebase_Read_Reserved_Car_Order_Number(plate):
    parking_data = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate))
    parking_dict_data = {} #建立空辭典
    '''
    parking_data是一個  Generator object 也是一個 Iterator，帶有 __iter__ 和 __next__ attributes。
    可和外部進行雙向溝通，可以傳出也可以傳入值。
    '''
    try:
        parking_data = parking_data.get()
        #print("car information: {}".format(parking_data.to_dict()))
        read_order_number = parking_data.to_dict()['訂單編號']
        #read_order = parking_data.to_dict()['User_uid']
        #a= []
        #a.append(read_order_number)
        #a.append(read_order)
    except:
        print('error')
    return read_order_number
    #return a 

def firebase_Read_Reserved_time(plate):
    parking_data = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate))
    parking_dict_data = {} #建立空辭典
    '''
    parking_data是一個  Generator object 也是一個 Iterator，帶有 __iter__ 和 __next__ attributes。
    可和外部進行雙向溝通，可以傳出也可以傳入值。
    '''
    try:
        parking_data = parking_data.get()
        #print("car information: {}".format(parking_data.to_dict()))
        read_time = parking_data.to_dict()['預約日期時間']
    except:
        print('error')
    return read_time


def firebase_Read_Users_Balance(User_uid):
    parking_data = db.collection(u'users').document(str(User_uid))
    parking_dict_data = {} #建立空辭典
    
    '''
    parking_data是一個  Generator object 也是一個 Iterator，帶有 __iter__ 和 __next__ attributes。
    可和外部進行雙向溝通，可以傳出也可以傳入值。
    '''
    try:
        parking_data = parking_data.get()
        #print("car information: {}".format(parking_data.to_dict()))
        read_balance = parking_data.to_dict()['錢包']
    except:
        print('error')
    return read_balance

def firebase_Change_Users_Balance_Time(User_uid,order_number,new_money,pay,total_time):
    doc_ref = db.collection(u'users').document(str(User_uid))
    doc_ref2 = db.collection(u'users').document(str(User_uid)).collection(u'record').document(str(order_number))
    try:
        #parking_data = doc_ref.get()
        doc = doc_ref.get()
        doc2 = doc_ref2.get()
        #print("car information: {}".format(parking_data.to_dict()))
    except:
        print('error')
        
    doc_ref.update({
        '錢包' : new_money,
        
    })    
    doc_ref2.update({
        '應付金額' : pay,
        'parking_total_sec' : total_time,
    })
    
def firebase_Car_Enter_Add_and_Update(plate,User_uid,order_number):
    parking_data = firebase_Read_ParkingGridData()
    parking_dict_data = {} #建立空辭典
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate))
    doc_ref2 = db.collection(u'users').document(str(User_uid)).collection(u'record').document(str(order_number))
    try:
        doc = doc_ref.get()
        doc2 = doc_ref2.get()
        print(u'Document data: {}'.format(doc.to_dict()))
        print(u'Document data: {}'.format(doc2.to_dict()))
    except:
        print(u'No such document!')
    
    doc_ref.update({
        'using' : True,
        'reservating' : False,
        
    })
    doc_ref2.update({
        'using' : True,
        'reservating' : False,
        
    })
def firebase_Car_Exit_and_Update(plate,User_uid,order_number):
    parking_data = firebase_Read_ParkingGridData()
    parking_dict_data = {} #建立空辭典
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate)).delete()
    doc_ref2 = db.collection(u'users').document(str(User_uid)).collection(u'record').document(str(order_number))
    try:
        #doc = doc_ref.get()
        doc2 = doc_ref2.get()
        #print(u'Document data: {}'.format(doc.to_dict()))
        print(u'Document data: {}'.format(doc2.to_dict()))
    except:
        print(u'No such document!')
        
    #doc_ref.update({
        #'使用中' : False,
        #'預約中' : False,
        #'訂單完成' : True,
    #})
    doc_ref2.update({
        'using' : False,
        'reservating' : False,
        '訂單完成' : True,
    })
    
def firebase_Car_Overtime_thirty():
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').where(u'reservating', u'==', True).stream()
    time2 = [];
    for doc in doc_ref:
        #print("car information: {}".format(doc.to_dict()))
        now = time.time()
        time2 = doc.to_dict()['預約日期時間']
        if now - time2.timestamp() > 60:#over time limit
            doc_ref2 = db.collection(u'users').document(doc.to_dict()['User_uid']).collection(u'record').document(doc.to_dict()['訂單編號'])
            try:   
                doc2 = doc_ref2.get()
                print(u'Document data: {}'.format(doc2.to_dict()))
                
                doc_ref2.update({
                                'using' : False,
                                'reservating' : False,
                                '訂單取消' : True,
                                'overtime_thirty' : True,
                    })
            except:
                print(u'No such document!')
                break
            
            db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(doc.to_dict()['預約車牌']).delete()            
def firebase_Car_Overtime_fifteen():
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').where(u'reservating', u'==', True).stream()
    time2 = [];
    for doc in doc_ref:
        #print("car information: {}".format(doc.to_dict()))
        now = time.time()
        time2 = doc.to_dict()['預約日期時間']
        if now - time2.timestamp() > 30:#over time limit
            doc_ref2 = db.collection(u'users').document(doc.to_dict()['User_uid']).collection(u'record').document(doc.to_dict()['訂單編號'])
            try:   
                doc2 = doc_ref2.get()
                print(u'Document data: {}'.format(doc2.to_dict()))
                
                doc_ref2.update({
                                'overtime_fifteen' : True,
                    })
            except:
                print(u'No such document!')
                break    
    
    '''
    parking_data = firebase_Read_ParkingGridData()
    parking_dict_data = {} #建立空辭典
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate)).delete()
    doc_ref2 = db.collection(u'users').document(str(User_uid)).collection(u'record').document(str(order_number))
    try:
        #doc = doc_ref.get()
        doc2 = doc_ref2.get()
        #print(u'Document data: {}'.format(doc.to_dict()))
        print(u'Document data: {}'.format(doc2.to_dict()))
    except:
        print(u'No such document!')
        
    #doc_ref.update({
        #'使用中' : False,
        #'預約中' : False,
        #'訂單完成' : True,
    #})
    doc_ref2.update({
        'using' : False,
        'reservating' : False,
        '訂單完成' : True,
    })
    
    1'''

def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(u'New car: {}'.format(change.document.id))
        elif change.type.name == 'MODIFIED':
            print(u'car info changed: {}'.format(change.document.id))
            check_user_paid(change.document.id)
            if True:
                get_paid_time(change.document.id)
                if firebase_Read_Using_Parking_Grid() == True:
                    count_again(True)
            
        elif change.type.name == 'REMOVED':
            print(u'Removed car: {}'.format(change.document.id))

def check_remain_place():
    parking_data = db.collection(u'reservatable parkinglot').document('北科大APP特約停車場').collection('info').document('detail_info')
    parking_dict_data = {} #建立空辭典
    
    '''
    parking_data是一個  Generator object 也是一個 Iterator，帶有 __iter__ 和 __next__ attributes。
    可和外部進行雙向溝通，可以傳出也可以傳入值。
    '''
    try:
        parking_data = parking_data.get()
        #print("car information: {}".format(parking_data.to_dict()))
        read_remain_place = parking_data.to_dict()['剩餘車位']
    except:
        print('error')
    return read_remain_place

def remain_place_add(read_remain_place):
    doc_ref = db.collection(u'reservatable parkinglot').document('北科大APP特約停車場').collection('info').document('detail_info')
    try:
        doc = doc_ref.get()
        read_remain_place = read_remain_place+1
            
    except:
        print(u'No such document!')
        
    
    doc_ref.update({
        '剩餘車位' : read_remain_place,
        
    })

def remain_place_sub(read_remain_place):
    doc_ref = db.collection(u'reservatable parkinglot').document('北科大APP特約停車場').collection('info').document('detail_info')
    try:
        doc = doc_ref.get()
        read_remain_place = read_remain_place-1
            
    except:
        print(u'No such document!')
        
    
    doc_ref.update({
        '剩餘車位' : read_remain_place,
        
    })

   
    
    
#寫成找訂單的形式   
def check_user_paid(plate):
    doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(str(plate))
    try:
        doc = doc_ref.get()
        #print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
    
    #print(doc.to_dict()['是否繳費完成'])
    if doc.to_dict()['是否繳費完成'] == True :
        print('please leave in 10 minutes')
        paid_time = doc.to_dict()['付費時間']
        return True
    if doc.to_dict()['是否繳費完成'] == False :
        print('please pay the parking fee')
        return False
            

    
def get_paid_time(plate):
    
    doc_ref = db.collection('reservatable parkinglot').document('北科大APP特約停車場').collection('parking grid').document(str(plate))
    try:
        doc = doc_ref.get()
        #print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
    
    paid_time = doc.to_dict()['付費時間']
    print(paid_time)
    should_leave_time = paid_time + datetime.timedelta(minutes=10)
    
    #print( int(time.mktime(should_leave_time)))
    print((should_leave_time-paid_time).seconds)
    return should_leave_time

def put_over_time(plate):    
    doc_ref = db.collection('reservatable parkinglot').document('北科大APP特約停車場').collection('parking grid').document(str(plate))
    try:
        doc = doc_ref.get()
        #print(u'Document data: {}'.format(doc.to_dict()))
    except google.cloud.exceptions.NotFound:
        print(u'No such document!')
    
    paid_time = doc.to_dict()['付費時間']
    print(paid_time)
    should_leave_time = paid_time + datetime.timedelta(minutes=10)
    
    #print( int(time.mktime(should_leave_time)))
    print((should_leave_time-paid_time).seconds)
    
    return should_leave_time
    #datetime.datetime(*ts[0:100])
    #dt_obj = datetime.datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S+%S:%S').date()
    
    #dateArray = datetime.datetime.utcfromtimestamp(ts)
    #print(dateArray)
#if __name__ == '__main__':
    #firebase_Car_Overtime_thirty()
    #this = firebase_Read_Using_Car()
    #print(this)
    #check_remain_place()
    #remain_place_sub(check_remain_place())
    #print(firebase_Read_Users_Balance('rJm10FH2PoYCE4iKuMfwD8LECBf1'))
    #col_query = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid')

    # Watch the collection query
    #query_watch = col_query.on_snapshot(on_snapshot)
        #callback_done = threading.Event()
        #doc_ref = db.collection(u'reservatable parkinglot').document(u'北科大APP特約停車場').collection(u'parking grid').document(u'EA7THE')
        # Watch the document
        #doc_watch = doc_ref.on_snapshot(on_snapshot)
    #print(query_watch)
        
    #firebase_Read_Reserved_Car('EA7THE')
    #get_paid_time('EA7THE')
    
    #count_again(True)