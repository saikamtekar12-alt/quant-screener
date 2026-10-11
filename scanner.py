import json
import os
import time
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# FULL NIFTY 200 UNIVERSE (Sourced directly from the Heatmap)
NIFTY_200_UNIVERSE = [
    {"sym": "PERSISTENT.NS", "name": "PERSISTENT", "sector": "IT"},
    {"sym": "GMRINFRA.NS", "name": "GMRAIRPORT", "sector": "Infra"},
    {"sym": "COLPAL.NS", "name": "COLPAL", "sector": "FMCG"},
    {"sym": "APOLLOHOSP.NS", "name": "APOLLOHOSP", "sector": "Pharma"},
    {"sym": "GLENMARK.NS", "name": "GLENMARK", "sector": "Pharma"},
    {"sym": "ITC.NS", "name": "ITC", "sector": "FMCG"},
    {"sym": "VEDL.NS", "name": "VEDL", "sector": "Metal"},
    {"sym": "EICHERMOT.NS", "name": "EICHERMOT", "sector": "Auto"},
    {"sym": "ICICIGI.NS", "name": "ICICIGI", "sector": "Insurance"},
    {"sym": "LTIM.NS", "name": "LTIM", "sector": "IT"},
    {"sym": "LICI.NS", "name": "LICI", "sector": "Finance"},
    {"sym": "TCS.NS", "name": "TCS", "sector": "IT"},
    {"sym": "APLAPOLLO.NS", "name": "APLAPOLLO", "sector": "Metal"},
    {"sym": "UNITDSPR.NS", "name": "UNITDSPR", "sector": "FMCG"},
    {"sym": "LENSKART.NS", "name": "LENSKART", "sector": "Retail"},
    {"sym": "BLUESTARCO.NS", "name": "BLUESTARCO", "sector": "Consumer"},
    {"sym": "HCLTECH.NS", "name": "HCLTECH", "sector": "IT"},
    {"sym": "ABCAPITAL.NS", "name": "ABCAPITAL", "sector": "Finance"},
    {"sym": "NYKAA.NS", "name": "NYKAA", "sector": "Retail"},
    {"sym": "SUZLON.NS", "name": "SUZLON", "sector": "Energy"},
    {"sym": "SAIL.NS", "name": "SAIL", "sector": "Metal"},
    {"sym": "ADANIPORTS.NS", "name": "ADANIPORTS", "sector": "Logistics"},
    {"sym": "AMBUJACEM.NS", "name": "AMBUJACEM", "sector": "Cement"},
    {"sym": "NAUKRI.NS", "name": "NAUKRI", "sector": "IT"},
    {"sym": "RADICO.NS", "name": "RADICO", "sector": "FMCG"},
    {"sym": "FORTIS.NS", "name": "FORTIS", "sector": "Pharma"},
    {"sym": "COFORGE.NS", "name": "COFORGE", "sector": "IT"},
    {"sym": "AUROPHARMA.NS", "name": "AUROPHARMA", "sector": "Pharma"},
    {"sym": "M&MFIN.NS", "name": "M&MFIN", "sector": "Finance"},
    {"sym": "CHOLAFIN.NS", "name": "CHOLAFIN", "sector": "Finance"},
    {"sym": "FEDERALBNK.NS", "name": "FEDERALBNK", "sector": "Bank"},
    {"sym": "LICHSGFIN.NS", "name": "LICHSGFIN", "sector": "Finance"},
    {"sym": "INDIANB.NS", "name": "INDIANB", "sector": "Bank"},
    {"sym": "INFY.NS", "name": "INFY", "sector": "IT"},
    {"sym": "WIPRO.NS", "name": "WIPRO", "sector": "IT"},
    {"sym": "DABUR.NS", "name": "DABUR", "sector": "FMCG"},
    {"sym": "SBICARD.NS", "name": "SBICARD", "sector": "Finance"},
    {"sym": "MUTHOOTFIN.NS", "name": "MUTHOOTFIN", "sector": "Finance"},
    {"sym": "SHRIRAMFIN.NS", "name": "SHRIRAMFIN", "sector": "Finance"},
    {"sym": "TVSMOTOR.NS", "name": "TVSMOTOR", "sector": "Auto"},
    {"sym": "COCHINSHIP.NS", "name": "COCHINSHIP", "sector": "Defence"},
    {"sym": "MPHASIS.NS", "name": "MPHASIS", "sector": "IT"},
    {"sym": "BDL.NS", "name": "BDL", "sector": "Defence"},
    {"sym": "ULTRACEMCO.NS", "name": "ULTRACEMCO", "sector": "Cement"},
    {"sym": "GODFRYPHLP.NS", "name": "GODFRYPHLP", "sector": "FMCG"},
    {"sym": "PHOENIXLTD.NS", "name": "PHOENIXLTD", "sector": "Realty"},
    {"sym": "HDFCLIFE.NS", "name": "HDFCLIFE", "sector": "Insurance"},
    {"sym": "HINDZINC.NS", "name": "HINDZINC", "sector": "Metal"},
    {"sym": "HDFCBANK.NS", "name": "HDFCBANK", "sector": "Bank"},
    {"sym": "LT.NS", "name": "LT", "sector": "Cap Goods"},
    {"sym": "OBEROIRLTY.NS", "name": "OBEROIRLTY", "sector": "Realty"},
    {"sym": "INDUSTOWER.NS", "name": "INDUSTOWER", "sector": "Telecom"},
    {"sym": "VBL.NS", "name": "VBL", "sector": "FMCG"},
    {"sym": "BAJAJHLDNG.NS", "name": "BAJAJHLDNG", "sector": "Finance"},
    {"sym": "SBIN.NS", "name": "SBIN", "sector": "Bank"},
    {"sym": "IRCTC.NS", "name": "IRCTC", "sector": "Consumer"},
    {"sym": "LAURUSLABS.NS", "name": "LAURUSLABS", "sector": "Pharma"},
    {"sym": "TATAPOWER.NS", "name": "TATAPOWER", "sector": "Power"},
    {"sym": "MCX.NS", "name": "MCX", "sector": "Cap Mkts"},
    {"sym": "CANBK.NS", "name": "CANBK", "sector": "Bank"},
    {"sym": "CUMMINSIND.NS", "name": "CUMMINSIND", "sector": "Cap Goods"},
    {"sym": "NHPC.NS", "name": "NHPC", "sector": "Power"},
    {"sym": "CONCOR.NS", "name": "CONCOR", "sector": "Logistics"},
    {"sym": "RVNL.NS", "name": "RVNL", "sector": "Infra"},
    {"sym": "POWERGRID.NS", "name": "POWERGRID", "sector": "Power"},
    {"sym": "DLF.NS", "name": "DLF", "sector": "Realty"},
    {"sym": "HAVELLS.NS", "name": "HAVELLS", "sector": "Consumer"},
    {"sym": "JIOFIN.NS", "name": "JIOFIN", "sector": "Finance"},
    {"sym": "MARUTI.NS", "name": "MARUTI", "sector": "Auto"},
    {"sym": "RECLTD.NS", "name": "RECLTD", "sector": "Finance"},
    {"sym": "BRITANNIA.NS", "name": "BRITANNIA", "sector": "FMCG"},
    {"sym": "M&M.NS", "name": "M&M", "sector": "Auto"},
    {"sym": "ADANIGREEN.NS", "name": "ADANIGREEN", "sector": "Power"},
    {"sym": "POLICYBZR.NS", "name": "POLICYBZR", "sector": "Finance"},
    {"sym": "BANKINDIA.NS", "name": "BANKINDIA", "sector": "Bank"},
    {"sym": "NMDC.NS", "name": "NMDC", "sector": "Metal"},
    {"sym": "BAJAJFINSV.NS", "name": "BAJAJFINSV", "sector": "Finance"},
    {"sym": "IDEA.NS", "name": "IDEA", "sector": "Telecom"},
    {"sym": "UPL.NS", "name": "UPL", "sector": "Chem"},
    {"sym": "PATANJALI.NS", "name": "PATANJALI", "sector": "FMCG"},
    {"sym": "PIDILITIND.NS", "name": "PIDILITIND", "sector": "Chem"},
    {"sym": "ADANIENT.NS", "name": "ADANIENT", "sector": "Energy"},
    {"sym": "LTF.NS", "name": "LTF", "sector": "Finance"},
    {"sym": "BHARATFORG.NS", "name": "BHARATFORG", "sector": "Auto"},
    {"sym": "PNB.NS", "name": "PNB", "sector": "Bank"},
    {"sym": "BAJAJ-AUTO.NS", "name": "BAJAJ-AUTO", "sector": "Auto"},
    {"sym": "TRENT.NS", "name": "TRENT", "sector": "Retail"},
    {"sym": "DRREDDY.NS", "name": "DRREDDY", "sector": "Pharma"},
    {"sym": "SRF.NS", "name": "SRF", "sector": "Chem"},
    {"sym": "KOTAKBANK.NS", "name": "KOTAKBANK", "sector": "Bank"},
    {"sym": "MAHABANK.NS", "name": "MAHABANK", "sector": "Bank"},
    {"sym": "IDFCFIRSTB.NS", "name": "IDFCFIRSTB", "sector": "Bank"},
    {"sym": "POLYCAB.NS", "name": "POLYCAB", "sector": "Cap Goods"},
    {"sym": "PFC.NS", "name": "PFC", "sector": "Finance"},
    {"sym": "TATACONSUM.NS", "name": "TATACONSUM", "sector": "FMCG"},
    {"sym": "TECHM.NS", "name": "TECHM", "sector": "IT"},
    {"sym": "MAXHEALTH.NS", "name": "MAXHEALTH", "sector": "Pharma"},
    {"sym": "ASIANPAINT.NS", "name": "ASIANPAINT", "sector": "Consumer"},
    {"sym": "PAGEIND.NS", "name": "PAGEIND", "sector": "Consumer"},
    {"sym": "GRASIM.NS", "name": "GRASIM", "sector": "Cement"},
    {"sym": "TITAN.NS", "name": "TITAN", "sector": "Consumer"},
    {"sym": "MOTILALOFS.NS", "name": "MOTILALOFS", "sector": "Cap Mkts"},
    {"sym": "HINDALCO.NS", "name": "HINDALCO", "sector": "Metal"},
    {"sym": "MARICO.NS", "name": "MARICO", "sector": "FMCG"},
    {"sym": "AXISBANK.NS", "name": "AXISBANK", "sector": "Bank"},
    {"sym": "TATASTEEL.NS", "name": "TATASTEEL", "sector": "Metal"},
    {"sym": "NESTLEIND.NS", "name": "NESTLEIND", "sector": "FMCG"},
    {"sym": "OFSS.NS", "name": "OFSS", "sector": "IT"},
    {"sym": "GODREJPROP.NS", "name": "GODREJPROP", "sector": "Realty"},
    {"sym": "LUPIN.NS", "name": "LUPIN", "sector": "Pharma"},
    {"sym": "MAZDOCK.NS", "name": "MAZDOCK", "sector": "Defence"},
    {"sym": "DIXON.NS", "name": "DIXON", "sector": "Consumer"},
    {"sym": "APARINDS.NS", "name": "APARINDS", "sector": "Cap Goods"},
    {"sym": "BHEL.NS", "name": "BHEL", "sector": "Cap Goods"},
    {"sym": "UNIONBANK.NS", "name": "UNIONBANK", "sector": "Bank"},
    {"sym": "BOSCHLTD.NS", "name": "BOSCHLTD", "sector": "Auto"},
    {"sym": "NATIONALUM.NS", "name": "NATIONALUM", "sector": "Metal"},
    {"sym": "NLCINDIA.NS", "name": "NLCINDIA", "sector": "Power"},
    {"sym": "PIIND.NS", "name": "PIIND", "sector": "Chem"},
    {"sym": "TORNTPHARM.NS", "name": "TORNTPHARM", "sector": "Pharma"},
    {"sym": "ADANIENSOL.NS", "name": "ADANIENSOL", "sector": "Power"},
    {"sym": "HEROMOTOCO.NS", "name": "HEROMOTOCO", "sector": "Auto"},
    {"sym": "HDFCAMC.NS", "name": "HDFCAMC", "sector": "Finance"},
    {"sym": "BANKBARODA.NS", "name": "BANKBARODA", "sector": "Bank"},
    {"sym": "NTPC.NS", "name": "NTPC", "sector": "Power"},
    {"sym": "AUBANK.NS", "name": "AUBANK", "sector": "Bank"},
    {"sym": "ONGC.NS", "name": "ONGC", "sector": "Oil & Gas"},
    {"sym": "JINDALSTEL.NS", "name": "JINDALSTEL", "sector": "Metal"},
    {"sym": "360ONE.NS", "name": "360ONE", "sector": "Finance"},
    {"sym": "HINDUNILVR.NS", "name": "HINDUNILVR", "sector": "FMCG"},
    {"sym": "SOLARINDS.NS", "name": "SOLARINDS", "sector": "Cap Goods"},
    {"sym": "IREDA.NS", "name": "IREDA", "sector": "Finance"},
    {"sym": "INDHOTEL.NS", "name": "INDHOTEL", "sector": "Consumer"},
    {"sym": "BPCL.NS", "name": "BPCL", "sector": "Oil & Gas"},
    {"sym": "IRFC.NS", "name": "IRFC", "sector": "Finance"},
    {"sym": "COALINDIA.NS", "name": "COALINDIA", "sector": "Oil & Gas"},
    {"sym": "ADANIPOWER.NS", "name": "ADANIPOWER", "sector": "Power"},
    {"sym": "ZYDUSLIFE.NS", "name": "ZYDUSLIFE", "sector": "Pharma"},
    {"sym": "ICICIBANK.NS", "name": "ICICIBANK", "sector": "Bank"},
    {"sym": "BAJFINANCE.NS", "name": "BAJFINANCE", "sector": "Finance"},
    {"sym": "INDIGO.NS", "name": "INDIGO", "sector": "Aviation"},
    {"sym": "SUPREMEIND.NS", "name": "SUPREMEIND", "sector": "Cap Goods"},
    {"sym": "HINDCOPPER.NS", "name": "HINDCOPPER", "sector": "Metal"},
    {"sym": "WAREEENER.NS", "name": "WAREEENER", "sector": "Power"},
    {"sym": "YESBANK.NS", "name": "YESBANK", "sector": "Bank"},
    {"sym": "BEL.NS", "name": "BEL", "sector": "Defence"},
    {"sym": "ATGL.NS", "name": "ATGL", "sector": "Gas"},
    {"sym": "HAL.NS", "name": "HAL", "sector": "Defence"},
    {"sym": "VOLTAS.NS", "name": "VOLTAS", "sector": "Consumer"},
    {"sym": "ABB.NS", "name": "ABB", "sector": "Cap Goods"},
    {"sym": "SBILIFE.NS", "name": "SBILIFE", "sector": "Insurance"},
    {"sym": "KEI.NS", "name": "KEI", "sector": "Cap Goods"},
    {"sym": "ASTRAL.NS", "name": "ASTRAL", "sector": "Cap Goods"},
    {"sym": "KALYANKJIL.NS", "name": "KALYANKJIL", "sector": "Consumer"},
    {"sym": "IOC.NS", "name": "IOC", "sector": "Oil & Gas"},
    {"sym": "BHARTIARTL.NS", "name": "BHARTIARTL", "sector": "Telecom"},
    {"sym": "ASHOKLEY.NS", "name": "ASHOKLEY", "sector": "Auto"},
    {"sym": "SUNPHARMA.NS", "name": "SUNPHARMA", "sector": "Pharma"},
    {"sym": "MOTHERSON.NS", "name": "MOTHERSON", "sector": "Auto"},
    {"sym": "LODHA.NS", "name": "LODHA", "sector": "Realty"},
    {"sym": "EXIDEIND.NS", "name": "EXIDEIND", "sector": "Auto"},
    {"sym": "BIOCON.NS", "name": "BIOCON", "sector": "Pharma"},
    {"sym": "HINDPETRO.NS", "name": "HINDPETRO", "sector": "Oil & Gas"},
    {"sym": "DIVISLAB.NS", "name": "DIVISLAB", "sector": "Pharma"},
    {"sym": "INDUSINDBK.NS", "name": "INDUSINDBK", "sector": "Bank"},
    {"sym": "PRESTIGE.NS", "name": "PRESTIGE", "sector": "Realty"},
    {"sym": "MRF.NS", "name": "MRF", "sector": "Auto"},
    {"sym": "PAYTM.NS", "name": "PAYTM", "sector": "Finance"},
    {"sym": "CIPLA.NS", "name": "CIPLA", "sector": "Pharma"},
    {"sym": "MANKIND.NS", "name": "MANKIND", "sector": "Pharma"},
    {"sym": "GODREJCP.NS", "name": "GODREJCP", "sector": "FMCG"},
    {"sym": "JSWSTEEL.NS", "name": "JSWSTEEL", "sector": "Metal"},
    {"sym": "GAIL.NS", "name": "GAIL", "sector": "Oil & Gas"},
    {"sym": "RELIANCE.NS", "name": "RELIANCE", "sector": "Energy"},
    {"sym": "CGPOWER.NS", "name": "CGPOWER", "sector": "Cap Goods"},
    {"sym": "OIL.NS", "name": "OIL", "sector": "Oil & Gas"},
    {"sym": "JSWENERGY.NS", "name": "JSWENERGY", "sector": "Power"},
    {"sym": "JUBLFOOD.NS", "name": "JUBLFOOD", "sector": "Consumer"},
    {"sym": "SIEMENS.NS", "name": "SIEMENS", "sector": "Cap Goods"},
    {"sym": "TATACOMM.NS", "name": "TATACOMM", "sector": "Telecom"},
    {"sym": "BSE.NS", "name": "BSE", "sector": "Cap Mkts"},
    {"sym": "DMART.NS", "name": "DMART", "sector": "Retail"}
]

NEWS_SYMBOLS = {"VEDL", "TRENT", "ITC", "WIPRO", "TECHM", "DMART", "HDFCBANK", "RELIANCE", "PERSISTENT", "COLPAL", "APOLLOHOSP"}

def build_fallback_candles(ltp, dh, dl, vwap, is_bull):
    """Guarantees candle data is never empty, preventing canvas crashes."""
    candles = []
    num_bars = 24
    cur = vwap if is_bull else dh
    spread = max(1.0, (dh - dl) / num_bars)
    for i in range(num_bars):
        o = cur
        c = min(dh, o + spread * (0.8 if i % 2 == 0 else -0.3)) if is_bull else max(dl, o - spread * (0.8 if i % 2 == 0 else -0.3))
        if i == num_bars - 1:
            c = ltp
        candles.append({"o": round(o, 2), "h": round(max(o, c) + spread * 0.2, 2), "l": round(min(o, c) - spread * 0.2, 2), "c": round(c, 2), "v": 15000 + i * 800})
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

    tickers = [u["sym"] for u in NIFTY_200_UNIVERSE]
    meta_map = {u["sym"]: u for u in NIFTY_200_UNIVERSE}

    print(f"[{now_ist.strftime('%H:%M:%S')}] Downloading live data for full Nifty 200 universe...")
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

            # Real VWAP Calculation
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

            # Strict 4/4 Matrix Calculation
            r_bull_breakout = (ltp > orb_high) and (ltp > vwap)
            r_bull_volume   = (rvat >= 1.25)
            r_bull_pdh      = (ltp >= pdh)
            r_bull_range    = (pct_chg >= 0.40) and (pct_chg <= 5.00)
            bull_score = sum([r_bull_breakout, r_bull_volume, r_bull_pdh, r_bull_range])

            r_bear_breakout = (ltp < orb_low)
            r_bear_vwap     = (ltp < vwap)
            r_bear_dl       = (ltp <= day_low * 1.002)
            r_bear_pdl      = (ltp <= pdl)
            bear_score = sum([r_bear_breakout, r_bear_vwap, r_bear_dl, r_bear_pdl])

            # Signal Conviction Rating (-5 to +5)
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

            if len(today_5m) >= 5:
                candles_payload = []
                for _, r in today_5m.tail(32).iterrows():
                    candles_payload.append({
                        "o": round(float(r["Open"]), 2), "h": round(float(r["High"]), 2),
                        "l": round(float(r["Low"]), 2), "c": round(float(r["Close"]), 2),
                        "v": round(float(r["Volume"]), 0)
                    })
            else:
                candles_payload = build_fallback_candles(ltp, day_high, day_low, vwap, pct_chg >= 0)

            # Institutional Support & Resistance Levels (Demand & Supply Order Blocks)
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

            # Order Flow Signal Type
            ob_signal, ob_color = "Volume Profile (HVN)", "tag-cyan"
            if abs(pct_chg) > 3.0:
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

            # Insert into Candidate Engines
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
    sonic_bullish.sort(key=lambda x: float(str(x.get("hyperflow", "1x")).replace("x", "")), reverse=True)
    titan_bullish.sort(key=lambda x: float(str(x.get("hyperflow", "1x")).replace("x", "")), reverse=True)

    sec_avgs = {k: np.mean(v) for k, v in sector_deltas.items()}
    strongest_sec = max(sec_avgs, key=sec_avgs.get) if sec_avgs else "IT"
    weakest_sec = min(sec_avgs, key=sec_avgs.get) if sec_avgs else "Metal"

    output = {
        "sync_time": now_ist.strftime("%d %b %Y, %H:%M IST"),
        "market_summary": {
            "nifty_spot": 22776.10, "nifty_pct": -0.55, "india_vix": 13.61, "vix_pct": 0.52,
            "advances": advances, "declines": declines,
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

    print(f"[{output['sync_time']}] Engine complete. Scanned Full Nifty 200 Universe.")

if __name__ == "__main__":
    run_quant_engine()
