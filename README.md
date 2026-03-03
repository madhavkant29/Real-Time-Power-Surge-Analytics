# ⚡ Voltage Monitoring & Surge Prediction System

An end-to-end IoT solution designed to monitor electrical parameters from ESP32-based sensors, visualize real-time trends, and predict short-term voltage surges using Linear Regression.

---

## 🚀 Project Overview

This system provides a robust pipeline for electrical safety. It collects high-granularity data (Voltage, Current, Power, Frequency) from hardware sensors, processes them through a FastAPI backend, and serves a dynamic Streamlit dashboard for real-time monitoring and autonomous protection logic.

---

## ✨ Key Features

- **Real-time Monitoring:** Periodic tracking of Voltage (V), Current (I), Power (W), and Frequency (Hz).
- **Surge Prediction:** Uses **Linear Regression** to analyze historical trends and forecast upcoming voltage levels.
- **Autonomous Protection:** Embedded logic to suggest or trigger appliance protection based on predicted spikes.
- **Containerized Architecture:** Fully Dockerized components for seamless deployment.
- **Interactive Dashboard:** Historical trend visualization and multi-metric health gauges.

---

## 🛠️ Setup & Installation

### Prerequisites

- Docker Desktop installed.
- Git installed.
- ESP32 Sensor *(Optional: can use mock POST requests for testing)*.

### 1. Clone & Enter Directory

```bash
git clone https://github.com/madhavkant29/electric-surge-monitoring-and-predictor.git
cd voltage-monitor
```

### 2. Launch with Docker

```bash
docker compose up --build
```

### 3. Access the Services

| Service | URL | Function |
|---|---|---|
| Streamlit Dashboard | http://localhost:8501 | View real-time graphs & predictions |
| FastAPI Docs | http://localhost:8000/docs | Interactive Swagger API documentation |

---

## 📡 Hardware Integration (ESP32)

To connect your physical hardware, ensure the ESP32 is configured to POST JSON data to your host machine's local IP address (e.g., `http://192.168.1.XX:8000/voltage`).

### Manual Testing (PowerShell)

If you don't have hardware ready, you can simulate a sensor pulse:

```bash
python test.py
```

> **Note:** Predicted voltage will appear after enough historical data points are collected (default is 15).
> can edit range of values in test.py

---

## 📊 Analytics & Prediction

The system calculates the predicted voltage by fitting a linear model to the most recent time-series data:

```
V = β₀ + β₁t
```

Where:
- `t` is the time sequence.
- `β₁` represents the voltage slope. A high positive slope triggers a **Surge Warning** on the dashboard.

---

## 🛠️ Future Roadmap

- [ ] **Voltage Safety Bands:** Visual thresholds (Green/Yellow/Red) on the dashboard.
- [ ] **Data Export:** Download historical sessions as `.csv` files.
- [ ] **Slope Visualization:** Real-time derivative graphs to show the rate of voltage change.
- [ ] **Alerting:** Integration with Telegram or WhatsApp for critical surge notifications.

---

## 📄 License

Distributed under the [MIT License](LICENSE).
