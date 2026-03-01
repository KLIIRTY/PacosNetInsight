import pandas as pd
import numpy as np

def engineer_features(df):
    # Example feature engineering
    df['failed_logins'] = df.get('failed_logins', 0)
    df['packet_size'] = df.get('packet_size', 0)
    return df

def classify_traffic(features_df):
    # Traffic classification based on port and packet size
    conditions = [
        features_df['port'].isin([80, 443]),       # Web traffic
        features_df['port'].isin([22, 3389]),      # Admin / Remote access
        features_df['packet_size'] > 5000          # Large packets
    ]
    choices = ['Web', 'Admin', 'Heavy']
    features_df['traffic_type'] = np.select(conditions, choices, default='Other')
    return features_df['traffic_type']