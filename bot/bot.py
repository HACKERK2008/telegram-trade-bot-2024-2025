# file: bot/bot.py

import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

# === Load token from .env ===
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Import handlers ===
import bot.handlers as handlers
from handler import callback_handler

# === Setup Bot & Dispatcher ===
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# === Register Message Handlers ===
def register_handlers():
    dp.message.register(handlers.handle_start, Command("start"))
    dp.message.register(handlers.handle_help, Command("help"))
    dp.message.register(handlers.handle_option_chain, Command("option_chain"))
    dp.message.register(handlers.handle_login, Command("login"))
    dp.message.register(handlers.handle_menu, Command("menu"))
    dp.message.register(handlers.handle_myinfo, Command("myinfo"))
    dp.message.register(handlers.handle_symbol_response)

    dp.callback_query.register(callback_handler.handle_strike_selection)
    dp.callback_query.register(callback_handler.handle_strike_selection, lambda q: q.data in ["analyze", "margin_calc", "chart", "myinfo"])
    dp.callback_query.register(callback_handler.handle_analysis_actions, lambda q: q.data in ["analyze_last_5", "export_excel", "send_chart"])

# === Setup Bot Commands in UI ===
async def set_bot_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="⚡ Start the bot"),
        BotCommand(command="help", description="❓ Get help info"),
        BotCommand(command="option_chain", description="📉 View option chain"),
        BotCommand(command="login", description="🔐 Login securely"),
        BotCommand(command="menu", description="🎛️ Quick menu")
    ])

# === Run Entry Point ===
async def run_bot():
    print("🚀 Launching TradeBot...")
    await set_bot_commands()
    register_handlers()
    await dp.start_polling(bot)
