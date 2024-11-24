from base import FirebaseManager
from datetime import datetime

def init_test_data():
    """Initialize test data for development"""
    firebase_manager = FirebaseManager()
    
    # Create a test user
    test_user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "password_hash": "hashed_password",  # In real app, use proper hashing
        "created_at": datetime.utcnow(),
        "house_ids": [],
        "notification_ids": []
    }
    
    user_id = firebase_manager.create_document("users", test_user_data)
    
    # Create a test house
    test_house_data = {
        "address": "123 Test Street",
        "owner_id": user_id,
        "construction_year": 2020,
        "total_area": 200.0,
        "room_ids": [],
        "current_energy_source": "grid"
    }
    
    house_id = firebase_manager.create_document("houses", test_house_data)
    
    # Update user with house ID
    firebase_manager.update_document("users", user_id, {
        "house_ids": [house_id]
    })
    
    # Create test rooms
    rooms = ["Living Room", "Kitchen", "Bedroom", "Bathroom"]
    room_ids = []
    
    for room_name in rooms:
        room_data = {
            "name": room_name,
            "house_id": house_id,
            "floor": 1,
            "device_ids": [],
            "room_type": "room"
        }
        room_id = firebase_manager.create_document("rooms", room_data)
        room_ids.append(room_id)
    
    # Update house with room IDs
    firebase_manager.update_document("houses", house_id, {
        "room_ids": room_ids
    })
    
    print("Test data initialized successfully!")
    
init_test_data()