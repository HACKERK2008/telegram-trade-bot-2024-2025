# analyzer/mocktest_analyzer.py

import pandas as pd
import numpy as np
from analyzer.analyzer import (
    process_features,
    run_strategies,
    get_stop_loss_zone,
    run_alerts,
    run_prediction
)
from strategy.volatility import generate_volatility_signal
from strategy.price_action import detect_price_action
from strategy.volume_based import detect_volume_signal
from strategy.parameter_tuning import sample_hyperparam_config
from strategy.strategy_utils import find_nearest_strike
from visualizer.chart_generator import (
    plot_main_price_candlestick,
    plot_option_chain_text_as_image
)

def generate_dummy_df(n=120):
    np.random.seed(42)
    price = np.cumsum(np.random.normal(0, 2, n)) + 100
    df = pd.DataFrame({
        "open": price + np.random.randn(n),
        "high": price + np.random.rand(n) * 2,
        "low": price - np.random.rand(n) * 2,
        "close": price + np.random.randn(n) * 0.5,
        "volume": np.random.randint(1000, 5000, size=n),
        "open_interest": np.random.randint(50000, 100000, size=n)
    }, index=pd.date_range(end=pd.Timestamp.today(), periods=n, freq="5min"))
    return df

def get_fake_option_chain_text():
    header = (
        "📘 FAKE_NIFTY\n"
        "🏛 NSE    💹 25,112.40   📈 +319.15 (+1.29%)\n"
        "🗓 Expiry: 26 Jun 2025 | 📍ATM: 25100\n"
        "───────────────────────────────────────────────────────\n"
        "   CALLS 📞                                  PUTS 📕\n"
        " Vol | ΔOI(%) |   OI   | LTP(Δ%)   STRIKE   LTP(Δ%) |   OI   | ΔOI(%) | Vol\n"
        "───────────────────────────────────────────────────────"
    )
    rows = [
        " 417K |   3.40% |   703K | ₹1199.98↑   24600.0   ₹15.11↓ |   978K |   1.68% |  173K",
        " 367K |   1.32% |    63K | ₹1165.92↑   24650.0   ₹ 85.4↓ |   903K |   0.04% |    5K",
        " 486K |   0.86% |  1168K | ₹1227.51↑   24700.0   ₹ 9.59↓ |   690K |   4.51% |  184K",
        " 362K |  -1.63% |   399K | ₹ 89.93↑   24750.0   ₹24.41↓ |  1016K |   4.88% |  420K",
        " 442K |   3.72% |   670K | ₹544.93↑   24800.0   ₹ 84.8↓ |   366K |   2.08% |  341K"
    ]
    return header + "\n" + "\n".join(rows)

def run_mock_test():
    symbol = "MOCK_STOCK"
    print(f"📦 Running Full Analyzer Mock Test on {symbol}")

    df = generate_dummy_df()
    df = process_features(df)

    print("\n📊 Strategy Signals:")
    signals = run_strategies(df)
    print(signals)

    print("\n📈 Extra Strategy Tests:")
    print(f"📊 Volatility Signal: {generate_volatility_signal(df)}")
    print(f"📊 Price Action: {detect_price_action(df)}")
    print(f"📊 Volume Signal: {detect_volume_signal(df)}")
    print(f"🎯 Suggested Strike: {find_nearest_strike(df['close'].iloc[-1])}")
    print(f"⚙️ Sample Tuning Config: {sample_hyperparam_config()}")

    print("\n🛡️ Stop Loss Calculation:")
    stop_loss, near_sl, entry = get_stop_loss_zone(df)
    print(f"💰 Entry: ₹{entry:.2f}, SL: ₹{stop_loss:.2f}, Near SL: {near_sl}")

    print("\n📊 Option Chain Snapshot:")
    option_chain_text = get_fake_option_chain_text()
    print(option_chain_text)

    print("\n🚨 Alerts Running:")
    alerts = run_alerts(symbol, df, signals, near_sl, entry)
    print(f"⚠️ Alerts: {alerts['any_alert']} | Score: {alerts['alert_score']}")
    for flag in alerts["text_flags"]:
        print(f"➡️ {flag}")

    print("\n🔮 ML Prediction:")
    try:
        signal, confidence, acc = run_prediction(df)
        print(f"📈 Prediction: {signal} @ {confidence}% confidence (Acc: {acc}%)")
    except ValueError as ve:
        print(str(ve))

    print("\n🖼️ Generating Charts:")
    price_chart = plot_main_price_candlestick(df, symbol)
    option_chart = plot_option_chain_text_as_image(option_chain_text, symbol)

    if price_chart:
        print(f"📈 Price Chart Path: {price_chart}")
    if option_chart:
        print(f"📊 Option Chain Chart Path: {option_chart}")

    print("\n✅ Full Mock Test Completed.")

if __name__ == "__main__":
    run_mock_test()
