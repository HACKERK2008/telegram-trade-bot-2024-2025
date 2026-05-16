# mocktest_all_strategies.py

import os
import sys
import pandas as pd
import numpy as np

# Add root path to imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import all strategy modules
from strategy.trend_following import generate_trend_signal
from strategy.mean_reversion import generate_mean_reversion_signal
from strategy.volatility import generate_volatility_signal
from strategy.momentum import generate_momentum_signal
from strategy.price_action import detect_price_action
from strategy.volume_based import detect_volume_signal
from strategy.ml_strategies import MLTrendPredictor

# Create dummy OHLCV DataFrame
def generate_dummy_df(rows=100):
    np.random.seed(42)
    close = np.cumsum(np.random.randn(rows)) + 100
    open_ = close + np.random.uniform(-1, 1, size=rows)
    high = np.maximum(open_, close) + np.random.uniform(0, 2, size=rows)
    low = np.minimum(open_, close) - np.random.uniform(0, 2, size=rows)
    volume = np.random.randint(1000, 10000, size=rows)

    return pd.DataFrame({
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume
    })

def test_strategies(df):
    print("📦 MOCK STRATEGY FUNCTION TESTER")
    print("=" * 40)

    tests = [
        ("TrendFollowing", generate_trend_signal),
        ("MeanReversion", generate_mean_reversion_signal),
        ("Volatility", generate_volatility_signal),
        ("Momentum", generate_momentum_signal),
        ("PriceAction", detect_price_action),
        ("VolumeBased", detect_volume_signal),
    ]

    for name, func in tests:
        try:
            result = func(df)
            print(f"✅ {name} → Output: {result}")
        except Exception as e:
            print(f"❌ {name} → Error: {e}")

    # ML Predictor
    try:
        ml = MLTrendPredictor()
        result = ml.predict_next(df)
        print(f"✅ MLPredictor → Output: {result}")
    except Exception as e:
        print(f"❌ MLPredictor → Error: {e}")

if __name__ == "__main__":
    df = generate_dummy_df()
    test_strategies(df)
