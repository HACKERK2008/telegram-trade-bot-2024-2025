# strategy/news_filter.py

def adjust_confidence_by_news(confidence: float, news_headlines: list[str], signal: str) -> float:
    """
    Boosts or reduces confidence score based on keywords.
    """
    if not news_headlines:
        return confidence

    trend_up_keywords = ["beats", "growth", "surge", "record"]
    trend_down_keywords = ["fall", "fraud", "loss", "strike"]

    boost = 0
    for line in news_headlines:
        line_lower = line.lower()
        if signal.lower() == "buy":
            if any(word in line_lower for word in trend_up_keywords):
                boost += 5
        elif signal.lower() == "sell":
            if any(word in line_lower for word in trend_down_keywords):
                boost += 5

    return min(confidence + boost, 100.0)
