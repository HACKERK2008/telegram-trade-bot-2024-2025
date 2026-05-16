# analyzer/technicals.py

import pandas as pd
import numpy as np

def calculate_ema(df: pd.DataFrame, period: int = 14, col: str = "close") -> pd.Series:
    return df[col].ewm(span=period, adjust=False).mean()

def calculate_sma(df: pd.DataFrame, period: int = 14, col: str = "close") -> pd.Series:
    return df[col].rolling(window=period).mean()

def calculate_rsi(df: pd.DataFrame, period: int = 14, col: str = "close") -> pd.Series:
    delta = df[col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))

def calculate_macd(df: pd.DataFrame, fast=12, slow=26, signal=9, col: str = "close"):
    ema_fast = df[col].ewm(span=fast, adjust=False).mean()
    ema_slow = df[col].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df["high"] - df["low"]
    high_close = np.abs(df["high"] - df["close"].shift())
    low_close = np.abs(df["low"] - df["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def calculate_bollinger_bands(df: pd.DataFrame, period=20, std_mult=2):
    sma = calculate_sma(df, period)
    std = df["close"].rolling(window=period).std()
    upper_band = sma + std_mult * std
    lower_band = sma - std_mult * std
    return upper_band, sma, lower_band

def detect_crossover(series1: pd.Series, series2: pd.Series) -> str:
    """
    Detects crossover between two series.
    Returns 'bullish', 'bearish', or 'none'
    """
    if len(series1) < 2 or len(series2) < 2:
        return "none"
    if series1.iloc[-2] < series2.iloc[-2] and series1.iloc[-1] > series2.iloc[-1]:
        return "bullish"
    elif series1.iloc[-2] > series2.iloc[-2] and series1.iloc[-1] < series2.iloc[-1]:
        return "bearish"
    return "none"
