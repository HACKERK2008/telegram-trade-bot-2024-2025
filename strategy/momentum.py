# strategy/momentum.py

import pandas as pd

def generate_momentum_signal(df: pd.DataFrame, rsi_period=14, roc_period=10) -> str:
    """
    Uses RSI and ROC to detect strength continuation or weakness.

    Args:
        df (pd.DataFrame): Must include 'close'
        rsi_period (int): RSI lookback
        roc_period (int): ROC lookback

    Returns:
        str: 'up', 'down', or 'neutral'
    """
    if "close" not in df.columns:
        raise ValueError("DataFrame must include 'close'")

    df = df.copy()

    # RSI calculation
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / (loss + 1e-9)
    df["rsi"] = 100 - (100 / (1 + rs))

    # ROC calculation
    df["roc"] = df["close"].pct_change(periods=roc_period) * 100

    last_rsi = df["rsi"].iloc[-1]
    last_roc = df["roc"].iloc[-1]

    print(f"💪 RSI: {last_rsi:.2f}, ROC: {last_roc:.2f}")

    # Interpretation
    if last_rsi > 60 and last_roc > 1.0:
        return "up"
    elif last_rsi < 40 and last_roc < -1.0:
        return "down"
    else:
        return "neutral"
