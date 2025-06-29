from telegram import Update
from telegram.ext import ContextTypes
from llm_engineering import Clara
from telegram_bot_functions.db.conversation_utils import (
    save_message_to_conversation,
    get_thread_id_by_telegram_message_id,
    get_conversation_history,
    get_conversation_status,
    close_conversation_thread
)
from datetime import datetime, timezone
import json

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:    
    
    # Check if its a reply
    if update.message and update.message.reply_to_message:
        original_message_id = update.message.reply_to_message.message_id
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        reply_text = update.message.text
        user_name = update.effective_user.first_name

        # Find the conversation_id of the original message
        conversation_id = get_thread_id_by_telegram_message_id(chat_id, original_message_id)

        if conversation_id:
            print(f"[HANDLER] User {user_name} is replying in conversation {conversation_id}")

            # Check if the conversation is closed
            status = get_conversation_status(conversation_id)
            if status == 'closed':
                print(f"[HANDLER] Conversation {conversation_id} is closed → not processing reply.")
                await update.message.reply_text("This conversation is already closed. Please start a new thread if needed.")
                return

            # Load conversation history to LLM
            conversation_history = get_conversation_history(conversation_id, limit=10)

            if conversation_history:
                # Format the conversation history for LLM
                json_conversation_history = json.dumps(conversation_history, indent=4)
                print(f"[HANDLER] Conversation history for LLM:\n{json_conversation_history}")

                # Call Clara
                client = Clara()

                validate_user_response = client.validateResponse(reply_text, json_conversation_history)

                if  isinstance(validate_user_response, str):
                    validate_user_response_json = json.loads(validate_user_response.replace('```json\n', '').replace('\n```', '').replace('```', '')) 

                print(f"[HANDLER] Validate user response JSON: {json.dumps(validate_user_response_json, indent=4)}")
                
                action_items_in_message = ", ".join(validate_user_response_json["action_items_in_message"])
                action_items_addressed = ", ".join(validate_user_response_json["action_items_addressed"])
                missing_information_for_response = ", ".join(validate_user_response_json["missing_information"])
                suggested_corrections_for_response = ", ".join(validate_user_response_json["suggested_corrections"])
                response_score = validate_user_response_json["accuracy_score"]


                print(f"[HANDLER] Clara validation score: {response_score}")

                # Save the users reply
                save_message_to_conversation(
                    thread_id=conversation_id,
                    chat_id=chat_id,
                    user_id=user_id,
                    sender_role="user",
                    message_text=reply_text,
                    telegram_message_id=update.message.message_id,
                    source_email_id=None,  # Already linked in initial message
                    timestamp=update.message.date
                )

                if len(validate_user_response_json["missing_information"]) == 0 and response_score >= 90: # If original message was fully answered
                    print(f"Email was sent, thread closing")

                    # Close Thread
                    close_conversation_thread(conversation_id)

                    # Set llm response
                    llm_response = "This thread is now closed. Thank you!"

                    # Send Draft()
                
                else:
                    # Create a response to the user maybe what they are missing
                    llm_response = client.requestMissingInformation(reply_text, action_items_in_message, action_items_addressed, missing_information_for_response, suggested_corrections_for_response)
            else:
                print(f"[WARN] No history found for conversation_id: {conversation_id}. Sending basic reply.")
                llm_response = "Hello! I don't have enough context yet."

            # Reply in GC
            bot_reply = await update.message.reply_text(llm_response)

            # Save Claras Message
            save_message_to_conversation(
                thread_id=conversation_id,
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