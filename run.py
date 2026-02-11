import pandas as pd
import matplotlib.pyplot as plt


from src.signals import momentum_vol_signal
from src.backtest import run_backtest, sharpe_ratio, max_drawdown


def _print_block(title: str, metrics: dict) -> None:
    print(f"\n===== {title} =====")
    for k, v in metrics.items():
        print(f"{k}: {v}")


def _summarize_results(results: dict) -> dict:
    """
    results is the dict returned by run_backtest.
    """
    net_equity = results["net_equity"]
    net_returns = results["net_returns"]

    summary = {
        "Total return (gross)": round(results["total_return_gross"], 4),
        "Total return (net)": round(results["total_return_net"], 4),
        "Sharpe (net)": round(results["sharpe_net"], 4),
        "Max drawdown (net)": round(results["max_drawdown_net"], 4),
        "Avg turnover": round(results["avg_turnover"], 4),
        "Trade count": int((results["turnover"] > 0).sum()),
        "Total cost": round(results["total_cost"], 4),
        "End equity (net)": round(float(net_equity.iloc[-1]), 4),
        "Mean daily net ret": round(float(net_returns.mean()), 6),
    }
    return summary


def _regime_metrics(net_returns: pd.Series, bull_mask: pd.Series) -> dict:
    """
    Compute regime metrics on net_returns, split by bull_mask (True=bull).
    """
    assert net_returns.index.equals(bull_mask.index)

    valid = bull_mask.notna()
    net_returns = net_returns[valid]
    bull_mask = bull_mask[valid]

    bull_ret = net_returns[bull_mask]
    bear_ret = net_returns[~bull_mask]

    def _equity_from_returns(r: pd.Series) -> pd.Series:
        return (1.0 + r.fillna(0.0)).cumprod()

    bull_eq = _equity_from_returns(bull_ret)
    bear_eq = _equity_from_returns(bear_ret)

    metrics = {
        "Bull days": int(bull_ret.shape[0]),
        "Bear days": int(bear_ret.shape[0]),
        "Bull total return": round(float(bull_eq.iloc[-1] - 1.0) if len(bull_eq) else 0.0, 4),
        "Bear total return": round(float(bear_eq.iloc[-1] - 1.0) if len(bear_eq) else 0.0, 4),
        "Bull Sharpe": round(float(sharpe_ratio(bull_ret)) if len(bull_ret) else 0.0, 4),
        "Bear Sharpe": round(float(sharpe_ratio(bear_ret)) if len(bear_ret) else 0.0, 4),
        "Bull MDD": round(float(max_drawdown(bull_eq)) if len(bull_eq) else 0.0, 4),
        "Bear MDD": round(float(max_drawdown(bear_eq)) if len(bear_eq) else 0.0, 4),
    }
    return metrics


def main():
    # === Data ===
    df = pd.read_csv(
        "data/btc_daily.csv",
        index_col=0,
        parse_dates=[0])
    df.index.name = "open_time"
    price = df["close"].astype(float)

    # === Research parameters ===
    MOM_WINDOW = 10
    VOL_WINDOW = 10

    signal = momentum_vol_signal(price, mom_window=MOM_WINDOW, vol_window=VOL_WINDOW)


    # === Costs ===
    fee_bps = 10.0
    slip_bps = 5.0

    # === Out-of-sample evaluation ===
    split_date = "2024-01-01"
    price_train = price.loc[:split_date]
    signal_train = signal.loc[:split_date]

    price_test = price.loc[split_date:]
    signal_test = signal.loc[split_date:]

    train_res = run_backtest(price_train, signal_train, fee_bps=fee_bps, slip_bps=slip_bps)
    test_res = run_backtest(price_test, signal_test, fee_bps=fee_bps, slip_bps=slip_bps)

    _print_block("Strategy - TRAIN (Net)", _summarize_results(train_res))
    _print_block("Strategy - TEST (Net)", _summarize_results(test_res))

    # === Buy & Hold baseline ===
    bh_train = pd.Series(1.0, index=price_train.index)
    bh_test = pd.Series(1.0, index=price_test.index)

    bh_train_res = run_backtest(price_train, bh_train, fee_bps=fee_bps, slip_bps=slip_bps)
    bh_test_res = run_backtest(price_test, bh_test, fee_bps=fee_bps, slip_bps=slip_bps)

    _print_block("Buy & Hold - TRAIN (Net)", _summarize_results(bh_train_res))
    _print_block("Buy & Hold - TEST (Net)", _summarize_results(bh_test_res))

    # === Regime analysis ===
    ma200 = price.rolling(200).mean()
    bull_mask = (price > ma200).fillna(False)

    # Strategy net returns on full history
    full_res = run_backtest(price, signal, fee_bps=fee_bps, slip_bps=slip_bps)
    regime_stats = _regime_metrics(full_res["net_returns"], bull_mask)
    _print_block("Regime Analysis (Strategy Net) - Bull vs Bear (MA200)", regime_stats)


    # === Plots ===

    # 1) Train/Test net equity for strategy
    ax = train_res["net_equity"].plot(title="Strategy Net Equity - Train vs Test", label="Train (Net)")
    test_res["net_equity"].plot(ax=ax, label="Test (Net)")
    ax.axvline(pd.Timestamp(split_date), linestyle="--", linewidth=1, label="Split date")
    ax.legend()
    plt.show()

    # 2) Net equity comparison (full): Strategy vs Buy & Hold
    bh_full = pd.Series(1.0, index=price.index)
    bh_full_res = run_backtest(price, bh_full, fee_bps=fee_bps, slip_bps=slip_bps)

    ax = full_res["net_equity"].plot(title="Net Equity Comparison (Full)", label="Strategy (Net)")
    bh_full_res["net_equity"].plot(ax=ax, label="Buy & Hold (Net)")
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
