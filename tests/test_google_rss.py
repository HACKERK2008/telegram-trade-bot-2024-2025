import sys
import os

# Add parent folder (your root tradebot/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from news_fetching.news_sources.google_rss import fetch_google_rss

news = fetch_google_rss("TATA MOTORS")
for i, article in enumerate(news, 1):
    print(f"\n{i}. 📰 {article['title']} \n   🏷️ Source: {article['source']}")
