import firebase_admin
from firebase_admin import credentials
from flask import Flask
import os

def init_firebase(app: Flask) -> None:
    """Initialize Firebase Admin SDK"""
    cred_path = 'credentials.json'
    
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            app.logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise