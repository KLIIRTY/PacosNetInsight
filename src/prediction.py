# src/prediction.py
from prophet import Prophet
import pandas as pd

def forecast_traffic(df):
    """Forecast traffic volume using Prophet."""
    df_count = df.groupby('timestamp').size().reset_index(name='y')
    df_count['ds'] = pd.to_datetime(df_count['timestamp'])
    df_count = df_count[['ds','y']]

    m = Prophet(daily_seasonality=True)
    m.fit(df_count)

    future = m.make_future_dataframe(periods=10, freq='min')
    forecast = m.predict(future)
    return forecast