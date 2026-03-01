import sys
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Add src to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from net_parser import capture_packets
from features import engineer_features, classify_traffic
from model import detect_anomalies, assign_risk
from prediction import forecast_traffic

# --- STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="Pacos NetInsight - Industrial", layout="wide")
st.title("🔥 Pacos NetInsight - Live Industrial Network Monitor 🔥")

# --- STREAMLIT PLACEHOLDERS ---
summary_placeholder = st.empty()
anomaly_placeholder = st.empty()
traffic_plot_placeholder = st.empty()
forecast_plot_placeholder = st.empty()

# --- LIVE MONITOR LOOP ---
iface = None  # Set your interface if needed, e.g., "en0" for Wi-Fi
packets_per_batch = 20  # number of packets per refresh
traffic_log = pd.DataFrame()

st.info("Starting live packet capture... (requires admin/root privileges)")

try:
    while True:
        df = capture_packets(count=packets_per_batch, iface=iface)
        if df.empty:
            continue

        features = engineer_features(df)
        df['traffic_type'] = classify_traffic(features)
        df['anomaly'] = detect_anomalies(features)
        df['risk_level'] = df.apply(assign_risk, axis=1)

        traffic_log = pd.concat([traffic_log, df], ignore_index=True)

        # --- DASHBOARD UPDATE ---
        total_packets = len(traffic_log)
        anomalies_detected = len(traffic_log[traffic_log['anomaly']==-1])
        traffic_counts = traffic_log['traffic_type'].value_counts()

        summary_placeholder.markdown(f"""
        **Total Packets:** {total_packets}  
        **Anomalies Detected:** {anomalies_detected}  
        **Traffic Breakdown:** {dict(traffic_counts)}
        """)

        anomalies = traffic_log[traffic_log['anomaly']==-1]
        if len(anomalies) > 0:
            anomaly_placeholder.dataframe(anomalies[['timestamp','source_ip','port','packet_size','failed_logins','traffic_type','risk_level']])
        else:
            anomaly_placeholder.success("No suspicious activity detected!")

        fig1, ax1 = plt.subplots()
        traffic_counts.plot.pie(ax=ax1, autopct='%1.1f%%', startangle=90)
        ax1.set_ylabel('')
        traffic_plot_placeholder.pyplot(fig1)

        forecast = forecast_traffic(traffic_log)
        fig2, ax2 = plt.subplots(figsize=(10,4))
        ax2.plot(forecast['ds'], forecast['yhat'], marker='o', label='Predicted Packets')
        ax2.set_title("Predicted Traffic Volume")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Packets")
        forecast_plot_placeholder.pyplot(fig2)

        time.sleep(1)

except KeyboardInterrupt:
    st.warning("Live capture stopped by user.")