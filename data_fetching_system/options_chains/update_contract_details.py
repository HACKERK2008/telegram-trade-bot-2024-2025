import requests
import pandas as pd
import os
from datetime import datetime

MASTER_URL = "https://margincalculator.angelone.in/OpenAPI_File/files/OpenAPIScripMaster.json"
FILENAME = "symbol_contracts.csv"
SAVE_PATH = os.path.join(os.path.dirname(__file__), FILENAME)

def is_thursday() -> bool:
    return datetime.today().weekday() == 4  # Monday=0 ... Friday=3

def fetch_and_save_fno_contracts():
    print("📡 Fetching AngelOne instrument master...")
    res = requests.get(MASTER_URL)
    res.raise_for_status()
    data = res.json()

    allowed_types = {"FUTSTK", "FUTIDX", "OPTSTK", "OPTIDX"}
    fno = [
        {
            "symbol": row["symbol"].strip().upper(),
            "exchange": row["exch_seg"].upper(),
            "token": row["token"],
            "lot_size": int(row.get("lotsize", 0)),
            "instrument_type": row["instrumenttype"].upper()
        }
        for row in data
        if row.get("exch_seg", "").upper() in ("NFO", "BFO")
        and row.get("instrumenttype", "").upper() in allowed_types
    ]

    df = pd.DataFrame(fno).drop_duplicates(subset=["symbol", "exchange", "instrument_type"])
    
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)
        print(f"🧹 Deleted old file: {FILENAME}")

    df.to_csv(SAVE_PATH, index=False)
    print(f"✅ Updated: {FILENAME} with {len(df)} contracts")

def update_if_thursday():
    if is_thursday():
        print("📆 Today is Friday — updating contracts.")
        fetch_and_save_fno_contracts()
    else:
        print("⏳ Not Friday — skipping update. Current data will be reused.")

if __name__ == "__main__":
    update_if_thursday()
