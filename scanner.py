from datetime import datetime
import json
import numpy as np
import yfinance as yf

# High-liquid NSE universe for baseline scanning
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

  for symbol in SYMBOLS:
    try:
      ticker = yf.Ticker(symbol)
      df = ticker.history(period='1mo', interval='1h')

      if len(df) < 15:
        continue

      ltp = float(df['Close'].iloc[-1])
      prev_close = float(df['Close'].iloc[-2])
      pct_change = round(((ltp - prev_close) / prev_close) * 100, 2)

      # 1. Volume Divergence (Self-Baseline Z-Score)
      current_vol = float(df['Volume'].iloc[-1])
      hist_vols = df['Volume'].iloc[:-1]
      v_mean = float(hist_vols.mean())
      v_std = float(hist_vols.std()) + 1e-6
      z_score = round((current_vol - v_mean) / v_std, 2)

      # 2. VWAP & Relative Momentum Score
      cum_vol = df['Volume'].sum() + 1e-6
      vwap = float((df['Close'] * df['Volume']).sum() / cum_vol)
      vwap_dist = ((ltp - vwap) / vwap) * 100
      vol_multiplier = current_vol / (v_mean + 1e-6)
      momentum_matrix = round(vwap_dist * vol_multiplier, 2)

      # 3. HyperFlow Metric: Base 1.0 bounded to 5.0 scale
      hyper_flow = round(float(np.clip(1.0 + max(0.0, z_score), 1.0, 5.0)), 2)

      records.append({
          'symbol': symbol.replace('.NS', ''),
          'ltp': round(ltp, 2),
          'pct_chg': pct_change,
          'hyper_flow': hyper_flow,
          'z_score': z_score,
          'momentum': momentum_matrix,
      })
    except Exception as e:
      print(f'Error processing {symbol}: {e}')

  # Sort by highest baseline divergence (HyperFlow rank)
  records.sort(key=lambda item: item['hyper_flow'], reverse=True)

  output = {
      'last_updated': datetime.utcnow().strftime('%d %b %Y, %H:%M UTC'),
      'stocks': records,
  }

  with open('screener.json', 'w') as f:
    json.dump(output, f, indent=2)


if __name__ == '__main__':
  run_scanner()
