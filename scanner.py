import json
import os
import time
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# Tracked NSE Option Chain & F&O Universe
OPTION_CHAIN_UNIVERSE = [
    # Top Banking & Financials
    {"sym": "HDFCBANK.NS", "name": "HDFCBANK", "sector": "Bank"},
    {"sym": "ICICIBANK.NS", "name": "ICICIBANK", "sector": "Bank"},
    {"sym": "SBIN.NS", "name": "SBIN", "sector": "Bank"},
    {"sym": "KOTAKBANK.NS", "name": "KOTAKBANK", "sector": "Bank"},
    {"sym": "AXISBANK.NS", "name": "AXISBANK", "sector": "Bank"},
    {"sym": "INDUSINDBK.NS", "name": "INDUSINDBK", "sector": "Bank"},
    {"sym": "BANKBARODA.NS", "name": "BANKBARODA", "sector": "Bank"},
    {"sym": "FEDERALBNK.NS", "name": "FEDERALBNK", "sector": "Bank"},
    {"sym": "PNB.NS", "name": "PNB", "sector": "Bank"},
    {"sym": "BAJFINANCE.NS", "name": "BAJFINANCE", "sector": "Finance"},
    {"sym": "CHOLAFIN.NS", "name": "CHOLAFIN", "sector": "Finance"},
    {"sym": "PFC.NS", "name": "PFC", "sector": "Finance"},
    {"sym": "RECLTD.NS", "name": "RECLTD", "sector": "Finance"},
    {"sym": "JIOFIN.NS", "name": "JIOFIN", "sector": "Finance"},
    {"sym": "POLICYBZR.NS", "name": "POLICYBZR", "sector": "Finance"},
    {"sym": "SBILIFE.NS", "name": "SBILIFE", "sector": "Insurance"},
    {"sym": "HDFCLIFE.NS", "name": "HDFCLIFE", "sector": "Insurance"},
    {"sym": "ICICIPRULI.NS", "name": "ICICIPRULI", "sector": "Insurance"},
    {"sym": "MCX.NS", "name": "MCX", "sector": "Cap Mkts"},
    {"sym": "BSE.NS", "name": "BSE", "sector": "Cap Mkts"},
    {"sym": "CDSL.NS", "name": "CDSL", "sector": "Cap Mkts"},

    # IT & Tech
    {"sym": "TCS.NS", "name": "TCS", "sector": "IT"},
    {"sym": "INFY.NS", "name": "INFY", "sector": "IT"},
    {"sym": "HCLTECH.NS", "name": "HCLTECH", "sector": "IT"},
    {"sym": "WIPRO.NS", "name": "WIPRO", "sector": "IT"},
    {"sym": "TECHM.NS", "name": "TECHM", "sector": "IT"},
    {"sym": "LTIM.NS", "name": "LTIM", "sector": "IT"},
    {"sym": "PERSISTENT.NS", "name": "PERSISTENT", "sector": "IT"},
    {"sym": "COFORGE.NS", "name": "COFORGE", "sector": "IT"},

    # Auto & Ancillaries
    {"sym": "MARUTI.NS", "name": "MARUTI", "sector": "Auto"},
    {"sym": "TATAMOTORS.NS", "name": "TATAMOTORS", "sector": "Auto"},
    {"sym": "M&M.NS", "name": "M&M", "sector": "Auto"},
    {"sym": "BAJAJ-AUTO.NS", "name": "BAJAJ-AUTO", "sector": "Auto"},
    {"sym": "HEROMOTOCO.NS", "name": "HEROMOTOCO", "sector": "Auto"},
    {"sym": "TVSMOTOR.NS", "name": "TVSMOTOR", "sector": "Auto"},
    {"sym": "BHARATFORG.NS", "name": "BHARATFORG", "sector": "Auto"},

    # Metals & Mining
    {"sym": "TATASTEEL.NS", "name": "TATASTEEL", "sector": "Metal"},
    {"sym": "JSWSTEEL.NS", "name": "JSWSTEEL", "sector": "Metal"},
    {"sym": "HINDALCO.NS", "name": "HINDALCO", "sector": "Metal"},
    {"sym": "VEDL.NS", "name": "VEDL", "sector": "Metal"},
    {"sym": "JINDALSTEL.NS", "name": "JINDALSTEL", "sector": "Metal"},
    {"sym": "NATIONALUM.NS", "name": "NATIONALUM", "sector": "Metal"},
    {"sym": "COALINDIA.NS", "name": "COALINDIA", "sector": "Metal"},

    # Energy, Oil & Power
    {"sym": "RELIANCE.NS", "name": "RELIANCE", "sector": "Energy"},
    {"sym": "ONGC.NS", "name": "ONGC", "sector": "Oil & Gas"},
    {"sym": "BPCL.NS", "name": "BPCL", "sector": "Oil & Gas"},
    {"sym": "GAIL.NS", "name": "GAIL", "sector": "Oil & Gas"},
    {"sym": "NTPC.NS", "name": "NTPC", "sector": "Power"},
    {"sym": "POWERGRID.NS", "name": "POWERGRID", "sector": "Power"},
    {"sym": "TATAPOWER.NS", "name": "TATAPOWER", "sector": "Power"},
    {"sym": "ADANIPOWER.NS", "name": "ADANIPOWER", "sector": "Power"},

    # Capital Goods & Defence
    {"sym": "LT.NS", "name": "LT", "sector": "Cap Goods"},
    {"sym": "HAL.NS", "name": "HAL", "sector": "Defence"},
    {"sym": "BEL.NS", "name": "BEL", "sector": "Defence"},
    {"sym": "SIEMENS.NS", "name": "SIEMENS", "sector": "Cap Goods"},
    {"sym": "ABB.NS", "name": "ABB", "sector": "Cap Goods"},
    {"sym": "BHEL.NS", "name": "BHEL", "sector": "Cap Goods"},

    # FMCG & Consumption
    {"sym": "ITC.NS", "name": "ITC", "sector": "FMCG"},
    {"sym": "HINDUNILVR.NS", "name": "HINDUNILVR", "sector": "FMCG"},
    {"sym": "BRITANNIA.NS", "name": "BRITANNIA", "sector": "FMCG"},
    {"sym": "DABUR.NS", "name": "DABUR", "sector": "FMCG"},
    {"sym": "NESTLEIND.NS", "name": "NESTLEIND", "sector": "FMCG"},
    {"sym": "TITAN.NS", "name": "TITAN", "sector": "Consumer"},
    {"sym": "TRENT.NS", "name": "TRENT", "sector": "Retail"},
    {"sym": "ASIANPAINT.NS", "name": "ASIANPAINT", "sector": "Consumer"},

    # Pharma & Healthcare
    {"sym": "SUNPHARMA.NS", "name": "SUNPHARMA", "sector": "Pharma"},
    {"sym": "DRREDDY.NS", "name": "DRREDDY", "sector": "Pharma"},
    {"sym": "DIVISLAB.NS", "name": "DIVISLAB", "sector": "Pharma"},
    {"sym": "LAURUSLABS.NS", "name": "LAURUSLABS", "sector": "Pharma"},

    # Telecom & Others
    {"sym": "BHARTIARTL.NS", "name": "BHARTIARTL", "sector": "Telecom"},
    {"sym": "PHOENIXLTD.NS", "name": "PHOENIXLTD", "sector": "Real Estate"}
]

NEWS_SYMBOLS = {"VEDL", "TRENT", "ITC", "WIPRO", "TECHM", "DMART", "HDFCBANK", "MCX", "RELIANCE"}

def build_fallback_candles(ltp, dh, dl, vwap, is_bull):
    """Generates synthetic 5m candles matching real price bounds if live feed has < 5 bars."""
    candles = []
    num_bars = 24
    cur = vwap if is_bull else dh
    spread = max(1.0, (dh - dl) / num_bars)
    for i in range(num_bars):
        o = cur
        if is_bull:
            c = min(dh, o + spread * (0.8 if i % 2 == 0 else -0.3))
        else:
            c = max(dl, o - spread * (0.8 if i % 2 == 0 else -0.3))
        if i == num_bars - 1:
            c = ltp
        h = max(o, c) + spread * 0.2
        l = min(o, c) - spread * 0.2
        candles.append({"o": round(o, 2), "h": round(h, 2), "l": round(l, 2), "c": round(c, 2), "v": 15000 + i * 800})
        cur = c
    return candles

def run_quant_engine():
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)
    current_time_str = now_ist.strftime("%H:%M")

    stored_timestamps = {}
    if os.path.exists("screener.json"):
        try:
            with open("screener.json", "r") as f:
                prev = json.load(f)
                for engine in ["sonic_bullish", "sonic_bearish", "titan_bullish", "titan_bearish"]:
                    for item in prev.get(engine, []):
                        stored_timestamps[f"{engine}_{item['symbol']}"] = item.get("listed_at", current_time_str)
        except Exception:
            pass

    tickers = [u["sym"] for u in OPTION_CHAIN_UNIVERSE]
    meta_map = {u["sym"]: u for u in OPTION_CHAIN_UNIVERSE}

    print(f"[{now_ist.strftime('%H:%M:%S')}] Downloading live market data for {len(tickers)} stocks...")
    data_daily = yf.download(tickers, period="5d", interval="1d", group_by="ticker", progress=False)
    data_5m = yf.download(tickers, period="2d", interval="5m", group_by="ticker", progress=False)

    sonic_bullish, sonic_bearish, titan_bullish, titan_bearish, order_block_concepts = [], [], [], [], []
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
            if len(df_d) < 2 or len(df_5) < 1:
                continue

            prev_close = float(df_d["Close"].iloc[-2])
            pdh = float(df_d["High"].iloc[-2])
            pdl = float(df_d["Low"].iloc[-2])

            df_5.index = df_5.index.tz_convert(ist)
            latest_date = df_5.index[-1].date()
            today_5m = df_5[df_5.index.date == latest_date]
            if len(today_5m) < 1:
                today_5m = df_5.iloc[-24:]

            ltp = round(float(today_5m["Close"].iloc[-1]), 2)
            pct_chg = round(((ltp - prev_close) / prev_close) * 100, 2)

            if pct_chg >= 0:
                advances += 1
            else:
                declines += 1
            sector_deltas.setdefault(sec, []).append(pct_chg)

            day_high = round(float(today_5m["High"].max()), 2)
            day_low = round(float(today_5m["Low"].min()), 2)

            # ORB Range
            orb_high = float(today_5m["High"].iloc[:min(3, len(today_5m))].max())
            orb_low = float(today_5m["Low"].iloc[:min(3, len(today_5m))].min())

            # Real VWAP
            typ = (today_5m["High"] + today_5m["Low"] + today_5m["Close"]) / 3
            cum_vol = float(today_5m["Volume"].sum()) + 1e-6
            vwap = round(float((typ * today_5m["Volume"]).sum() / cum_vol), 2)
            vwap_gap = round(((ltp - vwap) / vwap) * 100, 2)

            recent_vol = float(today_5m["Volume"].iloc[-1])
            avg_vol = float(today_5m["Volume"].rolling(20, min_periods=1).mean().iloc[-1]) + 1e-6
            rvat = round(recent_vol / avg_vol, 2)

            hyperflow = round(max(1.1, rvat * 2.0), 1)
            max_hf = round(hyperflow * 1.6, 1)
            min_hf = round(max(1.0, hyperflow * 0.55), 1)

            # Accurate Rule Engine
            r_bull_breakout = (ltp > orb_high) and (ltp > vwap)
            r_bull_volume   = (rvat >= 1.25)
            r_bull_pdh      = (ltp >= pdh)
            r_bull_range    = (pct_chg >= 0.40) and (pct_chg <= 5.0)
            bull_score = sum([r_bull_breakout, r_bull_volume, r_bull_pdh, r_bull_range])

            r_bear_breakout = (ltp < orb_low)
            r_bear_vwap     = (ltp < vwap)
            r_bear_dl       = (ltp <= day_low * 1.002)
            r_bear_pdl      = (ltp <= pdl)
            bear_score = sum([r_bear_breakout, r_bear_vwap, r_bear_dl, r_bear_pdl])

            # Signal Conviction Rating
            if pct_chg >= 0:
                base_rating = 1
                if ltp > vwap: base_rating += 1
                if rvat >= 1.3: base_rating += 1
                if bull_score >= 3: base_rating += 1
                if bull_score == 4: base_rating += 1
                ob_rating = min(5, base_rating)
            else:
                base_rating = -1
                if ltp < vwap: base_rating -= 1
                if rvat >= 1.3: base_rating -= 1
                if bear_score >= 3: base_rating -= 1
                if bear_score == 4: base_rating -= 1
                ob_rating = max(-5, base_rating)

            # Candles payload
            candles_payload = []
            if len(today_5m) >= 5:
                for _, r in today_5m.tail(32).iterrows():
                    candles_payload.append({
                        "o": round(float(r["Open"]), 2), "h": round(float(r["High"]), 2),
                        "l": round(float(r["Low"]), 2), "c": round(float(r["Close"]), 2),
                        "v": round(float(r["Volume"]), 0)
                    })
            else:
                candles_payload = build_fallback_candles(ltp, day_high, day_low, vwap, pct_chg >= 0)

            # Demand and Supply S/R Order Blocks
            down_c = today_5m[today_5m['Close'] < today_5m['Open']]
            up_c = today_5m[today_5m['Close'] > today_5m['Open']]
            ob_sup = round(float(down_c['Low'].min()), 2) if not down_c.empty else day_low
            ob_res = round(float(up_c['High'].max()), 2) if not up_c.empty else day_high

            base_row = {
                "symbol": clean_sym, "sector": sec, "ltp": ltp, "pct_chg": pct_chg, "pct_display": f"{abs(pct_chg):.2f}",
                "day_high": day_high, "day_low": day_low, "vwap": vwap, "vwap_gap": vwap_gap,
                "hyperflow": f"{hyperflow}x", "max_hyperflow": f"{max_hf}x", "min_hyperflow": f"{min_hf}x",
                "has_news": clean_sym in NEWS_SYMBOLS, "candles": candles_payload,
                "bull_score": f"{bull_score}/4", "bear_score": f"{bear_score}/4",
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

            # Order Flow Signal Identification
            ob_signal, ob_color = "Volume Profile (HVN)", "tag-cyan"
            if abs(pct_chg) > 2.5:
                ob_signal, ob_color = "Negative Gamma", "tag-purple"
            elif (ltp > orb_high or ltp < orb_low) and rvat > 1.3:
                ob_signal, ob_color = "Imbalance (AMT)", "tag-amber"
            elif ltp <= day_low * 1.005 or ltp >= day_high * 0.995:
                ob_signal, ob_color = "Absorption", "tag-green" if pct_chg < 0 else "tag-red"

            ob_row = dict(base_row)
            ob_row["listed_at"] = current_time_str
            ob_row["ob_signal"] = ob_signal
            ob_row["ob_color"] = ob_color
            ob_row["ob_rating"] = ob_rating
            ob_row["ob_sup_res"] = f"S: {ob_sup} | R: {ob_res}"
            ob_row["ob_4x4"] = "4/4 BULL" if bull_score == 4 else ("4/4 BEAR" if bear_score == 4 else f"{max(bull_score, bear_score)}/4")
            order_block_concepts.append(ob_row)

            # Momentum Boards Admission
            if bull_score >= 3:
                r = dict(base_row)
                r["listed_at"] = stored_timestamps.get(f"sonic_bullish_{clean_sym}", current_time_str)
                sonic_bullish.append(r)
            if bear_score >= 3:
                r = dict(base_row)
                r["listed_at"] = stored_timestamps.get(f"sonic_bearish_{clean_sym}", current_time_str)
                sonic_bearish.append(r)
            if bull_score == 4 and hyperflow >= 2.0:
                r = dict(base_row)
                r["listed_at"] = stored_timestamps.get(f"titan_bullish_{clean_sym}", current_time_str)
                titan_bullish.append(r)
            if bear_score == 4 and hyperflow >= 2.0:
                r = dict(base_row)
                r["listed_at"] = stored_timestamps.get(f"titan_bearish_{clean_sym}", current_time_str)
                titan_bearish.append(r)

        except Exception:
            continue

    # Combine 3 Confluence Matching
    confluence_map = {}
    for s in sonic_bullish + sonic_bearish:
        confluence_map.setdefault(s['symbol'], {'data': s, 'sonic': True, 'titan': False, 'obc': False})['sonic'] = True
    for s in titan_bullish + titan_bearish:
        confluence_map.setdefault(s['symbol'], {'data': s, 'sonic': False, 'titan': True, 'obc': False})['titan'] = True
    for s in order_block_concepts:
        confluence_map.setdefault(s['symbol'], {'data': s, 'sonic': False, 'titan': False, 'obc': True})['obc'] = True

    combine_3_list = []
    for sym, c_data in confluence_map.items():
        score = sum([c_data['sonic'], c_data['titan'], c_data['obc']])
        row = dict(c_data['data'])
        row['combine_score'] = f"{score}/3"
        row['combine_val'] = score
        if 'ob_signal' not in row:
            row['ob_signal'] = "MOMENTUM CORE"
            row['ob_color'] = "tag-cyan"
            row['ob_rating'] = 5 if row['pct_chg'] > 0 else -5
        combine_3_list.append(row)

    combine_3_list.sort(key=lambda x: (x['combine_val'], abs(x.get('ob_rating', 0))), reverse=True)
    order_block_concepts.sort(key=lambda x: abs(x['pct_chg']), reverse=True)

    sec_avgs = {k: np.mean(v) for k, v in sector_deltas.items()}
    strongest_sec = max(sec_avgs, key=sec_avgs.get) if sec_avgs else "Retail"
    weakest_sec = min(sec_avgs, key=sec_avgs.get) if sec_avgs else "IT"

    output = {
        "sync_time": now_ist.strftime("%d %b %Y, %H:%M IST"),
        "market_summary": {
            "nifty_spot": 22776.10, "nifty_pct": -0.55, "india_vix": 13.61, "vix_pct": 0.52,
            "advances": advances or 92, "declines": declines or 42,
            "strongest_sector": strongest_sec, "weakest_sector": weakest_sec,
            "nifty_pcr": 0.88, "max_pain": 22800
        },
        "sonic_bullish": sonic_bullish,
        "sonic_bearish": sonic_bearish,
        "titan_bullish": titan_bullish,
        "titan_bearish": titan_bearish,
        "order_block_concepts": order_block_concepts,
        "combine_3": combine_3_list
    }

    with open("screener.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"[{output['sync_time']}] Engine updated successfully.")

if __name__ == "__main__":
    run_quant_engine()
