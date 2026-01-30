# Quant Mini Project
by Ryan Kiang

## Overview
This project demonstrates a simple but robust quantitative research pipeline,
starting from raw market data to a backtest-ready dataset.

The goal is not to optimize profits, but to build correct foundations:
data integrity, reproducibility, and prevention of common backtesting errors.

---

## Step 1 – Data Ingestion & Cleaning

### Data Source
- Binance public REST API
- Instrument: BTC/USDT
- Timeframe: Daily candles

### Data Handling
- Convert raw timestamps to timezone-aware datetime (UTC)
- Set datetime as index and ensure monotonic ordering
- Ensure daily timeline continuity
- Forward-fill missing days to avoid implicit look-ahead

### Data Quality Checks
The following assertions are enforced before any research is performed:
- Datetime index with explicit timezone
- No missing close prices
- Close prices strictly greater than zero
- Sorted and continuous time index

### Outlier Handling
Daily returns are inspected for abnormal values.
Extreme returns are flagged for inspection rather than blindly removed,
to avoid introducing survivorship or look-ahead bias.

---

## Design Philosophy
Incorrect data handling can silently introduce:
- Look-ahead bias
- Timezone misalignment
- False performance during backtesting

This project prioritizes correctness and robustness over headline PnL.

---

## Next Steps
- Feature engineering (returns, volatility)
- Signal design
- Backtesting with transaction costs and slippage
