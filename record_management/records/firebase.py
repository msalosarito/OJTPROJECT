import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('C:\\Users\\sean.losarito\\Desktop\\FIREBASE\\recordmanagement-4a583-firebase-adminsdk-reznc-e0a192a154.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://recordmanagement-4a583-default-rtdb.firebaseio.com'})

db_instance = db.reference()