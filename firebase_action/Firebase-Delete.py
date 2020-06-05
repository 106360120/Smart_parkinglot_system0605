#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Delete Document
doc_ref = db.collection('Q1', 'DOC1', 'Q2').document('DOC2')
doc_ref.delete()

print('Done')