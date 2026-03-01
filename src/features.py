# src/features.py
import pandas as pd

def engineer_features(df):
    """
    Simple feature engineering: ensures numeric columns exist.
    """
    df['packet_size'] = df['packet_size'].astype(int)
    df['failed_logins'] = df['failed_logins'].astype(int)
    df['port'] = df['port'].fillna(0).astype(int)
    return df

def classify_traffic(features_df):
    """
    Classify traffic type based on simple rules (Web, Streaming, Other).
    """
    conditions = [
        (features_df['port'].isin([80, 443])),
        (features_df['port'].isin([1935, 554, 1755]))  # common streaming ports
    ]
    choices = ['Web', 'Streaming']

    # Use numpy from pandas or import numpy directly
    import numpy as np
    features_df['traffic_type'] = pd.Series(np.select(conditions, choices, default='Other'))
    return features_df['traffic_type']