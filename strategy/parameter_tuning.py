# strategy/parameter_tuning.py

import pandas as pd
from strategy.trend_following import generate_trend_signal
from data_fetching_system.data_fetcher import fetch_historical_data

def score_signal_accuracy(df: pd.DataFrame, signal_func, **kwargs) -> float:
    """
    Measures how accurate a signal function is in predicting the next price move.

    Args:
        df (DataFrame): Price data with 'close'
        signal_func (function): Strategy signal function (returns 'up'/'down')
        kwargs: Parameters passed to the signal function

    Returns:
        float: Accuracy score between 0 and 1
    """
    df = df.copy()
    df["signal"] = signal_func(df, **kwargs)
    df["future"] = df["close"].shift(-1) > df["close"]
    df["pred"] = df["signal"].apply(lambda x: 1 if x == "up" else 0)
    df.dropna(inplace=True)

    accuracy = (df["pred"] == df["future"].astype(int)).mean()
    return round(accuracy, 4)

def tune_trend_strategy(symbol: str, fast_range=(5, 20), slow_range=(15, 50)) -> dict:
    """
    Grid searches for the best EMA (fast, slow) pair for trend following strategy.

    Returns:
        dict: Best parameters and accuracy score.
    """
    print(f"📈 Tuning trend strategy for {symbol} using historical data...")
    df = fetch_historical_data(symbol, interval="FIVE_MINUTE", days=30)

    best_score = 0
    best_params = None
    results = []

    for fast in range(fast_range[0], fast_range[1], 2):
        for slow in range(slow_range[0], slow_range[1], 5):
            if fast >= slow:
                continue  # fast must be less than slow

            score = score_signal_accuracy(df, generate_trend_signal, fast=fast, slow=slow)
            results.append(((fast, slow), score))

            if score > best_score:
                best_score = score
                best_params = (fast, slow)

    print(f"🧠 Best EMA Combo: {best_params} → Accuracy: {best_score:.2%}")
    return {
        "symbol": symbol,
        "best_params": best_params,
        "accuracy": best_score,
        "all_results": results
    }

def sample_hyperparam_config():
    """
    Dummy config used in mock testing or dry runs of strategies.
    """
    return {
        "ema_fast": 10,
        "ema_slow": 21,
        "bb_window": 20,
        "rsi_period": 14,
        "roc_period": 10,
        "signal_threshold": 0.65
    }
