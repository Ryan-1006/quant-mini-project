import pandas as pd
from src.features import compute_returns, momentum, volatility

def momentum_vol_signal(
    prices: pd.Series,
    mom_window: int = 10,
    vol_window: int = 10
) -> pd.Series:
    """
    Momentum + volatility filter signal.
    Returns binary signal (0/1).
    """

    rets = compute_returns(prices)
    mom = momentum(prices, mom_window)
    vol = volatility(rets, vol_window)

    vol_threshold = vol.median()

    signal = (mom > 0) & (vol < vol_threshold)
    signal = signal.fillna(False).astype(int)

    return signal
