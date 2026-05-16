import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from fpdf import FPDF

load_dotenv()

# === File Paths
DIR = os.path.dirname(__file__)
EQ_PATH = os.path.join(DIR, "main_stock_contracts.csv")
FNO_PATH = os.path.join(DIR, "symbol_contracts.csv")

# === AngelOne Headers
HEADERS = {
    "Authorization": f"Bearer {os.getenv('ANGLE_FEED_TOKEN')}",
    "X-ClientLocalIP": os.getenv("LOCAL_IP"),
    "X-ClientPublicIP": os.getenv("PUBLIC_IP"),
    "X-MACAddress": os.getenv("MAC_ADDRESS"),
    "X-PrivateKey": os.getenv("ANGEL_API_KEY"),
    "X-SourceID": "WEB",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
MARGIN_URL = "https://apiconnect.angelone.in/rest/secure/angelbroking/margin/v1/batch"

# === Load symbol contract
def load_contract(symbol):
    symbol = symbol.upper()
    if os.path.exists(FNO_PATH):
        df = pd.read_csv(FNO_PATH)
        row = df[df["symbol"] == symbol]
        if not row.empty:
            return {
                "symbol": symbol,
                "exchange": row.iloc[0]["exchange"],
                "token": row.iloc[0]["token"],
                "lot_size": int(row.iloc[0]["lot_size"]),
                "type": "FNO"
            }
    if os.path.exists(EQ_PATH):
        df = pd.read_csv(EQ_PATH)
        row = df[df["symbol"] == symbol]
        if not row.empty:
            return {
                "symbol": symbol,
                "exchange": row.iloc[0]["exchange"],
                "token": row.iloc[0]["token"],
                "lot_size": 1,
                "type": "EQ"
            }
    raise Exception(f"❌ Symbol '{symbol}' not found in contract lists.")

# === SL/TP Estimator
def estimate_sl_tp(entry, trade_type, inst_type):
    if inst_type == "FNO":
        sl = entry * 0.7 if trade_type == "BUY" else entry * 1.3
        tp = entry * 1.6 if trade_type == "BUY" else entry * 0.4
    else:
        sl = entry * 0.98
        tp = entry * 1.04
    return round(sl, 2), round(tp, 2)

# === Risk Analysis
def calculate_metrics(entry, exit, sl, tp, qty, margin, capital, trade_type):
    direction = 1 if trade_type == "BUY" else -1
    pnl = round((exit - entry) * qty * direction, 2)
    sl_loss = round((sl - entry) * qty * direction, 2)
    tp_gain = round((tp - entry) * qty * direction, 2)
    risk = abs(sl_loss)
    reward = abs(tp_gain)
    rr_ratio = round(reward / risk, 2) if risk else None
    gain_pct = round((tp_gain / margin) * 100, 2)
    risk_pct = round((risk / capital) * 100, 2)
    score = min(max(100 - risk_pct, 10), 100) if rr_ratio and rr_ratio > 1 else 40
    advice = "✅ Safe Trade" if score > 75 else ("⚠️ Medium Risk" if score > 50 else "❌ Avoid")
    return pnl, sl_loss, tp_gain, rr_ratio, gain_pct, risk_pct, score, advice

# === Tax & Brokerage
def estimate_taxes_and_net(pnl, entry, exit, qty, inst_type, trade_type):
    turnover = (entry + exit) * qty
    buy_turn = entry * qty
    sell_turn = exit * qty
    brokerage = 20
    stt_rate = 0.001 if inst_type == "EQ" else 0.0005
    stt = round(sell_turn * stt_rate, 2)
    exchange = round(turnover * 0.0000325, 2)
    sebi = round(turnover * 0.000001, 2)
    gst = round((brokerage * 2) * 0.18, 2)
    stamp = round(buy_turn * (0.00015 if inst_type == "EQ" else 0.00003), 2)
    total = brokerage * 2 + stt + exchange + sebi + gst + stamp
    net = round(pnl - total, 2)
    return {
        "gross_pnl": pnl,
        "total_charges": round(total, 2),
        "net_pnl": net,
        "net_after_sell": round(exit * qty - total, 2)
    }

# === PDF Export
def generate_pdf(data):
    filename = f"trade_summary_{data['symbol']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(DIR, filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.cell(0, 10, "🔎 Trade Summary Report", ln=True)
    pdf.cell(0, 8, f"Symbol: {data['symbol']} | Type: {data['type']}", ln=True)
    pdf.cell(0, 8, f"Qty: {data['qty']} | Entry: {data['entry']} | Exit: {data['exit']}", ln=True)
    pdf.cell(0, 8, f"Stop Loss: {data['stop_loss']} | Target: {data['target']}", ln=True)
    pdf.cell(0, 8, f"Margin Required: ₹{data['margin_required']} | Capital: ₹{data['capital']}", ln=True)
    pdf.cell(0, 8, f"Capital Sufficient: {'Yes' if data['capital_sufficient'] else 'No'}", ln=True)
    pdf.cell(0, 8, f"P&L Estimate: ₹{data['pnl_estimate']}", ln=True)
    pdf.cell(0, 8, f"RR Ratio: {data['rr_ratio']} | Confidence: {data['confidence_score']}%", ln=True)
    pdf.cell(0, 8, f"Advice: {data['safety_advice']}", ln=True)
    pdf.cell(0, 8, f"---", ln=True)
    pdf.cell(0, 8, f"Gross P&L: ₹{data['gross_pnl']}", ln=True)
    pdf.cell(0, 8, f"Total Charges: ₹{data['total_charges']}", ln=True)
    pdf.cell(0, 8, f"Net P&L: ₹{data['net_pnl']}", ln=True)
    pdf.cell(0, 8, f"Net Amount After Sell: ₹{data['net_after_sell']}", ln=True)
    pdf.output(filepath)
    print(f"📄 PDF saved to: {filepath}")

# === Main Function
def calculate_margin(symbol, entry, capital, exit=None, trade_type="BUY", product_type="INTRADAY", generate_report=True):
    contract = load_contract(symbol)
    lotsize = contract["lot_size"]
    qty = lotsize if contract["type"] == "FNO" else int(capital // entry)
    if qty <= 0:
        raise Exception("❌ Not enough capital for even 1 unit.")

    sl, tp = estimate_sl_tp(entry, trade_type, contract["type"])
    exit_price = exit or tp

    pos = [{
        "exchange": contract["exchange"],
        "qty": qty,
        "price": float(entry),
        "productType": product_type,
        "orderType": "MARKET",
        "token": contract["token"],
        "tradeType": trade_type
    }]

    res = requests.post(MARGIN_URL, json={"positions": pos}, headers=HEADERS)
    res.raise_for_status()
    data = res.json()
    if not data.get("status"):
        raise Exception(data.get("message"))

    margin = round(data["data"]["totalMarginRequired"], 2)
    pnl, sl_loss, tp_gain, rr, g_pct, r_pct, score, advice = calculate_metrics(entry, exit_price, sl, tp, qty, margin, capital, trade_type)
    tax = estimate_taxes_and_net(pnl, entry, exit_price, qty, contract["type"], trade_type)

    result = {
        **contract,
        "qty": qty,
        "entry": entry,
        "exit": exit_price,
        "stop_loss": sl,
        "target": tp,
        "margin_required": margin,
        "capital": capital,
        "capital_sufficient": capital >= margin,
        "pnl_estimate": pnl,
        "rr_ratio": rr,
        "confidence_score": score,
        "safety_advice": advice,
        **tax
    }

    if generate_report:
        generate_pdf(result)

    return result

