from data_fetching_system.data_fetcher import (
    fetch_historical_candles,
    save_to_excel_with_chart,
    plot_monthly_candlesticks
)

def test_three_month_stock_ohlc():
    symbol = "RELIANCE"
    interval = "FIFTEEN_MINUTE"
    days = 90  # Approx. 3 months (AngelOne supports up to 200 for this interval)

    print(f"📦 Running 3-Month OHLC test for {symbol}")
    df = fetch_historical_candles(symbol, interval=interval, days=days)

    if df.empty:
        print("❌ No data returned.")
        return

    print(f"✅ {len(df)} candles fetched for {symbol} at {interval}")
    print(df[["datetime", "open", "high", "low", "close", "ltp_change_%", "volume", "candle_range"]].tail(5))

    # Save Excel report
    save_to_excel_with_chart(df, symbol)

    # Generate charts
    plot_monthly_candlesticks(df, symbol)

if __name__ == "__main__":
    test_three_month_stock_ohlc()
