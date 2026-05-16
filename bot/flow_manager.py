# file: bot/flow_manager.py
from aiogram.fsm.state import State, StatesGroup

class OptionChainFlow(StatesGroup):
    waiting_for_symbol = State()
    waiting_for_strike = State()

class MarginCalcFlow(StatesGroup):
    waiting_for_symbol = State()
    waiting_for_entry = State()
    waiting_for_capital = State()
