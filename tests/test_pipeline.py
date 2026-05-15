import pandas as pd
from io import StringIO

from src.net_parser import load_csv
from src.features import engineer_features, classify_traffic
from src.model import assign_risk, detect_anomalies


def test_load_csv_from_stringio():
    csv = StringIO("timestamp,source_ip,port,packet_size,failed_logins\n2026-03-01 10:00:00,192.168.1.10,80,1200,0\n")
    df = load_csv(csv)
    assert df.shape == (1, 5)
    assert df['source_ip'].iloc[0] == '192.168.1.10'


def test_engineer_features_and_classification():
    df = pd.DataFrame({
        'packet_size': [100, 8000],
        'failed_logins': [0, 4],
        'port': [80, 22],
    })
    features = engineer_features(df)
    assert list(features.columns) == ['packet_size', 'failed_logins', 'port']

    traffic = classify_traffic(features)
    assert traffic.iloc[0] == 'Web'
    assert traffic.iloc[1] == 'Authentication'


def test_assign_risk_high_for_anomaly():
    row = {'anomaly': -1, 'failed_logins': 0, 'packet_size': 100, 'traffic_type': 'Web'}
    assert assign_risk(row) == 'HIGH'


def test_assign_risk_medium_for_remote_access():
    row = {'anomaly': 1, 'failed_logins': 0, 'packet_size': 1000, 'traffic_type': 'Remote Access'}
    assert assign_risk(row) == 'MEDIUM'
