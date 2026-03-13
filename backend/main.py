from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
from models import ESP32Data
from storage import VoltageStorage
from predictor import predict_next_voltage, classify_risk

app = FastAPI()
storage = VoltageStorage()


kill_switch_state: Dict[str, str] = {}  # sensor_id -> "ON"/"OFF"


@app.post("/voltage")
def receive_data(data: ESP32Data):
    voltage_value = data.measurements.voltage

    record = {
        "sensor_id": data.sensor_id,
        "timestamp": data.timestamp.isoformat(),
        "voltage": voltage_value,
        "current": data.measurements.current,
        "power": data.measurements.power,
        "energy": data.measurements.energy,
        "frequency": data.measurements.frequency,
        "power_factor": data.measurements.power_factor,
        "load_state": data.load_state,
        "status": data.status
    }

    storage.add(record)

    history = storage.get_all()
    predicted = predict_next_voltage(history)
    risk = classify_risk(voltage_value, predicted)

    # Kill switch logic
    relay_state = "ON"
    if (predicted and predicted >= 250.0) or (kill_switch_state.get(data.sensor_id) == "OFF"):
        relay_state = "OFF"
        # Optional: send HTTP/MQTT to ESP32 relay here

    return {
        "sensor_id": data.sensor_id,
        "current_voltage": voltage_value,
        "predicted_voltage": predicted,
        "risk": risk,
        "relay_state": relay_state
    }

@app.post("/switch_off")
def switch_off(sensor: Dict[str, str]):
    sensor_id = sensor.get("sensor_id")
    if not sensor_id:
        return {"error": "sensor_id required"}

    kill_switch_state[sensor_id] = "OFF"
    # Optional: send HTTP/MQTT command to ESP32 relay
    return {"message": f"Kill switch activated for {sensor_id}", "relay_state": "OFF"}

@app.get("/history")
def get_history():
    return storage.get_all()

@app.get("/latest_prediction")
def get_latest_prediction():
    history = storage.get_all()
    if not history:
        return {"message": "No data"}

    latest = history[-1]
    predicted = predict_next_voltage(history)
    risk = classify_risk(latest["voltage"], predicted)

    relay_state = "ON"
    if (predicted and predicted >= 250.0) or (kill_switch_state.get(latest["sensor_id"]) == "OFF"):
        relay_state = "OFF"

    return {
        "sensor_id": latest["sensor_id"],
        "current_voltage": latest["voltage"],
        "predicted_voltage": predicted,
        "risk": risk,
        "relay_state": relay_state
    }