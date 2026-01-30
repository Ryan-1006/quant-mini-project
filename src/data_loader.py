import requests
import pandas as pd

def load_btc_daily():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1d",
        "limit": 1000
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore"
    ])

    return df

def clean_ohlc(df):
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.set_index("open_time")
    df = df.sort_index()
    return df

def assert_data_quality(df):
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.tz is not None
    assert df.index.is_monotonic_increasing
    assert (df["close"].astype(float) > 0).all()
    assert df["close"].isna().sum() == 0

def ensure_continuous_daily_index(df):
    expected_index = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )
    df = df.reindex(expected_index)
    df = df.ffill()
    return df

def flag_outlier_returns(df, threshold=1.0):
    returns = df["close"].astype(float).pct_change()
    outliers = returns.abs() > threshold
    return outliers

if __name__ == "__main__":
    df = load_btc_daily()
    df = clean_ohlc(df)
    assert_data_quality(df)
    df = ensure_continuous_daily_index(df)

    outliers = flag_outlier_returns(df)
    print("Outlier days:", outliers.sum())

    df.to_csv("data/btc_daily.csv")
