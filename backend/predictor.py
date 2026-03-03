import numpy as np
from sklearn.linear_model import LinearRegression

WINDOW_SIZE = 10
SURGE_THRESHOLD = 250

def predict_next_voltage(history: list):
    if len(history) < WINDOW_SIZE:
        return None

    window = history[-WINDOW_SIZE:]
    voltages = np.array([d["voltage"] for d in window])

    x = np.arange(WINDOW_SIZE).reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, voltages)

    predicted = model.predict([[WINDOW_SIZE]])[0]
    return float(predicted)

def classify_risk(current_voltage: float, predicted_voltage: float):
    if current_voltage > SURGE_THRESHOLD:
        return "CRITICAL"

    if predicted_voltage and predicted_voltage > SURGE_THRESHOLD:
        return "CRITICAL"

    if predicted_voltage and predicted_voltage > SURGE_THRESHOLD - 10:
        return "WARNING"

    return "NORMAL"