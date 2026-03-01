# src/features.py
import pandas as pd
import numpy as np

def engineer_features(df):
    """Create features for anomaly detection and traffic classification."""
    features = pd.DataFrame()
    features['packet_size'] = df['packet_size']
    features['failed_logins'] = df.get('failed_logins', 0)
    # Add more features as needed
    return features

def classify_traffic(features_df):
    """Classify traffic type based on simple thresholds."""
    conditions = [
        (features_df['packet_size'] > 1000),
        (features_df['failed_logins'] > 3)
    ]
    choices = ['Web', 'Other']
    features_df['traffic_type'] = pd.Series(
        np.select(conditions, choices, default='Other')
    )
    return features_df['traffic_type']