from telegram import Update
from telegram.ext import ContextTypes

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if its a reply
    if update.message and update.message.reply_to_message:
        original_message = update.message.reply_to_message

        # Check if the replied to message was the bots message
        if original_message.from_user and original_message.from_user.id == context.bot.id:
            user = update.effective_user.first_name
            reply_text = update.message.text
            await update.message.reply_text(f"Hi {user}, you said: {reply_text}")
