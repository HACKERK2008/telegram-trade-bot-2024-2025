# utils/formatters.py

import datetime
import json
import re
from typing import Optional, Any, Dict


def format_datetime(dt: Optional[Any], fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object or ISO date-time string to a formatted string.
    Defaults to 'YYYY-MM-DD HH:MM:SS'.

    Args:
        dt: datetime object, ISO date-time string, or None.
        fmt: format string for strftime.

    Returns:
        Formatted datetime string or empty string if input is invalid.
    """
    if not dt:
        return ""
    if isinstance(dt, str):
        try:
            dt = datetime.datetime.fromisoformat(dt)
        except ValueError:
            return dt  # Return original string if cannot parse
    if isinstance(dt, datetime.datetime):
        return dt.strftime(fmt)
    return str(dt)  # fallback to string conversion


def format_date(dt: Optional[Any], fmt: str = "%Y-%m-%d") -> str:
    """
    Format a date object or ISO date string to a formatted string.
    Defaults to 'YYYY-MM-DD'.

    Args:
        dt: date object, ISO date string, or None.
        fmt: format string for strftime.

    Returns:
        Formatted date string or empty string if input is invalid.
    """
    if not dt:
        return ""
    if isinstance(dt, str):
        try:
            dt = datetime.date.fromisoformat(dt)
        except ValueError:
            return dt
    if isinstance(dt, datetime.date):
        return dt.strftime(fmt)
    return str(dt)


def format_currency(amount: Optional[float], symbol: str = "$", decimals: int = 2) -> str:
    """
    Format a number as currency string.

    Args:
        amount: numeric value or None.
        symbol: currency symbol prefix.
        decimals: number of decimal places.

    Returns:
        Formatted currency string or empty string if amount is None.
    """
    if amount is None:
        return ""
    try:
        return f"{symbol}{amount:,.{decimals}f}"
    except (ValueError, TypeError):
        return ""


def format_percentage(value: Optional[float], decimals: int = 2) -> str:
    """
    Format a float as a percentage string (value * 100).

    Args:
        value: numeric value or None.
        decimals: number of decimal places.

    Returns:
        Formatted percentage string or empty string if value is None.
    """
    if value is None:
        return ""
    try:
        return f"{value * 100:.{decimals}f}%"
    except (ValueError, TypeError):
        return ""


def format_number(value: Optional[float], decimals: int = 2) -> str:
    """
    Format a number with commas and fixed decimals.

    Args:
        value: numeric value or None.
        decimals: number of decimal places.

    Returns:
        Formatted number string or empty string if value is None.
    """
    if value is None:
        return ""
    try:
        return f"{value:,.{decimals}f}"
    except (ValueError, TypeError):
        return ""


def title_case(text: Optional[str]) -> str:
    """
    Convert string to title case.

    Args:
        text: input string or None.

    Returns:
        Title cased string or empty string if input is None.
    """
    if not text:
        return ""
    return text.title()


def snake_case(text: Optional[str]) -> str:
    """
    Convert string to snake_case.

    Args:
        text: input string or None.

    Returns:
        snake_case string or empty string if input is None.
    """
    if not text:
        return ""
    text = re.sub(r"[\s\-]+", "_", text)
    text = re.sub(r"[^\w_]", "", text)
    return text.lower()


def remove_extra_spaces(text: Optional[str]) -> str:
    """
    Trim and reduce multiple spaces inside text to a single space.

    Args:
        text: input string or None.

    Returns:
        Cleaned string or empty string if input is None.
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def pretty_json(data: any) -> str:
    """
    Return pretty formatted JSON string for dict inputs.
    For any other input, return empty string.
    """
    if not isinstance(data, dict):
        return ""
    try:
        return json.dumps(data, indent=4, sort_keys=True)
    except (TypeError, ValueError):
        return ""
    

def format_percentage_change(
    current: Optional[float], previous: Optional[float], decimals: int = 2
) -> str:
    """
    Calculate and format percentage change from previous to current value.

    Args:
        current: current numeric value.
        previous: previous numeric value.
        decimals: decimal places.

    Returns:
        Percentage change string with sign or empty string if invalid input.
    """
    if current is None or previous in (None, 0):
        return ""
    try:
        change = ((current - previous) / abs(previous)) * 100
        sign = "+" if change >= 0 else "-"
        return f"{sign}{abs(change):.{decimals}f}%"
    except Exception:
        return ""


def format_duration(seconds: Optional[int]) -> str:
    """
    Convert seconds to H:MM:SS format string.

    Args:
        seconds: total seconds as integer.

    Returns:
        Duration string or empty string if invalid input.
    """
    try:
        seconds = int(seconds)
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h}:{m:02}:{s:02}"
    except Exception:
        return ""


def format_ticker_symbol(symbol: Optional[str]) -> str:
    """
    Clean and uppercase a ticker symbol.

    Args:
        symbol: input string or None.

    Returns:
        Uppercase ticker symbol without leading/trailing spaces or empty string.
    """
    if not symbol:
        return ""
    return symbol.strip().upper()


def safe_str(obj: Any) -> str:
    """
    Safely convert any object to string.

    Args:
        obj: any Python object.

    Returns:
        String representation or empty string if None.
    """
    return "" if obj is None else str(obj)


def format_ltp(ltp: float) -> str:
    """Format Last Traded Price with ₹ symbol"""
    return f"₹{ltp:.2f}"

def format_volume(vol: int) -> str:
    """Format volume into K / Lakh / Crore style"""
    if vol >= 10_000_000:
        return f"{vol / 1e7:.1f}Cr"
    elif vol >= 100_000:
        return f"{vol / 1e5:.1f}L"
    elif vol >= 1_000:
        return f"{vol / 1e3:.1f}K"
    return str(vol)
