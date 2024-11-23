from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from .base import FirebaseModel, EnergyTransactionType

@dataclass
class Notification(FirebaseModel):
    timestamp: datetime = field(default_factory=datetime.utcnow)
    message: str = ""
    type: str = ""  # alert, warning, info
    read: bool = False
    user_id: str = ""  # Reference to User
    device_id: Optional[str] = None  # Reference to Device

@dataclass
class EnergyTransaction(FirebaseModel):
    timestamp: datetime = field(default_factory=datetime.utcnow)
    transaction_type: EnergyTransactionType = EnergyTransactionType.GRID_TO_HOUSE
    amount: float = 0.0  # in kWh
    source_id: Optional[str] = None  # Reference to User
    destination_id: str = ""  # Reference to User
    cost: Optional[float] = None

@dataclass
class House(FirebaseModel):
    address: str = ""
    total_area: Optional[float] = None  # in square meters
    construction_year: Optional[int] = None
    room_ids: List[str] = field(default_factory=list)  # References to Rooms
    battery_ids: List[str] = field(default_factory=list)  # References to Batteries
    owner_id: str = ""  # Reference to User
    current_energy_source: str = "grid"  # 'battery', 'neighbor', 'grid'
    solar_panel_capacity: Optional[float] = None  # in kW
    energy_consumption_history: List[Dict] = field(default_factory=list)
    energy_production_history: List[Dict] = field(default_factory=list)
    maintenance_history: List[Dict] = field(default_factory=list)
    efficiency_score: Optional[float] = None

@dataclass
class User(FirebaseModel):
    username: str = ""
    email: str = ""
    password_hash: str = ""
    house_ids: List[str] = field(default_factory=list)  # References to Houses
    neighbor_ids: List[str] = field(default_factory=list)  # References to Users
    notification_ids: List[str] = field(default_factory=list)  # References to Notifications
    created_at: datetime = field(default_factory=datetime.utcnow)
    max_energy_share: Optional[float] = None  # maximum kWh willing to share
    min_battery_reserve: Optional[float] = None  # minimum battery % to keep
    energy_sharing_price: Optional[float] = None  # price per kWh for sharing
    energy_sharing_history: List[Dict] = field(default_factory=list)
    energy_consumption_patterns: List[Dict] = field(default_factory=list)
    carbon_footprint: List[Dict] = field(default_factory=list)