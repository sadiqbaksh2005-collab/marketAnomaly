import os
import duckdb

query = """
WITH r AS (
  SELECT "Date" AS d, ticker, "Volume" AS vol,
         "Close" / LAG("Close") OVER (PARTITION BY ticker ORDER BY "Date") - 1 AS ret
  FROM read_parquet('data/raw/prices.parquet')
),
s AS (
  SELECT d, ticker, ret, vol,
         AVG(ret) OVER w AS mu,  STDDEV(ret) OVER w AS sd,
         AVG(vol) OVER w AS vmu, STDDEV(vol) OVER w AS vsd
  FROM r
  WINDOW w AS (PARTITION BY ticker ORDER BY d
               ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING)
)
SELECT d AS date, ticker, ret,
       (ret - mu) / sd   AS ret_z,
       (vol - vmu) / vsd AS vol_z
FROM s
WHERE ABS((ret - mu) / sd) > 3 OR (vol - vmu) / vsd > 3
ORDER BY d DESC
"""

df = duckdb.sql(query).df()

os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/anomalies.csv", index=False)

print(len(df), "flagged rows")
print(df.head(20))