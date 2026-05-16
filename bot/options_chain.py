# file: analyzer/option_chain.py

import os
from datetime import datetime
from data_fetching_system.data_fetcher import (
    fetch_historical_candles,
    save_to_excel_with_chart,
    plot_monthly_candlesticks
)
from analyzer import analyzer
from fpdf import FPDF

# === Main Controller ===
def process_option_chain(symbol: str, segment: str, interval: str, days: int, analyze: bool = True, mode="historical") -> dict:
    try:
        if segment == "main":
            if mode == "historical":
                return handle_main_historical(symbol, interval, days, analyze)
            elif mode == "live":
                return handle_main_live(symbol)
            else:
                return {"error": "❌ Invalid mode for main segment."}

        elif segment == "option":
            if mode == "historical":
                return handle_option_historical(symbol, interval, days)
            elif mode == "live":
                return handle_option_live(symbol)
            else:
                return {"error": "❌ Invalid mode for option segment."}

        return {"error": "❌ Unknown segment."}

    except Exception as e:
        return {"error": f"❌ Exception: {e}"}

# === Main Historical Handler ===
def handle_main_historical(symbol: str, interval: str, days: int, analyze: bool) -> dict:
    df = fetch_historical_candles(symbol, interval=interval, days=days)
    if df.empty:
        return {"error": "⚠️ No historical data returned."}

    plot_monthly_candlesticks(df, symbol)
    save_to_excel_with_chart(df, symbol)

    result = {
        "summary": f"✅ {symbol} | Interval: {interval} | Days: {days} | Candles: {len(df)}",
        "chart_path": f"chart/{symbol.upper()}-{datetime.now().strftime('%Y-%m')}.png",
        "excel_path": f"chart/{symbol.upper()}_OHLC_REPORT.xlsx"
    }

    if analyze:
        prediction = run_analysis(df)
        result.update({
            "prediction": prediction.get("message"),
            "direction": prediction.get("signal")
        })

    pdf_path = generate_summary_pdf(symbol, result)
    result["pdf_path"] = pdf_path

    return result

# === PDF Export
def generate_summary_pdf(symbol: str, result: dict) -> str:
    os.makedirs("chart", exist_ok=True)
    filename = f"chart/{symbol}_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"📊 TradeBot Analysis for {symbol}", ln=True)
    pdf.ln(5)

    for key in ["summary", "prediction", "direction"]:
        val = result.get(key)
        if val:
            pdf.cell(0, 8, f"{key.capitalize()}: {val}", ln=True)

    pdf.output(filename)
    return filename

# === Stubs
def handle_main_live(symbol: str) -> dict:
    return {"summary": f"⚡ Live mode coming soon for {symbol}."}

def handle_option_historical(symbol: str, interval: str, days: int) -> dict:
    return {"summary": f"📉 Option historical not yet supported."}

def handle_option_live(symbol: str) -> dict:
    return {"summary": f"⚡ Option chain live view under development."}
