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

    conn = get_connection(
        servername='sql1.njit.edu',
        username=DB_USERNAME,
        password=DB_PASSWORD,
        dbname='lb356'
    )

    # Store it in bot_data so all handlers can access it
    app.bot_data["db_conn"] = conn

    # App handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_telegram_bot()