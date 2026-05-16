# utils/api_helpers.py

import os
import time
import requests
import pyotp
from dotenv import load_dotenv

load_dotenv()

# ✅ Correct base URL for all Angel One SmartAPI backend services
BASE_URL = "https://apiconnect.angelone.in"

# ✅ Endpoints
LOGIN_ENDPOINT = "/rest/auth/angelbroking/user/v1/loginByMPIN"
JWT_REFRESH_ENDPOINT = "/rest/auth/angelbroking/jwt/v1/generateTokens"
RMS_ENDPOINT = "/rest/secure/angelbroking/user/v1/getRMS"
LTP_ENDPOINT = "/rest/marketdata/quotes/v1.0.0/quote"
PROFILE_ENDPOINT = "/rest/secure/angelbroking/user/v1/getProfile"

def generate_totp(secret: str) -> str:
    totp = pyotp.TOTP(secret)
    return totp.now()

def angel_login(client_code: str, password: str, api_key: str, totp_secret: str):
    url = BASE_URL + LOGIN_ENDPOINT
    payload = {
    "clientcode": client_code,
    "mpin": password,
    "totp": generate_totp(totp_secret)
}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientLocalIP": os.getenv("CLIENT_LOCAL_IP", "192.168.1.2"),
        "X-ClientPublicIP": os.getenv("CLIENT_PUBLIC_IP", "1.2.3.4"),
        "X-MACAddress": os.getenv("CLIENT_MAC_ADDRESS", "00:11:22:33:44:55"),
        "X-PrivateKey": api_key
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    resp_json = response.json()
    print("Login response:", resp_json)

    if resp_json.get("status") and "data" in resp_json:
        return {
            "jwt": resp_json["data"].get("jwtToken"),
            "refresh_token": resp_json["data"].get("refreshToken"),
            "feed_token": resp_json["data"].get("feedToken")
        }
    else:
        return None

def refresh_jwt(api_key: str, refresh_token: str):
    url = BASE_URL + JWT_REFRESH_ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    payload = {
        "refreshToken": refresh_token
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    resp_json = response.json()
    print("Refresh response:", resp_json)
    if resp_json.get("status") and "data" in resp_json:
        return resp_json["data"].get("jwtToken")
    else:
        return None

def get_rms_margin(jwt_token: str, api_key: str):
    url = BASE_URL + RMS_ENDPOINT
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def get_ltp(jwt_token: str, api_key: str, symbol: str):
    url = BASE_URL + LTP_ENDPOINT
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "mode": "FULL",
        "exchangeTokens": {
            "NFO": [symbol]  # Example: ["NIFTY24JUNFUT"]
        }
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def get_profile(jwt_token: str, api_key: str, local_ip: str, public_ip: str, mac_address: str):
    url = BASE_URL + PROFILE_ENDPOINT
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientLocalIP": local_ip,
        "X-ClientPublicIP": public_ip,
        "X-MACAddress": mac_address,
        "X-PrivateKey": api_key
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    client_code = os.getenv("ANGEL_CLIENT_CODE")
    password = os.getenv("ANGEL_PASSWORD")
    api_key = os.getenv("ANGEL_API_KEY")
    totp_secret = os.getenv("TOTP_SECRET")
    local_ip = os.getenv("CLIENT_LOCAL_IP", "192.168.1.2")
    public_ip = os.getenv("CLIENT_PUBLIC_IP", "1.2.3.4")
    mac_address = os.getenv("CLIENT_MAC_ADDRESS", "00:11:22:33:44:55")

    if not all([client_code, password, api_key, totp_secret]):
        print("❌ Missing required environment variables!")
        exit(1)

    login_data = angel_login(client_code, password, api_key, totp_secret)
    if login_data:
        print("✅ Login successful!")
        jwt_token = login_data["jwt"]
        refresh_token = login_data["refresh_token"]

        rms = get_rms_margin(jwt_token, api_key)
        print("RMS Margin:", rms)

        ltp = get_ltp(jwt_token, api_key, "NIFTY24JUNFUT")
        print("LTP Data:", ltp)

        profile = get_profile(jwt_token, api_key, local_ip, public_ip, mac_address)
        print("User Profile:", profile)

        print("\nRefreshing JWT...")
        new_jwt = refresh_jwt(api_key, refresh_token)
        if new_jwt:
            print("✅ New JWT:", new_jwt[:20] + "...")
        else:
            print("❌ JWT refresh failed.")
    else:
        print("❌ Login failed.")
