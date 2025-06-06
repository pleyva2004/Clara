from telegram import Update
from telegram.ext import ContextTypes
from llm_engineering import Clara
from telegram_bot_functions.db.conversation_utils import (
    save_message_to_conversation,
    get_conversation_id_by_telegram_message_id,
    get_conversation_history
)
from datetime import datetime, timezone

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if its a reply
    if update.message and update.message.reply_to_message:
        original_message_id = update.message.reply_to_message.message_id
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        reply_text = update.message.text
        user_name = update.effective_user.first_name

        conn = context.bot_data["db_conn"]
        
        # Find the conversation_id of the original message
        conversation_id = get_conversation_id_by_telegram_message_id(conn, chat_id, original_message_id)

        if conversation_id:
            print(f"[HANDLER] User {user_name} is replying in conversation {conversation_id}")

            # Save the users reply
            save_message_to_conversation(
                conn=conn,
                conversation_id=conversation_id,
                chat_id=chat_id,
                user_id=user_id,
                sender_role="user",
                message_text=reply_text,
                telegram_message_id=update.message.message_id,
                source_email_id=None,  # Already linked in initial message
                timestamp=update.message.date
            )

            # Load conversation history to LLM
            conversation_history = get_conversation_history(conn, conversation_id, limit=10)

            if conversation_history:
                history_text = "\n".join([f"{entry['sender_role']}: {entry['message_text']}" for entry in conversation_history])
                print(f"[HANDLER] Conversation history for LLM:\n{history_text}")

                # Call Clara
                client = Clara()
                llm_response = client.readEmail(history_text)
            else:
                print(f"[WARN] No history found for conversation_id: {conversation_id}. Sending basic reply.")
                llm_response = "Hello! I don't have enough context yet."

            # Reply in GC
            bot_reply = await update.message.reply_text(llm_response)

            # Save Claras Message
            save_message_to_conversation(
                conn=conn,
                conversation_id=conversation_id,
                chat_id=chat_id,
                user_id=0,  # Bot
                sender_role="bot",
                message_text=llm_response,
                telegram_message_id=bot_reply.message_id,  # Will get assigned after sending the message
                source_email_id=None,
                timestamp=datetime.now(timezone.utc)  # Use current UTC time
            )
        
        else:
            # If no conversation_id is found, you may want to ignore or warn
            print(f"[WARN] No conversation_id found for reply to message_id {original_message_id}")
            await update.message.reply_text("Sorry, I could not link this reply to a known conversation. Please reply directly to a Clara message!")
       
