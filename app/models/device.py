from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from .base import FirebaseModel, DeviceType, DeviceStatus

@dataclass
class Device(FirebaseModel):
    name: str = ""
    device_type: DeviceType = DeviceType.LIGHT
    status: DeviceStatus = DeviceStatus.INACTIVE
    room_id: str = ""  # Reference to Room
    power_consumption: Optional[float] = None  # in watts
    last_maintenance: Optional[datetime] = None
    installation_date: datetime = field(default_factory=datetime.utcnow)
    firmware_version: Optional[str] = None
    total_runtime: float = 0  # in hours
    total_energy_consumed: float = 0  # in kWh
    usage_patterns: Dict = field(default_factory=dict)

@dataclass
class Light(Device):
    brightness_level: int = 0  # 0-100
    color_temperature: Optional[int] = None  # in Kelvin
    is_motion_activated: bool = False

@dataclass
class Window(Device):
    is_open: bool = False
    opening_percentage: int = 0  # 0-100
    last_cleaned: Optional[datetime] = None

@dataclass
class Door(Device):
    is_locked: bool = True
    access_log: List[Dict] = field(default_factory=list)

@dataclass
class CleaningRobot(Device):
    battery_level: int = 100  # 0-100
    cleaning_schedule: List[Dict] = field(default_factory=list)
    coverage_area: Optional[float] = None  # in square meters

@dataclass
class Battery(FirebaseModel):
    capacity: float = 0.0  # in kWh
    current_charge: float = 0.0  # in kWh
    type: str = "permanent"  # 'permanent', 'car', etc.
    charge_cycles: int = 0
    efficiency: Optional[float] = None  # charging efficiency percentage
    last_charged: Optional[datetime] = None
    house_id: str = ""  # Reference to House
    charging_history: List[Dict] = field(default_factory=list)
    discharge_rate: Optional[float] = None  # kWh per hour
    
@dataclass
class SolarPanel(FirebaseModel):
    panel_model: str = ""
    manufacturer: str = ""
    rated_power: float = 0.0  # in watts puissance 
    efficiency: float = 0.0  # percentage (e.g., 20.5 for 20.5%)
    area: float = 0.0  # in square meters
    orientation: str = "south"  # north, south, east, west
    tilt_angle: float = 0.0  # in degrees
    status: DeviceStatus = DeviceStatus.ACTIVE
    installation_date: datetime = field(default_factory=datetime.utcnow)
    last_maintenance: Optional[datetime] = None
    house_id: str = ""  # Reference to House
    
    # Performance metrics
    total_energy_generated: float = 0.0  # in kWh
    daily_generation: List[Dict] = field(default_factory=list)  # List of daily generation records
    peak_power_output: float = 0.0  # maximum recorded power output in watts
    current_power_output: float = 0.0  # current power output in watts
    
    # Environmental factors
    temperature: Optional[float] = None  # panel temperature in Celsius
    shading_factor: Optional[float] = None  # percentage of panel shaded
    soiling_level: Optional[float] = None  # cleanliness level (0-100%)
    
    # Maintenance info
    cleaning_history: List[Dict] = field(default_factory=list)
    inspection_history: List[Dict] = field(default_factory=list)
    warranty_info: Dict = field(default_factory=dict)
    
    # Performance degradation
    initial_efficiency: float = 0.0  # initial efficiency when installed
    annual_degradation_rate: float = 0.5  # typical 0.5% per year
    estimated_lifespan: int = 25  # in years
    