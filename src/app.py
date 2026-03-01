# src/app.py
import sys
import os
import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- ENSURE RELATIVE IMPORTS WORK ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- IMPORT INTERNAL MODULES ---
from net_parser import capture_packets
from features import engineer_features, classify_traffic
from model import detect_anomalies, assign_risk
from prediction import forecast_traffic

# --- STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="Pacos NetInsight - Industrial", layout="wide")
st.title("🔥 Pacos NetInsight - Live Industrial Network Monitor 🔥")

# --- PLACEHOLDERS ---
summary_placeholder = st.empty()
anomaly_placeholder = st.empty()
traffic_plot_placeholder = st.empty()
forecast_plot_placeholder = st.empty()

# --- CONFIG ---
iface = None  # e.g., "en0" for Wi-Fi
packets_per_batch = 20
traffic_log = pd.DataFrame()

# --- CLOUD DETECTION ---
RUNNING_ON_CLOUD = os.environ.get("STREAMLIT_DEPLOY") == "true"

if RUNNING_ON_CLOUD:
    st.info("Running on Streamlit Cloud – using CSV mock data")
    df = pd.read_csv(os.path.join(os.path.dirname(BASE_DIR), "data", "network_log.csv"))
    traffic_log = df.copy()
else:
    st.info("Starting live packet capture... (requires admin/root privileges)")

    try:
        while True:
            # Capture live packets
            df = capture_packets(count=packets_per_batch, iface=iface)
            if df.empty:
                continue

            # Feature engineering
            features = engineer_features(df)

            # Traffic classification
            df['traffic_type'] = classify_traffic(features)

            # Anomaly detection
            df['anomaly'] = detect_anomalies(features)
            df['risk_level'] = df.apply(assign_risk, axis=1)

            # Append to main log
            traffic_log = pd.concat([traffic_log, df], ignore_index=True)

            # --- DASHBOARD UPDATE ---
            total_packets = len(traffic_log)
            anomalies_detected = len(traffic_log[traffic_log['anomaly'] == -1])
            traffic_counts = traffic_log['traffic_type'].value_counts()

            # Summary
            summary_placeholder.markdown(f"""
            **Total Packets:** {total_packets}  
            **Anomalies Detected:** {anomalies_detected}  
            **Traffic Breakdown:** {dict(traffic_counts)}
            """)

            # Suspicious Activity Table
            anomalies = traffic_log[traffic_log['anomaly'] == -1]
            if len(anomalies) > 0:
                anomaly_placeholder.dataframe(anomalies[['timestamp','source_ip','port','packet_size','failed_logins','traffic_type','risk_level']])
            else:
                anomaly_placeholder.success("No suspicious activity detected!")

            # Traffic Classification Pie Chart
            fig1, ax1 = plt.subplots()
            traffic_counts.plot.pie(ax=ax1, autopct='%1.1f%%', startangle=90,
                                    colors=['#1f77b4','#ff7f0e','#d62728','#2ca02c'])
            ax1.set_ylabel('')
            traffic_plot_placeholder.pyplot(fig1)

            # Predictive Bandwidth Forecast
            forecast = forecast_traffic(traffic_log)
            fig2, ax2 = plt.subplots(figsize=(10,4))
            ax2.plot(forecast['ds'], forecast['yhat'], marker='o', label='Predicted Packets')
            ax2.set_title("Predicted Traffic Volume")
            ax2.set_xlabel("Time")
            ax2.set_ylabel("Packets")
            forecast_plot_placeholder.pyplot(fig2)

            time.sleep(1)  # live refresh interval

    except KeyboardInterrupt:
        st.warning("Live capture stopped by user.")