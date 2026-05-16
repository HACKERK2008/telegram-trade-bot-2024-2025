# utils/validators.py

import re
from typing import Optional, List
from datetime import datetime

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_email(email: str) -> bool:
    """
    Validate email with stricter RFC 5322-like regex pattern.
    Raises ValidationError if invalid.
    """
    email_regex = re.compile(
        r"(^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z]{2,})+$)"
    )
    if not isinstance(email, str) or not email_regex.match(email):
        raise ValidationError(f"Invalid email format: {email}")
    return True

def validate_url(url: str) -> bool:
    """
    Validate URL with HTTPS mandatory (no plain HTTP).
    Raises ValidationError if invalid.
    """
    url_regex = re.compile(
        r"^(https:\/\/)"               # Must start with https://
        r"(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6})"  # domain (subdomains allowed)
        r"(\/[\w\-._~:/?#[\]@!$&'()*+,;=]*)?$", re.IGNORECASE
    )
    if not isinstance(url, str) or not url_regex.match(url):
        raise ValidationError(f"Invalid or insecure URL (HTTPS only): {url}")
    return True

def validate_stock_symbol(symbol: str) -> bool:
    """
    Validate stock ticker symbol: uppercase letters/numbers (up to 5 chars).
    Prevent suspicious symbols (no special chars).
    """
    if not isinstance(symbol, str):
        raise ValidationError(f"Stock symbol must be string: {symbol}")
    if not re.fullmatch(r'^[A-Z0-9]{1,5}$', symbol):
        raise ValidationError(f"Invalid stock symbol: {symbol}")
    return True

def validate_numeric_range(value: float, min_val: Optional[float] = None, max_val: Optional[float] = None) -> bool:
    """
    Validate that a numeric value is within min and max.
    Checks type strictly.
    """
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Value must be a number: {value}")
    if min_val is not None and value < min_val:
        raise ValidationError(f"Value {value} less than minimum allowed {min_val}")
    if max_val is not None and value > max_val:
        raise ValidationError(f"Value {value} greater than maximum allowed {max_val}")
    return True

def validate_date(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
    """
    Validate date string matches format strictly.
    """
    if not isinstance(date_str, str):
        raise ValidationError("Date must be a string")
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        raise ValidationError(f"Date '{date_str}' does not match format '{date_format}'")

def validate_telegram_command(command: str, valid_commands: Optional[List[str]] = None) -> bool:
    """
    Validate Telegram bot commands:
    - Must start with /
    - Contains only letters, digits, and underscores after /
    - Optional whitelist for allowed commands
    """
    if not isinstance(command, str):
        raise ValidationError("Command must be a string")
    if not command.startswith('/'):
        raise ValidationError(f"Command must start with '/': {command}")
    if not re.fullmatch(r'/[a-zA-Z0-9_]+', command):
        raise ValidationError(f"Invalid characters in command: {command}")
    if valid_commands and command not in valid_commands:
        raise ValidationError(f"Command '{command}' not in allowed commands list")
    return True

def validate_telegram_user_id(user_id: int) -> bool:
    """
    Validate Telegram user ID:
    - Must be positive integer (Telegram IDs are positive)
    - Typically less than 2^63 but no hard limit here
    """
    if not isinstance(user_id, int):
        raise ValidationError(f"User ID must be integer: {user_id}")
    if user_id <= 0:
        raise ValidationError(f"User ID must be positive: {user_id}")
    return True

def validate_telegram_username(username: str) -> bool:
    """
    Validate Telegram usernames:
    - Allowed: a-z, A-Z, 0-9, underscores
    - Length: 5 to 32 chars
    - No starting with underscore or digits (Telegram rules)
    """
    if not isinstance(username, str):
        raise ValidationError("Username must be a string")
    if not 5 <= len(username) <= 32:
        raise ValidationError("Username length must be between 5 and 32 characters")
    if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]{4,31}', username):
        raise ValidationError(f"Invalid Telegram username: {username}")
    return True

def validate_password_strength(password: str, min_length: int = 8) -> bool:
    """
    Validate password strength:
    - Min length (default 8)
    - Must include uppercase, lowercase, digit, and special char
    """
    if not isinstance(password, str):
        raise ValidationError("Password must be a string")
    if len(password) < min_length:
        raise ValidationError(f"Password must be at least {min_length} characters long")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must include an uppercase letter")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must include a lowercase letter")
    if not re.search(r'\d', password):
        raise ValidationError("Password must include a digit")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must include a special character")
    return True
