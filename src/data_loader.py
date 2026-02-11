import time
import requests
import pandas as pd

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"

def load_btc_daily(
    symbol: str = "BTCUSDT",
    interval: str = "1d",
    start: str = "2019-01-01",
    end: str | None = None,
    limit: int = 1000,
    sleep_sec: float = 0.2,
) -> pd.DataFrame:
    """
    Load BTC daily OHLCV data from Binance using paginated /klines (limit=1000 per request).
    """

    assert 1 <= limit <= 1000

    start_ts = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)
    end_ts = None if end is None else int(pd.Timestamp(end, tz="UTC").timestamp() * 1000)

    all_rows: list[list] = []
    cur_start = start_ts

    while True:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
            "startTime": cur_start,
        }
        if end_ts is not None:
            params["endTime"] = end_ts

        resp = requests.get(BINANCE_KLINES_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if not data:
            break

        all_rows.extend(data)

        last_open_time = int(data[-1][0])

        # Stop when reaching end_ts
        if end_ts is not None and last_open_time >= end_ts:
            break

        # Advance startTime to avoid overlapping last candle
        next_start = last_open_time + 1

        # Safety check to avoid infinite loop if API misbehaves
        if next_start <= cur_start:
            break

        cur_start = next_start
        time.sleep(sleep_sec)

    df = pd.DataFrame(
        all_rows,
        columns=[
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
            "ignore",
        ],
    )

    # Deduplicate in case of overlapping pages
    df = df.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)

    return df

def clean_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.set_index("open_time").sort_index()
    return df

def assert_data_quality(df: pd.DataFrame) -> None:
    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.tz is not None
    assert df.index.is_monotonic_increasing

    close = df["close"].astype(float)
    assert (close > 0).all()
    assert close.isna().sum() == 0

def ensure_continuous_daily_index(df: pd.DataFrame) -> pd.DataFrame:
    expected_index = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )
    df = df.reindex(expected_index)
    df = df.ffill()
    return df

def flag_outlier_returns(df: pd.DataFrame, threshold: float = 1.0) -> pd.DataFrame:
    returns = df["close"].astype(float).pct_change()
    df["is_outlier"] = returns.abs() > threshold
    return df

if __name__ == "__main__":
    
    df = load_btc_daily(start="2019-01-01")

    df = clean_ohlc(df)
    assert_data_quality(df)
    df = ensure_continuous_daily_index(df)

    df = flag_outlier_returns(df)
    print("Rows:", len(df))
    print("Outlier days:", int(df["is_outlier"].sum()))

    df.to_csv("data/btc_daily.csv")
    print("Saved to data/btc_daily.csv")
