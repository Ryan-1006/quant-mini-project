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

    # === Step 4: Run backtest (strategy) ===
    results = run_backtest(price, signal)

    print("===== Strategy Results =====")
    print("Total return:", results["total_return"])
    print("Sharpe ratio:", results["sharpe_ratio"])
    print("Max drawdown:", results["max_drawdown"])

    # Plot strategy equity curve
    equity = results["equity"]
    equity.plot(title="Strategy Equity Curve")
    plt.show()

    # === Step 6: Baseline Buy & Hold ===
    bh_signal = pd.Series(1.0, index=price.index)
    bh_results = run_backtest(price, bh_signal)

    print("\n===== Buy & Hold Results =====")
    print("Total return:", bh_results["total_return"])
    print("Sharpe ratio:", bh_results["sharpe_ratio"])
    print("Max drawdown:", bh_results["max_drawdown"])

    # Plot equity comparison
    ax = equity.plot(label="Strategy", title="Equity Comparison")
    bh_results["equity"].plot(ax=ax, label="Buy & Hold")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()
