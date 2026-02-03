# Quant Mini Project
by Ryan Kiang

## Overview
This project implements a minimal end-to-end quantitative research pipeline
on cryptocurrency market data. The goal is to showcase correct data handling,
feature engineering, and signal design prior to backtesting.

---

## Project Structure

```text
quant-mini-project/
├── data/
│   └── btc_daily.csv
├── src/
│   ├── data_loader.py
│   ├── features.py
│   └── signals.py
└── README.md
```
---

## Pipeline Overview

The research pipeline is incrementally developed in logical steps:

1. **Data Ingestion & Cleaning:**  
   Load daily OHLCV data from Binance API, enforce clear datetime indexing,
   and perform basic quality checks.

2. **Feature Engineering:**  
   Compute essential quantitative features such as returns, momentum and volatility.

3. **Signal Design:**  
   Define trading signals based on feature thresholds without backtesting logic.

4. **Backtest Architecture:** *(next step)*  
   Implement architecture to evaluate strategy performance over time.

5. **Risk & Robustness Analysis:** *(future work)*  
   Incorporate transaction costs, slippage, and stress testing of signals.

---

## Step 1 — Data Ingestion & Cleaning

- **Data source:** Binance REST API (BTC/USDT, daily data)  
- **Index:** timezone-aware datetime; sorted and continuous  
- **Checks:** no missing close values, positive pricing  
- **Outliers:** flagged but not removed to avoid irreversible bias

**Implementation:** `src/data_loader.py`  
**Output:** `data/btc_daily.csv`

---

## Step 2 — Feature Engineering

Quantitative features implemented:

- **Returns:** simple daily percentage returns  
- **Momentum:** rolling change over a fixed window  
- **Volatility:** rolling standard deviation of returns

**Implementation:** `src/features.py`

---

## Step 3: Signal Design

**Objective**

Define a simple, interpretable trading signal using previously engineered features, without introducing backtesting or execution logic.

**Signal Logic**

The strategy generates a binary long-only signal (0/1) based on:

- **Positive momentum** over a fixed lookback window
- **Low volatility regime**, defined as volatility below its historical median

Formally:

- Signal = 1 if
	Momentum > 0
	Volatility < median(volatility)
- Signal = 0 otherwise

**Implementation Notes**

- Signal computation reuses feature functions from Step 2 (returns, momentum, volatility)
- The output is a pd.Series aligned with the price index
- Initial periods with insufficient data naturally result in 0 signals
- No NaN values are propagated into the final signal to ensure downstream compatibility

---

## Next Steps

Backtest logic, and robust evaluation are in progress
and will be added incrementally.

---

## Notes

This project is intended to demonstrate proper quantitative workflow,
not to produce a live automated trading strategy.