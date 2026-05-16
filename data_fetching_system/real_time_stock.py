# file: analyzer/real_time_stock.py

import os
import http.client
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from analyzer.symbol_lookup import resolve_symbol
from security.generate_token import generate_and_update_token

load_dotenv()

# === API CONFIG ===
CANDLE_URL = "https://apiconnect.angelone.in/rest/secure/angelbroking/historical/v1/getCandleData"

STATIC_HEADERS = {
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "X-ClientLocalIP": os.getenv("LOCAL_IP"),
    "X-ClientPublicIP": os.getenv("PUBLIC_IP"),
    "X-MACAddress": os.getenv("MAC_ADDRESS"),
    "X-PrivateKey": os.getenv("ANGEL_API_KEY"),
    "Authorization": os.getenv("ANGEL_AUTH_TOKEN"),
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def fetch_live_ohlc(symbol: str, minutes_back=120, interval="FIVE_MINUTE"):
    resolved = resolve_symbol(symbol)
    if not resolved:
        raise ValueError(f"❌ Symbol could not be resolved: {symbol}")

    generate_and_update_token()
    jwt_token = os.getenv("ANGEL_AUTH_TOKEN")
    headers = STATIC_HEADERS.copy()
    headers["Authorization"] = f"Bearer {jwt_token}"
    headers["X-ClientCode"] = os.getenv("ANGEL_CLIENT_CODE")

    now = datetime.now()
    from_time = now - timedelta(minutes=minutes_back)

    payload = {
        "exchange": resolved["exchange"],
        "symboltoken": resolved["token"],
        "interval": interval,
        "fromdate": from_time.strftime("%Y-%m-%d %H:%M"),
        "todate": now.strftime("%Y-%m-%d %H:%M")
    }

    try:
        res = requests.post(CANDLE_URL, headers=headers, json=payload)
        res.raise_for_status()
        raw = res.json().get("data", [])
        if not raw:
            if datetime.today().weekday() >= 5:
                print("📴 Market closed (Weekend) — no OHLC data available.")
            else:
                print("⚠️ No OHLC data returned from API.")
            return pd.DataFrame()

        df = pd.DataFrame(raw, columns=["datetime", "open", "high", "low", "close", "volume"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        return df

    except Exception as e:
        print(f"❌ OHLC fetch failed for {symbol}: {e}")
        return pd.DataFrame()

def fetch_live_ltp_full(symbol: str):
    resolved = resolve_symbol(symbol)
    if not resolved:
        raise ValueError(f"❌ Symbol could not be resolved: {symbol}")

    generate_and_update_token()
    jwt_token = os.getenv("ANGEL_AUTH_TOKEN")

    conn = http.client.HTTPSConnection("apiconnect.angelone.in")
    payload = json.dumps({
        "mode": "FULL",
        "exchangeTokens": {
            resolved["exchange"]: [resolved["token"]]
        }
    })

    headers = STATIC_HEADERS.copy()
    headers["Authorization"] = f"Bearer {jwt_token}"
    headers["X-ClientCode"] = os.getenv("ANGEL_CLIENT_CODE")

    try:
        conn.request("POST", "/rest/secure/angelbroking/market/v1/quote/", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        parsed = json.loads(data)

        item = parsed["data"]["fetched"][0] if "fetched" in parsed["data"] else parsed["data"]

        return {
            "symbol": resolved["symbol"],
            "exchange": resolved["exchange"],
            "ltp": item.get("ltp"),
            "open": item.get("open"),
            "high": item.get("high"),
            "low": item.get("low"),
            "close": item.get("close"),
            "volume": item.get("volume"),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

    except Exception as e:
        print(f"❌ Quote fetch failed for {symbol}: {e}")
        return {}


def build_stock_summary(df: pd.DataFrame, symbol: str):
    if df.empty:
        return {}

    latest = df.iloc[-1]
    high = df.loc[df['high'].idxmax()]
    low = df.loc[df['low'].idxmin()]
    open_price = df.iloc[0]["open"]

    return {
        "symbol": symbol,
        "open": round(open_price, 2),
        "current_price": round(latest["close"], 2),
        "high": round(high["high"], 2),
        "high_time": high["datetime"].strftime("%H:%M"),
        "low": round(low["low"], 2),
        "low_time": low["datetime"].strftime("%H:%M"),
        "percent_change": round(((latest["close"] - open_price) / open_price) * 100, 2),
        "volume_total": int(df["volume"].sum()),
        "dataframe": df
    }


def get_main_stock_snapshot(symbol: str):
    df = fetch_live_ohlc(symbol)
    return build_stock_summary(df, symbol)
