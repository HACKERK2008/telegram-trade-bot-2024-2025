# file: bot/replies.py

def get_welcome_message(username: str = "Trader") -> str:
    return f"""
👋 <b>Welcome {username}!</b>

🤖 I am <b>TradeMaster AI</b> – your trading assistant bot.
I help analyze <b>main stocks</b>, <b>F&O option chains</b>, and generate:
• 📈 Charts
• 🧠 Strategy Predictions
• 🧮 Margin + P&L Calculations
• 📊 Excel & PDF Reports

Start with: <code>/option_chain</code> or <code>/help</code>
"""

def get_help_message() -> str:
    return """
🆘 <b>How I can help you:</b>

<b>Commands:</b>
/start – Restart the bot
/option_chain – Analyze a stock or option
/help – View help & usage
/login – Link your AngelOne credentials
/settings – Customize bot behavior (coming soon)

/margin – Margin & Risk calculator (EQ/FNO)
/chart – Generate latest OHLC charts

<b>Supported Modes:</b>
- main (NSE/BSE stocks)
- option (F&O derivatives)
- live & historical

<b>Reports:</b>
✔️ Excel
✔️ Chart Image
✔️ Strategy Prediction
✔️ PDF Summary

<b>Safety First 🛡️</b>
This bot is designed to help with analysis only. Final decisions must be made wisely and with personal discretion. Use proper capital management 💼.
"""

def get_option_chain_symbol_prompt() -> str:
    return """
🔍 Please enter the symbol you want to analyze:
e.g. RELIANCE, TCS, INFY, NIFTY25JUL26600CE
"""

def get_chart_tip():
    return "💡 Chart auto-generates for historical scans (saved in Excel + PNG format)."

def get_margin_tip():
    return "🧮 Use /margin to simulate entry → exit including SL/TP, tax & brokerage."

def get_login_reply() -> str:
    return (
        "🔐 Login feature is coming soon...\n"
        "You'll be able to securely connect your trading account here."
    )

def get_menu_reply() -> str:
    return (
        "📋 Menu Options:\n"
        "/option_chain - Analyze market\n"
        "/help - Get command info\n"
        "/myinfo - Show your user ID"
    )

def get_myinfo_reply(uid: int) -> str:
    return f"👤 Your Telegram ID is: <code>{uid}</code>"

def get_error_reply() -> str:
    return (
        "❌ Something went wrong. Please try again later."
    )
