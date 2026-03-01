from sklearn.ensemble import IsolationForest

def detect_anomalies(features):
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)

    predictions = model.predict(features)
    return predictions
