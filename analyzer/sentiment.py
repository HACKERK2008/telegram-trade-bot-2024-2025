# analyzer/sentiment.py

import re
import requests
from datetime import datetime
from analyzer.news_trend_tracker import get_news_sentiment

CONFIDENCE_STATE = {
    "last_action_time": None,
    "consecutive_trades": 0,
    "loss_streak": 0,
    "confidence_level": 100  # 0 - 100 scale
}

WARNING_MESSAGES = {
    "overtrading": "⚠️ You're trading frequently. Consider taking a break.",
    "losing_streak": "🚫 Losses detected. Review strategy before next trade.",
    "emotion_check": "🧠 Trade only when calm. Avoid revenge trading.",
    "patience_reminder": "⏳ Sometimes no trade is the best trade."
}

def clean_text(text):
    return re.sub(r"[^\w\s]", "", text).lower()

def get_emotional_sentiment(symbol: str) -> str:
    """
    Combines headline tone + user behavior to return 'calm', 'risk', or 'danger'.
    """
    news_sentiment = get_news_sentiment(symbol)
    user = CONFIDENCE_STATE.copy()

    if user["loss_streak"] >= 3:
        return "danger"
    if user["consecutive_trades"] >= 4:
        return "risk"
    if news_sentiment in ["negative", "panic"]:
        return "risk"
    return "calm"

def update_trading_behavior(success: bool):
    """
    Updates user emotion tracker.
    """
    now = datetime.now()
    CONFIDENCE_STATE["consecutive_trades"] += 1
    CONFIDENCE_STATE["last_action_time"] = now

    if success:
        CONFIDENCE_STATE["loss_streak"] = 0
        CONFIDENCE_STATE["confidence_level"] = min(CONFIDENCE_STATE["confidence_level"] + 5, 100)
    else:
        CONFIDENCE_STATE["loss_streak"] += 1
        CONFIDENCE_STATE["confidence_level"] = max(CONFIDENCE_STATE["confidence_level"] - 10, 10)

def get_emotion_feedback() -> str:
    """
    Provides a recommendation or warning message based on current state.
    """
    state = CONFIDENCE_STATE
    if state["loss_streak"] >= 3:
        return WARNING_MESSAGES["losing_streak"]
    elif state["consecutive_trades"] >= 5:
        return WARNING_MESSAGES["overtrading"]
    elif state["confidence_level"] < 40:
        return WARNING_MESSAGES["emotion_check"]
    elif state["confidence_level"] > 90:
        return "💪 You're confident. Stay sharp and risk-aware."
    return WARNING_MESSAGES["patience_reminder"]
