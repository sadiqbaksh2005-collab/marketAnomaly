from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI(title="TSX Market Anomaly Monitor")

DATA_PATH = "data/processed/anomalies.csv"


def load() -> pd.DataFrame:
    try:
        return pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Run src/transform.py first")


@app.get("/anomalies")
def anomalies(ticker: Optional[str] = None,
              start: Optional[str] = None,
              limit: int = 50):
    df = load()
    if ticker:
        df = df[df["ticker"] == ticker.upper()]
    if start:
        df = df[df["date"] >= start]
    df = df.head(limit)
    # JSON cannot hold NaN, so convert missing values to null
    return df.astype(object).where(df.notna(), None).to_dict(orient="records")


@app.get("/summary")
def summary():
    df = load()
    counts = df.groupby("ticker").size().sort_values(ascending=False)
    return {
        "total_flagged": int(len(df)),
        "by_ticker": counts.to_dict(),
        "latest_date": str(df["date"].max()),
    }