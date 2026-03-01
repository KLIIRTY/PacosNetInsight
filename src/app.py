import sys
import os
import time
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Detect cloud environment
RUNNING_ON_CLOUD = os.environ.get("STREAMLIT_DEPLOY") == "true"

# Ensure src/ is in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Internal modules
from features import engineer_features, classify_traffic
from model import detect_anomalies, assign_risk
from prediction import forecast_traffic

if not RUNNING_ON_CLOUD:
    from net_parser import capture_packets

# Page setup
st.set_page_config(page_title="Pacos NetInsight - Industrial", layout="wide")
st.title("🔥 Pacos NetInsight - Live Industrial Network Monitor 🔥")

# Placeholders
summary_placeholder = st.empty()
anomaly_placeholder = st.empty()
traffic_plot_placeholder = st.empty()
forecast_plot_placeholder = st.empty()

# Data
if RUNNING_ON_CLOUD:
    st.info("Running on Streamlit Cloud – using CSV fallback")
    df = pd.read_csv(os.path.join(os.path.dirname(BASE_DIR), "data/network_log.csv"))
    traffic_log = df.copy()
else:
    st.info("Starting live packet capture... (requires admin/root)")
    iface = None  # e.g., "en0"
    packets_per_batch = 20
    traffic_log = pd.DataFrame()

    try:
        while True:
            df = capture_packets(iface=iface, count=packets_per_batch)
            if df.empty:
                continue

            features = engineer_features(df)
            df['traffic_type'] = classify_traffic(features)
            df['anomaly'] = detect_anomalies(features)
            df['risk_level'] = df.apply(assign_risk, axis=1)
            traffic_log = pd.concat([traffic_log, df], ignore_index=True)

            # Dashboard
            total_packets = len(traffic_log)
            anomalies_detected = len(traffic_log[traffic_log['anomaly']==-1])
            traffic_counts = traffic_log['traffic_type'].value_counts()

            summary_placeholder.markdown(f"""
            **Total Packets:** {total_packets}  
            **Anomalies Detected:** {anomalies_detected}  
            **Traffic Breakdown:** {dict(traffic_counts)}
            """)

            anomalies = traffic_log[traffic_log['anomaly'] == -1]
            if len(anomalies) > 0:
                anomaly_placeholder.dataframe(anomalies[['timestamp','source_ip','port','packet_size','failed_logins','traffic_type','risk_level']])
            else:
                anomaly_placeholder.success("No suspicious activity detected!")

            # Pie chart
            fig1, ax1 = plt.subplots()
            traffic_counts.plot.pie(ax=ax1, autopct='%1.1f%%', startangle=90)
            ax1.set_ylabel('')
            traffic_plot_placeholder.pyplot(fig1)

            # Forecast
            forecast = forecast_traffic(traffic_log)
            fig2, ax2 = plt.subplots(figsize=(10,4))
            ax2.plot(forecast['ds'], forecast['yhat'], marker='o')
            ax2.set_title("Predicted Traffic Volume")
            ax2.set_xlabel("Time")
            ax2.set_ylabel("Packets")
            forecast_plot_placeholder.pyplot(fig2)

            time.sleep(1)

    except KeyboardInterrupt:
        st.warning("Live capture stopped by user.")