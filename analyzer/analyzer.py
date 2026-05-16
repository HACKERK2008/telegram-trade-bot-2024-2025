# analyzer/analyzer.py

import os
import sys
import pandas as pd
from analyzer.predictor import predict_trade
from analyzer.alerts import run_alerts
from data_fetching_system.options_chains.margin_calculator import calculate_margin

from analyzer.auto_strategy_generator import generate_strategy_recommendation
from analyzer.strategy_handler import analyze_symbol

from strategy.price_forcaster import forecast_one_month_target
from strategy.news_filter import adjust_confidence_by_news
from strategy.confidence_score import compute_confidence_score

from visualizer.forecast_chart import plot_forecast_overlay


def analyze_stock(input_data: dict) -> dict:
    """
    Universal analyzer for main stock with smart strategy selection,
    margin logic, forecast growth, alerts, and Telegram output.
    """
    ohlc_df = input_data.get("ohlc_df")
    meta = input_data.get("meta", {})
    symbol = meta.get("symbol", "").upper()
    capital = meta.get("capital", None)
    headlines = meta.get("headlines", [])

    if ohlc_df is None or ohlc_df.empty:
        return {"error": "❌ OHLC data not found."}

    if capital is None or not isinstance(capital, (int, float)):
        return {"error": "❌ Capital must be provided as a numeric value in rupees."}

    # 1. Predictive Strategy
    strategy_result = generate_strategy_recommendation(ohlc_df)
    recommended_strategy = strategy_result.get("recommended_strategy")
    strategy_conf = strategy_result.get("confidence_score")

    # 2. ML Prediction
    prediction, confidence = predict_trade(ohlc_df)

    # 3. Alerts & Reasoning
    alerts = run_alerts(symbol, ohlc_df, signals={"strategy": recommended_strategy})
    reasoning = ", ".join(alerts.get("text_flags", [])) or "No major indicator match."

    # 4. Confidence Emoji
    if confidence >= 85:
        emoji, status = "✅🟢", "Very Safe"
    elif 60 <= confidence < 85:
        emoji, status = "⚠️🟡", "Moderate Risk"
    else:
        emoji, status = "❌🔴", "High Risk"

    # 5. Forecast Price
    forecast_price, growth_pct = forecast_one_month_target(ohlc_df)

    # 6. Margin Logic
    entry = ohlc_df.iloc[-1]["close"]
    margin_info = calculate_margin(symbol, entry=entry, capital=capital, trade_type="BUY")

    # 7. Confidence + News boost
    if headlines:
        confidence = adjust_confidence_by_news(confidence, headlines, prediction)

    # 8. Chart
    chart_path = plot_forecast_overlay(ohlc_df, forecast_price, symbol)

    return {
        "symbol": symbol,
        "entry_price": entry,
        "strategy_signal": recommended_strategy,
        "strategy_score": strategy_conf,
        "prediction": prediction,
        "confidence_score": round(confidence, 2),
        "confidence_status": status,
        "confidence_emoji": emoji,
        "alerts": alerts,
        "why": reasoning,
        "margin": margin_info,
        "forecast_price": round(forecast_price, 2),
        "growth_pct": round(growth_pct, 2),
        "capital_used": capital,
        "chart_path": chart_path
    }


def to_telegram_summary(result: dict) -> str:
    """
    Formats analyzer result into a Telegram message block.
    """
    margin = result.get("margin", {})
    return f"""
📊 <b>{result['symbol']} - Main Stock Analyzer</b>

💸 <b>Capital:</b> ₹{int(result['capital_used'])}
🔍 <b>Strategy:</b> {result['strategy_signal']} ({result['strategy_score']}%)  
🤖 <b>Prediction:</b> <code>{result['prediction']}</code>
🔒 <b>Confidence:</b> {result['confidence_score']}% {result['confidence_emoji']} ({result['confidence_status']})

💰 <b>Entry:</b> ₹{result['entry_price']}
🎯 <b>Target:</b> ₹{margin.get('target')}
💣 <b>Stop Loss:</b> ₹{margin.get('stop_loss')}
📉 <b>Breakeven:</b> ₹{margin.get('breakeven_price')}

📈 <b>1M Growth:</b> +{result['growth_pct']}%
🔮 <b>Projected Price:</b> ₹{result['forecast_price']}

💡 <b>Why:</b> {result['why']}
🛡️ <b>Advice:</b> {margin.get('safety_advice')}
""".strip()
