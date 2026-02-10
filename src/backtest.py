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
    Gross strategy returns:
    strategy_return_t = signal_{t-1} * asset_return_t
    """
    _assert_input(price, signal)

    asset_ret = compute_returns(price).fillna(0.0)
    position = signal.shift(1).fillna(0.0)

    return position * asset_ret

def compute_net_strategy_returns(
    price: pd.Series,
    signal: pd.Series,
    fee_bps: float = 0.0,
    slip_bps: float = 0.0,
):
    """
    Net strategy returns with simple cost model.

    turnover_t = |pos_t - pos_{t-1}|
    cost_t = (fee_bps + slip_bps) / 10000 * turnover_t
    net_ret_t = gross_ret_t - cost_t
    """
    _assert_input(price, signal)

    # Gross returns
    gross_ret = compute_strategy_returns(price, signal)

    # Positions (current and lagged)
    pos = signal.astype(float)
    pos_lag = pos.shift(1).fillna(0.0)

    # Turnover
    turnover = (pos - pos_lag).abs()

    # Costs
    cost_rate = (fee_bps + slip_bps) / 10000.0
    costs = turnover * cost_rate

    # Net returns
    net_ret = gross_ret - costs

    return net_ret, gross_ret, turnover, costs


def cumulative_returns(returns: pd.Series) -> pd.Series:
    """
    cum_t = (1 + r_t).cumprod() - 1
    """
    assert isinstance(returns, pd.Series)
    return (1.0 + returns).cumprod() - 1.0


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


def run_backtest(
    price: pd.Series,
    signal: pd.Series,
    risk_free_rate: float = 0.0,
    fee_bps: float = 0.0,
    slip_bps: float = 0.0,
) -> dict:
    _assert_input(price, signal)

    net_ret, gross_ret, turnover, costs = compute_net_strategy_returns(
        price, signal, fee_bps=fee_bps, slip_bps=slip_bps
    )

    # Gross
    gross_cum = cumulative_returns(gross_ret)
    gross_equity = 1.0 + gross_cum

    # Net
    net_cum = cumulative_returns(net_ret)
    net_equity = 1.0 + net_cum

    results = {
        # Series
        "gross_returns": gross_ret,
        "net_returns": net_ret,
        "turnover": turnover,
        "costs": costs,
        "gross_equity": gross_equity,
        "net_equity": net_equity,
        # Summary metrics (focus on net)
        "total_return_gross": float(gross_cum.iloc[-1]),
        "total_return_net": float(net_cum.iloc[-1]),
        "max_drawdown_net": max_drawdown(net_equity),
        "sharpe_net": sharpe_ratio(net_ret, risk_free_rate=risk_free_rate),
        # Trading Statistics
        "avg_turnover": float(turnover.mean()),
        "trade_count": int((turnover > 0).sum()),
        "total_cost": float(costs.sum()),
    }

    return results
