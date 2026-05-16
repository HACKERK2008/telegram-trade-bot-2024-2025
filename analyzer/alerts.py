# analyzer/alerts.py

import pandas as pd

# ─── Legacy Alert Components ─────────────────────────────────────────────────────

def run_alerts(symbol, df, signals=None, stop_loss_zone=None):
    """
    Wrapper to attach signals/SL zone into DataFrame and call detect_alerts().
    This makes it compatible with analyzer.py and mocktest workflows.
    """
    df = df.copy()
    if signals is not None:
        df["signals"] = signals
    if stop_loss_zone is not None:
        df["stop_loss_zone"] = stop_loss_zone
    return detect_alerts(symbol, df)

def detect_volume_spike(df, lookback=20, mult=2.5):
    df = df.copy()
    df["avg_volume"] = df["volume"].rolling(lookback).mean()
    return len(df) >= lookback and df["volume"].iloc[-1] > mult * df["avg_volume"].iloc[-1]

def detect_price_breakout(df, lookback=20):
    if len(df) < lookback:
        return False
    high = df["high"].iloc[-lookback:-1].max()
    low = df["low"].iloc[-lookback:-1].min()
    last = df["close"].iloc[-1]
    return last > high or last < low

def detect_momentum_flip(df):
    if len(df) < 3:
        return False
    prev, curr_open, curr = df["close"].iloc[-2], df["open"].iloc[-1], df["close"].iloc[-1]
    return (prev < curr_open < curr) or (prev > curr_open > curr)

def detect_atr_spike(df, atr_period=14, mult=1.5):
    df = df.copy()
    df["H-L"] = df["high"] - df["low"]
    df["H-PC"] = abs(df["high"] - df["close"].shift(1))
    df["L-PC"] = abs(df["low"] - df["close"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    df["ATR"] = df["TR"].rolling(atr_period).mean()
    return df["TR"].iloc[-1] > mult * df["ATR"].iloc[-1]

def detect_price_gap(df, threshold_pct=1.0):
    if len(df) < 2:
        return False
    prev_close, curr_open = df["close"].iloc[-2], df["open"].iloc[-1]
    return abs(curr_open - prev_close) / prev_close * 100 >= threshold_pct

def detect_rsi_extreme(df, period=14, low=30, high=70):
    df = df.copy()
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / (loss + 1e-9)
    df["rsi"] = 100 - (100 / (1 + rs))
    last = df["rsi"].iloc[-1]
    return last < low or last > high

# ─── Smart Alert Engine ──────────────────────────────────────────────────────────

def detect_signal_conflict(signals):
    return (
        (signals.get("trend") == "up" and signals.get("momentum") == "down") or
        (signals.get("trend") == "down" and signals.get("momentum") == "up")
    )

def detect_alerts(symbol, df):
    """
    Combines legacy alerts + enhanced analyzer insights.
    """
    legacy = {
        "volume_spike": detect_volume_spike(df),
        "price_breakout": detect_price_breakout(df),
        "momentum_flip": detect_momentum_flip(df),
        "atr_spike": detect_atr_spike(df),
        "price_gap": detect_price_gap(df),
        "rsi_extreme": detect_rsi_extreme(df),
    }

    smart_flags = []
    try:
        # Smart analysis from signals, volume, OI, volatility, SL zone
        signals = df.get("signals", {})
        sl_zone = df.get("stop_loss_zone", False)

        if "oi_change" in df.columns and df["oi_change"].iloc[-1] > 15:
            smart_flags.append("🔺 High OI spike")

        if "avg_volume" in df.columns and df["volume"].iloc[-1] > df["avg_volume"].iloc[-1] * 2:
            smart_flags.append("📊 Volume surge")

        if "atr" in df.columns and df["atr"].iloc[-1] > df["close"].iloc[-1] * 0.03:
            smart_flags.append("⚡ ATR Volatility High")

        if detect_signal_conflict(signals):
            smart_flags.append("⚠️ Signal Conflict")

        # ✅ Fixed line here:
        if isinstance(sl_zone, (pd.Series, pd.DataFrame)):
            if sl_zone.iloc[-1]:
                smart_flags.append("🛑 Near SL Zone")
        elif sl_zone:
            smart_flags.append("🛑 Near SL Zone")

    except Exception as e:
        print(f"⚠️ Error in smart alert generation: {e}")

    alerts = {
        **legacy,
        "any_alert": any(legacy.values()) or bool(smart_flags),
        "alert_count": sum(legacy.values()) + len(smart_flags),
        "alert_score": sum({
            "volume_spike": 2, "price_breakout": 2, "atr_spike": 1.5,
            "momentum_flip": 1.5, "price_gap": 1, "rsi_extreme": 1
        }[k] for k, v in legacy.items() if v) + len(smart_flags) * 1.5,
        "text_flags": smart_flags
    }

    return alerts
