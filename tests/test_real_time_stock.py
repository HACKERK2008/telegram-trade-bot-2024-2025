# file: tests/test_real_time_stock.py

from data_fetching_system.real_time_stock import (
    fetch_live_ohlc,
    fetch_live_ltp_full,
    build_stock_summary
)

def test_ohlc(symbol: str):
    print(f"\n📊 Testing fetch_live_ohlc('{symbol}')...")
    df = fetch_live_ohlc(symbol)
    if df.empty:
        print("❌ Failed to fetch OHLC data.")
    else:
        summary = build_stock_summary(df, symbol)
        print("✅ OHLC Summary:", summary)

def test_ltp(symbol: str):
    print(f"\n📡 Testing fetch_live_ltp_full('{symbol}')...")
    data = fetch_live_ltp_full(symbol)
    if data:
        print("✅ LTP Data:", data)
    else:
        print("❌ Failed to fetch LTP data.")

if __name__ == "__main__":
    symbol = "RELIANCE"
    test_ohlc(symbol)
    test_ltp(symbol)
