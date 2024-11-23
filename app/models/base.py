from dataclasses import dataclass, asdict, field
from typing import Dict, Any
from datetime import datetime
from enum import Enum
import firebase_admin
from firebase_admin import credentials, firestore

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
    def __init__(self):
        self.db = firestore.client()

    def create_document(self, collection: str, data: FirebaseModel) -> str:
        """Create a new document in Firebase"""
        doc_ref = self.db.collection(collection).document()
        data.id = doc_ref.id
        doc_ref.set(data.to_dict())
        return doc_ref.id

    def update_document(self, collection: str, doc_id: str, data: dict):
        """Update an existing document"""
        self.db.collection(collection).document(doc_id).update(data)

    def get_document(self, collection: str, doc_id: str) -> dict:
        """Retrieve a document"""
        doc = self.db.collection(collection).document(doc_id).get()
        return doc.to_dict() if doc.exists else None

    def delete_document(self, collection: str, doc_id: str):
        """Delete a document"""
        self.db.collection(collection).document(doc_id).delete()

    def query_collection(self, collection: str, filters: list[tuple] = None) -> list[dict]:
        """Query documents with filters"""
        query = self.db.collection(collection)
        if filters:
            for field, op, value in filters:
                query = query.where(field, op, value)
        return [doc.to_dict() for doc in query.stream()]