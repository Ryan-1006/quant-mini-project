-- Example schema (Postgres):
-- CREATE TABLE prices (
--   symbol TEXT,
--   ts TIMESTAMPTZ,
--   open DOUBLE PRECISION,
--   high DOUBLE PRECISION,
--   low DOUBLE PRECISION,
--   close DOUBLE PRECISION,
--   volume DOUBLE PRECISION
-- );

-- =========================================
-- Market Data Exploratory Analysis (SQL)
-- =========================================

-- 1) Daily returns
SELECT
  ts,
  close / LAG(close) OVER (PARTITION BY symbol ORDER BY ts) - 1 AS daily_return
FROM prices
WHERE symbol = 'BTCUSDT'
ORDER BY ts;

-- 2) Rolling 20-day volatility
WITH rets AS (
  SELECT
    ts,
    close / LAG(close) OVER (ORDER BY ts) - 1 AS ret
  FROM prices
  WHERE symbol = 'BTCUSDT'
)
SELECT
  ts,
  STDDEV(ret) OVER (
    ORDER BY ts
    ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
  ) AS vol_20d
FROM rets
ORDER BY ts;

-- 3) Monthly returns
WITH m AS (
  SELECT
    DATE_TRUNC('month', ts) AS month,
    ts,
    close
  FROM prices
  WHERE symbol = 'BTCUSDT'
),
bounds AS (
  SELECT
    month,
    MIN(ts) AS first_ts,
    MAX(ts) AS last_ts
  FROM m
  GROUP BY month
)
SELECT
  b.month,
  (m_last.close / m_first.close) - 1 AS monthly_return
FROM bounds b
JOIN m m_first
  ON m_first.month = b.month AND m_first.ts = b.first_ts
JOIN m m_last
  ON m_last.month = b.month AND m_last.ts = b.last_ts
ORDER BY b.month;


-- 4) Regime definition using MA200 (bull/bear)
WITH ma AS (
  SELECT
    ts,
    close,
    AVG(close) OVER (
      PARTITION BY symbol
      ORDER BY ts
      ROWS BETWEEN 199 PRECEDING AND CURRENT ROW
    ) AS ma200
  FROM prices
  WHERE symbol = 'BTCUSDT'
),
rets AS (
  SELECT
    ts,
    close / LAG(close) OVER (PARTITION BY symbol ORDER BY ts) - 1 AS ret
  FROM prices
  WHERE symbol = 'BTCUSDT'
)
SELECT
  CASE
    WHEN m.close > m.ma200 THEN 'BULL'
    ELSE 'BEAR'
  END AS regime,
  COUNT(r.ret) AS n_days,
  AVG(r.ret) AS avg_daily_return,
  STDDEV(r.ret) AS daily_vol
FROM ma m
JOIN rets r
  ON m.ts = r.ts
WHERE m.ma200 IS NOT NULL
  AND r.ret IS NOT NULL
GROUP BY 1
ORDER BY 1;