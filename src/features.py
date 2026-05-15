import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create numeric features for anomaly detection and traffic classification."""
    features = pd.DataFrame(index=df.index)
    features['packet_size'] = pd.to_numeric(df['packet_size'], errors='coerce').fillna(0)
    features['failed_logins'] = pd.to_numeric(df.get('failed_logins', 0), errors='coerce').fillna(0)
    features['port'] = pd.to_numeric(df.get('port', 0), errors='coerce').fillna(0)
    return features

def classify_traffic(features_df: pd.DataFrame) -> pd.Series:
    """Classify traffic type using packet size, failed logins, and port metadata."""
    conditions = [
        features_df['failed_logins'] > 0,
        features_df['port'].isin([22, 23, 3389]),
        features_df['packet_size'] > 5000,
        features_df['port'].isin([80, 443, 8080]),
        features_df['port'] == 53,
    ]
    choices = ['Authentication', 'Remote Access', 'Large Transfer', 'Web', 'DNS']
    return pd.Series(np.select(conditions, choices, default='Other'), index=features_df.index)
