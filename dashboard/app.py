import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# Config
# Docker internal network
BACKEND = "http://backend:8000"  
# BACKEND = "http://127.0.0.1:8000"
REFRESH_INTERVAL = 5000  # milliseconds

# Sidebar
st.sidebar.title("ESP32 Voltage Monitor")
sensor_id = st.sidebar.text_input("Sensor ID", "ESP32_PZEM_01")
st.sidebar.markdown("**Thresholds**")
voltage_warning = st.sidebar.number_input("Warning Voltage (V)", 240.0)
voltage_critical = st.sidebar.number_input("Critical Voltage (V)", 250.0)

# Helper Functions
@st.cache_data(ttl=5)
def fetch_history():
    try:
        resp = requests.get(f"{BACKEND}/history")
        resp.raise_for_status()
        data = pd.DataFrame(resp.json())
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        return data
    except:
        return pd.DataFrame()

@st.cache_data(ttl=1)
def fetch_latest_prediction():
    try:
        resp = requests.get(f"{BACKEND}/latest_prediction")
        resp.raise_for_status()
        return resp.json()
    except:
        return {}

def send_kill_switch_off():
    try:
        resp = requests.post(f"{BACKEND}/switch_off", json={"sensor_id": sensor_id})
        if resp.status_code == 200:
            st.info("Kill switch activated: Load turned OFF due to critical voltage!")
        else:
            st.error("Failed to activate kill switch.")
    except Exception as e:
        st.error(f"Error sending kill switch command: {e}")

# Main
st.title("Voltage Monitoring & Surge Prediction")

# Fetch Data
df = fetch_history()
prediction = fetch_latest_prediction()

if not df.empty:
    latest = df.iloc[-1]  # last row

    voltage_level = latest['voltage']
    load_state = latest.get('load_state', 'OFF').upper()

    # Kill switch logic: force OFF if voltage exceeds critical threshold
    if voltage_level >= voltage_critical and load_state == "ON":
        load_state = "OFF"
        send_kill_switch_off()

    # Metrics Cards (Multi-Metric)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Voltage (V)", voltage_level)
    col2.metric("Current (A)", latest['current'])
    col3.metric("Power (W)", latest['power'])
    col4.metric("Frequency (Hz)", latest['frequency'])
    col5.metric("Power Factor", latest['power_factor'])

    # System Status Panel with kill switch display
    status_text = "🟢 Online" if latest.get('status', 'offline') == 'online' else "🔴 Offline"
    load_state_display = "🟢 Relay ON" if load_state == "ON" else "🔴 Relay OFF"

    if voltage_level >= voltage_critical:
        voltage_status = "🔴 CRITICAL"
    elif voltage_level >= voltage_warning:
        voltage_status = "🟠 WARNING"
    else:
        voltage_status = "🟢 Normal"

    st.markdown(f"**Sensor Status:** {status_text}  |  **Load State:** {load_state_display}  |  **Voltage Status:** {voltage_status}")

    # Voltage Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['voltage'],
        mode='lines+markers',
        name='Voltage'
    ))

    # Predicted Voltage
    if prediction:
        last_time = df['timestamp'].iloc[-1]
        fig.add_trace(go.Scatter(
            x=[last_time],
            y=[prediction.get('predicted_voltage', voltage_level)],
            mode='markers',
            name='Predicted',
            marker=dict(size=12, color='orange', symbol='diamond')
        ))

    # Safety Bands
    fig.add_hline(y=voltage_warning, line_dash="dash", line_color="orange", annotation_text="Warning")
    fig.add_hline(y=voltage_critical, line_dash="dash", line_color="red", annotation_text="Critical")

    fig.update_layout(
        title=f"Voltage Trend (Latest: {voltage_level:.2f} V - {voltage_status})",
        xaxis_title="Time",
        yaxis_title="Voltage (V)",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # Historical Statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Max Voltage", f"{df['voltage'].max():.2f}")
    col2.metric("Min Voltage", f"{df['voltage'].min():.2f}")
    col3.metric("Mean Voltage", f"{df['voltage'].mean():.2f}")
    col4.metric("Std Dev", f"{df['voltage'].std():.2f}")

    # CSV Export
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "voltage_data.csv"
    )

else:
    st.warning("No data received yet from ESP32.")

# Auto-refresh every 5 seconds
st_autorefresh(interval=REFRESH_INTERVAL, key="data_refresh")