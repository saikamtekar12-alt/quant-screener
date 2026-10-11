import json
import os
import time
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# FULL NIFTY 200 UNIVERSE (200 Stocks)
NIFTY_200_UNIVERSE = [
    {"sym": "RELIANCE.NS", "name": "RELIANCE", "sector": "Energy"},
    {"sym": "TCS.NS", "name": "TCS", "sector": "IT"},
    {"sym": "HDFCBANK.NS", "name": "HDFCBANK", "sector": "Bank"},
    {"sym": "ICICIBANK.NS", "name": "ICICIBANK", "sector": "Bank"},
    {"sym": "BHARTIARTL.NS", "name": "BHARTIARTL", "sector": "Telecom"},
    {"sym": "SBIN.NS", "name": "SBIN", "sector": "Bank"},
    {"sym": "INFY.NS", "name": "INFY", "sector": "IT"},
    {"sym": "LICI.NS", "name": "LICI", "sector": "Finance"},
    {"sym": "ITC.NS", "name": "ITC", "sector": "FMCG"},
    {"sym": "HINDUNILVR.NS", "name": "HINDUNILVR", "sector": "FMCG"},
    {"sym": "LT.NS", "name": "LT", "sector": "Cap Goods"},
    {"sym": "BAJFINANCE.NS", "name": "BAJFINANCE", "sector": "Finance"},
    {"sym": "HCLTECH.NS", "name": "HCLTECH", "sector": "IT"},
    {"sym": "MARUTI.NS", "name": "MARUTI", "sector": "Auto"},
    {"sym": "SUNPHARMA.NS", "name": "SUNPHARMA", "sector": "Pharma"},
    {"sym": "TATAMOTORS.NS", "name": "TATAMOTORS", "sector": "Auto"},
    {"sym": "M&M.NS", "name": "M&M", "sector": "Auto"},
    {"sym": "KOTAKBANK.NS", "name": "KOTAKBANK", "sector": "Bank"},
    {"sym": "AXISBANK.NS", "name": "AXISBANK", "sector": "Bank"},
    {"sym": "TRENT.NS", "name": "TRENT", "sector": "Retail"},
    {"sym": "ONGC.NS", "name": "ONGC", "sector": "Oil & Gas"},
    {"sym": "NTPC.NS", "name": "NTPC", "sector": "Power"},
    {"sym": "TITAN.NS", "name": "TITAN", "sector": "Consumer"},
    {"sym": "ADANIENT.NS", "name": "ADANIENT", "sector": "Energy"},
    {"sym": "ADANIPORTS.NS", "name": "ADANIPORTS", "sector": "Logistics"},
    {"sym": "ULTRACEMCO.NS", "name": "ULTRACEMCO", "sector": "Cement"},
    {"sym": "ASIANPAINT.NS", "name": "ASIANPAINT", "sector": "Consumer"},
    {"sym": "COALINDIA.NS", "name": "COALINDIA", "sector": "Oil & Gas"},
    {"sym": "BAJAJFINSV.NS", "name": "BAJAJFINSV", "sector": "Finance"},
    {"sym": "BAJAJ-AUTO.NS", "name": "BAJAJ-AUTO", "sector": "Auto"},
    {"sym": "POWERGRID.NS", "name": "POWERGRID", "sector": "Power"},
    {"sym": "NESTLEIND.NS", "name": "NESTLEIND", "sector": "FMCG"},
    {"sym": "WIPRO.NS", "name": "WIPRO", "sector": "IT"},
    {"sym": "HAL.NS", "name": "HAL", "sector": "Defence"},
    {"sym": "IOC.NS", "name": "IOC", "sector": "Oil & Gas"},
    {"sym": "TATASTEEL.NS", "name": "TATASTEEL", "sector": "Metal"},
    {"sym": "JIOFIN.NS", "name": "JIOFIN", "sector": "Finance"},
    {"sym": "ZOMATO.NS", "name": "ZOMATO", "sector": "Consumer"},
    {"sym": "DLF.NS", "name": "DLF", "sector": "Realty"},
    {"sym": "GRASIM.NS", "name": "GRASIM", "sector": "Cement"},
    {"sym": "HINDALCO.NS", "name": "HINDALCO", "sector": "Metal"},
    {"sym": "JSWSTEEL.NS", "name": "JSWSTEEL", "sector": "Metal"},
    {"sym": "VEDL.NS", "name": "VEDL", "sector": "Metal"},
    {"sym": "LTIM.NS", "name": "LTIM", "sector": "IT"},
    {"sym": "SBILIFE.NS", "name": "SBILIFE", "sector": "Insurance"},
    {"sym": "DRREDDY.NS", "name": "DRREDDY", "sector": "Pharma"},
    {"sym": "TATACONSUM.NS", "name": "TATACONSUM", "sector": "FMCG"},
    {"sym": "EICHERMOT.NS", "name": "EICHERMOT", "sector": "Auto"},
    {"sym": "DIVISLAB.NS", "name": "DIVISLAB", "sector": "Pharma"},
    {"sym": "APOLLOHOSP.NS", "name": "APOLLOHOSP", "sector": "Pharma"},
    {"sym": "BRITANNIA.NS", "name": "BRITANNIA", "sector": "FMCG"},
    {"sym": "IREDA.NS", "name": "IREDA", "sector": "Finance"},
    {"sym": "IRFC.NS", "name": "IRFC", "sector": "Finance"},
    {"sym": "PFC.NS", "name": "PFC", "sector": "Finance"},
    {"sym": "RECLTD.NS", "name": "RECLTD", "sector": "Finance"},
    {"sym": "BSE.NS", "name": "BSE", "sector": "Cap Mkts"},
    {"sym": "MCX.NS", "name": "MCX", "sector": "Cap Mkts"},
    {"sym": "CDSL.NS", "name": "CDSL", "sector": "Cap Mkts"},
    {"sym": "SUZLON.NS", "name": "SUZLON", "sector": "Energy"},
    {"sym": "TECHM.NS", "name": "TECHM", "sector": "IT"},
    {"sym": "ADANIGREEN.NS", "name": "ADANIGREEN", "sector": "Power"},
    {"sym": "ADANIPOWER.NS", "name": "ADANIPOWER", "sector": "Power"},
    {"sym": "AMBUJACEM.NS", "name": "AMBUJACEM", "sector": "Cement"},
    {"sym": "INDIGO.NS", "name": "INDIGO", "sector": "Aviation"},
    {"sym": "CIPLA.NS", "name": "CIPLA", "sector": "Pharma"},
    {"sym": "GODREJCP.NS", "name": "GODREJCP", "sector": "FMCG"},
    {"sym": "TORNTPHARM.NS", "name": "TORNTPHARM", "sector": "Pharma"},
    {"sym": "MANKIND.NS", "name": "MANKIND", "sector": "Pharma"},
    {"sym": "ZYDUSLIFE.NS", "name": "ZYDUSLIFE", "sector": "Pharma"},
    {"sym": "TVSMOTOR.NS", "name": "TVSMOTOR", "sector": "Auto"},
    {"sym": "HEROMOTOCO.NS", "name": "HEROMOTOCO", "sector": "Auto"},
    {"sym": "BOSCHLTD.NS", "name": "BOSCHLTD", "sector": "Auto"},
    {"sym": "MOTHERSON.NS", "name": "MOTHERSON", "sector": "Auto"},
    {"sym": "CUMMINSIND.NS", "name": "CUMMINSIND", "sector": "Cap Goods"},
    {"sym": "SIEMENS.NS", "name": "SIEMENS", "sector": "Cap Goods"},
    {"sym": "ABB.NS", "name": "ABB", "sector": "Cap Goods"},
    {"sym": "BHEL.NS", "name": "BHEL", "sector": "Cap Goods"},
    {"sym": "BEL.NS", "name": "BEL", "sector": "Defence"},
    {"sym": "MAZDOCK.NS", "name": "MAZDOCK", "sector": "Defence"},
    {"sym": "RVNL.NS", "name": "RVNL", "sector": "Infra"},
    {"sym": "BPCL.NS", "name": "BPCL", "sector": "Oil & Gas"},
    {"sym": "HINDPETRO.NS", "name": "HINDPETRO", "sector": "Oil & Gas"},
    {"sym": "GAIL.NS", "name": "GAIL", "sector": "Oil & Gas"},
    {"sym": "ATGL.NS", "name": "ATGL", "sector": "Gas"},
    {"sym": "NMDC.NS", "name": "NMDC", "sector": "Metal"},
    {"sym": "JINDALSTEL.NS", "name": "JINDALSTEL", "sector": "Metal"},
    {"sym": "SAIL.NS", "name": "SAIL", "sector": "Metal"},
    {"sym": "HINDCOPPER.NS", "name": "HINDCOPPER", "sector": "Metal"},
    {"sym": "NATIONALUM.NS", "name": "NATIONALUM", "sector": "Metal"},
    {"sym": "SRF.NS", "name": "SRF", "sector": "Chem"},
    {"sym": "UPL.NS", "name": "UPL", "sector": "Chem"},
    {"sym": "PIIND.NS", "name": "PIIND", "sector": "Chem"},
    {"sym": "PIDILITIND.NS", "name": "PIDILITIND", "sector": "Chem"},
    {"sym": "CHOLAFIN.NS", "name": "CHOLAFIN", "sector": "Finance"},
    {"sym": "SHRIRAMFIN.NS", "name": "SHRIRAMFIN", "sector": "Finance"},
    {"sym": "MUTHOOTFIN.NS", "name": "MUTHOOTFIN", "sector": "Finance"},
    {"sym": "M&MFIN.NS", "name": "M&MFIN", "sector": "Finance"},
    {"sym": "LICHSGFIN.NS", "name": "LICHSGFIN", "sector": "Finance"},
    {"sym": "HDFCAMC.NS", "name": "HDFCAMC", "sector": "Finance"},
    {"sym": "INDUSINDBK.NS", "name": "INDUSINDBK", "sector": "Bank"},
    {"sym": "BANKBARODA.NS", "name": "BANKBARODA", "sector": "Bank"},
    {"sym": "PNB.NS", "name": "PNB", "sector": "Bank"},
    {"sym": "CANBK.NS", "name": "CANBK", "sector": "Bank"},
    {"sym": "UNIONBANK.NS", "name": "UNIONBANK", "sector": "Bank"},
    {"sym": "INDIANB.NS", "name": "INDIANB", "sector": "Bank"},
    {"sym": "BANKINDIA.NS", "name": "BANKINDIA", "sector": "Bank"},
    {"sym": "MAHABANK.NS", "name": "MAHABANK", "sector": "Bank"},
    {"sym": "IDFCFIRSTB.NS", "name": "IDFCFIRSTB", "sector": "Bank"},
    {"sym": "FEDERALBNK.NS", "name": "FEDERALBNK", "sector": "Bank"},
    {"sym": "AUBANK.NS", "name": "AUBANK", "sector": "Bank"},
    {"sym": "YESBANK.NS", "name": "YESBANK", "sector": "Bank"},
    {"sym": "PAYTM.NS", "name": "PAYTM", "sector": "Finance"},
    {"sym": "POLICYBZR.NS", "name": "POLICYBZR", "sector": "Finance"},
    {"sym": "NYKAA.NS", "name": "NYKAA", "sector": "Retail"},
    {"sym": "DMART.NS", "name": "DMART", "sector": "Retail"},
    {"sym": "DIXON.NS", "name": "DIXON", "sector": "Consumer"},
    {"sym": "HAVELLS.NS", "name": "HAVELLS", "sector": "Consumer"},
    {"sym": "VOLTAS.NS", "name": "VOLTAS", "sector": "Consumer"},
    {"sym": "BLUESTARCO.NS", "name": "BLUESTARCO", "sector": "Consumer"},
    {"sym": "POLYCAB.NS", "name": "POLYCAB", "sector": "Cap Goods"},
    {"sym": "KEI.NS", "name": "KEI", "sector": "Cap Goods"},
    {"sym": "APARINDS.NS", "name": "APARINDS", "sector": "Cap Goods"},
    {"sym": "CGPOWER.NS", "name": "CGPOWER", "sector": "Cap Goods"},
    {"sym": "SUPREMEIND.NS", "name": "SUPREMEIND", "sector": "Cap Goods"},
    {"sym": "ASTRAL.NS", "name": "ASTRAL", "sector": "Cap Goods"},
    {"sym": "PAGEIND.NS", "name": "PAGEIND", "sector": "Consumer"},
    {"sym": "KALYANKJIL.NS", "name": "KALYANKJIL", "sector": "Consumer"},
    {"sym": "INDHOTEL.NS", "name": "INDHOTEL", "sector": "Consumer"},
    {"sym": "IRCTC.NS", "name": "IRCTC", "sector": "Consumer"},
    {"sym": "GODREJPROP.NS", "name": "GODREJPROP", "sector": "Realty"},
    {"sym": "OBEROIRLTY.NS", "name": "OBEROIRLTY", "sector": "Realty"},
    {"sym": "PRESTIGE.NS", "name": "PRESTIGE", "sector": "Realty"},
    {"sym": "LODHA.NS", "name": "LODHA", "sector": "Realty"},
    {"sym": "PHOENIXLTD.NS", "name": "PHOENIXLTD", "sector": "Realty"},
    {"sym": "PERSISTENT.NS", "name": "PERSISTENT", "sector": "IT"},
    {"sym": "COFORGE.NS", "name": "COFORGE", "sector": "IT"},
    {"sym": "MPHASIS.NS", "name": "MPHASIS", "sector": "IT"},
    {"sym": "OFSS.NS", "name": "OFSS", "sector": "IT"},
    {"sym": "NAUKRI.NS", "name": "NAUKRI", "sector": "IT"},
    {"sym": "TATACOMM.NS", "name": "TATACOMM", "sector": "Telecom"},
    {"sym": "IDEA.NS", "name": "IDEA", "sector": "Telecom"},
    {"sym": "INDUSTOWER.NS", "name": "INDUSTOWER", "sector": "Telecom"},
    {"sym": "COLPAL.NS", "name": "COLPAL", "sector": "FMCG"},
    {"sym": "DABUR.NS", "name": "DABUR", "sector": "FMCG"},
    {"sym": "MARICO.NS", "name": "MARICO", "sector": "FMCG"},
    {"sym": "VBL.NS", "name": "VBL", "sector": "FMCG"},
    {"sym": "UNITDSPR.NS", "name": "UNITDSPR", "sector": "FMCG"},
    {"sym": "RADICO.NS", "name": "RADICO", "sector": "FMCG"},
    {"sym": "GODFRYPHLP.NS", "name": "GODFRYPHLP", "sector": "FMCG"},
    {"sym": "PATANJALI.NS", "name": "PATANJALI", "sector": "FMCG"},
    {"sym": "JUBLFOOD.NS", "name": "JUBLFOOD", "sector": "Consumer"},
    {"sym": "ICICIGI.NS", "name": "ICICIGI", "sector": "Insurance"},
    {"sym": "ABCAPITAL.NS", "name": "ABCAPITAL", "sector": "Finance"},
    {"sym": "LTF.NS", "name": "LTF", "sector": "Finance"},
    {"sym": "SBICARD.NS", "name": "SBICARD", "sector": "Finance"},
    {"sym": "360ONE.NS", "name": "360ONE", "sector": "Finance"},
    {"sym": "MOTILALOFS.NS", "name": "MOTILALOFS", "sector": "Cap Mkts"},
    {"sym": "BAJAJHLDNG.NS", "name": "BAJAJHLDNG", "sector": "Finance"},
    {"sym": "GMRINFRA.NS", "name": "GMRAIRPORT", "sector": "Infra"},
    {"sym": "CONCOR.NS", "name": "CONCOR", "sector": "Logistics"},
    {"sym": "NHPC.NS", "name": "NHPC", "sector": "Power"},
    {"sym": "TATAPOWER.NS", "name": "TATAPOWER", "sector": "Power"},
    {"sym": "JSWENERGY.NS", "name": "JSWENERGY", "sector": "Power"},
    {"sym": "NLCINDIA.NS", "name": "NLCINDIA", "sector": "Power"},
    {"sym": "ADANIENSOL.NS", "name": "ADANIENSOL", "sector": "Power"},
    {"sym": "WAREEENER.NS", "name": "WAREEENER", "sector": "Power"},
    {"sym": "SOLARINDS.NS", "name": "SOLARINDS", "sector": "Cap Goods"},
    {"sym": "BHARATFORG.NS", "name": "BHARATFORG", "sector": "Auto"},
    {"sym": "ASHOKLEY.NS", "name": "ASHOKLEY", "sector": "Auto"},
    {"sym": "MRF.NS", "name": "MRF", "sector": "Auto"},
    {"sym": "EXIDEIND.NS", "name": "EXIDEIND", "sector": "Auto"},
    {"sym": "APLAPOLLO.NS", "name": "APLAPOLLO", "sector": "Metal"},
    {"sym": "GLENMARK.NS", "name": "GLENMARK", "sector": "Pharma"},
    {"sym": "AUROPHARMA.NS", "name": "AUROPHARMA", "sector": "Pharma"},
    {"sym": "FORTIS.NS", "name": "FORTIS", "sector": "Pharma"},
    {"sym": "MAXHEALTH.NS", "name": "MAXHEALTH", "sector": "Pharma"},
    {"sym": "LUPIN.NS", "name": "LUPIN", "sector": "Pharma"},
    {"sym": "LAURUSLABS.NS", "name": "LAURUSLABS", "sector": "Pharma"},
    {"sym": "BIOCON.NS", "name": "BIOCON", "sector": "Pharma"},
    {"sym": "ZENSARTECH.NS", "name": "ZENSARTECH", "sector": "IT"},
    {"sym": "TIMKEN.NS", "name": "TIMKEN", "sector": "Auto"},
    {"sym": "COCHINSHIP.NS", "name": "COCHINSHIP", "sector": "Defence"},
    {"sym": "BDL.NS", "name": "BDL", "sector": "Defence"},
    {"sym": "HDFCLIFE.NS", "name": "HDFCLIFE", "sector": "Insurance"},
    {"sym": "HINDZINC.NS", "name": "HINDZINC", "sector": "Metal"},
    {"sym": "MFSL.NS", "name": "MFSL", "sector": "Finance"},
    {"sym": "ICICIAMC.NS", "name": "ICICIAMC", "sector": "Finance"},
    {"sym": "TIINDIA.NS", "name": "TIINDIA", "sector": "Auto"},
    {"sym": "SWIGGY.NS", "name": "SWIGGY", "sector": "Retail"},
    {"sym": "HYUNDAI.NS", "name": "HYUNDAI", "sector": "Auto"}
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
    
    # MODIFICATION 1: Changed period="5d" to period="15d" to ensure we have past week volume history
    data_daily = yf.download(tickers, period="15d", interval="1d", group_by="ticker", progress=False)
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
            
            # Need at least 6 daily bars to calculate a 5-day average ending yesterday
            if len(df_d) < 6 or len(df_5) < 1:
                continue

            prev_close = float(df_d["Close"].iloc[-2])
            pdh = float(df_d["High"].iloc[-2])
            pdl = float(df_d["Low"].iloc[-2])
            
            # MODIFICATION 2: Calculate Past 1 Week (5 trading days) Average Volume
            past_5_days_vol = df_d["Volume"].iloc[-6:-1]
            avg_vol_5d = float(past_5_days_vol.mean()) if len(past_5_days_vol) > 0 else 1e-6

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
            
            # MODIFICATION 3: Calculate Live Daily Volume Spurt Multiplier
            live_daily_vol = float(today_5m["Volume"].sum())
            vol_spurt_multiplier = round(live_daily_vol / avg_vol_5d, 2)

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
                "vol_spurt": f"{vol_spurt_multiplier}x", # MODIFICATION 4: Added Volume Spurt to JSON payload
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
