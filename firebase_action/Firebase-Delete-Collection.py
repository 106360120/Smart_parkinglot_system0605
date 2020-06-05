#!/usr/bin/python3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Get Collection
doc_ref = db.collection('Q1', 'DOC1', 'Q2')
docs = doc_ref.get()

# Delete Collection
for delete_list in docs:
    doc_del = db.collection('Q1', 'DOC1', 'Q2').document(delete_list.id)
    doc_del.delete()
    print('Delete Doc: {} Complete.'.format(delete_list.id))

print('Done')

"""
$ python Firebase-Delete-Collection.py
Delete Doc: DOC1 Complete.
Delete Doc: DOC2 Complete.
Delete Doc: SDSAD Complete.
Done
"""