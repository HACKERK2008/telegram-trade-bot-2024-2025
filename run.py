# File: run.py

import asyncio
from bot.bot import run_bot

def main():
    try:
        print("🚀 Starting TradeBot...")
        asyncio.run(run_bot())
    except Exception as e:
        print(f"❌ Startup failed: {e}")

if __name__ == "__main__":
    main()
