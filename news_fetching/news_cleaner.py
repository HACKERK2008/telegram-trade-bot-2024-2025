from typing import List, Dict

# Financial & trading-relevant keywords
RELEVANT_KEYWORDS = [
    "results", "q1", "q2", "q3", "q4", "profit", "loss", "revenue", "dividend",
    "merger", "acquisition", "stake", "invest", "deal", "block deal",
    "stock", "share", "price", "target", "forecast", "buyback",
    "SEBI", "RBI", "NSE", "BSE", "Moody", "rating", "upgrade", "downgrade"
]

# Banned spam/junk phrases
BANNED_TERMS = [
    "how to", "step-by-step", "personal finance", "loan tips", "bank holiday",
    "ITR", "guide", "retail customers", "NRI", "mutual fund", "tax filing", "credit card"
]

def is_relevant(title: str) -> bool:
    """
    Checks if a news title is relevant for stock traders.
    """
    title_lower = title.lower()

    # Must have at least one financial/trading keyword
    if not any(word in title_lower for word in RELEVANT_KEYWORDS):
        return False

    # Must not contain spammy keywords
    if any(banned in title_lower for banned in BANNED_TERMS):
        return False

    return True


def clean_news_articles(raw_articles: List[Dict], max_return: int = 5) -> List[Dict]:
    """
    Filters a list of articles for trading relevance.
    
    Args:
        raw_articles (List[Dict]): Output list from fetch_newsapi()
        max_return (int): Maximum number of top relevant articles to return

    Returns:
        List[Dict]: Cleaned list with useful headlines only
    """
    cleaned = []

    for article in raw_articles:
        if "text" in article and is_relevant(article["text"]):
            cleaned.append(article)

    return cleaned[:max_return]
