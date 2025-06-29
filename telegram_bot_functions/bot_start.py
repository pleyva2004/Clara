from telegram.ext import Application,MessageHandler, filters
from telegram_bot_functions.handlers.reply import message_handler
from data_pipeline.database_functions import get_connection
from dotenv import load_dotenv
import os

def run_telegram_bot():
    load_dotenv()
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # App handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    # Vote_message_handler using /vote
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_telegram_bot()