import pandas as pd

def compute_returns(prices: pd.Series) -> pd.Series:
    """
    Compute simple returns.
    Return[t] = price[t] / price[t-1] - 1
    """
    return prices.pct_change()


def momentum(prices: pd.Series, window: int) -> pd.Series:
    """
    Compute momentum as percentage change over a given window.
    Momentum[t] = price[t] / price[t-window] - 1
    """
    return prices.pct_change(window)


def volatility(returns: pd.Series, window: int) -> pd.Series:
    """
    Compute rolling volatility (standard deviation of returns).
    """
    return returns.rolling(window).std()