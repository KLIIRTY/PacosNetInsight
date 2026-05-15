from pathlib import Path
import pandas as pd
import streamlit as st
import altair as alt

from net_parser import load_csv
from features import engineer_features, classify_traffic
from model import detect_anomalies, assign_risk
from prediction import forecast_traffic

st.set_page_config(page_title="Pacos NetInsight", layout="wide")
st.title("🔥 Pacos NetInsight")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "network_log.csv"

st.sidebar.header("Settings")
use_sample_data = st.sidebar.checkbox("Use sample dataset", value=False)
contamination = st.sidebar.slider("Anomaly contamination (%)", 1, 20, 5)
show_forecast = st.sidebar.checkbox("Show traffic forecast", value=False)
forecast_horizon = st.sidebar.number_input(
    "Forecast horizon (minutes)", min_value=10, max_value=240, value=60, step=10
)

uploaded_file = st.file_uploader("Upload your network log CSV", type="csv")
source = None
if uploaded_file is not None:
    source = uploaded_file
elif use_sample_data and DATA_PATH.exists():
    source = str(DATA_PATH)

if source is None:
    st.info("Upload a CSV file or enable the sample dataset to start analysis.")
    if not DATA_PATH.exists():
        st.warning("Sample dataset not found. Run `python src/generate_logs.py` to create test data.")
else:
    df = load_csv(source)
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

    required_cols = ['timestamp', 'source_ip', 'port', 'packet_size', 'failed_logins']
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        st.error(f"Uploaded CSV is missing required columns: {missing_cols}")
        st.stop()

    features = engineer_features(df)
    df['traffic_type'] = classify_traffic(features)

    numeric_features = features.select_dtypes(include=['int64', 'float64', 'float32'])
    if numeric_features.empty:
        st.error("No numeric features available for anomaly detection!")
        st.stop()

    df['anomaly'] = detect_anomalies(numeric_features, contamination=contamination / 100)
    df['risk_level'] = df.apply(assign_risk, axis=1)

    total_packets = len(df)
    anomalies_detected = int((df['anomaly'] == -1).sum())
    risk_counts = df['risk_level'].value_counts().reindex(['HIGH', 'MEDIUM', 'LOW'], fill_value=0)

    st.markdown("### Summary")
    cols = st.columns(3)
    cols[0].metric("Total packets", total_packets)
    cols[1].metric("Anomalies", anomalies_detected)
    cols[2].metric("High risk", int(risk_counts['HIGH']))

    st.markdown("### Traffic breakdown")
    traffic_counts = df['traffic_type'].value_counts().reset_index()
    traffic_counts.columns = ['traffic_type', 'count']
    st.altair_chart(
        alt.Chart(traffic_counts)
        .mark_bar()
        .encode(x='traffic_type:N', y='count:Q', color='traffic_type:N')
        .properties(height=350),
        use_container_width=True
    )

    st.markdown("### Traffic over time")
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    time_df = df.dropna(subset=['timestamp'])
    if not time_df.empty:
        timeline = (
            time_df
            .groupby(pd.Grouper(key='timestamp', freq='5min'))
            .size()
            .reset_index(name='count')
        )
        st.altair_chart(
            alt.Chart(timeline)
            .mark_line(point=True)
            .encode(x='timestamp:T', y='count:Q')
            .properties(title='Packets over time', height=350),
            use_container_width=True
        )

    st.markdown("### Suspicious activity")
    anomalies = df[df['anomaly'] == -1]
    if not anomalies.empty:
        st.dataframe(
            anomalies[
                ['timestamp', 'source_ip', 'port', 'packet_size', 'failed_logins', 'traffic_type', 'risk_level']
            ].sort_values(by='timestamp', ascending=False).reset_index(drop=True)
        )
    else:
        st.success("No suspicious activity detected!")

    if show_forecast:
        st.markdown("### Traffic forecast")
        try:
            forecast_df = forecast_traffic(time_df, periods=forecast_horizon, freq='min')
            forecast_chart = alt.Chart(forecast_df).mark_line().encode(
                x='ds:T',
                y='yhat:Q',
                tooltip=['ds:T', 'yhat:Q', 'yhat_lower:Q', 'yhat_upper:Q']
            ).properties(height=350)
            st.altair_chart(forecast_chart, use_container_width=True)
        except Exception as exc:
            st.error(f"Unable to generate forecast: {exc}")

    st.download_button(
        label="Download analyzed CSV",
        data=df.to_csv(index=False),
        file_name="analyzed_network.csv",
        mime="text/csv"
    )
