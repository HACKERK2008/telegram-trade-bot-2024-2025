# strategy/growth_screener.py

from data_fetching_system.data_fetcher import get_ohlc
from strategy.price_forecaster import forecast_one_month_target
import pandas as pd

def run_growth_forecast_screener(symbols: list[str], days: int = 30) -> pd.DataFrame:
    results = []

    for sym in symbols:
        try:
            df = get_ohlc(sym, interval="1day", days=days)
            price, pct = forecast_one_month_target(df)
            last = df.iloc[-1]["close"]
            results.append({
                "Symbol": sym,
                "Last Close": round(last, 2),
                "Forecast": round(price, 2),
                "Growth %": round(pct, 2)
            })
        except Exception as e:
            continue

    return pd.DataFrame(results).sort_values(by="Growth %", ascending=False).reset_index(drop=True)
