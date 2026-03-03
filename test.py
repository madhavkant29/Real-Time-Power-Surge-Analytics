import requests
from datetime import datetime, timedelta
import random

BACKEND = "http://127.0.0.1:8000/voltage"  # Change if using Docker container name

sensor_id = "ESP32_PZEM_01"
base_time = datetime.utcnow()

for i in range(15):
    timestamp = (base_time + timedelta(seconds=i*3)).isoformat() + "Z"
    
    data = {
        "sensor_id": sensor_id,
        "timestamp": timestamp,
        "status": "online",
        "measurements": {
            "voltage": round(random.uniform(250, 265), 2),  # random voltage between 225-235
            "current": round(random.uniform(0.2, 0.5), 2),
            "power": round(random.uniform(50, 70), 2),
            "energy": round(random.uniform(10, 15), 2),
            "frequency": 50.0,
            "power_factor": 1.0
        },
        "load_state": "ON",
        "units": {
            "voltage": "V",
            "current": "A",
            "power": "W",
            "energy": "kWh",
            "frequency": "Hz",
            "power_factor": "pf"
        }
    }
    
    resp = requests.post(BACKEND, json=data)
    print(f"{i+1}/15 sent, status code: {resp.status_code}")