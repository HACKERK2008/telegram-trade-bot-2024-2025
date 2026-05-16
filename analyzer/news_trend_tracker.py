# analyzer/news_trend_tracker.py

import os
import sys
import requests
from datetime import datetime
from analyzer.symbol_lookup import resolve_symbol
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_recent_news(symbol: str, max_articles: int = 8) -> list[dict]:
    """
    Fetches top recent news for a given stock symbol using NewsAPI.

    Returns:
        List of dicts with title, url, published time.
    """
    info = resolve_symbol(symbol)
    if not info:
        raise ValueError(f"❌ Could not resolve symbol: {symbol}")
    
    query = info["symbol"]
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY
    }

    try:
        print(f"📰 Fetching news for {query}")
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        articles = []
        for article in data.get("articles", [])[:max_articles]:
            articles.append({
                "title": article["title"],
                "url": article["url"],
                "published": parse_time(article["publishedAt"])
            })

        print(f"✅ Retrieved {len(articles)} articles for {symbol}")
        return articles

    except Exception as e:
        print(f"❌ News API error: {e}")
        return []

def parse_time(iso_string):
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y %H:%M")
    except:
        return iso_string
