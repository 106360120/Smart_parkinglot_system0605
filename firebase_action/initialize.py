# -*- encoding: utf-8 -*-
# 引用必要套件
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('car-project-b45b3-firebase-adminsdk-41ei0-555cf34e12.json')
firebase_admin.initialize_app(cred)

db = firestore.client()