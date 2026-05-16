# analyzer/pattern_recognition.py

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import ta

def detect_swing_high_low(df, order=5):
    """
    Identify local maxima & minima in the 'close' price.
    Returns lists of indices for swing highs and lows.
    """
    close = df['close'].values
    highs = argrelextrema(close, np.greater, order=order)[0]
    lows = argrelextrema(close, np.less, order=order)[0]
    return highs.tolist(), lows.tolist()

def detect_double_top_bottom(df):
    """
    Check latest swing pattern for double top or bottom.
    """
    highs, lows = detect_swing_high_low(df)
    if len(highs) >= 2:
        if abs(df['close'][highs[-1]] - df['close'][highs[-2]]) / df['close'][highs[-2]] < 0.01:
            return 'double_top'
    if len(lows) >= 2:
        if abs(df['close'][lows[-1]] - df['close'][lows[-2]]) / df['close'][lows[-2]] < 0.01:
            return 'double_bottom'
    return None

def detect_head_and_shoulders(df):
    """
    Detect a simple H&S formation among last 7 swing points.
    """
    highs, _ = detect_swing_high_low(df, order=3)
    if len(highs) >= 3:
        p1, p2, p3 = highs[-3], highs[-2], highs[-1]
        c = df['close']
        if c[p1] > c[p2] < c[p3] and c[p2] < c[p1] and c[p2] < c[p3]:
            return 'head_and_shoulders'
    return None

def detect_bollinger_squeeze(df, period=20, thresh=0.02):
    """
    Check for Bollinger Band 'squeeze' (tight band indicating consolidation).
    """
    indicator = ta.volatility.BollingerBands(df['close'], window=period)
    width = (indicator.bollinger_hband() - indicator.bollinger_lband()) / indicator.bollinger_mavg()
    if width.iloc[-1] < thresh:
        return True
    return False

def detect_patterns(df):
    """
    Run all pattern detectors and return found signals.
    """
    patterns = {}
    dt = detect_double_top_bottom(df)
    hs = detect_head_and_shoulders(df)
    squeeze = detect_bollinger_squeeze(df)

    if dt:
        patterns['double_top_bottom'] = dt
    if hs:
        patterns['head_and_shoulders'] = hs
    if squeeze:
        patterns['bollinger_squeeze'] = True

    return patterns
