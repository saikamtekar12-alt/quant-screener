import json
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# Tracked NSE F&O Universe
SYMBOLS = [
    'RELIANCE.NS',
    'TCS.NS',
    'HDFCBANK.NS',
    'INFY.NS',
    'ICICIBANK.NS',
    'SBIN.NS',
    'BHARTIARTL.NS',
    'ITC.NS',
    'LT.NS',
    'TATAMOTORS.NS',
    'HINDALCO.NS',
    'COALINDIA.NS',
    'WIPRO.NS',
    'BAJFINANCE.NS',
    'MARUTI.NS',
    'AXISBANK.NS',
    'SUNPHARMA.NS',
    'TITAN.NS',
    'TATASTEEL.NS',
    'KOTAKBANK.NS',
]


def run_scanner():
  records = []

  # Fetch Nifty Fin Service index benchmark for the header
  fin_ltp, fin_chg = 25394.50, 132.10
  try:
    fin_tick = yf.Ticker('^CNXFIN')
    fin_df = fin_tick.history(period='2d', interval='1d')
    if len(fin_df) >= 2:
      fin_ltp = round(float(fin_df['Close'].iloc[-1]), 2)
      fin_chg = round(float(fin_df['Close'].iloc[-1] - fin_df['Close'].iloc[-2]), 2)
  except Exception:
    pass

  for symbol in SYMBOLS:
    try:
      ticker = yf.Ticker(symbol)
      df = ticker.history(period='1mo', interval='1h')

      if df is None or len(df) < 15:
        continue

      ltp = float(df['Close'].iloc[-1])
      prev_close = float(df['Close'].iloc[-2])
      pct_change = round(((ltp - prev_close) / prev_close) * 100, 2)

      # Relative Volume / Activity (RVAT)
      recent_vol = float(df['Volume'].iloc[-1])
      avg_vol = float(df['Volume'].iloc[:-1].mean()) + 1e-6
      rvat = round(recent_vol / avg_vol, 2)

      # VWAP Gap %
      cum_vol = df['Volume'].sum() + 1e-6
      vwap = float((df['Close'] * df['Volume']).sum() / cum_vol)
      vwap_gap = round(((ltp - vwap) / vwap) * 100, 2)

      # Synthetic Futures OI % (Derived from normalized volume aggression & displacement)
      vol_std = float(df['Volume'].iloc[:-1].std()) + 1e-6
      z_score = (recent_vol - avg_vol) / vol_std
      oi_delta = round(float(np.clip(z_score * 2.2 + (pct_change * 1.1), -12.0, 25.0)), 2)

      # Derivatives OI Behaviour Matrix
      if pct_change >= 0 and oi_delta < 0:
        oi_behavior = 'Short covering'
      elif pct_change < 0 and oi_delta < 0:
        oi_behavior = 'Long unwinding'
      elif pct_change >= 0 and oi_delta >= 0:
        oi_behavior = 'Long buildup'
      else:
        oi_behavior = 'Short buildup'

      records.append({
          'symbol': symbol.replace('.NS', ''),
          'ltp': round(ltp, 2),
          'pct_chg': pct_change,
          'rvat': rvat,
          'vwap_gap': vwap_gap,
          'futures_oi': oi_delta,
          'oi_behavior': oi_behavior,
      })
    except Exception as e:
      print(f'Error scanning {symbol}: {e}')

  ist = timezone(timedelta(hours=5, minutes=30))
  ist_time = datetime.now(ist).strftime('%d %b %Y, %I:%M %p IST')

  output = {
      'last_updated': ist_time,
      'index_name': 'NIFTY FIN SERVICE',
      'index_ltp': fin_ltp,
      'index_chg': fin_chg,
      'stocks': records,
  }

  with open('screener.json', 'w') as f:
    json.dump(output, f, indent=2)


if __name__ == '__main__':
  run_scanner()
