# file: handler/callback_handler.py

import os
from aiogram.types import CallbackQuery, FSInputFile
from bot.handlers import user_last_result
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# === Inline Command Actions from /help
async def handle_strike_selection(query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    if data == "analyze":
        await query.message.answer("📊 Start analyzing with /option_chain.\nChoose 'main' + 'historical' to fetch stock data.")

    elif data == "margin_calc":
        await query.message.answer("🧮 Use /margin to simulate margin, RR, taxes, and profit calculation.")

    elif data == "chart":
        await query.message.answer("📈 Charts and Excel reports auto-generate after option_chain historical fetch.")

    elif data == "myinfo":
        await query.message.answer(f"👤 Your User ID: <code>{user_id}</code>", parse_mode="HTML")

    await query.answer()

# === Inline Follow-ups from send_analysis_result()
async def handle_analysis_actions(query: CallbackQuery):
    user_id = query.from_user.id
    result = user_last_result.get(user_id)

    if not result:
        await query.message.answer("⚠️ No previous analysis found. Use /option_chain first.")
        await query.answer()
        return

    data = query.data

    if data == "analyze_last_5":
        await query.message.answer("📊 Micro-analysis of last 5 candles coming soon...")

    elif data == "export_excel":
        path = result.get("excel_path")
        if path and os.path.exists(path):
            await query.message.answer_document(FSInputFile(path), caption="📤 Excel Report")
        else:
            await query.message.answer("⚠️ Excel not found. Please re-run /option_chain.")

    elif data == "send_chart":
        path = result.get("chart_path")
        if path and os.path.exists(path):
            await query.message.answer_photo(FSInputFile(path), caption="📈 Chart Snapshot")
        else:
            await query.message.answer("⚠️ Chart not found. Please re-run /option_chain.")

    await query.answer()
