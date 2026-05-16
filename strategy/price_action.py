# strategy/price_action.py

import pandas as pd

def detect_price_action(df: pd.DataFrame) -> str:
    """
    Detects key price action signals from OHLC data:
    - Pin bar
    - Inside bar
    - Breakout
    
    Returns:
        str: 'up', 'down', or 'neutral'
    """
    if not all(col in df.columns for col in ['open', 'high', 'low', 'close']):
        raise ValueError("DataFrame must contain OHLC columns.")

    df = df.copy()
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # === 1. Pin Bar
    body = abs(last["close"] - last["open"])
    upper_wick = last["high"] - max(last["close"], last["open"])
    lower_wick = min(last["close"], last["open"]) - last["low"]

    if body < (upper_wick + lower_wick) / 2:
        if lower_wick > body * 2:
            return "up"  # bullish pin
        elif upper_wick > body * 2:
            return "down"  # bearish pin

    # === 2. Inside Bar
    if last["high"] < prev["high"] and last["low"] > prev["low"]:
        return "neutral"

    # === 3. Breakout Candle (outside bar + large body)
    if last["high"] > prev["high"] and last["low"] < prev["low"]:
        if last["close"] > last["open"]:
            return "up"
        elif last["close"] < last["open"]:
            return "down"

    return "neutral"
