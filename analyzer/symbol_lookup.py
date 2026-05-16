# file: analyzer/symbol_lookup.py

import os
import csv

CSV_PATH = os.path.join(os.path.dirname(__file__), "../nse_bse_stock_tokens.csv")
DEBUG = False  # ⬅️ Set to True if you want debug prints

def load_instruments():
    """Load instruments from CSV quietly, or with debug output if enabled."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    instruments = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if DEBUG:
            print("🧾 Detected columns:", reader.fieldnames)

        for i, row in enumerate(reader):
            instruments.append(row)
            if DEBUG and i < 5:
                print("🔍 ROW:", row)

    if DEBUG:
        print(f"📦 Total raw records loaded: {len(instruments)}")

    return instruments

def resolve_symbol(user_input: str) -> dict:
    symbol = user_input.strip().upper()
    instruments = load_instruments()

    for row in instruments:
        raw_symbol = row["symbol"].strip().upper()
        raw_name = row["name"].strip().upper()

        if symbol in (raw_symbol, raw_name, raw_symbol.replace("-EQ", ""), raw_name.replace("-EQ", "")):
            return {
                "symbol": row["symbol"],
                "exchange": "NSE",  # Always NSE for now
                "token": row["token"]
            }

    raise ValueError(f"❌ Could not resolve symbol: {symbol}")
