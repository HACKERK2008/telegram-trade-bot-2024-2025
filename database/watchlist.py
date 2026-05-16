# database/watchlist.py

import json
from pathlib import Path

WATCHLIST_FILE = Path("data/watchlist.json")
WATCHLIST_FILE.parent.mkdir(parents=True, exist_ok=True)

def _load_watchlist():
    if not WATCHLIST_FILE.exists():
        return {}
    with open(WATCHLIST_FILE, "r") as f:
        return json.load(f)

def _save_watchlist(data):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_to_watchlist(user_id: str, symbol: str):
    symbol = symbol.upper()
    data = _load_watchlist()
    user_list = set(data.get(user_id, []))
    user_list.add(symbol)
    data[user_id] = list(user_list)
    _save_watchlist(data)
    return f"✅ Added {symbol} to your watchlist."

def remove_from_watchlist(user_id: str, symbol: str):
    symbol = symbol.upper()
    data = _load_watchlist()
    user_list = set(data.get(user_id, []))
    if symbol in user_list:
        user_list.remove(symbol)
        data[user_id] = list(user_list)
        _save_watchlist(data)
        return f"❌ Removed {symbol} from your watchlist."
    return f"⚠️ {symbol} not found in your watchlist."

def get_user_watchlist(user_id: str):
    data = _load_watchlist()
    return data.get(user_id, [])

def clear_watchlist(user_id: str):
    data = _load_watchlist()
    if user_id in data:
        del data[user_id]
        _save_watchlist(data)
        return "🧹 Watchlist cleared."
    return "⚠️ No watchlist found for you."
