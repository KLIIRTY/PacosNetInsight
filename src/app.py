import sys
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Make sure Python can find modules in the same folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Correct imports (no 'src.' prefix)
from net_parser import load_logs
from features import engineer_features
from model import detect_anomalies
# Risk assignment function
def assign_risk(row):
    if row['failed_logins'] >= 3 or row['packet_size'] > 8000:
        return "HIGH"
    elif row['port'] in [22, 3389]:
        return "MEDIUM"
    else:
        return "LOW"

# Load network logs CSV
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # one level up from src/
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "network_log.csv")
df = load_logs(DATA_PATH)

# Feature engineering and anomaly detection
features = engineer_features(df)
predictions = detect_anomalies(features)

df['anomaly'] = predictions
df['risk_level'] = df.apply(assign_risk, axis=1)
anomalies = df[df['anomaly'] == -1]

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Pacos NetInsight", layout="wide")
st.title(" Pacos NetInsight Dashboard ")

# Summary
st.subheader("Summary")
st.markdown(f"- Total Logs Analyzed: {len(df)}")
st.markdown(f"- Anomalies Detected: {len(anomalies)}")

# Suspicious activity table
st.subheader("Suspicious Activity")
if len(anomalies) > 0:
    st.dataframe(anomalies[['timestamp','source_ip','port','packet_size','failed_logins','risk_level']])
else:
    st.success("No suspicious activity detected!")

# Traffic spike visualization
st.subheader("Visualizations")
df['timestamp'] = pd.to_datetime(df['timestamp'])
traffic_counts = df.groupby(df['timestamp'].dt.floor('T')).size()

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(traffic_counts.index, traffic_counts.values, marker='o')
ax.set_title("Network Traffic Over Time (per minute)")
ax.set_xlabel("Time")
ax.set_ylabel("Number of Packets")
st.pyplot(fig)