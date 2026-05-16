# strategy/confidence_score.py

def compute_confidence_score(strategy: str, alerts: dict, headlines: list[str], prediction: str) -> float:
    """
    Combines strategy match, alert signals, and news headlines to compute a confidence score.

    Returns:
        Confidence score: float (0–100)
    """
    score = 50  # base score

    # ✅ Strategy confidence boost
    strategy_weights = {
        "volume_spike": 10,
        "breakout": 12,
        "momentum": 8,
        "volatility": 7,
        "rsi_extreme": 5,
        "macd": 6,
        "supertrend": 9,
        "price_action": 8
    }
    strategy_key = strategy.lower().replace(" ", "_")
    score += strategy_weights.get(strategy_key, 5)

    # 📊 Alert signal strength
    if alerts:
        score += min(alerts.get("alert_score", 5), 20)

    # 📰 News sentiment boost
    sentiment_boost = 0
    if headlines:
        sentiment_boost += sum(
            3 for line in headlines
            if any(word in line.lower() for word in ["beats", "surge", "growth", "record", "bullish"])
        )
        sentiment_boost -= sum(
            3 for line in headlines
            if any(word in line.lower() for word in ["loss", "strike", "fraud", "scam", "fall", "fear"])
        )

    score += sentiment_boost

    # 🤖 Adjust by prediction direction
    if prediction.lower() == "sell":
        score -= 5

    return max(0, min(round(score, 2), 100))
