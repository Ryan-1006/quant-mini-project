import pandas as pd
import matplotlib.pyplot as plt

# === Step 3: Build signal ===
from src.signals import momentum_vol_signal

# === Step 4: Backtest engine ===
from src.backtest import run_backtest


def main():
    # === Step 1: Load data from CSV ===
    df = pd.read_csv(
        "data/btc_daily.csv",
        index_col=0,
        parse_dates=[0])
    df.index.name = "open_time"

    price = df["close"].astype(float)

    # === Step 3: Build signal ===
    signal = momentum_vol_signal(price)

    # === Step 4: Run backtest ===
    fee_bps = 10.0
    slip_bps = 5.0

    results = run_backtest(price, signal, fee_bps=fee_bps, slip_bps=slip_bps)

    print("===== Strategy Results (Net) =====")
    print("Total return (gross):", results["total_return_gross"])
    print("Total return (net):", results["total_return_net"])
    print("Sharpe (net):", results["sharpe_net"])
    print("Max drawdown (net):", results["max_drawdown_net"])
    print("Trade count:", results["trade_count"])
    print("Avg turnover:", results["avg_turnover"])
    print("Total cost:", results["total_cost"])

    # Plot strategy equity: Gross vs Net
    ax = results["gross_equity"].plot(label="Strategy (Gross)", title="Strategy Equity: Gross vs Net")
    results["net_equity"].plot(ax=ax, label="Strategy (Net)")
    ax.legend()
    plt.show()

    # === Step 6: Baseline Buy & Hold ===
    bh_signal = pd.Series(1.0, index=price.index)
    bh_results = run_backtest(price, bh_signal, fee_bps=fee_bps, slip_bps=slip_bps)

    print("\n===== Buy & Hold Results (Net) =====")
    print("Total return (gross):", bh_results["total_return_gross"])
    print("Total return (net):", bh_results["total_return_net"])
    print("Sharpe (net):", bh_results["sharpe_net"])
    print("Max drawdown (net):", bh_results["max_drawdown_net"])
    print("Avg turnover:", bh_results["avg_turnover"])
    print("Total cost:", bh_results["total_cost"])

    # Plot equity comparison (Net)
    ax = results["net_equity"].plot(label="Strategy (Net)", title="Equity Comparison (Net)")
    bh_results["net_equity"].plot(ax=ax, label="Buy & Hold (Net)")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
