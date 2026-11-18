# TSX Market Anomaly Monitor

Flags unusual daily price and volume moves for 10 TSX stocks.

## Pipeline
1. `src/ingest.py` pulls 2 years of daily data (yfinance) and saves Parquet
2. `src/transform.py` computes returns and 20 day rolling z-scores with SQL
   window functions (DuckDB), excluding the current day from its baseline
3. Days with |return z| > 3 or volume z > 3 are saved to `data/processed/anomalies.csv`

## Run
pip install yfinance pandas pyarrow duckdb
python src/ingest.py
python src/transform.py

## Limitations and next steps
- A z-score threshold of 3 assumes roughly normal returns; real returns have fat tails
- Market wide moves flag many stocks at once; compare against an index instead
- Add a FastAPI endpoint and a daily report script