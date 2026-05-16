# strategy/volatility.py

import pandas as pd

def generate_volatility_signal(df: pd.DataFrame, atr_period: int = 14, multiplier: float = 1.5) -> str:
    """
    Uses ATR-based breakout logic to detect volatility surges.

    Args:
        df (pd.DataFrame): Must include 'high', 'low', 'close'
        atr_period (int): ATR lookback window
        multiplier (float): Breakout sensitivity threshold

    Returns:
        str: 'up' if bullish breakout, 'down' if bearish breakdown
    """
    if not all(col in df.columns for col in ["high", "low", "close"]):
        raise ValueError("DataFrame must include high, low, close")

    df = df.copy()

    # 1. Compute ATR (Average True Range)
    df["H-L"] = df["high"] - df["low"]
    df["H-PC"] = abs(df["high"] - df["close"].shift(1))
    df["L-PC"] = abs(df["low"] - df["close"].shift(1))
    df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1)
    df["ATR"] = df["TR"].rolling(window=atr_period).mean()

    # 2. Define breakout thresholds
    last_close = df["close"].iloc[-1]
    prev_close = df["close"].iloc[-2]
    last_range = df["TR"].iloc[-1]
    avg_atr = df["ATR"].iloc[-1]

    print(f"⚡ ATR: {avg_atr:.2f}, Last Range: {last_range:.2f}, Prev Close: {prev_close:.2f}")

    if last_range > (avg_atr * multiplier):
        return "up" if last_close > prev_close else "down"
    else:
        return "neutral"
