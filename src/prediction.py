from prophet import Prophet
import pandas as pd

def forecast_traffic(df: pd.DataFrame, periods: int = 60, freq: str = 'min') -> pd.DataFrame:
    """Forecast traffic volume using Prophet."""
    if 'timestamp' not in df.columns:
        raise ValueError('DataFrame must include a timestamp column for forecasting.')

    df_count = df.copy()
    df_count['ds'] = pd.to_datetime(df_count['timestamp'], errors='coerce')
    df_count = df_count.dropna(subset=['ds'])
    df_count = df_count.groupby('ds').size().reset_index(name='y')

    if len(df_count) < 10:
        raise ValueError('Not enough data points for forecast. At least 10 timestamps are required.')

    m = Prophet(daily_seasonality=True, weekly_seasonality=False, yearly_seasonality=False)
    m.fit(df_count)
    future = m.make_future_dataframe(periods=periods, freq=freq)
    return m.predict(future)
