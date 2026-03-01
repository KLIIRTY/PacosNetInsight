# src/model.py
from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(features_df):
    """Detect anomalies using Isolation Forest."""
    clf = IsolationForest(n_estimators=50, contamination=0.05, random_state=42)
    clf.fit(features_df)
    anomalies = clf.predict(features_df)
    return anomalies  # -1 for anomaly, 1 for normal

def assign_risk(row):
    """Assign risk level based on anomalies and traffic type."""
    if row['anomaly'] == -1:
        return 'High'
    elif row['traffic_type'] == 'Other':
        return 'Medium'
    else:
        return 'Low'