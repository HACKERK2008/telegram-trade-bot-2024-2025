def format_human_friendly(symbol_str: str) -> str:
    """
    Converts human-friendly input like:
        "NIFTY 03 JUL 2025 CE 25200"
    Into AngelOne-compatible:
        "NIFTY03JUL2525200CE"
    
    Supports:
        - CE/PE detection
        - Case/space tolerance
    """
    try:
        parts = symbol_str.strip().upper().split()
        if len(parts) < 6:
            raise ValueError("❌ Expected format: SYMBOL DD MMM YYYY CE/PE STRIKE")

        symbol, day, month, year, opt_type, strike = parts[:6]

        if len(year) == 4:
            year = year[-2:]  # convert 2025 → 25

        code = f"{symbol}{day}{month}{year}{int(strike)}{opt_type}"
        return code
    except Exception as e:
        raise ValueError(f"❌ Could not parse input: {symbol_str}\nReason: {e}")

# 🔬 Test runner
if __name__ == "__main__":
    inputs = [
        "NIFTY 03 JUL 2025 CE 25200",
        "banknifty 04 jul 2025 pe 49500",
        "RELIANCE 18 JUL 2025 ce 2700"
    ]

    for s in inputs:
        try:
            print(f"✅ {s} → {format_human_friendly(s)}")
        except Exception as e:
            print(f"❌ {s} → {e}")
