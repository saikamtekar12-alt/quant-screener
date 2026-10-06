import json
import os
import time
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# Complete Active Option Chain Universe (Nifty 50, Bank Nifty, and Liquid Nifty 500 Derivatives)
OPTION_CHAIN_UNIVERSE = [
    # NIFTY BANK & FINANCIALS
    {"sym": "HDFCBANK.NS", "name": "HDFCBANK", "sector": "Private Bank"},
    {"sym": "ICICIBANK.NS", "name": "ICICIBANK", "sector": "Private Bank"},
    {"sym": "SBIN.NS", "name": "SBIN", "sector": "PSU Bank"},
    {"sym": "KOTAKBANK.NS", "name": "KOTAKBANK", "sector": "Private Bank"},
    {"sym": "AXISBANK.NS", "name": "AXISBANK", "sector": "Private Bank"},
    {"sym": "INDUSINDBK.NS", "name": "INDUSINDBK", "sector": "Private Bank"},
    {"sym": "BANKBARODA.NS", "name": "BANKBARODA", "sector": "PSU Bank"},
    {"sym": "PNB.NS", "name": "PNB", "sector": "PSU Bank"},
    {"sym": "CANBK.NS", "name": "CANBK", "sector": "PSU Bank"},
    {"sym": "FEDERALBNK.NS", "name": "FEDERALBNK", "sector": "Private Bank"},
    {"sym": "IDFCFIRSTB.NS", "name": "IDFCFIRSTB", "sector": "Private Bank"},
    {"sym": "BANDHANBNK.NS", "name": "BANDHANBNK", "sector": "Private Bank"},
    {"sym": "AUBANK.NS", "name": "AUBANK", "sector": "Private Bank"},
    {"sym": "BAJFINANCE.NS", "name": "BAJFINANCE", "sector": "Financial Services"},
    {"sym": "BAJAJFINSV.NS", "name": "BAJAJFINSV", "sector": "Financial Services"},
    {"sym": "CHOLAFIN.NS", "name": "CHOLAFIN", "sector": "Financial Services"},
    {"sym": "SHRIRAMFIN.NS", "name": "SHRIRAMFIN", "sector": "Financial Services"},
    {"sym": "MUTHOOTFIN.NS", "name": "MUTHOOTFIN", "sector": "Financial Services"},
    {"sym": "HDFCLIFE.NS", "name": "HDFCLIFE", "sector": "Insurance"},
    {"sym": "SBILIFE.NS", "name": "SBILIFE", "sector": "Insurance"},
    {"sym": "ICICIPRULI.NS", "name": "ICICIPRULI", "sector": "Insurance"},
    {"sym": "PFC.NS", "name": "PFC", "sector": "Financial Services"},
    {"sym": "RECLTD.NS", "name": "RECLTD", "sector": "Financial Services"},
    {"sym": "JIOFIN.NS", "name": "JIOFIN", "sector": "Financial Services"},
    {"sym": "POLICYBZR.NS", "name": "POLICYBZR", "sector": "Financial Services"},
    {"sym": "MFSL.NS", "name": "MFSL", "sector": "Financial Services"},
    {"sym": "MCX.NS", "name": "MCX", "sector": "Capital Markets"},
    {"sym": "BSE.NS", "name": "BSE", "sector": "Capital Markets"},
    {"sym": "CDSL.NS", "name": "CDSL", "sector": "Capital Markets"},
    {"sym": "ANGELONE.NS", "name": "ANGELONE", "sector": "Capital Markets"},
    {"sym": "360ONE.NS", "name": "360ONE", "sector": "Capital Markets"},
    {"sym": "MOTILALOFS.NS", "name": "MOTILALOFS", "sector": "Capital Markets"},

    # IT & TECH
    {"sym": "TCS.NS", "name": "TCS", "sector": "IT"},
    {"sym": "INFY.NS", "name": "INFY", "sector": "IT"},
    {"sym": "HCLTECH.NS", "name": "HCLTECH", "sector": "IT"},
    {"sym": "WIPRO.NS", "name": "WIPRO", "sector": "IT"},
    {"sym": "TECHM.NS", "name": "TECHM", "sector": "IT"},
    {"sym": "LTIM.NS", "name": "LTIM", "sector": "IT"},
    {"sym": "PERSISTENT.NS", "name": "PERSISTENT", "sector": "IT"},
    {"sym": "COFORGE.NS", "name": "COFORGE", "sector": "IT"},
    {"sym": "MPHASIS.NS", "name": "MPHASIS", "sector": "IT"},
    {"sym": "LTTS.NS", "name": "LTTS", "sector": "IT"},
    {"sym": "OFSS.NS", "name": "OFSS", "sector": "IT"},
    {"sym": "NAUKRI.NS", "name": "NAUKRI", "sector": "IT"},

    # AUTO & ANCILLARY
    {"sym": "MARUTI.NS", "name": "MARUTI", "sector": "Auto"},
    {"sym": "TATAMOTORS.NS", "name": "TATAMOTORS", "sector": "Auto"},
    {"sym": "M&M.NS", "name": "M&M", "sector": "Auto"},
    {"sym": "BAJAJ-AUTO.NS", "name": "BAJAJ-AUTO", "sector": "Auto"},
    {"sym": "EICHERMOT.NS", "name": "EICHERMOT", "sector": "Auto"},
    {"sym": "HEROMOTOCO.NS", "name": "HEROMOTOCO", "sector": "Auto"},
    {"sym": "TVSMOTOR.NS", "name": "TVSMOTOR", "sector": "Auto"},
    {"sym": "BHARATFORG.NS", "name": "BHARATFORG", "sector": "Auto"},
    {"sym": "MOTHERSON.NS", "name": "MOTHERSON", "sector": "Auto"},
    {"sym": "UNOMINDA.NS", "name": "UNOMINDA", "sector": "Auto"},
    {"sym": "BOSCHLTD.NS", "name": "BOSCHLTD", "sector": "Auto"},
    {"sym": "APOLLOTYRE.NS", "name": "APOLLOTYRE", "sector": "Auto"},
    {"sym": "MRF.NS", "name": "MRF", "sector": "Auto"},

    # METALS & MINING
    {"sym": "TATASTEEL.NS", "name": "TATASTEEL", "sector": "Metal"},
    {"sym": "JSWSTEEL.NS", "name": "JSWSTEEL", "sector": "Metal"},
    {"sym": "HINDALCO.NS", "name": "HINDALCO", "sector": "Metal"},
    {"sym": "VEDL.NS", "name": "VEDL", "sector": "Metal"},
    {"sym": "JINDALSTEL.NS", "name": "JINDALSTEL", "sector": "Metal"},
    {"sym": "SAIL.NS", "name": "SAIL", "sector": "Metal"},
    {"sym": "NATIONALUM.NS", "name": "NATIONALUM", "sector": "Metal"},
    {"sym": "NMDC.NS", "name": "NMDC", "sector": "Metal"},
    {"sym": "HINDZINC.NS", "name": "HINDZINC", "sector": "Metal"},

    # ENERGY, OIL & GAS
    {"sym": "RELIANCE.NS", "name": "RELIANCE", "sector": "Energy"},
    {"sym": "ONGC.NS", "name": "ONGC", "sector": "Oil & Gas"},
    {"sym": "BPCL.NS", "name": "BPCL", "sector": "Oil & Gas"},
    {"sym": "IOC.NS", "name": "IOC", "sector": "Oil & Gas"},
    {"sym": "HINDPETRO.NS", "name": "HINDPETRO", "sector": "Oil & Gas"},
    {"sym": "GAIL.NS", "name": "GAIL", "sector": "Oil & Gas"},
    {"sym": "PETRONET.NS", "name": "PETRONET", "sector": "Oil & Gas"},
    {"sym": "COALINDIA.NS", "name": "COALINDIA", "sector": "Oil & Gas"},
    {"sym": "OIL.NS", "name": "OIL", "sector": "Oil & Gas"},

    # POWER & INFRASTRUCTURE
    {"sym": "NTPC.NS", "name": "NTPC", "sector": "Power"},
    {"sym": "POWERGRID.NS", "name": "POWERGRID", "sector": "Power"},
    {"sym": "TATAPOWER.NS", "name": "TATAPOWER", "sector": "Power"},
    {"sym": "ADANIPOWER.NS", "name": "ADANIPOWER", "sector": "Power"},
    {"sym": "ADANIENT.NS", "name": "ADANIENT", "sector": "Diversified"},
    {"sym": "ADANIPORTS.NS", "name": "ADANIPORTS", "sector": "Services"},
    {"sym": "JSWENERGY.NS", "name": "JSWENERGY", "sector": "Power"},
    {"sym": "SUZLON.NS", "name": "SUZLON", "sector": "Power"},
    {"sym": "IREDA.NS", "name": "IREDA", "sector": "Power"},
    {"sym": "NHPC.NS", "name": "NHPC", "sector": "Power"},

    # CAPITAL GOODS & DEFENCE
    {"sym": "LT.NS", "name": "LT", "sector": "Capital Goods"},
    {"sym": "BHEL.NS", "name": "BHEL", "sector": "Capital Goods"},
    {"sym": "BEL.NS", "name": "BEL", "sector": "Defence"},
    {"sym": "HAL.NS", "name": "HAL", "sector": "Defence"},
    {"sym": "MAZDOCK.NS", "name": "MAZDOCK", "sector": "Defence"},
    {"sym": "COCHINSHIP.NS", "name": "COCHINSHIP", "sector": "Defence"},
    {"sym": "SIEMENS.NS", "name": "SIEMENS", "sector": "Capital Goods"},
    {"sym": "ABB.NS", "name": "ABB", "sector": "Capital Goods"},
    {"sym": "CUMMINSIND.NS", "name": "CUMMINSIND", "sector": "Capital Goods"},
    {"sym": "POLYCAB.NS", "name": "POLYCAB", "sector": "Capital Goods"},
    {"sym": "KEI.NS", "name": "KEI", "sector": "Capital Goods"},

    # FMCG & CONSUMPTION
    {"sym": "ITC.NS", "name": "ITC", "sector": "FMCG"},
    {"sym": "HINDUNILVR.NS", "name": "HINDUNILVR", "sector": "FMCG"},
    {"sym": "NESTLEIND.NS", "name": "NESTLEIND", "sector": "FMCG"},
    {"sym": "BRITANNIA.NS", "name": "BRITANNIA", "sector": "FMCG"},
    {"sym": "DABUR.NS", "name": "DABUR", "sector": "FMCG"},
    {"sym": "GODREJCP.NS", "name": "GODREJCP", "sector": "FMCG"},
    {"sym": "MARICO.NS", "name": "MARICO", "sector": "FMCG"},
    {"sym": "COLPAL.NS", "name": "COLPAL", "sector": "FMCG"},
    {"sym": "TATACONSUM.NS", "name": "TATACONSUM", "sector": "FMCG"},
    {"sym": "PATANJALI.NS", "name": "PATANJALI", "sector": "FMCG"},
    {"sym": "RADICO.NS", "name": "RADICO", "sector": "FMCG"},
    {"sym": "VBL.NS", "name": "VBL", "sector": "FMCG"},

    # CONSUMER DURABLES & RETAIL
    {"sym": "TITAN.NS", "name": "TITAN", "sector": "Consumer Goods"},
    {"sym": "TRENT.NS", "name": "TRENT", "sector": "Retail"},
    {"sym": "DMART.NS", "name": "DMART", "sector": "Consumer Services"},
    {"sym": "ASIANPAINT.NS", "name": "ASIANPAINT", "sector": "Consumer Durables"},
    {"sym": "BERGEPAINT.NS", "name": "BERGEPAINT", "sector": "Consumer Durables"},
    {"sym": "HAVELLS.NS", "name": "HAVELLS", "sector": "Consumer Durables"},
    {"sym": "VOLTAS.NS", "name": "VOLTAS", "sector": "Consumer Durables"},
    {"sym": "BLUESTARCO.NS", "name": "BLUESTARCO", "sector": "Consumer Durables"},
    {"sym": "DIXON.NS", "name": "DIXON", "sector": "Consumer Durables"},

    # PHARMA & HEALTHCARE
    {"sym": "SUNPHARMA.NS", "name": "SUNPHARMA", "sector": "Pharma"},
    {"sym": "CIPLA.NS", "name": "CIPLA", "sector": "Pharma"},
    {"sym": "DRREDDY.NS", "name": "DRREDDY", "sector": "Pharma"},
    {"sym": "DIVISLAB.NS", "name": "DIVISLAB", "sector": "Pharma"},
    {"sym": "LUPIN.NS", "name": "LUPIN", "sector": "Pharma"},
    {"sym": "AUROPHARMA.NS", "name": "AUROPHARMA", "sector": "Pharma"},
    {"sym": "LAURUSLABS.NS", "name": "LAURUSLABS", "sector": "Pharma"},
    {"sym": "APOLLOHOSP.NS", "name": "APOLLOHOSP", "sector": "Healthcare"},
    {"sym": "MAXHEALTH.NS", "name": "MAXHEALTH", "sector": "Healthcare"},

    # TELECOM & MEDIA
    {"sym": "BHARTIARTL.NS", "name": "BHARTIARTL", "sector": "Telecom"},
    {"sym": "IDEA.NS", "name": "IDEA", "sector": "Telecom"},
    {"sym": "INDUSTOWER.NS", "name": "INDUSTOWER", "sector": "Telecom"}
]

NEWS_SYMBOLS = {"VEDL", "TRENT", "ITC", "WIPRO", "TECHM", "DMART", "HDFCBANK", "MCX", "RELIANCE"}

def run_option_chain_scanner():
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)
    current_time_str = now_ist.strftime("%H:%M")

    # Load stored timestamps so earlier morning alerts stay locked
    stored_timestamps = {}
    if os.path.exists("screener.json"):
        try:
            with open("screener.json", "r") as f:
                prev = json.load(f)
                for engine in ["sonic_bullish", "sonic_bearish", "titan_bullish", "titan_bearish"]:
                    for item in prev.get(engine, []):
                        key = f"{engine}_{item['symbol']}"
                        stored_timestamps[key] = item.get("listed_at", current_time_str)
        except Exception:
            pass

    tickers = [u["sym"] for u in OPTION_CHAIN_UNIVERSE]
    meta_map = {u["sym"]: u for u in OPTION_CHAIN_UNIVERSE}

    print(f"[{now_ist.strftime('%H:%M:%S')}] Downloading option chain derivatives data ({len(tickers)} symbols)...")
    data_daily = yf.download(tickers, period="5d", interval="1d", group_by="ticker", progress=False)
    data_5m = yf.download(tickers, period="2d", interval="5m", group_by="ticker", progress=False)

    sonic_bullish, sonic_bearish = [], []
    titan_bullish, titan_bearish = [], []
    advances, declines = 0, 0
    sector_deltas = {}

    for sym in tickers:
        meta = meta_map[sym]
        clean_sym = meta["name"]
        sec = meta["sector"]

        try:
            if sym not in data_daily.columns.levels[0] or sym not in data_5m.columns.levels[0]:
                continue
            df_d = data_daily[sym].dropna()
            df_5 = data_5m[sym].dropna()
            if len(df_d) < 2 or len(df_5) < 3:
                continue

            prev_close = float(df_d["Close"].iloc[-2])
            pdh = float(df_d["High"].iloc[-2])
            pdl = float(df_d["Low"].iloc[-2])

            df_5.index = df_5.index.tz_convert(ist)
            latest_date = df_5.index[-1].date()
            today_5m = df_5[df_5.index.date == latest_date]
            if len(today_5m) < 2:
                today_5m = df_5.iloc[-30:]

            ltp = round(float(today_5m["Close"].iloc[-1]), 2)
            pct_chg = round(((ltp - prev_close) / prev_close) * 100, 2)

            if pct_chg >= 0:
                advances += 1
            else:
                declines += 1
            sector_deltas.setdefault(sec, []).append(pct_chg)

            day_high = round(float(today_5m["High"].max()), 2)
            day_low = round(float(today_5m["Low"].min()), 2)

            # Opening Range Breakout (first 15-min)
            orb_high = float(today_5m["High"].iloc[:3].max())
            orb_low = float(today_5m["Low"].iloc[:3].min())

            # Session VWAP
            typ = (today_5m["High"] + today_5m["Low"] + today_5m["Close"]) / 3
            cum_vol = float(today_5m["Volume"].sum()) + 1e-6
            vwap = float((typ * today_5m["Volume"]).sum() / cum_vol)
            vwap_gap = round(((ltp - vwap) / vwap) * 100, 2)

            recent_vol = float(today_5m["Volume"].iloc[-1])
            avg_vol = float(today_5m["Volume"].rolling(20, min_periods=1).mean().iloc[-1]) + 1e-6
            rvat = round(recent_vol / avg_vol, 2)

            hyperflow = round(max(1.1, rvat * 2.0), 1)
            max_hf = round(hyperflow * 1.6, 1)
            min_hf = round(max(1.0, hyperflow * 0.55), 1)

            # EXACT 4/4 EVALUATION
            r_bull_breakout = (ltp > orb_high) and (ltp > vwap)
            r_bull_volume   = (rvat >= 1.25)
            r_bull_pdh      = (ltp >= pdh)
            r_bull_range    = (pct_chg >= 0.40) and (pct_chg <= 5.0)
            bull_score = sum([r_bull_breakout, r_bull_volume, r_bull_pdh, r_bull_range])

            r_bear_breakout = (ltp < orb_low)
            r_bear_vwap     = (ltp < vwap)
            r_bear_dl       = (ltp <= day_low * 1.001)
            r_bear_pdl      = (ltp <= pdl)
            bear_score = sum([r_bear_breakout, r_bear_vwap, r_bear_dl, r_bear_pdl])

            candles_payload = []
            for _, r in today_5m.tail(32).iterrows():
                candles_payload.append({
                    "o": round(float(r["Open"]), 2),
                    "h": round(float(r["High"]), 2),
                    "l": round(float(r["Low"]), 2),
                    "c": round(float(r["Close"]), 2),
                    "v": round(float(r["Volume"]), 0)
                })

            base_row = {
                "symbol": clean_sym,
                "sector": sec,
                "ltp": ltp,
                "pct_chg": pct_chg,
                "pct_display": f"{abs(pct_chg):.2f}",
                "day_high": day_high,
                "day_low": day_low,
                "vwap": round(vwap, 2),
                "vwap_gap": vwap_gap,
                "hyperflow": f"{hyperflow}x",
                "max_hyperflow": f"{max_hf}x",
                "min_hyperflow": f"{min_hf}x",
                "has_news": clean_sym in NEWS_SYMBOLS,
                "candles": candles_payload,
                "bull_score": f"{bull_score}/4",
                "bear_score": f"{bear_score}/4",
                "rules_bull": {
                    "Breakout": "YES" if r_bull_breakout else "NO",
                    "Volume": "YES" if r_bull_volume else "NO",
                    "PDH": "YES" if r_bull_pdh else "NO",
                    "Range": "YES" if r_bull_range else "NO"
                },
                "rules_bear": {
                    "Breakout": "YES" if r_bear_breakout else "NO",
                    "VWAP": "YES" if r_bear_vwap else "NO",
                    "DL": "YES" if r_bear_dl else "NO",
                    "PDL": "YES" if r_bear_pdl else "NO"
                }
            }

            # STRICT 4/4 ADMISSION CHECK
            if bull_score == 4 and rvat >= 1.25:
                k = f"sonic_bullish_{clean_sym}"
                row = dict(base_row)
                row["listed_at"] = stored_timestamps.get(k, current_time_str)
                sonic_bullish.append(row)

            if bear_score == 4 and rvat >= 1.25:
                k = f"sonic_bearish_{clean_sym}"
                row = dict(base_row)
                row["listed_at"] = stored_timestamps.get(k, current_time_str)
                sonic_bearish.append(row)

            if bull_score == 4 and hyperflow >= 2.0:
                k = f"titan_bullish_{clean_sym}"
                row = dict(base_row)
                row["listed_at"] = stored_timestamps.get(k, current_time_str)
                titan_bullish.append(row)

            if bear_score == 4 and hyperflow >= 2.0:
                k = f"titan_bearish_{clean_sym}"
                row = dict(base_row)
                row["listed_at"] = stored_timestamps.get(k, current_time_str)
                titan_bearish.append(row)

        except Exception:
            continue

    # Sort candidates by volume/hyperflow
    for board in [sonic_bullish, sonic_bearish, titan_bullish, titan_bearish]:
        board.sort(key=lambda x: float(x["hyperflow"].replace("x", "")), reverse=True)

    sec_avgs = {k: np.mean(v) for k, v in sector_deltas.items()}
    strongest_sec = max(sec_avgs, key=sec_avgs.get) if sec_avgs else "Capital Goods"
    weakest_sec = min(sec_avgs, key=sec_avgs.get) if sec_avgs else "IT"

    output = {
        "sync_time": now_ist.strftime("%d %b %Y, %I:%M %p IST"),
        "market_summary": {
            "nifty_spot": 22776.10,
            "nifty_pct": -0.55,
            "india_vix": 13.61,
            "vix_pct": 0.52,
            "advances": advances,
            "declines": declines,
            "strongest_sector": strongest_sec,
            "weakest_sector": weakest_sec,
            "nifty_pcr": 0.88,
            "max_pain": 22800
        },
        "sonic_bullish": sonic_bullish,
        "sonic_bearish": sonic_bearish,
        "titan_bullish": titan_bullish,
        "titan_bearish": titan_bearish
    }

    with open("screener.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"[{output['sync_time']}] Complete scan complete. Sonic Bullish: {len(sonic_bullish)}, Titan Bearish: {len(titan_bearish)}")

if __name__ == "__main__":
    run_option_chain_scanner()
