# src/app.py
import os
import sys
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- ENSURE RELATIVE IMPORTS WORK ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --- IMPORT INTERNAL MODULES ---
from net_parser import load_csv
from features import engineer_features, classify_traffic
from model import detect_anomalies, assign_risk

# --- STREAMLIT PAGE SETUP ---
st.set_page_config(page_title="Pacos NetInsight - Industrial", layout="wide")
st.title("🔥 Pacos NetInsight - CSV Network Analyzer 🔥")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload your network log CSV", type="csv")

if uploaded_file is not None:
    # Load CSV
    df = load_csv(uploaded_file)

    # --- SANITIZE COLUMN NAMES ---
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # --- CHECK REQUIRED COLUMNS ---
    required_cols = ['timestamp','source_ip','port','packet_size','failed_logins','traffic_type']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        st.error(f"Uploaded CSV is missing required columns: {missing_cols}")
        st.stop()

    st.success(f"Loaded {len(df)} packets from CSV")

    # --- FEATURE ENGINEERING ---
    features = engineer_features(df)

    # --- TRAFFIC CLASSIFICATION ---
    df['traffic_type'] = classify_traffic(features)

    # --- ANOMALY DETECTION ---
    df['anomaly'] = detect_anomalies(features)
    df['risk_level'] = df.apply(assign_risk, axis=1)

    # --- DASHBOARD ---
    st.subheader("Summary")
    total_packets = len(df)
    anomalies_detected = len(df[df['anomaly'] == -1])
    traffic_counts = df['traffic_type'].value_counts()
    st.markdown(f"""
    **Total Packets:** {total_packets}  
    **Anomalies Detected:** {anomalies_detected}  
    **Traffic Breakdown:** {dict(traffic_counts)}
    """)

    st.subheader("Suspicious Activity")
    anomalies = df[df['anomaly'] == -1]
    if len(anomalies) > 0:
        st.dataframe(anomalies[['timestamp','source_ip','port','packet_size','failed_logins','traffic_type','risk_level']])
    else:
        st.success("No suspicious activity detected!")

    st.subheader("Traffic Classification Pie Chart")
    fig1, ax1 = plt.subplots()
    traffic_counts.plot.pie(ax=ax1, autopct='%1.1f%%', startangle=90,
                            colors=['#1f77b4','#ff7f0e','#d62728','#2ca02c'])
    ax1.set_ylabel('')
    st.pyplot(fig1)

    # --- TRAFFIC FORECASTING REMOVED ---
    st.info("Traffic forecasting disabled to simplify deployment.")

    # --- DOWNLOAD ANALYZED CSV ---
    st.download_button(
        label="Download Analyzed CSV",
        data=df.to_csv(index=False),
        file_name="analyzed_network.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file to start analysis.")