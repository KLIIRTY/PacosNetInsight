def engineer_features(df):
    feature_df = df.copy()

    feature_df['hour'] = feature_df['timestamp'].dt.hour

    selected_features = feature_df[
        ['port', 'packet_size', 'failed_logins', 'hour']
    ]

    return selected_features
