import hashlib
import re
import hmac
import secrets
import time
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from config import settings


# --- PASSWORD HASHING ---

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    Hash a password with a random or provided salt using PBKDF2-HMAC-SHA256.
    Returns salt and hashed password combined as salt$hash.
    """
    if salt is None:
        salt = secrets.token_hex(16)  # 32 hex chars = 16 bytes salt
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    )
    return f"{salt}${pwd_hash.hex()}"


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against the stored salt$hash.
    """
    try:
        salt, stored_hash = hashed_password.split('$')
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000
        ).hex()
        # Use hmac.compare_digest for timing attack resistance
        return hmac.compare_digest(pwd_hash, stored_hash)
    except Exception:
        return False


def is_strong_password(password: str) -> bool:
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[!@#$%^&*()_+={}\[\]:;\"'<>,.?/-]", password)
    )


# --- JWT TOKEN MANAGEMENT ---

def generate_jwt_token(data: dict, expires_in: int = 3600) -> str:
    """
    Generate JWT token with expiration time (in seconds).
    """
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token


def decode_jwt_token(token: str) -> Optional[dict]:
    """
    Decode and verify JWT token, returns payload if valid, else None.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# --- OTP GENERATION AND VERIFICATION ---

def generate_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP code of specified length.
    """
    digits = "0123456789"
    return ''.join(secrets.choice(digits) for _ in range(length))


def verify_otp(input_otp: str, actual_otp: str, expiry_timestamp: float) -> bool:
    """
    Verify OTP matches and is within expiry time (timestamp in seconds).
    """
    current_time = time.time()
    return input_otp == actual_otp and current_time <= expiry_timestamp


# --- TELEGRAM AUTHORIZATION CHECK ---

def is_authorized_telegram_user(user_id: int, allowed_user_ids: set) -> bool:
    """
    Check if Telegram user ID is in the allowed list.
    """
    return user_id in allowed_user_ids
