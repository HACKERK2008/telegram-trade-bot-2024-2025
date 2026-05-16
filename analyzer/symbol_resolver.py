import os
import requests
import csv
from dotenv import load_dotenv

load_dotenv()

# Environment variables
AUTH_TOKEN = os.getenv("ANGELONE_AUTH_TOKEN")
API_KEY = os.getenv("ANGEL_API_KEY")
LOCAL_IP = os.getenv("LOCAL_IP")
PUBLIC_IP = os.getenv("PUBLIC_IP")
MAC_ADDRESS = os.getenv("MAC_ADDRESS")

HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "X-ClientLocalIP": LOCAL_IP,
    "X-ClientPublicIP": PUBLIC_IP,
    "X-MACAddress": MAC_ADDRESS,
    "X-PrivateKey": API_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

SEARCH_URL = "https://apiconnect.angelone.in/rest/secure/angelbroking/order/v1/searchScrip"

# 📁 Load fallback CSV (tokens)
FALLBACK_TOKENS = {}
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'nse_bse_stock_tokens.csv')

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row['symbol'].strip().upper()
            token = row['token'].strip()
            exchange = row.get('exchange', 'NFO').strip() if row.get('exchange') else 'NFO'
            lot_size = int(row.get("lotsize", 50)) if row.get("lotsize") else 50
            FALLBACK_TOKENS[symbol] = {
                "symbol": symbol,
                "exchange": exchange,
                "symboltoken": token,
                "lot_size": lot_size
            }

def resolve_option_symbol(symbol: str) -> dict:
    """
    Resolves an option/future tradingsymbol (e.g. NIFTY03JUL2525200CE) to its token and exchange.
    First tries AngelOne search API, falls back to local CSV.
    """
    expiry_prefix = symbol[:12].upper()

    try:
        response = requests.post(SEARCH_URL, headers=HEADERS, json={
            "exchange": "NFO",
            "searchscrip": expiry_prefix
        })
        response.raise_for_status()
        results = response.json().get("data", [])
        matches = [item for item in results if item["tradingsymbol"].upper() == symbol.upper()]
        if matches:
            item = matches[0]
            return {
                "symbol": item["tradingsymbol"],
                "exchange": item["exchange"],
                "symboltoken": item["symboltoken"],
                "lot_size": int(item.get("lotsize", 50))
            }
    except Exception as e:
        print(f"⚠️ AngelOne API failed: {e}")

    # Fallback logic
    fallback_key = symbol.upper()
    if fallback_key in FALLBACK_TOKENS:
        return FALLBACK_TOKENS[fallback_key]

    raise ValueError(f"❌ No matching symbol for {symbol}. CSV has: {list(FALLBACK_TOKENS.keys())[:5]}...")


