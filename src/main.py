import os
from net_parser import load_csv
from features import engineer_features, classify_traffic
from model import detect_anomalies, assign_risk


def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, "data", "network_log.csv")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Sample network log not found: {DATA_PATH}")

    df = load_csv(DATA_PATH)
    features = engineer_features(df)
    df['traffic_type'] = classify_traffic(features)
    df['anomaly'] = detect_anomalies(features)
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
             'packet_size', 'failed_logins', 'traffic_type', 'risk_level']
        ])
    else:
        print("\nNo suspicious activity detected.")


if __name__ == "__main__":
    main()
