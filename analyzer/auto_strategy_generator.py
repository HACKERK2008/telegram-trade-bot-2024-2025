# analyzer/auto_strategy_generator.py

import pandas as pd
from strategy.trend_following import generate_trend_signal
from strategy.mean_reversion import generate_mean_reversion_signal
from strategy.volatility import generate_volatility_signal
from strategy.momentum import generate_momentum_signal
from strategy.volume_based import detect_volume_signal
from strategy.price_action import detect_price_action
from strategy.ml_strategies import MLTrendPredictor

def generate_strategy_recommendation(df: pd.DataFrame) -> dict:
    """
    Analyze the last N candles and score each strategy.
    Recommend the best based on alignment + volatility + price behavior.
    """
    if df.shape[0] < 20:
        raise ValueError("⛔ Not enough data to evaluate strategies.")

    ml = MLTrendPredictor()
    scores = {}

    try:
        if generate_trend_signal(df) == "up":
            scores["TrendFollowing"] = 2
    except: pass

    try:
        if generate_mean_reversion_signal(df) == "down":
            scores["MeanReversion"] = 2
    except: pass

    try:
        if generate_volatility_signal(df) != "neutral":
            scores["Volatility"] = 1.5
    except: pass

    try:
        if generate_momentum_signal(df) != "neutral":
            scores["Momentum"] = 1.5
    except: pass

    try:
        if detect_volume_signal(df) != "neutral":
            scores["Volume"] = 1
    except: pass

    try:
        if detect_price_action(df) != "neutral":
            scores["PriceAction"] = 1
    except: pass

    try:
        if ml.predict_next(df) != "neutral":
            scores["MLPredictor"] = 2
    except: pass

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best = top[0] if top else ("NoClearStrategy", 0)

    return {
        "strategy_scores": scores,
        "recommended_strategy": best[0],
        "confidence_score": best[1] * 10 + 50
    }
