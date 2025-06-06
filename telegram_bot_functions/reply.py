from telegram import Update
from telegram.ext import ContextTypes
from llm_engineering import Clara

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if its a reply
    if update.message and update.message.reply_to_message:
        original_message = update.message.reply_to_message

        # Check if the replied to message was the bots message
        if original_message.from_user and original_message.from_user.id == context.bot.id:
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id
            username = update.effective_user.first_name
            reply_text = update.message.text

            # Save User Message
            # save_message_to_db(user_id, chat_id, "user", reply_text)

            # Get Conversation Context/History
            # conversation_history = get_conversation_history(user_id, chat_id, limit=10) # Limit is the amount of messages you want to load for context
            #history_text = "\n".join([f"{entry['role']}: {entry['text']}" for entry in conversation_history])

            # Call LLM
            #client = Clara()
            #llm_response = client.readEmail(history_text)

            # Save LLM response
            #save_message_to_db(user_id, chat_id, "bot", llm_response)

            # Reply Back
            #await update.message.reply_text(llm_response)
