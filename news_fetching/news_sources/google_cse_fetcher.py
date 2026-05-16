# ✅ Finalized google_cse_fetcher.py with enhanced output formatting, summaries, and impact hints
import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
from datetime import datetime

# Load API key and CSE ID from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX", "02716bee25855404d")

# Headline tag definitions
TAG_KEYWORDS = {
    "[EARNINGS]": ["q1", "q2", "q3", "q4", "results", "profit", "loss", "revenue"],
    "[MERGER]": ["merger", "acquisition", "stake", "buyout", "deal"],
    "[FRAUD]": ["fraud", "scam", "raid", "sebi", "ed", "penalty"],
    "[ANALYST]": ["upgrade", "downgrade", "rating", "target", "buy", "sell"],
    "[GLOBAL]": ["fed", "us market", "china", "oil", "inflation"],
    "[SECTOR]": ["auto", "bank", "tech", "it", "pharma"]
}

# Filters for headline cleaning
RELEVANT_KEYWORDS = [
    "results", "q1", "profit", "loss", "merger", "acquisition", "stock",
    "price", "target", "rbi", "sebi", "invest", "dividend"
]
BANNED_TERMS = [
    "how to", "step-by-step", "loan", "itr", "guide", "holiday",
    "nri", "credit card", "mutual fund"
]

def tag_article(title: str) -> List[str]:
    title_lower = title.lower()
    return [tag for tag, kws in TAG_KEYWORDS.items() if any(k in title_lower for k in kws)] or ["[GENERAL]"]

def is_relevant(title: str) -> bool:
    title_lower = title.lower()
    return any(k in title_lower for k in RELEVANT_KEYWORDS) and not any(b in title_lower for b in BANNED_TERMS)

def guess_impact(tags: List[str]) -> str:
    if "[EARNINGS]" in tags or "[ANALYST]" in tags:
        return "📉 Possible bearish move" if any(x in tags for x in ["[EARNINGS]", "[FRAUD]"]) else "📈 Possible bullish move"
    elif "[MERGER]" in tags:
        return "📈 Strategic development likely"
    elif "[FRAUD]" in tags:
        return "🚨 Regulatory or reputational risk"
    else:
        return "⚠️ Neutral or mixed sentiment"

def summarize_title(title: str) -> str:
    title = title.strip()
    if len(title) > 110:
        return title[:107] + "..."
    return title

def fetch_google_cse(symbol: str, max_results: int = 5) -> List[Dict]:
    """
    Fetches relevant company news using Google Custom Search (CSE).
    Applies filtering and tagging to return cleaned, Telegram-ready output.
    """
    if not GOOGLE_API_KEY or not GOOGLE_CX:
        return [{"error": "Missing GOOGLE_API_KEY or GOOGLE_CX in .env file"}]

    query = f"{symbol} stock news"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": max_results,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()

        items = results.get("items", [])
        if not items:
            return [{"message": f"No news found for {symbol}."}]

        news = []
        for item in items:
            title = item.get("title", "")
            if not is_relevant(title):
                continue

            clean_title = summarize_title(title)
            tags = tag_article(clean_title)
            impact = guess_impact(tags)

            news.append({
                "text": (
                    f"\n📰 *{clean_title}*\n"
                    f"📍 Summary: Based on headline, this news may reflect important financial movement.\n"
                    f"🏷️ Tags: {' '.join(tags)}\n"
                    f"📊 Impact: {impact}\n"
                    f"📚 Source: {item.get('displayLink', 'Unknown')}\n"
                    f"⏰ Published: {datetime.utcnow().strftime('%Y-%m-%d')}\n"
                    f"🔗 [Read Full Article]({item.get('link')})"
                )
            })

        return news or [{"message": f"No relevant news found for {symbol}."}]

    except Exception as e:
        return [{"error": str(e)}]
