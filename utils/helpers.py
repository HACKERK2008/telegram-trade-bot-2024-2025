# utils/helpers.py

import re
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:
    """
    Validate email format using regex.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    match = re.match(pattern, email)
    is_valid = bool(match)
    logger.debug(f"Validating email '{email}': {is_valid}")
    return is_valid

def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a number as currency string.
    Example: 1234.5 -> $1,234.50
    """
    try:
        formatted = f"{currency_symbol(currency)}{amount:,.2f}"
        logger.debug(f"Formatted amount {amount} as {formatted}")
        return formatted
    except Exception as e:
        logger.error(f"Error formatting currency: {e}")
        return f"{amount:.2f}"

def currency_symbol(currency: str) -> str:
    """
    Return the symbol for a given currency code.
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "INR": "₹",
        # Add more as needed
    }
    return symbols.get(currency.upper(), currency + " ")

def safe_get(dct: Dict, key: Any, default: Optional[Any] = None) -> Any:
    """
    Safely get a value from dictionary, return default if key not found.
    """
    value = dct.get(key, default)
    logger.debug(f"Getting key '{key}' from dict, returning: {value}")
    return value

def list_to_str(items: List[Any], sep: str = ", ") -> str:
    """
    Convert a list of items to a string separated by sep.
    """
    result = sep.join(str(i) for i in items)
    logger.debug(f"Converted list {items} to string: {result}")
    return result
