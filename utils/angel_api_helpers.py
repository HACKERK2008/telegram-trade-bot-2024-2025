# utils/angel_api_helpers.py

import os
import json
import requests
import pyotp
from dotenv import load_dotenv
from SmartApi.smartConnect import SmartConnect

load_dotenv()

ANGEL_API_KEY = os.getenv("ANGEL_API_KEY")
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
MPIN = os.getenv("ANGEL_MPIN")
TOTP_SECRET = os.getenv("TOTP_SECRET")
LOCAL_IP = os.getenv("LOCAL_IP", "127.0.0.1")
PUBLIC_IP = os.getenv("PUBLIC_IP", "127.0.0.1")
MAC_ADDRESS = os.getenv("MAC_ADDRESS", "00:00:00:00:00:00")
FEED_TOKEN = os.getenv("FEED_TOKEN")

BASE_URL = "https://apiconnect.angelone.in/rest/secure/angelbroking"

def get_headers(feed_token=None, api_key=None):
    return {
        "X-PrivateKey": api_key or ANGEL_API_KEY,
        "X-SourceID": "WEB",
        "X-ClientLocalIP": LOCAL_IP,
        "X-ClientPublicIP": PUBLIC_IP,
        "X-MACAddress": MAC_ADDRESS,
        "X-UserType": "USER",
        "Authorization": f"Bearer {feed_token or FEED_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

def refresh_feed_token():
    sc = SmartConnect(api_key=ANGEL_API_KEY)
    # Generate current 6-digit TOTP code
    current_totp_code = pyotp.TOTP(TOTP_SECRET).now()
    
    print(f"Current TOTP Code: {current_totp_code}")  # For debugging
    
    data = sc.generateSession(CLIENT_CODE, MPIN, current_totp_code)
    
    if not data or not data.get("status"):
        print(f"Failed to generate session: {data}")
        return None
    
    token = data["data"]["feedToken"]
    print(f"New FEED_TOKEN: {token}")
    return token

def get_scrip_master():
    """
    Fetch the complete scrip master data.
    Caches locally to a JSON file for repeated use.
    """
    import os
    cache_file = "scrip_master_cache.json"

    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            print("Loading scrip master from cache")
            return json.load(f)

    url = f"{BASE_URL}/historical/v1/getScripMaster"
    try:
        response = requests.get(url, headers=HEADERS_BASE, timeout=20)
        print(f"Raw response status: {response.status_code}")
        print(f"Raw response text: {response.text[:500]}")  # Print first 500 chars

        response.raise_for_status()
        res = response.json()
        if res.get("status") and "data" in res:
            with open(cache_file, "w") as f:
                json.dump(res["data"], f)
            print("Scrip master downloaded and cached")
            return res["data"]
        else:
            print(f"Failed to get scrip master: {res}")
            return []
    except Exception as e:
        print(f"Exception fetching scrip master: {e}")
        return []


def find_symbol_token(symbol_name, exchange="NSE"):
    scrips = get_scrip_master()
    symbol_name = symbol_name.upper()
    for scrip in scrips:
        if (
            scrip.get("exch_seg") == exchange
            and scrip.get("tradingsymbol", "").upper() == symbol_name
        ):
            return scrip.get("symboltoken")
    print(f"[✘] Symbol not found: {symbol_name} in {exchange}")
    return None
