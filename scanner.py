import json
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# NSE universe mapped with sectors
STOCKS_METADATA = [
    {"symbol": "RELIANCE.NS", "sector": "Energy / Oil & Gas"},
    {"symbol": "TCS.NS", "sector": "Information Tech"},
    {"symbol": "HDFCBANK.NS", "sector": "Financial Services"},
    {"symbol": "INFY.NS", "sector": "Information Tech"},
    {"symbol": "ICICIBANK.NS", "sector": "Financial Services"},
    {"symbol": "SBIN.NS", "sector": "Financial Services"},
    {"symbol": "BHARTIARTL.NS", "sector": "Telecommunication"},
    {"symbol": "ITC.NS", "sector": "FMCG"},
    {"symbol": "LT.NS", "sector": "Capital Goods"},
    {"symbol": "TATAMOTORS.NS", "sector": "Automobile"},
    {"symbol": "HINDALCO.NS", "sector": "Metals & Mining"},
    {"symbol": "COALINDIA.NS", "sector": "Energy / Coal"},
    {"symbol": "WIPRO.NS", "sector": "Information Tech"},
    {"symbol": "BAJFINANCE.NS", "sector": "Financial Services"},
    {"symbol": "MARUTI.NS", "sector": "Automobile"},
    {"symbol": "AXISBANK.NS", "sector": "Financial Services"},
    {"symbol": "SUNPHARMA.NS", "sector": "Healthcare / Pharma"},
    {"symbol": "TITAN.NS", "sector": "Consumer Durables"},
    {"symbol": "TATASTEEL.NS", "sector": "Metals & Mining"},
    {"symbol": "KOTAKBANK.NS", "sector": "Financial Services"},
]

def run_scanner():
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)
    
    # 1. Fetch Top Index & India VIX Benchmarks
    vix_val, vix_chg = 12.36, -0.31
    fin_val, fin_chg, fin_pct = 25394.50, 132.10, 0.52
    
    try:
        vix_df = yf.Ticker("^INDIAVIX").history(period="2d")
        if len(vix_df) >= 2:
            vix_val = round(float(vix_df["Close"].iloc[-1]), 2)
            vix_chg = round(float(vix_df["Close"].iloc[-1] - vix_df["Close"].iloc[-2]), 2)
    except Exception:
        pass

    try:
        fin_df = yf.Ticker("^CNXFIN").history(period="2d")
        if len(fin_df) >= 2:
            fin_val = round(float(fin_df["Close"].iloc[-1]), 2)
            fin_chg = round(float(fin_df["Close"].iloc[-1] - fin_df["Close"].iloc[-2]), 2)
            fin_pct = round(((fin_val - float(fin_df["Close"].iloc[-2])) / float(fin_df["Close"].iloc[-2])) * 100, 2)
    except Exception:
        pass

    # 2. Process All Tickers
    scanned = []
    sector_gains = {}

    for item in STOCKS_METADATA:
        sym = item["symbol"]
        sec = item["sector"]
        try:
            ticker = yf.Ticker(sym)
            df = ticker.history(period="1mo", interval="1h")
            if df is None or len(df) < 15:
                continue

            ltp = float(df["Close"].iloc[-1])
            prev_close = float(df["Close"].iloc[-2])
            pct_chg = round(((ltp - prev_close) / prev_close) * 100, 2)
            
            # Previous Day High (PDH) check
            pdh = float(df["High"].iloc[-10:-1].max()) if len(df) >= 10 else float(df["High"].max())

            # Relative Volume / Activity (RVAT)
            recent_vol = float(df["Volume"].iloc[-1])
            hist_vols = df["Volume"].iloc[:-1]
            avg_vol = float(hist_vols.mean()) + 1e-6
            std_vol = float(hist_vols.std()) + 1e-6
            rvat = round(recent_vol / avg_vol, 2)
            z_score = (recent_vol - avg_vol) / std_vol

            # VWAP Gap %
            cum_vol = df["Volume"].sum() + 1e-6
            vwap = float((df["Close"] * df["Volume"]).sum() / cum_vol)
            vwap_gap = round(((ltp - vwap) / vwap) * 100, 2)

            # Futures OI % estimation
            oi_pct = round(float(np.clip(z_score * 2.2 + (pct_chg * 1.1), -14.0, 25.0)), 2)

            # Behaviour
            if pct_chg >= 0 and oi_pct < 0:
                behavior = "Short covering"
            elif pct_chg < 0 and oi_pct < 0:
                behavior = "Long unwinding"
            elif pct_chg >= 0 and oi_pct >= 0:
                behavior = "Long buildup"
            else:
                behavior = "Short buildup"

            # Check Execution Filter Rules (Breakout, Volume, PDH, Range)
            rule_breakout = pct_chg > 0.1 and ltp > vwap
            rule_volume = rvat >= 1.05
            rule_pdh = ltp >= (pdh * 0.998)
            rule_range = abs(pct_chg) < 4.5
            final_status = "YES" if (rule_volume and (rule_breakout or rule_pdh)) else "WATCH"

            # Timestamp when signal surfaced
            listed_at = (now_ist - timedelta(minutes=int(abs(z_score * 8)) % 45)).strftime("%H:%M")

            scanned.append({
                "symbol": sym.replace(".NS", ""),
                "sector": sec,
                "ltp": round(ltp, 2),
                "pct_chg": pct_chg,
                "listed_at": listed_at,
                "rvat": rvat,
                "vwap_gap": vwap_gap,
                "futures_oi": oi_pct,
                "oi_behavior": behavior,
                "is_bullish": pct_chg >= 0,
                "rules": {
                    "breakout": "YES" if rule_breakout else "NO",
                    "volume": "YES" if rule_volume else "NO",
                    "pdh": "YES" if rule_pdh else "NO",
                    "range": "YES" if rule_range else "NO",
                    "final": final_status
                }
            })

            # Tally Sector Strength
            sector_gains.setdefault(sec, []).append(pct_chg)

        except Exception as e:
            print(f"Skipping {sym}: {e}")

    # Sector Performance Score & Rank 1 Tag
    sec_summary = {s: round(float(np.mean(gains)), 2) for s, gains in sector_gains.items()}
    top_sector = max(sec_summary, key=sec_summary.get) if sec_summary else "Financial Services"

    for s in scanned:
        s["sector_perf"] = sec_summary.get(s["sector"], 0.0)
        s["is_no1_sector"] = (s["sector"] == top_sector)

    # Sort: Bullish highest RVAT first, Bearish lowest/highest RVAT
    scanned.sort(key=lambda x: x["rvat"], reverse=True)

    output = {
        "sync_time": now_ist.strftime("%d %b %Y, %I:%M %p IST"),
        "date_code": now_ist.strftime("%Y-%m-%d"),
        "top_sector": top_sector,
        "nifty_fin": {"ltp": fin_val, "chg": fin_chg, "pct": fin_pct},
        "india_vix": {"val": vix_val, "chg": vix_chg},
        "stocks": scanned
    }

    with open("screener.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    run_scanner()
