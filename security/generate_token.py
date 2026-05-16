# security/generate_token.py

import os
from dotenv import load_dotenv
import pyotp
import requests

# Load env from root project directory (assuming script runs in /security)
ROOT_ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(ROOT_ENV_PATH)

# Load required variables
CLIENT_CODE = os.getenv("ANGEL_CLIENT_CODE")
MPIN = os.getenv("ANGEL_MPIN")
TOTP_SECRET = os.getenv("TOTP_SECRET")
API_KEY = os.getenv("ANGEL_API_KEY")
SECRATE_KEY = os.getenv("ANGELONE_SECRATE_KEY")
LOCAL_IP = os.getenv("LOCAL_IP")
PUBLIC_IP = os.getenv("PUBLIC_IP")
MAC = os.getenv("MAC_ADDRESS")

LOGIN_URL = "https://apiconnect.angelone.in/rest/auth/angelbroking/user/v1/loginByPassword"
TOKEN_URL = "https://apiconnect.angelone.in/rest/auth/angelbroking/jwt/v1/generateTokens"

HEADERS = {
    "X-UserType": "USER",
    "X-SourceID": "WEB",
    "X-ClientLocalIP": LOCAL_IP,
    "X-ClientPublicIP": PUBLIC_IP,
    "X-MACAddress": MAC,
    "X-PrivateKey": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def generate_totp():
    return pyotp.TOTP(TOTP_SECRET).now()

def update_env_file(key, value, env_path):
    lines = []
    updated = False
    with open(env_path, "r") as file:
        for line in file:
            if line.startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                updated = True
            else:
                lines.append(line)
    if not updated:
        lines.append(f"{key}={value}\n")
    with open(env_path, "w") as file:
        file.writelines(lines)

def generate_and_update_token():
    print("🔐 Step 1: Logging in with TOTP...")
    payload = {
        "clientcode": CLIENT_CODE,
        "password": MPIN,
        "totp": generate_totp()
    }

    login_res = requests.post(LOGIN_URL, json=payload, headers=HEADERS)
    login_data = login_res.json()

    if not login_data.get("status"):
        raise Exception("❌ Login failed: " + login_data.get("message", "Unknown error"))

    jwt_token = login_data["data"]["jwtToken"]
    refresh_token = login_data["data"]["refreshToken"]

    print("✅ Login success. Requesting final token...")
    token_headers = HEADERS.copy()
    token_headers["Authorization"] = f"Bearer {jwt_token}"

    final_res = requests.post(TOKEN_URL, json={"refreshToken": refresh_token}, headers=token_headers)
    token_data = final_res.json()

    if not token_data.get("status"):
        raise Exception("❌ Token generation failed: " + token_data.get("message", "Unknown error"))

    auth_token = token_data["data"]["jwtToken"]
    feed_token = token_data["data"]["feedToken"]

    print("✅ Token Generated")
    print("🔑 AUTH_TOKEN:", auth_token[:50], "...")
    print("📡 FEED_TOKEN:", feed_token[:50], "...")

    update_env_file("ANGEL_AUTH_TOKEN", auth_token, ROOT_ENV_PATH)
    update_env_file("ANGLE_FEED_TOKEN", feed_token, ROOT_ENV_PATH)
    print("📁 .env file updated successfully at:", ROOT_ENV_PATH)

generate_and_update_token()
