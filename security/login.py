# File: security/login.py

import os
import pyotp
import requests
from dotenv import load_dotenv
from uuid import getnode as get_mac
import socket

load_dotenv()

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "127.0.0.1"

def generate_totp():
    secret = os.getenv("TOTP_SECRET").strip()
    return pyotp.TOTP(secret).now()

def get_profile(jwt_token):
    url = "https://apiconnect.angelone.in/rest/secure/angelbroking/user/v1/getProfile"
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': get_local_ip(),
        'X-ClientPublicIP': get_local_ip(),
        'X-MACAddress': ':'.join(format((get_mac() >> ele) & 0xff, '02x') for ele in range(0,8*6,8))[::-1],
        'X-PrivateKey': os.getenv("ANGEL_API_KEY")
    }

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.json().get("data", {})
    except Exception as e:
        print(f"[Profile Fetch Error] {e}")
        return None

def login_to_angel_rest():
    url = "https://apiconnect.angelone.in/rest/auth/angelbroking/user/v1/loginByPassword"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-UserType': 'USER',
        'X-SourceID': 'WEB',
        'X-ClientLocalIP': get_local_ip(),
        'X-ClientPublicIP': get_local_ip(),
        'X-MACAddress': ':'.join(format((get_mac() >> ele) & 0xff, '02x') for ele in range(0,8*6,8))[::-1],
        'X-PrivateKey': os.getenv("ANGEL_API_KEY")
    }

    payload = {
        "clientcode": os.getenv("ANGEL_CLIENT_CODE"),
        "password": os.getenv("ANGEL_MPIN"),
        "totp": generate_totp(),
        "state": "tradebot"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data["status"]:
            jwt = data["data"]["jwtToken"]
            return {
                "clientcode": payload["clientcode"],
                "access_token": jwt,
                "refresh_token": data["data"]["refreshToken"],
                "feed_token": data["data"]["feedToken"],
                "state": data["data"]["state"],
                "profile": get_profile(jwt)
            }
        else:
            print(f"[Login Error] {data.get('message')}")
            return None
    except Exception as e:
        print(f"[HTTP Login Failed] {e}")
        return None
