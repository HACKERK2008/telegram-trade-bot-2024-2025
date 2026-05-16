# visualizer/forecast_chart.py

import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_forecast_overlay(ohlc_df: pd.DataFrame, forecast_price: float, symbol: str) -> str:
    """
    Plots price chart with forecast target as a line.

    Returns path to saved image.
    """
    close = ohlc_df["close"]
    dates = pd.to_datetime(ohlc_df["date"])

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close, label="Actual Close", color="blue")
    plt.axhline(y=forecast_price, color="green", linestyle="--", label=f"1M Forecast: ₹{forecast_price:.2f}")
    plt.title(f"{symbol} – Price vs Forecast")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)

    os.makedirs("chart", exist_ok=True)
    path = f"chart/{symbol}_forecast_overlay.png"
    plt.savefig(path)
    plt.close()
    return path
