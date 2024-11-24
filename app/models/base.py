from dataclasses import dataclass, asdict, field
from typing import Dict, Any
from datetime import datetime
from enum import Enum
import firebase_admin
from firebase_admin import credentials, firestore
import os

class EnergyTransactionType(str, Enum):
    SOLAR_TO_BATTERY = "solar_to_battery"
    NEIGHBOR_TO_HOUSE = "neighbor_to_house"
    GRID_TO_HOUSE = "grid_to_house"
    CAR_TO_HOUSE = "car_to_house"

class DeviceStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class DeviceType(str, Enum):
    LIGHT = "light"
    WINDOW = "window"
    DOOR = "door"
    CLEANING_ROBOT = "cleaning_robot"
    MAGNETIC_LOCK = "magnetic_lock"
    GARAGE_DOOR = "garage_door"

@dataclass
class FirebaseModel:
    id: str = field(default="")

    def to_dict(self) -> dict:
        def convert_value(v):
            if isinstance(v, Enum):
                return v.value
            if isinstance(v, datetime):
                return v.isoformat()
            if isinstance(v, FirebaseModel):
                return v.to_dict()
            if isinstance(v, list):
                return [convert_value(i) for i in v]
            if isinstance(v, dict):
                return {k: convert_value(v) for k, v in v.items()}
            return v

        data = asdict(self)
        return {k: convert_value(v) for k, v in data.items() if v is not None}
    
class FirebaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize Firebase with credentials
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', r'C:\Users\saif\OneDrive - SUPCOM\SupCom1\Projects\challenge CAS\Back end\app\credentials.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        
        # Get Firestore client
        self.db = firestore.client()
        self._initialized = True
    
    def init_database(self):
        """Initialize database collections and example data"""
        try:
            # Create collections
            collections = [
                'users', 'houses', 'rooms', 'devices', 
                'batteries', 'solar_panels', 'notifications',
                'energy_transactions'
            ]
            
            for collection in collections:
                if not self.db.collection(collection).get():
                    print(f"Initializing {collection} collection...")
                    
            print("Database collections initialized successfully!")
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False
    
    def create_document(self, collection: str, data: Dict[str, Any]) -> str:
        """Create a new document in a collection"""
        try:
            doc_ref = self.db.collection(collection).document()
            doc_ref.set(data)
            return doc_ref.id
        except Exception as e:
            print(f"Error creating document: {e}")
            raise
    
    def get_document(self, collection: str, doc_id: str) -> Dict[str, Any]:
        """Get a document by ID"""
        try:
            doc = self.db.collection(collection).document(doc_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            print(f"Error getting document: {e}")
            raise
    
    def update_document(self, collection: str, doc_id: str, data: Dict[str, Any]) -> bool:
        """Update an existing document"""
        try:
            self.db.collection(collection).document(doc_id).update(data)
            return True
        except Exception as e:
            print(f"Error updating document: {e}")
            raise
    
    def delete_document(self, collection: str, doc_id: str) -> bool:
        """Delete a document"""
        try:
            self.db.collection(collection).document(doc_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting document: {e}")
            raise
    
    def query_collection(self, collection: str, filters: list = None, order_by: str = None):
        """Query a collection with optional filters and ordering"""
        try:
            query = self.db.collection(collection)
            
            if filters:
                for field, op, value in filters:
                    query = query.where(field, op, value)
            
            if order_by:
                query = query.order_by(order_by)
                
            return [doc.to_dict() for doc in query.stream()]
        except Exception as e:
            print(f"Error querying collection: {e}")
            raise
    