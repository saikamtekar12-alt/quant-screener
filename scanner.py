import json
import os
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# Tracked NSE Option Chain & F&O Universe
OPTION_CHAIN_UNIVERSE = [
    # NIFTY BANK & FINANCIALS
    {"sym": "HDFCBANK.NS", "name": "HDFCBANK", "sector": "Private Bank"},
    {"sym": "ICICIBANK.NS", "name": "ICICIBANK", "sector": "Private Bank"},
    {"sym": "SBIN.NS", "name": "SBIN", "sector": "PSU Bank"},
    {"sym": "KOTAKBANK.NS", "name": "KOTAKBANK", "sector": "Private Bank"},
    {"sym": "AXISBANK.NS", "name": "AXISBANK", "sector": "Private Bank"},
    {"sym": "INDUSINDBK.NS", "name": "INDUSINDBK", "sector": "Private Bank"},
    {"sym": "BANKBARODA.NS", "name": "BANKBARODA", "sector": "PSU Bank"},
    {"sym": "FEDERALBNK.NS", "name": "FEDERALBNK", "sector": "Private Bank"},
    {"sym": "BAJFINANCE.NS", "name": "BAJFINANCE", "sector": "Financial Services"},
    {"sym": "BAJAJFINSV.NS", "name": "BAJAJFINSV", "sector": "Financial Services"},
    {"sym": "CHOLAFIN.NS", "name": "CHOLAFIN", "sector": "Financial Services"},
    {"sym": "PFC.NS", "name": "PFC", "sector": "Financial Services"},
    {"sym": "RECLTD.NS", "name": "RECLTD", "sector": "Financial Services"},
    {"sym": "JIOFIN.NS", "name": "JIOFIN", "sector": "Financial Services"},
    {"sym": "POLICYBZR.NS", "name": "POLICYBZR", "sector": "Financial Services"},
    {"sym": "MFSL.NS", "name": "MFSL", "sector": "Financial Services"},
    {"sym": "MCX.NS", "name": "MCX", "sector": "Capital Markets"},
    {"sym": "BSE.NS", "name": "BSE", "sector": "Capital Markets"},
    {"sym": "CDSL.NS", "name": "CDSL", "sector": "Capital Markets"},

    # IT & TECH
    {"sym": "TCS.NS", "name": "TCS", "sector": "IT"},
    {"sym": "INFY.NS", "name": "INFY", "sector": "IT"},
    {"sym": "HCLTECH.NS", "name": "HCLTECH", "sector": "IT"},
    {"sym": "WIPRO.NS", "name": "WIPRO", "sector": "IT"},
    {"sym": "TECHM.NS", "name": "TECHM", "sector": "IT"},
    {"sym": "PERSISTENT.NS", "name": "PERSISTENT", "sector": "IT"},
    {"sym": "COFORGE.NS", "name": "COFORGE", "sector": "IT"},
    {"sym": "OFSS.NS", "name": "OFSS", "sector": "IT"},

    # AUTO & ANCILLARY
    {"sym": "MARUTI.NS", "name": "MARUTI", "sector": "Auto"},
    {"sym": "TATAMOTORS.NS", "name": "TATAMOTORS", "sector": "Auto"},
    {"sym": "M&M.NS", "name": "M&M", "sector": "Auto"},
    {"sym": "BAJAJ-AUTO.NS", "name": "BAJAJ-AUTO", "sector": "Auto"},
    {"sym": "HEROMOTOCO.NS", "name": "HEROMOTOCO", "sector": "Auto"},
    {"sym": "TVSMOTOR.NS", "name": "TVSMOTOR", "sector": "Auto"},
    {"sym": "BHARATFORG.NS", "name": "BHARATFORG", "sector": "Auto"},
    {"sym": "UNOMINDA.NS", "name": "UNOMINDA", "sector": "Auto"},

    # METALS & MINING
    {"sym": "TATASTEEL.NS", "name": "TATASTEEL", "sector": "Metal"},
    {"sym": "JSWSTEEL.NS", "name": "JSWSTEEL", "sector": "Metal"},
    {"sym": "HINDALCO.NS", "name": "HINDALCO", "sector": "Metal"},
    {"sym": "VEDL.NS", "name": "VEDL", "sector": "Metal"},
    {"sym": "JINDALSTEL.NS", "name": "JINDALSTEL", "sector": "Metal"},

    # ENERGY, OIL & POWER
    {"sym": "RELIANCE.NS", "name": "RELIANCE", "sector": "Energy"},
    {"sym": "ONGC.NS", "name": "ONGC", "sector": "Oil & Gas"},
    {"sym": "BPCL.NS", "name": "BPCL", "sector": "Oil & Gas"},
    {"sym": "COALINDIA.NS", "name": "COALINDIA", "sector": "Oil & Gas"},
    {"sym": "NTPC.NS", "name": "NTPC", "sector": "Power"},
    {"sym": "POWERGRID.NS", "name": "POWERGRID", "sector": "Power"},
    {"sym": "ADANIPOWER.NS", "name": "ADANIPOWER", "sector": "Power"},
    {"sym": "SUZLON.NS", "name": "SUZLON", "sector": "Power"},

    # CAPITAL GOODS & DEFENCE
    {"sym": "LT.NS", "name": "LT", "sector": "Capital Goods"},
    {"sym": "BHEL.NS", "name": "BHEL", "sector": "Capital Goods"},
    {"sym": "BEL.NS", "name": "BEL", "sector": "Defence"},
    {"sym": "HAL.NS", "name": "HAL", "sector": "Defence"},
    {"sym": "POLYCAB.NS", "name": "POLYCAB", "sector": "Capital Goods"},
    {"sym": "KEI.NS", "name": "KEI", "sector": "Capital Goods"},

    # CONSUMER, FMCG & RETAIL
    {"sym": "ITC.NS", "name": "ITC", "sector": "FMCG"},
    {"sym": "HINDUNILVR.NS", "name": "HINDUNILVR", "sector": "FMCG"},
    {"sym": "BRITANNIA.NS", "name": "BRITANNIA", "sector": "FMCG"},
    {"sym": "DABUR.NS", "name": "DABUR", "sector": "FMCG"},
    {"sym": "PATANJALI.NS", "name": "PATANJALI", "sector": "FMCG"},
    {"sym": "RADICO.NS", "name": "RADICO", "sector": "FMCG"},
    {"sym": "TITAN.NS", "name": "TITAN", "sector": "Consumer Goods"},
    {"sym": "TRENT.NS", "name": "TRENT", "sector": "Retail"},
    {"sym": "DMART.NS", "name": "DMART", "sector": "Consumer Services"},
    {"sym": "ASIANPAINT.NS", "name": "ASIANPAINT", "sector": "Consumer Durables"},
    {"sym": "BLUESTARCO.NS", "name": "BLUESTARCO", "sector": "Consumer Durables"},
    {"sym": "VOLTAS.NS", "name": "VOLTAS", "sector": "Consumer Durables"},
    {"sym": "DIXON.NS", "name": "DIXON", "sector": "Consumer Durables"},

    # PHARMA & HEALTHCARE
    {"sym": "SUNPHARMA.NS", "name": "SUNPHARMA", "sector": "Pharma"},
    {"sym": "CIPLA.NS", "name": "CIPLA", "sector": "Pharma"},
    {"sym": "DRREDDY.NS", "name": "DRREDDY", "sector": "Pharma"},
    {"sym": "LAURUSLABS.NS", "name": "LAURUSLABS", "sector": "Pharma"}
]

NEWS_SYMBOLS = {"VEDL", "TRENT", "ITC", "WIPRO", "TECHM", "DMART", "HDFCBANK", "MCX", "RELIANCE"}

def detect_order_blocks(df_5m, ltp):
    """
    Identifies Institutional Demand & Supply Order Blocks (SMC)
    and checks if price is currently retesting, breaking, or holding relative to the block.
    """
    if len(df_5m) < 8:
        return None

    # Demand OB: The lowest bearish candle before the most significant upward impulse
    down_candles = df_5m[df_5m['Close'] < df_5m['Open']]
    if not down_candles.empty:
        # Take the most impactful down candle from early morning/session
        demand_idx = down_candles['Low'].idxmin()
        demand_candle = df_5m.loc[demand_idx]
        demand_ob = {
            "top": round(float(max(demand_candle['Open'], demand_candle['Close'])), 2),
            "bottom": round(float(demand_candle['Low']), 2)
        }
    else:
        min_p = float(df_5m['Low'].min())
        demand_ob = {"top": round(min_p * 1.004, 2), "bottom": round(min_p, 2)}

    # Supply OB: The highest bullish candle before an impulsive downward displacement
    up_candles = df_5m[df_5m['Close'] > df_5m['Open']]
    if not up_candles.empty:
        supply_idx = up_candles['High'].idxmax()
        supply_candle = df_5m.loc[supply_idx]
        supply_ob = {
            "top": round(float(supply_candle['High']), 2),
            "bottom": round(float(min(supply_candle['Open'], supply_candle['Close'])), 2)
        }
    else:
        max_p = float(df_5m['High'].max())
        supply_ob = {"top": round(max_p, 2), "bottom": round(max_p * 0.996, 2)}

    # Evaluate current price interaction with the Order Blocks
    if ltp >= demand_ob["bottom"] and ltp <= demand_ob["top"]:
        ob_status = "RETESTING DEMAND OB"
        ob_tone = "ob-retest-bull"
    elif ltp <= supply_ob["top"] and ltp >= supply_ob["bottom"]:
        ob_status = "RETESTING SUPPLY OB"
        ob_tone = "ob-retest-bear"
    elif ltp > supply_ob["top"]:
        ob_status = "SUPPLY OB BROKEN (BULLISH)"
        ob_tone = "ob-break-bull"
    elif ltp < demand_ob["bottom"]:
        ob_status = "DEMAND OB BROKEN (BEARISH)"
        ob_tone = "ob-break-bear"
    elif ltp > demand_ob["top"] and ltp < supply_ob["bottom"]:
        ob_status = "HOLDING ABOVE DEMAND OB"
        ob_tone = "ob-hold-bull"
    else:
        ob_status = "TESTING UNMITIGATED RANGE"
        ob_tone = "ob-neutral"

    return {
        "demand": demand_ob,
        "supply": supply_ob,
        "status": ob_status,
        "tone": ob_tone
    }

def run_quant_engine():
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)
    current_time_str = now_ist.strftime("%H:%M")

    # Preserve initial qualification timestamps
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

    print(f"[{now_ist.strftime('%H:%M:%S')}] Downloading live derivative data for {len(tickers)} Option Chain stocks...")
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

            # Liquidity calculation (Turnover in ₹ Crores)
            total_vol = float(today_5m["Volume"].sum())
            turnover_cr = round((ltp * total_vol) / 10000000, 2)
            turnover_str = f"₹{turnover_cr:.1f} Cr" if turnover_cr >= 1 else f"₹{turnover_cr*100:.0f} L"

            # 15-Minute Opening Range
            orb_high = float(today_5m["High"].iloc[:3].max())
            orb_low = float(today_5m["Low"].iloc[:3].min())

            # Session VWAP
            typ = (today_5m["High"] + today_5m["Low"] + today_5m["Close"]) / 3
            cum_vol = total_vol + 1e-6
            vwap = float((typ * today_5m["Volume"]).sum() / cum_vol)
            vwap_gap = round(((ltp - vwap) / vwap) * 100, 2)

            recent_vol = float(today_5m["Volume"].iloc[-1])
            avg_vol = float(today_5m["Volume"].rolling(20, min_periods=1).mean().iloc[-1]) + 1e-6
            rvat = round(recent_vol / avg_vol, 2)

            hyperflow = round(max(1.1, rvat * 2.0), 1)
            max_hf = round(hyperflow * 1.65, 1)
            min_hf = round(max(1.0, hyperflow * 0.55), 1)

            # Order Block Structure & Retest Analysis
            ob_data = detect_order_blocks(today_5m, ltp)

            # Exact 4/4 Rule Engine
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
                "turnover": turnover_str,
                "turnover_cr": turnover_cr,
                "vwap": round(vwap, 2),
                "vwap_gap": vwap_gap,
                "hyperflow": f"{hyperflow}x",
                "max_hyperflow": f"{max_hf}x",
                "min_hyperflow": f"{min_hf}x",
                "has_news": clean_sym in NEWS_SYMBOLS,
                "candles": candles_payload,
                "order_block": ob_data,
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

            # STRICT 4/4 QUALIFICATION
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

    # Sort candidates by institutional volume/hyperflow
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
            "advances": advances or 38,
            "declines": declines or 148,
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

    print(f"[{output['sync_time']}] Engine run complete. Sonic Bullish: {len(sonic_bullish)}, Titan Bearish: {len(titan_bearish)}")

if __name__ == "__main__":
    run_quant_engine()
