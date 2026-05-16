# bot/handlers.py

import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot import replies
from analyzer.analyzer import analyze_stock, to_telegram_summary
from bot.options_chain import process_option_chain
from data_fetching_system.data_fetcher import fetch_historical_candles

router = Router()
user_last_result: dict[int, dict] = {}

# === FSM States ===
class OptionFlow(StatesGroup):
    waiting_for_symbol = State()
    waiting_for_segment = State()
    waiting_for_data_type = State()
    waiting_for_interval = State()
    waiting_for_days = State()

class AnalyzeFlow(StatesGroup):
    waiting_for_symbol = State()
    waiting_for_capital = State()

# === START ===
@router.message(Command("start"))
async def handle_start(message: Message):
    image = FSInputFile("visualizer/Assets/logo.png")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("/start"), KeyboardButton("/option_chain")],
            [KeyboardButton("/analyze"), KeyboardButton("/login")],
            [KeyboardButton("/settings"), KeyboardButton("/help")]
        ],
        resize_keyboard=True
    )

    caption = replies.get_welcome_message(message.from_user.first_name)
    try:
        await message.answer_photo(photo=image, caption=caption, parse_mode="HTML", reply_markup=keyboard)
    except:
        await message.answer(caption, reply_markup=keyboard, parse_mode="HTML")

# === HELP ===
@router.message(Command("help"))
async def handle_help(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Analyze", callback_data="analyze")],
            [InlineKeyboardButton(text="🧮 Margin", callback_data="margin_calc")],
            [InlineKeyboardButton(text="📈 Chart", callback_data="chart")],
            [InlineKeyboardButton(text="ℹ️ My Info", callback_data="myinfo")]
        ]
    )
    await message.answer(replies.get_help_message(), parse_mode="HTML", reply_markup=keyboard)

# === /ANALYZE FLOW ===
@router.message(Command("analyze"))
async def handle_analyze(message: Message, state: FSMContext):
    await message.answer("📌 Enter stock symbol (e.g. RELIANCE):")
    await state.set_state(AnalyzeFlow.waiting_for_symbol)

@router.message(AnalyzeFlow.waiting_for_symbol)
async def handle_analyze_symbol(message: Message, state: FSMContext):
    await state.update_data(symbol=message.text.upper())
    await message.answer("💸 Enter your capital amount (e.g. 50000):")
    await state.set_state(AnalyzeFlow.waiting_for_capital)

@router.message(AnalyzeFlow.waiting_for_capital)
async def handle_analyze_capital(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        symbol = data["symbol"]
        capital = float(message.text)

        await message.answer(f"⏳ Analyzing <b>{symbol}</b> with ₹{int(capital)}...", parse_mode="HTML")

        df = fetch_historical_candles(symbol, interval="2hour", days=20)

        result = analyze_stock({
            "ohlc_df": df,
            "meta": {
                "symbol": symbol,
                "capital": capital
            }
        })

        user_last_result[message.from_user.id] = result
        msg = to_telegram_summary(result)
        await message.answer(msg, parse_mode="HTML")

        if "chart_path" in result and os.path.exists(result["chart_path"]):
            file = FSInputFile(result["chart_path"])
            await message.answer_photo(file, caption="📉 Forecast Chart", parse_mode="HTML")

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

    await state.clear()

# === OPTION CHAIN FLOW ===
@router.message(Command("option_chain"))
async def handle_option_chain(message: Message, state: FSMContext):
    await message.answer(replies.get_option_chain_symbol_prompt())
    await state.set_state(OptionFlow.waiting_for_symbol)

@router.message(OptionFlow.waiting_for_symbol)
async def handle_symbol_response(message: Message, state: FSMContext):
    await state.update_data(symbol=message.text.upper())
    await message.answer("📈 Choose segment: main / option")
    await state.set_state(OptionFlow.waiting_for_segment)

@router.message(OptionFlow.waiting_for_segment)
async def handle_segment_choice(message: Message, state: FSMContext):
    segment = message.text.lower()
    if segment not in ["main", "option"]:
        await message.answer("❌ Invalid segment. Use: main / option")
        return
    await state.update_data(segment=segment)
    await message.answer("📡 Select data mode: live / historical")
    await state.set_state(OptionFlow.waiting_for_data_type)

@router.message(OptionFlow.waiting_for_data_type)
async def handle_data_type_choice(message: Message, state: FSMContext):
    data_type = message.text.lower()
    if data_type not in ["live", "historical"]:
        await message.answer("❌ Invalid. Choose: live / historical")
        return
    await state.update_data(data_type=data_type)

    if data_type == "historical":
        await message.answer("📊 Choose interval:\n" + "\n".join([
            "ONE_MINUTE", "THREE_MINUTE", "FIVE_MINUTE", "TEN_MINUTE",
            "FIFTEEN_MINUTE", "THIRTY_MINUTE", "ONE_HOUR", "ONE_DAY"
        ]))
        await state.set_state(OptionFlow.waiting_for_interval)
    else:
        await message.answer("⚠️ Live system not implemented yet.")

@router.message(OptionFlow.waiting_for_interval)
async def handle_interval_choice(message: Message, state: FSMContext):
    interval = message.text.upper()
    valid = [
        "ONE_MINUTE", "THREE_MINUTE", "FIVE_MINUTE", "TEN_MINUTE",
        "FIFTEEN_MINUTE", "THIRTY_MINUTE", "ONE_HOUR", "ONE_DAY"
    ]
    if interval not in valid:
        await message.answer("❌ Invalid interval. Try again.")
        return
    await state.update_data(interval=interval)
    await message.answer("📅 How many days to fetch? (e.g. 5, 10, 30)")
    await state.set_state(OptionFlow.waiting_for_days)

@router.message(OptionFlow.waiting_for_days)
async def handle_day_entry(message: Message, state: FSMContext):
    try:
        days = int(message.text)
        user_data = await state.get_data()
        symbol = user_data["symbol"]
        segment = user_data["segment"]
        interval = user_data["interval"]
        mode = user_data["data_type"]

        result = process_option_chain(symbol, segment, interval, days, analyze=True, mode=mode)
        user_last_result[message.from_user.id] = result
        await send_analysis_result(message, result)

        await state.clear()

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

# === SEND ANALYSIS RESULT
async def send_analysis_result(message: Message, result: dict):
    if "error" in result:
        await message.answer(result["error"])
        return

    await message.answer(result.get("summary", "✅ Analysis Complete."))

    if "chart_path" in result and os.path.exists(result["chart_path"]):
        await message.answer_photo(FSInputFile(result["chart_path"]))

    if "excel_path" in result and os.path.exists(result["excel_path"]):
        await message.answer_document(FSInputFile(result["excel_path"]))

    if "pdf_path" in result and os.path.exists(result["pdf_path"]):
        await message.answer_document(FSInputFile(result["pdf_path"]), caption="📄 Analysis PDF Report")

    if "prediction" in result:
        await message.answer(f"📊 <b>Strategy Prediction:</b>\n{result['prediction']}", parse_mode="HTML")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Analyze Last 5", callback_data="analyze_last_5")],
            [InlineKeyboardButton(text="📤 Export Excel", callback_data="export_excel")],
            [InlineKeyboardButton(text="📈 Send Chart", callback_data="send_chart")]
        ]
    )
    await message.answer("🔧 Choose next action:", reply_markup=keyboard)
