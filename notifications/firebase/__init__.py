import firebase_admin
from firebase_admin import credentials

creds = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(creds)
