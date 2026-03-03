from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class Measurements(BaseModel):
    voltage: float
    current: float
    power: float
    energy: float
    frequency: float
    power_factor: float

class ESP32Data(BaseModel):
    sensor_id: str
    timestamp: datetime
    status: str
    measurements: Measurements
    load_state: str
    units: Dict[str, str]