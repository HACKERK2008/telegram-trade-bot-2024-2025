import os
import sys
from news_fetching.news_sources.google_cse_fetcher import fetch_google_cse

if __name__ == "__main__":
    symbol = "SBIN"  # Change to YESBANK, TATAMOTORS, etc.
    results = fetch_google_cse(symbol, max_results=10)

    for item in results:
        if "text" in item:
            print(item["text"])
        elif "message" in item:
            print(f"[❕] {item['message']}")
        elif "error" in item:
            print(f"[❌ ERROR] {item['error']}")
