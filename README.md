# Quant Mini Project
by Ryan Kiang

## Overview

This project demonstrates a clean quantitative research workflow on BTC daily data, from feature engineering and signal design to vectorized backtesting, with a focus on research methodology, reproducibility, and honest evaluation against a Buy & Hold benchmark.

## What this project does

- Load & clean BTC daily data
- Build features: returns, momentum, volatility
- Design a simple **long/flat** signal (momentum + volatility filter)
- Run a **vectorized backtest**:
  - Strategy returns, cumulative returns, equity curve
  - Total return, Sharpe ratio, Max Drawdown
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

- **Strategy Total Return:** ~ +32%
- **Strategy Sharpe Ratio:** ~ 0.57
- **Strategy Max Drawdown:** ~ -21%
- Buy & Hold significantly outperforms the strategy during the same period

**Interpretation:**
The strategy underperforms Buy & Hold in a strong bull market regime, indicating that the volatility filter keeps the strategy out during some strong trending phases. The main goal here is to demonstrate correct research workflow and backtesting architecture, not to optimize returns.

**Limitations & Next Steps**

- No transaction costs or slippage
- Only long/flat positions
- No out-of-sample testing

**Possible extensions:**

- Add costs & slippage
- Add position sizing
- Add regime / out-of-sample tests