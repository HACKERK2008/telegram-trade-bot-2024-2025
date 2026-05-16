# bot/cmds.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.replies import (
    get_welcome_message,
    get_help_message,
    get_menu_markup,
    get_about_message,
    get_prediction_intro_message,
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    chat_id = update.effective_chat.id
    welcome_message = get_welcome_message()
    menu_markup = get_menu_markup()
    await context.bot.send_message(chat_id=chat_id, text=welcome_message, reply_markup=menu_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(get_help_message())

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    await update.message.reply_text(get_about_message())

async def prediction_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /predict command"""
    await update.message.reply_text(get_prediction_intro_message())
