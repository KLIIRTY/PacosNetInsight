import os
from parser import load_logs
from features import engineer_features
from model import detect_anomalies


def assign_risk(row):
    # High Risk
    if row['failed_logins'] >= 3 or row['packet_size'] > 8000:
        return "HIGH"
    # Medium Risk
    elif row['port'] in [22, 3389]:
        return "MEDIUM"
    # Low Risk
    else:
        return "LOW"


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "network_log.csv")

    df = load_logs(DATA_PATH)
    features = engineer_features(df)
    predictions = detect_anomalies(features)

    df['anomaly'] = predictions
    df['risk_level'] = df.apply(assign_risk, axis=1)

    total = len(df)
    anomalies = df[df['anomaly'] == -1]

    print("\n==== PACOS NETINSIGHT REPORT ====\n")
    print(f"Total Logs Analyzed: {total}")
    print(f"Anomalies Detected: {len(anomalies)}")

    if len(anomalies) > 0:
        print("\n⚠ Suspicious Activity Detected:\n")
        print(anomalies[
            ['timestamp', 'source_ip', 'port',
             'packet_size', 'failed_logins', 'risk_level']
        ])
    else:
        print("\nNo suspicious activity detected.")


if __name__ == "__main__":
    main()