import numpy as np
import pandas as pd

from src.features import compute_returns

TRADING_DAYS = 365


def _assert_input(price: pd.Series, signal: pd.Series):
    assert isinstance(price, pd.Series)
    assert isinstance(signal, pd.Series)
    assert len(price) == len(signal)
    assert price.index.equals(signal.index)
    assert price.isnull().sum() == 0
    assert signal.isnull().sum() == 0


def compute_strategy_returns(price: pd.Series, signal: pd.Series) -> pd.Series:
    """
    strategy_return_t = signal_{t-1} * asset_return_t
    """
    _assert_input(price, signal)

    asset_ret = compute_returns(price).fillna(0.0)
    position = signal.shift(1).fillna(0.0)

    return position * asset_ret


def cumulative_returns(strategy_returns: pd.Series) -> pd.Series:
    """
    cum_t = (1 + r_t).cumprod() - 1
    """
    assert isinstance(strategy_returns, pd.Series)
    return (1.0 + strategy_returns).cumprod() - 1.0


def max_drawdown(equity: pd.Series) -> float:
    """
    MDD = min( equity / cummax(equity) - 1 )
    """
    assert isinstance(equity, pd.Series)

    running_max = equity.cummax()
    drawdown = equity / running_max - 1.0

    return float(drawdown.min())


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    annualization: int = TRADING_DAYS,
) -> float:
    """
    excess = returns - rf / annualization
    Sharpe = mean(excess) / std(excess) * sqrt(annualization)
    """
    assert isinstance(returns, pd.Series)

    excess = returns - risk_free_rate / annualization
    mu = excess.mean()
    sigma = excess.std(ddof=1)

    if sigma == 0 or np.isnan(sigma):
        return 0.0

    return float(mu / sigma * np.sqrt(annualization))


def run_backtest(price: pd.Series, signal: pd.Series, risk_free_rate: float = 0.0) -> dict:
    _assert_input(price, signal)

    strategy_returns = compute_strategy_returns(price, signal)
    cum_returns = cumulative_returns(strategy_returns)
    equity = 1.0 + cum_returns

    results = {
        "strategy_returns": strategy_returns,
        "cumulative_returns": cum_returns,
        "equity": equity,
        "total_return": float(cum_returns.iloc[-1]),
        "max_drawdown": max_drawdown(equity),
        "sharpe_ratio": sharpe_ratio(strategy_returns, risk_free_rate=risk_free_rate),
    }

    return results