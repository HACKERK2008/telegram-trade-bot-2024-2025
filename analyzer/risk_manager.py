# analyzer/risk_manager.py

import pandas as pd
import numpy as np
from analyzer.technicals import calculate_atr

def calculate_position_size(
    capital: float,
    entry_price: float,
    stop_loss_price: float,
    risk_per_trade_pct: float = 1.0
) -> int:
    """
    Calculates position size based on max loss allowed and SL distance.
    """
    risk_amount = capital * (risk_per_trade_pct / 100)
    stop_loss_per_unit = abs(entry_price - stop_loss_price)
    if stop_loss_per_unit == 0:
        return 0
    quantity = int(risk_amount / stop_loss_per_unit)
    return quantity

def recommend_stop_loss(
    df: pd.DataFrame,
    method: str = "ATR",  # or "percent"
    entry_price: float = None,
    atr_mult: float = 1.5,
    percent: float = 2.0
) -> float:
    """
    Suggest a stop-loss price using ATR or fixed percentage.
    """
    if method.upper() == "ATR":
        atr = calculate_atr(df).iloc[-1]
        return round(entry_price - atr * atr_mult, 2)
    elif method.upper() == "PERCENT":
        return round(entry_price * (1 - percent / 100), 2)
    return entry_price

def recommend_target(
    entry_price: float,
    stop_loss_price: float,
    rr_ratio: float = 2.0
) -> float:
    """
    Recommend target price based on Risk:Reward ratio.
    """
    sl_per_unit = abs(entry_price - stop_loss_price)
    return round(entry_price + rr_ratio * sl_per_unit, 2)

def risk_summary(
    capital: float,
    entry: float,
    sl: float,
    rr: float = 2.0,
    risk_pct: float = 1.0
) -> dict:
    qty = calculate_position_size(capital, entry, sl, risk_pct)
    target = recommend_target(entry, sl, rr)
    risk_amt = abs(entry - sl) * qty
    reward_amt = abs(target - entry) * qty
    return {
        "entry": entry,
        "stop_loss": sl,
        "target": target,
        "quantity": qty,
        "risk_amount": round(risk_amt, 2),
        "reward_amount": round(reward_amt, 2),
        "r_r_ratio": rr
    }
