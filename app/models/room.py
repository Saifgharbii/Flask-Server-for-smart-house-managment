from dataclasses import dataclass, field
from typing import List, Dict, Optional
from .base import FirebaseModel

@dataclass
class Room(FirebaseModel):
    name: str = ""
    floor: int = 0
    area: Optional[float] = None  # in square meters
    device_ids: List[str] = field(default_factory=list)  # References to Devices
    house_id: str = ""  # Reference to House
    room_type: str = "room"  # For inheritance
    temperature_history: List[Dict] = field(default_factory=list)
    humidity_history: List[Dict] = field(default_factory=list)
    occupancy_patterns: List[Dict] = field(default_factory=list)
    energy_consumption: List[Dict] = field(default_factory=list)

@dataclass
class Garage(Room):
    car_capacity: int = 1
    has_charging_station: bool = False
    charging_station_power: Optional[float] = None  # in kW

@dataclass
class Bathroom(Room):
    has_ventilation: bool = True
    water_usage_history: List[Dict] = field(default_factory=list)

@dataclass
class Kitchen(Room):
    appliance_inventory: List[Dict] = field(default_factory=list)
    water_usage_history: List[Dict] = field(default_factory=list)

@dataclass
class Toilet(Room):
    water_usage_history: List[Dict] = field(default_factory=list)
