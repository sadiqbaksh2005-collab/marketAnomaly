import pandas as pd

df = pd.read_csv("data/processed/anomalies.csv")
latest = df["date"].max()
top = df[df["date"] == latest]
print(f"Anomaly report for {latest}")
print(top[["ticker", "ret", "ret_z", "vol_z"]].to_string(index=False)
      if len(top) else "No anomalies on the latest date.")
print("\nMost flagged tickers:")
print(df.groupby("ticker").size().sort_values(ascending=False).head(5))