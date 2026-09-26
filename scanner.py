import json
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "ITC.NS",
    "LT.NS",
    "TATAMOTORS.NS",
    "HINDALCO.NS",
    "COALINDIA.NS",
    "WIPRO.NS",
    "BAJFINANCE.NS",
    "MARUTI.NS",
    "AXISBANK.NS",
    "SUNPHARMA.NS",
    "TITAN.NS",
    "TATASTEEL.NS",
    "KOTAKBANK.NS",
]


def run_scanner():
  records = []

  for symbol in SYMBOLS:
    try:
      ticker = yf.Ticker(symbol)
      df = ticker.history(period="1mo", interval="1h")

      if df is None or len(df) < 15:
        continue

      ltp = float(df["Close"].iloc[-1])
      prev_close = float(df["Close"].iloc[-2])
      pct_change = round(((ltp - prev_close) / prev_close) * 100, 2)

      # Baseline Volume Divergence
      current_vol = float(df["Volume"].iloc[-1])
      hist_vols = df["Volume"].iloc[:-1]
      v_mean = float(hist_vols.mean())
      v_std = float(hist_vols.std()) + 1e-6
      z_score = round((current_vol - v_mean) / v_std, 2)

      # VWAP & Momentum
      cum_vol = df["Volume"].sum() + 1e-6
      vwap = float((df["Close"] * df["Volume"]).sum() / cum_vol)
      vwap_dist = ((ltp - vwap) / vwap) * 100
      vol_multiplier = current_vol / (v_mean + 1e-6)
      momentum_matrix = round(vwap_dist * vol_multiplier, 2)

      # Normalized HyperFlow Score
      hyper_flow = round(float(np.clip(1.0 + max(0.0, z_score), 1.0, 5.0)), 2)

      records.append({
          "symbol": symbol.replace(".NS", ""),
          "ltp": round(ltp, 2),
          "pct_chg": pct_change,
          "hyper_flow": hyper_flow,
          "z_score": z_score,
          "momentum": momentum_matrix,
      })
    except Exception as e:
      print(f"Skipping {symbol}: {e}")

  records.sort(key=lambda item: item["hyper_flow"], reverse=True)

  # Exact IST calculation (+5:30)
  ist = timezone(timedelta(hours=5, minutes=30))
  ist_time_str = datetime.now(ist).strftime("%d %b %Y, %I:%M %p IST")

  output = {"last_updated": ist_time_str, "stocks": records}

  with open("screener.json", "w") as f:
    json.dump(output, f, indent=2)


if __name__ == "__main__":
  run_scanner()
