# Quant Mini Project
by Ryan Kiang

## Overview

This project demonstrates a clean quantitative research workflow on BTC daily data, from feature engineering and signal design to vectorized backtesting with transaction cost modeling, with a focus on research methodology, reproducibility, and honest evaluation against a Buy & Hold benchmark.

The goal is to show how a signal behaves after realistic trading frictions, not to optimize or overfit performance.

## What this project does

- Load & clean BTC daily data
- Build features: returns, momentum, volatility
- Design a simple **long/flat** signal (momentum + volatility filter)
- Run a **vectorized backtest** with:
  - Gross vs Net returns
  - Transaction costs (fees + slippage in bps)
  - Turnover and trade count diagnostics
  - Equity curve, Total return, Sharpe ratio, Max Drawdown
- Compare performance with **Buy & Hold**

---

## Project Structure

```text
quant-mini-project/
├── run.py
├── data/
│   └── btc_daily.csv
└── src/
    ├── data_loader.py   # data ingestion & cleaning
    ├── features.py      # feature engineering
    ├── signals.py       # signal design
    └── backtest.py      # backtesting engine
```

---

## How to run

```bash
pip install numpy pandas matplotlib requests
# Optional: regenerate data
python src/data_loader.py
# Run backtest
python run.py
```

---

## Example Results (current sample)

**Strategy (Net):**

- Total return (gross): ~ +32%
- Total return (net): ~ +9%
- Sharpe (net): ~ 0.25
- Max Drawdown (net): ~ -25%
- Trade count: ~ 128
- Avg turnover: ~ 0.13
- Total cost: ~ 19%

**Buy & Hold (Net):**

- Total return (net): ~ +190%
- Sharpe (net): ~ 1.08
- Avg turnover: ~ 0.001
- Total cost: ~ 0.15%

**Interpretation:**
Although the strategy shows some gross performance, **most of the edge is eaten by transaction costs due to relatively high turnover**. In a strong bull market regime, Buy & Hold significantly outperforms the strategy both gross and net. This highlights the importance of **cost-aware backtesting and turnover control** in quantitative research.

---

**Limitations & Next Steps**

- Only long/flat positions
- Single-asset (BTC)
- No out-of-sample testing
- No position sizing or portfolio construction

**Possible extensions:**

- Out-of-sample / regime-based evaluation
- Turnover reduction and signal smoothing
- Position sizing
- Multi-asset backtesting
- Parameter sensitivity analysis