# strategy/volume_based.py

import pandas as pd

def detect_volume_signal(df: pd.DataFrame, lookback: int = 20, spike_ratio: float = 2.0) -> str:
    """
    Detects trading signal based on volume spikes and price reaction.

    Args:
        df (pd.DataFrame): Must have 'close' and 'volume'
        lookback (int): Rolling window for average volume
        spike_ratio (float): Multiplier over average to detect spikes

    Returns:
        str: 'up', 'down', or 'neutral'
    """
    if not all(col in df.columns for col in ['close', 'volume']):
        raise ValueError("DataFrame must contain 'close' and 'volume'")

    df = df.copy()
    df["avg_volume"] = df["volume"].rolling(window=lookback).mean()
    df.dropna(inplace=True)

    latest = df.iloc[-1]
    prev = df.iloc[-2]

    print(f"🔍 Latest Volume: {latest['volume']}, Avg Volume: {latest['avg_volume']:.0f}")

    if latest["volume"] > (latest["avg_volume"] * spike_ratio):
        # If price rises with spike → bullish interest
        if latest["close"] > prev["close"]:
            return "up"
        elif latest["close"] < prev["close"]:
            return "down"

    return "neutral"
