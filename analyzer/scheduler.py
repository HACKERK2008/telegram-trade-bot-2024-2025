# analyzer/scheduler.py

import time
import traceback
from datetime import datetime, timedelta

from analyzer.analyzer import analyze_symbol
from analyzer.alerts import detect_alerts
from analyzer.news_trend_tracker import get_news_sentiment
from analyzer.sentiment import get_emotion_feedback
from database.watchlist import get_user_watchlist

ANALYSIS_INTERVAL = 15 * 60  # every 15 mins
SENTIMENT_INTERVAL = 60 * 60  # every 1 hour

USER_ID = "user_001"  # later pulled from Telegram

next_sentiment_check = datetime.now()

def scheduled_job():
    print(f"\n⏰ Job Triggered @ {datetime.now().strftime('%H:%M:%S')}")
    symbols = get_user_watchlist(USER_ID)
    if not symbols:
        print("⚠️ No symbols in watchlist. Skipping...")
        return

    for symbol in symbols:
        try:
            print(f"\n🔍 Analyzing {symbol}")
            result = analyze_symbol(symbol)
            alerts = detect_alerts(symbol, result.get("data", {}))
            sentiment = get_news_sentiment(symbol)

            print(f"📢 {symbol} → {result['decision']['action']} @ {result['decision']['confidence']}%")
            if alerts["any_alert"]:
                print(f"⚠️ Alerts: {alerts}")
            print(f"📰 News Sentiment: {sentiment}")
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            traceback.print_exc()

def run_sentiment_check():
    print(f"\n🧠 Sentiment Check @ {datetime.now().strftime('%H:%M:%S')}")
    msg = get_emotion_feedback()
    print(f"💬 Bot Emotional Advice → {msg}")

def start_scheduler():
    global next_sentiment_check
    print("🚀 Scheduler started. Press Ctrl+C to stop.")

    while True:
        try:
            now = datetime.now()
            if now.hour >= 15:
                print("🛑 Market time over. Scheduler stopping.")
                break

            scheduled_job()

            if now >= next_sentiment_check:
                run_sentiment_check()
                next_sentiment_check = now + timedelta(hours=1)

            time.sleep(ANALYSIS_INTERVAL)

        except KeyboardInterrupt:
            print("🛑 Scheduler manually stopped.")
            break
        except Exception as e:
            print(f"⛔ Unhandled error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    start_scheduler()
