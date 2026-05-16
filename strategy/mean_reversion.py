# strategy/mean_reversion.py

import pandas as pd

def generate_mean_reversion_signal(df: pd.DataFrame, period: int = 20, std_dev: float = 2) -> str:
    """
    Detects mean reversion using Bollinger Bands.

    Args:
        df (pd.DataFrame): Must include 'close'
        period (int): SMA window size
        std_dev (float): Standard deviation multiplier

    Returns:
        str: 'up' if bounce from lower band, 'down' if rejection at upper band
    """
    if "close" not in df.columns:
        raise ValueError("DataFrame must include 'close' column")

    df = df.copy()
    df["sma"] = df["close"].rolling(window=period).mean()
    df["upper"] = df["sma"] + (df["close"].rolling(window=period).std() * std_dev)
    df["lower"] = df["sma"] - (df["close"].rolling(window=period).std() * std_dev)

    latest_close = df["close"].iloc[-1]
    lower = df["lower"].iloc[-1]
    upper = df["upper"].iloc[-1]

    print(f"🔎 Close: {latest_close:.2f}, Lower: {lower:.2f}, Upper: {upper:.2f}")

    if latest_close <= lower:
        return "up"    # Buy signal (reversion from oversold)
    elif latest_close >= upper:
        return "down"  # Sell signal (reversion from overbought)
    else:
        return "neutral"
