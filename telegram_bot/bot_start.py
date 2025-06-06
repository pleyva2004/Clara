from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram_bot.reply import message_handler
from dotenv import load_dotenv
import os

def run_telegram_bot():
    load_dotenv()
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()
