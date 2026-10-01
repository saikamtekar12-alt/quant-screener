import json
import os
import time
from datetime import datetime, timedelta, timezone
import numpy as np
import pandas as pd
import yfinance as yf

# Tracked universe with sector and market cap classification
FANDO_UNIVERSE = [
    {"sym": "DOLPHIN.NS", "name": "DOLPHIN", "sector": "Energy", "mkt_cap_type": "S", "mkt_cap_val": "₹1.8k Cr", "seg": "EQ"},
    {"sym": "AMNPLST.NS", "name": "AMNPLST", "sector": "Basic Materials", "mkt_cap_type": "S", "mkt_cap_val": "₹1.1k Cr", "seg": "EQ"},
    {"sym": "WAKEFIT.NS", "name": "WAKEFIT", "sector": "Retail trade", "mkt_cap_type": "M", "mkt_cap_val": "₹5.6k Cr", "seg": "EQ"},
    {"sym": "CSLFINANCE.NS", "name": "CSLFINANCE", "sector": "Financial", "mkt_cap_type": "S", "mkt_cap_val": "₹671 Cr", "seg": "EQ"},
    {"sym": "SYNGENE.NS", "name": "SYNGENE", "sector": "Healthcare", "mkt_cap_type": "L", "mkt_cap_val": "₹25.5k Cr", "seg": "EQ"},
    {"sym": "REGENCERAM.NS", "name": "REGENCERAM", "sector": "Producer manufac..", "mkt_cap_type": "μ", "mkt_cap_val": "₹127 Cr", "seg": "EQ"},
    {"sym": "HMAAGRO.NS", "name": "HMAAGRO", "sector": "Consumer Non-Cyc..", "mkt_cap_type": "S", "mkt_cap_val": "₹1.4k Cr", "seg": "EQ"},
    {"sym": "MANBA.NS", "name": "MANBA", "sector": "Financial", "mkt_cap_type": "S", "mkt_cap_val": "₹691 Cr", "seg": "EQ"},
    {"sym": "MCX.NS", "name": "MCX", "sector": "Capital Markets", "mkt_cap_type": "L", "mkt_cap_val": "₹16.5k Cr", "seg": "F&O"},
    {"sym": "DIXON.NS", "name": "DIXON", "sector": "Consumer Durables", "mkt_cap_type": "L", "mkt_cap_val": "₹78.2k Cr", "seg": "F&O"},
    {"sym": "DABUR.NS", "name": "DABUR", "sector": "FMCG", "mkt_cap_type": "L", "mkt_cap_val": "₹98.4k Cr", "seg": "F&O"},
    {"sym": "DRREDDY.NS", "name": "DRREDDY", "sector": "Pharma", "mkt_cap_type": "L", "mkt_cap_val": "₹1.0L Cr", "seg": "F&O"},
    {"sym": "HEROMOTOCO.NS", "name": "HEROMOTOCO", "sector": "Auto", "mkt_cap_type": "L", "mkt_cap_val": "₹1.1L Cr", "seg": "F&O"},
    {"sym": "ADANIPOWER.NS", "name": "ADANIPOWER", "sector": "Power", "mkt_cap_type": "L", "mkt_cap_val": "₹75.4k Cr", "seg": "F&O"},
    {"sym": "BANDHANBNK.NS", "name": "BANDHANBNK", "sector": "Financial Services", "mkt_cap_type": "M", "mkt_cap_val": "₹28.1k Cr", "seg": "F&O"},
    {"sym": "BANKBARODA.NS", "name": "BANKBARODA", "sector": "Financial Services", "mkt_cap_type": "L", "mkt_cap_val": "₹1.2L Cr", "seg": "F&O"},
    {"sym": "BEL.NS", "name": "BEL", "sector": "Defence", "mkt_cap_type": "L", "mkt_cap_val": "₹2.2L Cr", "seg": "F&O"},
    {"sym": "BSE.NS", "name": "BSE", "sector": "Capital Markets", "mkt_cap_type": "M", "mkt_cap_val": "₹38.6k Cr", "seg": "F&O"},
    {"sym": "INFY.NS", "name": "INFY", "sector": "IT", "mkt_cap_type": "L", "mkt_cap_val": "₹6.8L Cr", "seg": "F&O"},
    {"sym": "TCS.NS", "name": "TCS", "sector": "IT", "mkt_cap_type": "L", "mkt_cap_val": "₹14.2L Cr", "seg": "F&O"},
    {"sym": "RELIANCE.NS", "name": "RELIANCE", "sector": "Energy", "mkt_cap_type": "L", "mkt_cap_val": "₹19.4L Cr", "seg": "F&O"},
    {"sym": "HDFCBANK.NS", "name": "HDFCBANK", "sector": "Financial Services", "mkt_cap_type": "L", "mkt_cap_val": "₹12.8L Cr", "seg": "F&O"},
    {"sym": "ICICIBANK.NS", "name": "ICICIBANK", "sector": "Financial Services", "mkt_cap_type": "L", "mkt_cap_val": "₹9.1L Cr", "seg": "F&O"},
    {"sym": "SBIN.NS", "name": "SBIN", "sector": "Financial Services", "mkt_cap_type": "L", "mkt_cap_val": "₹7.4L Cr", "seg": "F&O"},
    {"sym": "COALINDIA.NS", "name": "COALINDIA", "sector": "Oil & Gas", "mkt_cap_type": "L", "mkt_cap_val": "₹2.6L Cr", "seg": "F&O"},
    {"sym": "TITAN.NS", "name": "TITAN", "sector": "Consumer Goods", "mkt_cap_type": "L", "mkt_cap_val": "₹3.1L Cr", "seg": "F&O"},
    {"sym": "TATASTEEL.NS", "name": "TATASTEEL", "sector": "Metal", "mkt_cap_type": "L", "mkt_cap_val": "₹1.9L Cr", "seg": "F&O"},
    {"sym": "LT.NS", "name": "LT", "sector": "Capital Goods", "mkt_cap_type": "L", "mkt_cap_val": "₹4.8L Cr", "seg": "F&O"},
    {"sym": "RADICO.NS", "name": "RADICO", "sector": "FMCG", "mkt_cap_type": "M", "mkt_cap_val": "₹31.2k Cr", "seg": "F&O"},
    {"sym": "SUNPHARMA.NS", "name": "SUNPHARMA", "sector": "Pharma", "mkt_cap_type": "L", "mkt_cap_val": "₹4.1L Cr", "seg": "F&O"},
    {"sym": "AXISBANK.NS", "name": "AXISBANK", "sector": "Financial Services", "mkt_cap_type": "L", "mkt_cap_val": "₹3.6L Cr", "seg": "F&O"},
    {"sym": "OFSS.NS", "name": "OFSS", "sector": "IT", "mkt_cap_type": "L", "mkt_cap_val": "₹92.5k Cr", "seg": "F&O"},
    {"sym": "PERSISTENT.NS", "name": "PERSISTENT", "sector": "IT", "mkt_cap_type": "M", "mkt_cap_val": "₹41.8k Cr", "seg": "F&O"},
    {"sym": "JIOFIN.NS", "name": "JIOFIN", "sector": "Financial Services", "mkt_cap_type": "L", "mkt_cap_val": "₹1.8L Cr", "seg": "F&O"},
    {"sym": "SUZLON.NS", "name": "SUZLON", "sector": "Power", "mkt_cap_type": "M", "mkt_cap_val": "₹52.0k Cr", "seg": "F&O"}
]

def run_quant_engine():
    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist)

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

    tickers_list = [item["sym"] for item in FANDO_UNIVERSE]
    meta_map = {item["sym"]: item for item in FANDO_UNIVERSE}

    print(f"[{now_ist.strftime('%H:%M:%S')}] Batch fetching market data for {len(tickers_list)} tickers...")
    data_5m = yf.download(tickers=tickers_list, period="2d", interval="5m", group_by="ticker", threads=True, progress=False)
    data_daily = yf.download(tickers=tickers_list, period="1mo", interval="1d", group_by="ticker", threads=True, progress=False)

    scanned_quant = []
    smart_money_stocks = []
    sector_deltas = {}

    for sym in tickers_list:
        meta = meta_map[sym]
        clean_sym = meta["name"]
        sec = meta["sector"]

        try:
            if sym in data_daily.columns.levels[0]:
                df_d = data_daily[sym].dropna()
            else:
                continue

            if len(df_d) < 5:
                continue

            prev_day_close = float(df_d["Close"].iloc[-2])
            pdh = float(df_d["High"].iloc[-2])
            pdl = float(df_d["Low"].iloc[-2])

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

            typical_price = (today_candles["High"] + today_candles["Low"] + today_candles["Close"]) / 3
            cum_vol = float(today_candles["Volume"].sum()) + 1e-6
            vwap = float((typical_price * today_candles["Volume"]).sum() / cum_vol)
            vwap_gap = round(((ltp - vwap) / vwap) * 100, 2)

            vol_series = today_candles["Volume"]
            recent_vol = float(vol_series.iloc[-1])
            avg_vol = float(vol_series.rolling(20, min_periods=1).mean().iloc[-1]) + 1e-6
            rvat = round(recent_vol / avg_vol, 2)

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

            # --- SMART MONEY FOOTPRINT MATHEMATICAL ENGINE ---
            # 10-day volume & activity history
            daily_vols = df_d["Volume"].tail(10).values
            daily_pcts = df_d["Close"].pct_change().tail(10).fillna(0).values * 100

            # Daily institutional activity score calculation (Volume multiple * momentum factor)
            norm_vol_scores = []
            v_med = np.median(daily_vols) if len(daily_vols) > 0 else 1.0
            for v_val, p_val in zip(daily_vols, daily_pcts):
                act_score = round(float((v_val / (v_med + 1e-6)) * (1.0 + abs(p_val) * 0.35) * 4.2), 2)
                norm_vol_scores.append(min(60.0, max(1.2, act_score)))

            selected_score = norm_vol_scores[-1] if norm_vol_scores else 8.5
            prev_score = norm_vol_scores[-2] if len(norm_vol_scores) >= 2 else (selected_score * 0.8)
            prev_delta = round(selected_score - prev_score, 2)
            
            four_day_avg = round(float(np.mean(norm_vol_scores[-4:])), 2) if len(norm_vol_scores) >= 4 else selected_score
            ten_day_avg = round(float(np.mean(norm_vol_scores)), 2)

            # Streak calculation: days score maintained above 6.0
            streak_count = 0
            for sc in reversed(norm_vol_scores):
                if sc >= 6.0:
                    streak_count += 1
                else:
                    break
            streak_str = f"{max(1, streak_count)}d"

            # Signal tags
            sig_list = []
            if selected_score >= 10.0 or rvat >= 1.8:
                sig_list.append("⚡ surge")
            if streak_count >= 2:
                sig_list.append(f"🔥 {streak_count}d")
            if selected_score > four_day_avg:
                sig_list.append("↑ above avg")
            if not sig_list:
                sig_list.append("steady")

            stock_item = {
                "symbol": clean_sym,
                "sector": sec,
                "seg": meta["seg"],
                "mkt_cap_type": meta["mkt_cap_type"],
                "mkt_cap_val": meta["mkt_cap_val"],
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
                },
                # Institutional Footprint
                "sm_score": selected_score,
                "sm_prev_delta": prev_delta,
                "sm_4d_avg": four_day_avg,
                "sm_10d_avg": ten_day_avg,
                "sm_streak": streak_str,
                "sm_trend_bars": norm_vol_scores[-10:],
                "sm_signals": sig_list
            }

            scanned_quant.append(stock_item)
            smart_money_stocks.append(stock_item)
            sector_deltas.setdefault(sec, []).append(pct_chg)
        except Exception:
            continue

    sector_perf = {k: round(float(np.mean(v)), 2) for k, v in sector_deltas.items()}
    top_sec = max(sector_perf, key=sector_perf.get) if sector_perf else "Energy"
    weak_sec = min(sector_perf, key=sector_perf.get) if sector_perf else "Financial"

    for s in scanned_quant:
        s["sector_pct"] = sector_perf.get(s["sector"], 0.0)

    bullish = [s for s in scanned_quant if s["is_bullish"]]
    bearish = [s for s in scanned_quant if not s["is_bullish"]]

    bullish.sort(key=lambda x: x["rvat"], reverse=True)
    bearish.sort(key=lambda x: x["rvat"], reverse=True)

    # Sort Smart Money stocks by highest Institutional Activity Score
    smart_money_stocks.sort(key=lambda x: x["sm_score"], reverse=True)

    focus = (bullish if bullish else bearish)[0] if scanned_quant else None

    # Institutional summary counts for top banner
    score_6_plus = sum(1 for s in smart_money_stocks if s["sm_score"] >= 6.0)
    streak_2d_plus = sum(1 for s in smart_money_stocks if int(s["sm_streak"].replace("d", "")) >= 2)
    surge_count = sum(1 for s in smart_money_stocks if "⚡ surge" in s["sm_signals"])

    output = {
        "sync_time": now_ist.strftime("%d %b %Y, %I:%M %p IST"),
        "selected_date": now_ist.strftime("%d %b %Y"),
        "indices": indices,
        "market_cards": {
            "advances": len(bullish),
            "declines": len(bearish),
            "tracked": len(scanned_quant),
            "top_sector": top_sec,
            "weak_sector": weak_sec
        },
        "sm_stats": {
            "universe_count": 2055,
            "filtered_count": len(smart_money_stocks),
            "score_6_plus": score_6_plus,
            "streak_2d": streak_2d_plus,
            "surge_day": surge_count
        },
        "focus_stock": focus,
        "bullish_stocks": bullish,
        "bearish_stocks": bearish,
        "smart_money_stocks": smart_money_stocks
    }

    with open("screener.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"[{output['sync_time']}] screener.json regenerated with Smart Money Institutional footprints.")

if __name__ == "__main__":
    run_quant_engine()
