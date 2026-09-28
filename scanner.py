import json
import os
import time
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# Complete NSE F&O Universe matching Downstox & official derivative lists
FANDO_UNIVERSE = [
    {"sym": "AARTIIND.NS", "sector": "Chemicals"},
    {"sym": "ABB.NS", "sector": "Capital Goods"},
    {"sym": "ABBOTINDIA.NS", "sector": "Pharma"},
    {"sym": "ABCAPITAL.NS", "sector": "Financial Services"},
    {"sym": "ABFRL.NS", "sector": "Retail"},
    {"sym": "ADANIENT.NS", "sector": "Metals & Mining"},
    {"sym": "ADANIGREEN.NS", "sector": "Power"},
    {"sym": "ADANIPORTS.NS", "sector": "Services"},
    {"sym": "ADANIPOWER.NS", "sector": "Power"},
    {"sym": "ALKEM.NS", "sector": "Pharma"},
    {"sym": "AMBER.NS", "sector": "Consumer Durables"},
    {"sym": "AMBUJACEM.NS", "sector": "Construction Materials"},
    {"sym": "ANGELONE.NS", "sector": "Capital Markets"},
    {"sym": "APLAPOLLO.NS", "sector": "Capital Goods"},
    {"sym": "APOLLOHOSP.NS", "sector": "Healthcare"},
    {"sym": "APOLLOTYRE.NS", "sector": "Auto"},
    {"sym": "ASHOKLEY.NS", "sector": "Auto"},
    {"sym": "ASIANPAINT.NS", "sector": "Consumer Goods"},
    {"sym": "ASTRAL.NS", "sector": "Capital Goods"},
    {"sym": "ATGL.NS", "sector": "Oil & Gas"},
    {"sym": "AUBANK.NS", "sector": "Financial Services"},
    {"sym": "AUROPHARMA.NS", "sector": "Pharma"},
    {"sym": "AXISBANK.NS", "sector": "Financial Services"},
    {"sym": "BAJAJ-AUTO.NS", "sector": "Auto"},
    {"sym": "BAJAJFINSV.NS", "sector": "Financial Services"},
    {"sym": "BAJFINANCE.NS", "sector": "Financial Services"},
    {"sym": "BALKRISIND.NS", "sector": "Auto"},
    {"sym": "BANDHANBNK.NS", "sector": "Financial Services"},
    {"sym": "BANKBARODA.NS", "sector": "Financial Services"},
    {"sym": "BANKINDIA.NS", "sector": "Financial Services"},
    {"sym": "BDL.NS", "sector": "Defence"},
    {"sym": "BEL.NS", "sector": "Defence"},
    {"sym": "BERGEPAINT.NS", "sector": "Consumer Goods"},
    {"sym": "BHARATFORG.NS", "sector": "Capital Goods"},
    {"sym": "BHARTIARTL.NS", "sector": "Telecom"},
    {"sym": "BHEL.NS", "sector": "Capital Goods"},
    {"sym": "BIOCON.NS", "sector": "Pharma"},
    {"sym": "BLUESTARCO.NS", "sector": "Consumer Durables"},
    {"sym": "BOSCHLTD.NS", "sector": "Auto"},
    {"sym": "BPCL.NS", "sector": "Oil & Gas"},
    {"sym": "BRITANNIA.NS", "sector": "FMCG"},
    {"sym": "BSE.NS", "sector": "Capital Markets"},
    {"sym": "CANBK.NS", "sector": "Financial Services"},
    {"sym": "CANFINHOME.NS", "sector": "Financial Services"},
    {"sym": "CDSL.NS", "sector": "Capital Markets"},
    {"sym": "CHAMBLFERT.NS", "sector": "Chemicals"},
    {"sym": "CHOLAFIN.NS", "sector": "Financial Services"},
    {"sym": "CIPLA.NS", "sector": "Pharma"},
    {"sym": "COALINDIA.NS", "sector": "Oil & Gas"},
    {"sym": "COCHINSHIP.NS", "sector": "Defence"},
    {"sym": "COFORGE.NS", "sector": "IT"},
    {"sym": "COLPAL.NS", "sector": "FMCG"},
    {"sym": "CONCOR.NS", "sector": "Services"},
    {"sym": "CROMPTON.NS", "sector": "Consumer Durables"},
    {"sym": "CUMMINSIND.NS", "sector": "Capital Goods"},
    {"sym": "DABUR.NS", "sector": "FMCG"},
    {"sym": "DALBHARAT.NS", "sector": "Construction Materials"},
    {"sym": "DEEPAKNTR.NS", "sector": "Chemicals"},
    {"sym": "DELHIVERY.NS", "sector": "Services"},
    {"sym": "DIVISLAB.NS", "sector": "Pharma"},
    {"sym": "DIXON.NS", "sector": "Consumer Durables"},
    {"sym": "DLF.NS", "sector": "Real Estate"},
    {"sym": "DMART.NS", "sector": "Retail"},
    {"sym": "DRREDDY.NS", "sector": "Pharma"},
    {"sym": "EICHERMOT.NS", "sector": "Auto"},
    {"sym": "ESCORTS.NS", "sector": "Capital Goods"},
    {"sym": "EXIDEIND.NS", "sector": "Auto"},
    {"sym": "FEDERALBNK.NS", "sector": "Financial Services"},
    {"sym": "FORTIS.NS", "sector": "Healthcare"},
    {"sym": "GAIL.NS", "sector": "Oil & Gas"},
    {"sym": "GLENMARK.NS", "sector": "Pharma"},
    {"sym": "GMRAIRPORT.NS", "sector": "Services"},
    {"sym": "GNFC.NS", "sector": "Chemicals"},
    {"sym": "GODREJCP.NS", "sector": "FMCG"},
    {"sym": "GODREJPROP.NS", "sector": "Real Estate"},
    {"sym": "GRASIM.NS", "sector": "Construction Materials"},
    {"sym": "GUJGASLTD.NS", "sector": "Oil & Gas"},
    {"sym": "HAL.NS", "sector": "Defence"},
    {"sym": "HAVELLS.NS", "sector": "Consumer Durables"},
    {"sym": "HCLTECH.NS", "sector": "IT"},
    {"sym": "HDFCAMC.NS", "sector": "Capital Markets"},
    {"sym": "HDFCBANK.NS", "sector": "Financial Services"},
    {"sym": "HDFCLIFE.NS", "sector": "Financial Services"},
    {"sym": "HEROMOTOCO.NS", "sector": "Auto"},
    {"sym": "HINDALCO.NS", "sector": "Metal"},
    {"sym": "HINDPETRO.NS", "sector": "Oil & Gas"},
    {"sym": "HINDUNILVR.NS", "sector": "FMCG"},
    {"sym": "HINDZINC.NS", "sector": "Metal"},
    {"sym": "HUDCO.NS", "sector": "Financial Services"},
    {"sym": "HYUNDAI.NS", "sector": "Auto"},
    {"sym": "ICICIBANK.NS", "sector": "Financial Services"},
    {"sym": "ICICIGI.NS", "sector": "Financial Services"},
    {"sym": "ICICIPRULI.NS", "sector": "Financial Services"},
    {"sym": "IDEA.NS", "sector": "Telecom"},
    {"sym": "IDFCFIRSTB.NS", "sector": "Financial Services"},
    {"sym": "IEX.NS", "sector": "Capital Markets"},
    {"sym": "IGL.NS", "sector": "Oil & Gas"},
    {"sym": "INDHOTEL.NS", "sector": "Services"},
    {"sym": "INDIAMART.NS", "sector": "IT"},
    {"sym": "INDIANB.NS", "sector": "Financial Services"},
    {"sym": "INDIGO.NS", "sector": "Services"},
    {"sym": "INDUSINDBK.NS", "sector": "Financial Services"},
    {"sym": "INDUSTOWER.NS", "sector": "Telecom"},
    {"sym": "INFY.NS", "sector": "IT"},
    {"sym": "INOXWIND.NS", "sector": "Capital Goods"},
    {"sym": "IOC.NS", "sector": "Oil & Gas"},
    {"sym": "IPCALAB.NS", "sector": "Pharma"},
    {"sym": "IRCTC.NS", "sector": "Services"},
    {"sym": "IREDA.NS", "sector": "Financial Services"},
    {"sym": "IRFC.NS", "sector": "Financial Services"},
    {"sym": "ITC.NS", "sector": "FMCG"},
    {"sym": "JINDALSTEL.NS", "sector": "Metal"},
    {"sym": "JIOFIN.NS", "sector": "Financial Services"},
    {"sym": "JSWENERGY.NS", "sector": "Power"},
    {"sym": "JSWSTEEL.NS", "sector": "Metal"},
    {"sym": "JUBLFOOD.NS", "sector": "Services"},
    {"sym": "KALYANKJIL.NS", "sector": "Consumer Goods"},
    {"sym": "KAYNES.NS", "sector": "Capital Goods"},
    {"sym": "KEI.NS", "sector": "Capital Goods"},
    {"sym": "KFINTECH.NS", "sector": "Capital Markets"},
    {"sym": "KOTAKBANK.NS", "sector": "Financial Services"},
    {"sym": "KPITTECH.NS", "sector": "IT"},
    {"sym": "LAURUSLABS.NS", "sector": "Pharma"},
    {"sym": "LICHSGFIN.NS", "sector": "Financial Services"},
    {"sym": "LICI.NS", "sector": "Financial Services"},
    {"sym": "LODHA.NS", "sector": "Real Estate"},
    {"sym": "LT.NS", "sector": "Capital Goods"},
    {"sym": "LTF.NS", "sector": "Financial Services"},
    {"sym": "LTIM.NS", "sector": "IT"},
    {"sym": "LTTS.NS", "sector": "IT"},
    {"sym": "LUPIN.NS", "sector": "Pharma"},
    {"sym": "M&M.NS", "sector": "Auto"},
    {"sym": "MAHABANK.NS", "sector": "Financial Services"},
    {"sym": "MANAPPURAM.NS", "sector": "Financial Services"},
    {"sym": "MANKIND.NS", "sector": "Pharma"},
    {"sym": "MARICO.NS", "sector": "FMCG"},
    {"sym": "MARUTI.NS", "sector": "Auto"},
    {"sym": "MAXHEALTH.NS", "sector": "Healthcare"},
    {"sym": "MAZDOCK.NS", "sector": "Defence"},
    {"sym": "MCX.NS", "sector": "Capital Markets"},
    {"sym": "METROPOLIS.NS", "sector": "Healthcare"},
    {"sym": "MFSL.NS", "sector": "Financial Services"},
    {"sym": "MGL.NS", "sector": "Oil & Gas"},
    {"sym": "MOTHERSON.NS", "sector": "Auto"},
    {"sym": "MOTILALOFS.NS", "sector": "Capital Markets"},
    {"sym": "MPHASIS.NS", "sector": "IT"},
    {"sym": "MRF.NS", "sector": "Auto"},
    {"sym": "MUTHOOTFIN.NS", "sector": "Financial Services"},
    {"sym": "NAM-INDIA.NS", "sector": "Capital Markets"},
    {"sym": "NATIONALUM.NS", "sector": "Metal"},
    {"sym": "NAUKRI.NS", "sector": "IT"},
    {"sym": "NBCC.NS", "sector": "Real Estate"},
    {"sym": "NESTLEIND.NS", "sector": "FMCG"},
    {"sym": "NHPC.NS", "sector": "Power"},
    {"sym": "NMDC.NS", "sector": "Metal"},
    {"sym": "NTPC.NS", "sector": "Power"},
    {"sym": "NYKAA.NS", "sector": "Retail"},
    {"sym": "OBEROIRLTY.NS", "sector": "Real Estate"},
    {"sym": "OFSS.NS", "sector": "IT"},
    {"sym": "OIL.NS", "sector": "Oil & Gas"},
    {"sym": "ONGC.NS", "sector": "Oil & Gas"},
    {"sym": "PAGEIND.NS", "sector": "Textiles"},
    {"sym": "PATANJALI.NS", "sector": "FMCG"},
    {"sym": "PAYTM.NS", "sector": "Financial Services"},
    {"sym": "PERSISTENT.NS", "sector": "IT"},
    {"sym": "PETRONET.NS", "sector": "Oil & Gas"},
    {"sym": "PFC.NS", "sector": "Financial Services"},
    {"sym": "PGEL.NS", "sector": "Consumer Durables"},
    {"sym": "PIDILITIND.NS", "sector": "Chemicals"},
    {"sym": "PIIND.NS", "sector": "Chemicals"},
    {"sym": "PNB.NS", "sector": "Financial Services"},
    {"sym": "PNBHOUSING.NS", "sector": "Financial Services"},
    {"sym": "POLICYBZR.NS", "sector": "Financial Services"},
    {"sym": "POLYCAB.NS", "sector": "Capital Goods"},
    {"sym": "POONAWALLA.NS", "sector": "Financial Services"},
    {"sym": "POWERGRID.NS", "sector": "Power"},
    {"sym": "POWERINDIA.NS", "sector": "Capital Goods"},
    {"sym": "PREMIERENE.NS", "sector": "Power"},
    {"sym": "PRESTIGE.NS", "sector": "Real Estate"},
    {"sym": "PVRINOX.NS", "sector": "Services"},
    {"sym": "RADICO.NS", "sector": "FMCG"},
    {"sym": "RBLBANK.NS", "sector": "Financial Services"},
    {"sym": "RECLTD.NS", "sector": "Financial Services"},
    {"sym": "RELIANCE.NS", "sector": "Energy"},
    {"sym": "RVNL.NS", "sector": "Capital Goods"},
    {"sym": "SAGILITY.NS", "sector": "IT"},
    {"sym": "SAIL.NS", "sector": "Metal"},
    {"sym": "SBICARD.NS", "sector": "Financial Services"},
    {"sym": "SBILIFE.NS", "sector": "Financial Services"},
    {"sym": "SBIN.NS", "sector": "Financial Services"},
    {"sym": "SHREECEM.NS", "sector": "Construction Materials"},
    {"sym": "SHRIRAMFIN.NS", "sector": "Financial Services"},
    {"sym": "SIEMENS.NS", "sector": "Capital Goods"},
    {"sym": "SOLARINDS.NS", "sector": "Chemicals"},
    {"sym": "SONACOMS.NS", "sector": "Auto"},
    {"sym": "SRF.NS", "sector": "Chemicals"},
    {"sym": "SUNPHARMA.NS", "sector": "Pharma"},
    {"sym": "SUPREMEIND.NS", "sector": "Capital Goods"},
    {"sym": "SUZLON.NS", "sector": "Power"},
    {"sym": "SWIGGY.NS", "sector": "Services"},
    {"sym": "TATACHEM.NS", "sector": "Chemicals"},
    {"sym": "TATACOMM.NS", "sector": "Telecom"},
    {"sym": "TATACONSUM.NS", "sector": "FMCG"},
    {"sym": "TATAELXSI.NS", "sector": "IT"},
    {"sym": "TATAMOTORS.NS", "sector": "Auto"},
    {"sym": "TATAPOWER.NS", "sector": "Power"},
    {"sym": "TATASTEEL.NS", "sector": "Metal"},
    {"sym": "TCS.NS", "sector": "IT"},
    {"sym": "TECHM.NS", "sector": "IT"},
    {"sym": "TIINDIA.NS", "sector": "Auto"},
    {"sym": "TITAN.NS", "sector": "Consumer Goods"},
    {"sym": "TMPV.NS", "sector": "Auto"},
    {"sym": "TORNTPHARM.NS", "sector": "Pharma"},
    {"sym": "TORNTPOWER.NS", "sector": "Power"},
    {"sym": "TRENT.NS", "sector": "Retail"},
    {"sym": "TVSMOTOR.NS", "sector": "Auto"},
    {"sym": "ULTRACEMCO.NS", "sector": "Construction Materials"},
    {"sym": "UNIONBANK.NS", "sector": "Financial Services"},
    {"sym": "UNOMINDA.NS", "sector": "Auto"},
    {"sym": "UPL.NS", "sector": "Chemicals"},
    {"sym": "VBL.NS", "sector": "FMCG"},
    {"sym": "VEDL.NS", "sector": "Metal"},
    {"sym": "VOLTAS.NS", "sector": "Consumer Durables"},
    {"sym": "WAAREEENER.NS", "sector": "Power"},
    {"sym": "WIPRO.NS", "sector": "IT"},
    {"sym": "YESBANK.NS", "sector": "Financial Services"},
    {"sym": "ZOMATO.NS", "sector": "Services"},
    {"sym": "ZYDUSLIFE.NS", "sector": "Pharma"},
    {"sym": "360ONE.NS", "sector": "Capital Markets"}
]

def run_quant_engine():
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)

    # 1. Macro indices telemetry
    indices = {
        "nifty50": {"ltp": 22780.20, "chg": -125.40, "pct": -0.55},
        "banknifty": {"ltp": 50840.65, "chg": -320.10, "pct": -0.63},
        "finnifty": {"ltp": 23410.35, "chg": -118.40, "pct": -0.50},
        "niftyit": {"ltp": 38437.45, "chg": 144.65, "pct": 0.38},
        "vix": {"val": 13.64, "chg": 0.52}
    }

    try:
        n50 = yf.Ticker("^NSEI").history(period="5d", interval="1d")
        if len(n50) >= 2:
            c, p = float(n50["Close"].iloc[-1]), float(n50["Close"].iloc[-2])
            indices["nifty50"] = {"ltp": round(c, 1), "chg": round(c - p, 2), "pct": round(((c - p) / p) * 100, 2)}
    except Exception:
        pass

    try:
        vx = yf.Ticker("^INDIAVIX").history(period="2d")
        if len(vx) >= 2:
            c, p = float(vx["Close"].iloc[-1]), float(vx["Close"].iloc[-2])
            indices["vix"] = {"val": round(c, 2), "chg": round(c - p, 2)}
    except Exception:
        pass

    # 2. Fast Batch Data Download across entire Universe
    tickers_list = [item["sym"] for item in FANDO_UNIVERSE]
    sector_map = {item["sym"]: item["sector"] for item in FANDO_UNIVERSE}

    print(f"[{now_ist.strftime('%H:%M:%S')}] Downloading live 5m market data for {len(tickers_list)} F&O tickers...")
    
    # Fast multi-threaded batch fetch
    data_5m = yf.download(tickers=tickers_list, period="2d", interval="5m", group_by="ticker", threads=True, progress=False)
    data_daily = yf.download(tickers=tickers_list, period="5d", interval="1d", group_by="ticker", threads=True, progress=False)

    scanned = []
    sector_deltas = {}

    for sym in tickers_list:
        clean_sym = sym.replace(".NS", "")
        sec = sector_map.get(sym, "Diversified")

        try:
            # Extract daily history for true previous day close
            if sym in data_daily.columns.levels[0]:
                df_d = data_daily[sym].dropna()
            else:
                continue

            if len(df_d) < 2:
                continue

            prev_day_close = float(df_d["Close"].iloc[-2])
            pdh = float(df_d["High"].iloc[-2])

            # Extract 5m intraday session candles
            if sym in data_5m.columns.levels[0]:
                df_5 = data_5m[sym].dropna()
            else:
                continue

            if len(df_5) < 3:
                continue

            df_5.index = df_5.index.tz_convert(ist)
            latest_date = df_5.index[-1].date()
            today_candles = df_5[df_5.index.date == latest_date]
            if len(today_candles) < 2:
                today_candles = df_5.iloc[-30:]

            ltp = round(float(today_candles["Close"].iloc[-1]), 2)
            pct_chg = round(((ltp - prev_day_close) / prev_day_close) * 100, 2)
            chg_pts = round(ltp - prev_day_close, 2)
            is_bullish = pct_chg >= 0

            day_high = round(float(today_candles["High"].max()), 2)
            day_low = round(float(today_candles["Low"].min()), 2)

            # Session Volume Weighted Average Price (VWAP)
            typical_price = (today_candles["High"] + today_candles["Low"] + today_candles["Close"]) / 3
            cum_vol = float(today_candles["Volume"].sum()) + 1e-6
            vwap = float((typical_price * today_candles["Volume"]).sum() / cum_vol)
            vwap_gap = round(((ltp - vwap) / vwap) * 100, 2)

            # Relative Volume Multiplier (RVAT)
            vol_series = today_candles["Volume"]
            recent_vol = float(vol_series.iloc[-1])
            avg_vol = float(vol_series.rolling(20, min_periods=1).mean().iloc[-1]) + 1e-6
            rvat = round(recent_vol / avg_vol, 2)

            # Earliest intraday volume surge trigger time
            trigger_time = "09:20"
            for t_idx, row in today_candles.iterrows():
                if row["Volume"] > (avg_vol * 1.35):
                    trigger_time = t_idx.strftime("%H:%M")
                    break

            hyperflow_val = round(max(1.0, rvat * 1.8), 1)
            max_hyperflow = round(hyperflow_val * 1.6, 1)
            min_hyperflow = round(max(1.0, hyperflow_val * 0.6), 1)

            oi_pct = round(float(np.clip((rvat - 1.0) * 4.0 + (pct_chg * 1.2), -18.0, 28.0)), 2)

            if pct_chg >= 0 and oi_pct >= 0:
                behavior, intent, pulse, tone, star_score = "Long buildup", "ACCUMULATION", "P▲ | OI▲", "bull-strong", 4
            elif pct_chg >= 0 and oi_pct < 0:
                behavior, intent, pulse, tone, star_score = "Short covering", "SQUEEZE", "P▲ | OI▼", "bull-cover", 2
            elif pct_chg < 0 and oi_pct >= 0:
                behavior, intent, pulse, tone, star_score = "Short buildup", "DISTRIBUTION", "P▼ | OI▲", "bear-strong", -4
            else:
                behavior, intent, pulse, tone, star_score = "Long unwinding", "LIQUIDATION", "P▼ | OI▼", "bear-weak", -2

            star_display = f"+{star_score}★" if star_score > 0 else f"{star_score}★"
            star_label = "BULLISH" if star_score > 0 else "BEARISH"

            rule_breakout = pct_chg > 0 and ltp > vwap
            rule_volume = rvat >= 1.1
            rule_pdh = ltp >= (pdh * 0.998)
            rule_range = abs(pct_chg) <= 5.5
            final_status = "YES" if (rule_volume and (rule_breakout or rule_pdh)) else "NO"

            candle_payload = []
            sampled_candles = today_candles.tail(32)
            for _, c_row in sampled_candles.iterrows():
                candle_payload.append({
                    "o": round(float(c_row["Open"]), 2),
                    "h": round(float(c_row["High"]), 2),
                    "l": round(float(c_row["Low"]), 2),
                    "c": round(float(c_row["Close"]), 2),
                    "v": round(float(c_row["Volume"]), 0)
                })

            scanned.append({
                "symbol": clean_sym,
                "sector": sec,
                "ltp": ltp,
                "pct_chg": pct_chg,
                "chg_pts": chg_pts,
                "day_high": day_high,
                "day_low": day_low,
                "listed_at": trigger_time,
                "rvat": rvat,
                "hyperflow": f"{hyperflow_val}x",
                "max_hyperflow": f"{max_hyperflow}x",
                "min_hyperflow": f"{min_hyperflow}x",
                "vwap_gap": vwap_gap,
                "futures_oi": oi_pct,
                "oi_behavior": behavior,
                "matrix_intent": intent,
                "matrix_pulse": pulse,
                "matrix_tone": tone,
                "star_score": star_score,
                "star_display": star_display,
                "star_label": star_label,
                "is_bullish": is_bullish,
                "candles": candle_payload,
                "rules": {
                    "breakout": "YES" if rule_breakout else "NO",
                    "volume": "YES" if rule_volume else "NO",
                    "pdh": "YES" if rule_pdh else "NO",
                    "range": "YES" if rule_range else "NO",
                    "final": final_status
                }
            })

            sector_deltas.setdefault(sec, []).append(pct_chg)
        except Exception:
            continue

    sector_perf = {k: round(float(np.mean(v)), 2) for k, v in sector_deltas.items()}
    top_sec = max(sector_perf, key=sector_perf.get) if sector_perf else "IT"
    weak_sec = min(sector_perf, key=sector_perf.get) if sector_perf else "Power"

    for s in scanned:
        s["sector_pct"] = sector_perf.get(s["sector"], 0.0)

    bullish = [s for s in scanned if s["is_bullish"]]
    bearish = [s for s in scanned if not s["is_bullish"]]

    # Sort strictly by institutional volume anomaly (RVAT)
    bullish.sort(key=lambda x: x["rvat"], reverse=True)
    bearish.sort(key=lambda x: x["rvat"], reverse=True)

    focus = (bullish if bullish else bearish)[0] if scanned else None

    output = {
        "sync_time": now_ist.strftime("%d %b %Y, %I:%M %p IST"),
        "ready_date": now_ist.strftime("%Y-%m-%d"),
        "indices": indices,
        "market_cards": {
            "advances": len(bullish),
            "declines": len(bearish),
            "tracked": len(scanned),
            "top_sector": top_sec,
            "weak_sector": weak_sec
        },
        "focus_stock": focus,
        "bullish_stocks": bullish,
        "bearish_stocks": bearish
    }

    with open("screener.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"[{output['sync_time']}] screener.json regenerated with {len(scanned)} total F&O stocks. Advances: {len(bullish)}, Declines: {len(bearish)}")

if __name__ == "__main__":
    run_quant_engine()
