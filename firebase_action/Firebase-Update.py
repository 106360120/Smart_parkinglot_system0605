#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('test-6a8a7-firebase-adminsdk-tgspq-f9a1230d6b.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection('fuck').document('cat')
#Method 1
#doc_ref.update({
 #   '工作': '魔法師',
#})




#Method 2
while True:
    A = 0
    data = {
    'nonono': A,
    }
    doc_ref.update(data)
    #timesleep
    print('Done')

