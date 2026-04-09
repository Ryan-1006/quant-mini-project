# BTC Market Data Analysis & Dashboard Project
by Dat Kiang

## Overview

This project demonstrates an end-to-end data analysis workflow using BTC market data, focusing on data cleaning, transformation, and visualization.

The goal is to analyze trends and patterns in time-series data and present insights through dashboards to support data-driven decision-making.

The project emphasizes data processing, SQL-based analytics, and visualization rather than trading strategy optimization.

## Business Value

- Demonstrates ability to process and analyze large datasets  
- Transforms raw data into actionable insights  
- Builds dashboards to support data exploration  
- Applies SQL and analytics skills in real-world scenarios

## What this project does

- Load and clean BTC market data
- Transform raw data into structured datasets using Python and SQL
- Compute key metrics such as returns, volatility, and rolling averages
- Analyze trends and patterns in time-series data
- Build a Tableau dashboard to visualize key insights (price trends, volume, market behavior)

---

## Project Structure

```text
quant-mini-project/
├── run.py
├── sql/
│   └── market_data_eda.sql	# Market data research queries in Postgres (returns/vol/regime)
├── data/
│   └── btc_daily.csv
├── images/
│   └── btc_dashboard.png	# Tableau dashboard screenshot
└── src/
    ├── data_loader.py
    ├── features.py
    ├── signals.py	# Feature engineering logic
    └── backtest.py	# Evaluation & validation logic
```

---

## How to run

```bash
pip install numpy pandas matplotlib requests

# Optional: regenerate data
python src/data_loader.py

# Run data analysis pipeline
python run.py
```
---

## SQL (Postgres)

This repo includes SQL queries used to analyze time-series data, including calculating rolling metrics and identifying trends in market behavior.

---

## Key Insights

- Market behavior differs significantly across trending and sideways periods, affecting the stability of observed patterns.

- Strong trends are often accompanied by increased trading volume, indicating higher market participation.

- Results highlight the importance of validating insights on unseen data to avoid overfitting and ensure reliability.

---

## Tableau Dashboard – Market Exploration

The dashboard was built to explore trends and patterns in BTC market data through interactive visualizations.

It allows users to analyze price movements, trading activity, and key metrics over time.

The goal is to support data exploration and insight generation rather than predictive modeling.

### Dashboard Preview

![BTC Dashboard](images/btc_dashboard.png)

**Live Dashboard:**  https://public.tableau.com/app/profile/dat.kiang/viz/Book1_17731725954590/Dashboard1

The dashboard focuses on three aspects:

### 1. Market Overview
The price chart shows long-term BTC trends and major market cycles.

### 2. Market Activity
Volume data highlights periods of increased trading activity, often coinciding with major price movements.

### 3. Market Behavior
The visual patterns in price and volume help explain how certain patterns perform differently under various market conditions, especially between trending and sideways periods.

This dashboard serves as a visual layer to support data exploration and decision-making.

---

## Scope and Limitations

Scope:
- Focuses on single-asset time-series data (BTC)
- Uses historical data for analysis

Limitations:
- Limited dataset scope
- Does not include external macroeconomic factors

## Possible Extensions

- Incorporate additional datasets (e.g., macro indicators, market sentiment)
- Improve data pipeline automation
- Enhance dashboard interactivity and usability
- Apply the workflow to other datasets (e.g., sales, customer behavior)