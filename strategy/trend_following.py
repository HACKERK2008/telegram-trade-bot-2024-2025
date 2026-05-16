# strategy/trend_following.py

import os
import sys
import pandas as pd
from strategy.base_strategy import BaseStrategy

def generate_trend_signal(df: pd.DataFrame, fast: int = 10, slow: int = 21) -> str:
    """
    Simple EMA crossover trend detector.

    Args:
        df (pd.DataFrame): Must have 'close' column.
        fast (int): Fast EMA period.
        slow (int): Slow EMA period.

    Returns:
        'up' if bullish trend, 'down' if bearish trend.
    """
    if "close" not in df.columns:
        raise ValueError("DataFrame must include 'close' column")

    df = df.copy()
    df["ema_fast"] = df["close"].ewm(span=fast, adjust=False).mean()
    df["ema_slow"] = df["close"].ewm(span=slow, adjust=False).mean()

    # Check for crossover in the last 2 candles
    recent = df.iloc[-2:]
    bullish = recent["ema_fast"].iloc[-1] > recent["ema_slow"].iloc[-1]
    bearish = recent["ema_fast"].iloc[-1] < recent["ema_slow"].iloc[-1]

    print(f"📊 EMA Fast: {recent['ema_fast'].iloc[-1]:.2f}, EMA Slow: {recent['ema_slow'].iloc[-1]:.2f}")
    print(f"📈 Trend Detected: {'up' if bullish else 'down'}")

    return "up" if bullish else "down"

class TrendFollowingStrategy(BaseStrategy):
    def __init__(self, fast=10, slow=21):
        super().__init__("TrendFollowing")
        self.fast = fast
        self.slow = slow

    def generate_signal(self, df):
        df["ema_fast"] = df["close"].ewm(span=self.fast, adjust=False).mean()
        df["ema_slow"] = df["close"].ewm(span=self.slow, adjust=False).mean()

        recent = df.iloc[-2:]
        if recent["ema_fast"].iloc[-1] > recent["ema_slow"].iloc[-1]:
            return "up"
        else:
            return "down"
