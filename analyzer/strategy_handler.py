# analyzer/strategy_handler.py

from data_fetching_system.data_fetcher import fetch_historical_candles
from analyzer.news_trend_tracker import fetch_recent_news
from strategy.trend_following import generate_trend_signal
from strategy.strategy_utils import find_nearest_strike
from visualizer.chart_generator import plot_main_price_candlestick

def analyze_symbol(symbol: str, interval="FIVE_MINUTE", days=90) -> dict:
    """
    Main strategy runner — fetches data, analyzes trend, combines with news (optional).

    Returns:
        dict with analysis summary
    """
    print(f"🧠 Running strategy analysis for {symbol}...")

    # 1. Fetch historical price data
    df = fetch_historical_data(symbol, interval, days)
    last_price = df["close"].iloc[-1]
    chart_path = plot_main_price_candlestick(df, symbol)

    # 2. Run strategy
    trend = generate_trend_signal(df)
    direction = "CALL" if trend == "up" else "PUT"
    strike = find_nearest_strike(last_price)

    # 3. Fetch recent news (optional)
    news = fetch_recent_news(symbol)
    news_headlines = [n["title"] for n in news]

    return {
        "symbol": symbol.upper(),
        "last_price": round(last_price, 2),
        "direction": direction,
        "strike": strike,
        "trend": trend,
        "chart": chart_path,
        "news": news_headlines[:3]  # Top 3 headlines
    }
