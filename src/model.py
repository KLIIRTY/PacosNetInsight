from sklearn.ensemble import IsolationForest

def detect_anomalies(features_df):
    model = IsolationForest(contamination=0.1, random_state=42)
    numeric_cols = ['packet_size', 'failed_logins']
    model.fit(features_df[numeric_cols])
    preds = model.predict(features_df[numeric_cols])
    return preds

def assign_risk(row):
    if row['failed_logins'] >= 3 or row['packet_size'] > 8000:
        return "HIGH"
    elif row['port'] in [22, 3389]:
        return "MEDIUM"
    else:
        return "LOW"