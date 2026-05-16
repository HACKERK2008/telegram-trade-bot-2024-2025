# strategy/price_forecaster.py

import pandas as pd

def forecast_one_month_target(ohlc_df: pd.DataFrame) -> tuple[float, float]:
    """
    Predicts 1-month future price based on ROC, EMA slope, and trend.
    
    Returns:
        forecast_price (float): Expected price after 1 month
        growth_pct (float): Estimated growth percentage from last close
    """
    if ohlc_df is None or len(ohlc_df) < 40:
        return (0.0, 0.0)

    close = ohlc_df["close"]

    # Calculate rate of change
    roc_10 = ((close.iloc[-1] - close.iloc[-10]) / close.iloc[-10]) * 100
    roc_20 = ((close.iloc[-1] - close.iloc[-20]) / close.iloc[-20]) * 100

    # EMA direction
    ema_9 = close.ewm(span=9).mean()
    ema_21 = close.ewm(span=21).mean()
    ema_slope = ((ema_9.iloc[-1] - ema_21.iloc[-1]) / ema_21.iloc[-1]) * 100

    # Weighted momentum
    momentum_score = (roc_10 * 0.3 + roc_20 * 0.5 + ema_slope * 0.2)
    last_close = close.iloc[-1]
    forecast_price = last_close * (1 + momentum_score / 100)
    growth_pct = (forecast_price - last_close) / last_close * 100

    return forecast_price, growth_pct
