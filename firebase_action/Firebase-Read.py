#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
#Get Collection
doc_ref = db.collection('reservatable parkinglot', 'users')
docs = doc_ref.get()
for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

#Get Doc
def whether_place_is_using():
    doc_ref = db.collection('reservatable parkinglot').document('北科大').collection('parking grid')
    docs = doc_ref.get()
    condition = doc[False, False, False, False, True, False, False]
    usingplace = doc[condition]
    filteredData = usingplace.str.contains("true")
    print(filteredData)

def whether_place_is_reserved():
    doc_ref = db.collection('reservatable').document('北科大').collection('parking grid')
    docs = doc_ref.get()
    condition = doc[True, False, False, False, False, False, False]
    usingplace = doc[condition]
    filteredData = usingplace.str.contains("true")
    print(filteredData)


print('Done')
#print('姓名 => {}'.format(doc.to_dict()['姓名']))
"""
$ python Firebase-Read.py
DOC2 => {'年紀': '23', '工作': '魔法師', '姓名': '劉德華'}
姓名 => 劉德華
年紀 => 23
工作 => 魔法師
Done
"""