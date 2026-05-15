from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(features_df: pd.DataFrame, contamination: float = 0.05):
    """Detect anomalies using Isolation Forest."""
    clf = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
        max_samples='auto'
    )
    clf.fit(features_df)
    return clf.predict(features_df)

def assign_risk(row):
    """Assign risk level based on anomaly score and suspicious traffic characteristics."""
    if row.get('anomaly') == -1:
        return 'HIGH'
    if row.get('failed_logins', 0) >= 3 or row.get('packet_size', 0) >= 8000:
        return 'HIGH'
    if row.get('traffic_type') in {'Remote Access', 'Authentication', 'Brute Force'}:
        return 'MEDIUM'
    return 'LOW'
