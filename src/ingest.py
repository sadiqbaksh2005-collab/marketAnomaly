import yfinance as yf
import pandas as pd

tickers = ["RY.TO", "TD.TO", "SHOP.TO", "ENB.TO", "CNQ.TO",
           "BNS.TO", "BMO.TO", "TRP.TO", "SU.TO", "CP.TO"]

frames = []
for t in tickers:
    df = yf.Ticker(t).history(period="2y").reset_index()
    df["ticker"] = t
    frames.append(df[["Date", "ticker", "Close", "Volume"]])

out = pd.concat(frames)
out["Date"] = out["Date"].dt.tz_localize(None)
out.to_parquet("data/raw/prices.parquet", index=False)

print(out.shape)
print(out.groupby("ticker").size())