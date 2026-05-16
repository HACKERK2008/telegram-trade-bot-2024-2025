# strategy/strategy_utils.py

def find_nearest_strike(price: float, step: int = 50) -> int:
    """
    Aligns the price to the nearest valid strike (default step = 50).
    Example: 24312 → 24300

    Args:
        price (float): Current spot price
        step (int): Strike spacing (default 50 for NIFTY/BANKNIFTY)

    Returns:
        int: Rounded strike
    """
    return round(price / step) * step


def detect_volatility_spike(df, window=10, threshold=1.5) -> bool:
    """
    Detects a volatility spike using rolling standard deviation.
    If current candle volatility > threshold × rolling average, returns True

    Args:
        df (DataFrame): Must have 'close' column
        window (int): Rolling window
        threshold (float): Multiplier

    Returns:
        bool: True if spike detected
    """
    df = df.copy()
    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(window=window).std()

    latest_vol = df["volatility"].iloc[-1]
    avg_vol = df["volatility"].iloc[-window:].mean()

    print(f"⚡ Latest Volatility: {latest_vol:.4f}, Avg: {avg_vol:.4f}")

    return latest_vol > (avg_vol * threshold)


def score_confidence(trend: str, news: list[str]) -> int:
    """
    Scores a trend signal based on trend direction + news reinforcement

    Args:
        trend (str): 'up' or 'down'
        news (list): List of top news headlines

    Returns:
        int: Confidence score 0–100
    """
    boost_keywords = {
        "up": ["beats", "record", "strong", "approval", "growth"],
        "down": ["misses", "strike", "cut", "downturn", "fraud"]
    }

    boost = 0
    for headline in news:
        if any(word in headline.lower() for word in boost_keywords[trend]):
            boost += 10

    base_score = 60 if trend == "up" else 50  # example baseline
    confidence = min(100, base_score + boost)

    return confidence
