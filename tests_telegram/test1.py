from telegram_bot.create_connection import connect_telegram
from telegram_bot.group_exists import isGroup
from telegram_bot.create_chat import create_group
from telegram_bot.add_users import add_users_to_group
from telegram_bot.bot_permissions import bot_get_admin
from telegram_bot.send_messages import send_bot_message
from dotenv import load_dotenv
import os

if __name__ == "__main__":

    load_dotenv()

    app_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    session_name = 'session_name'
    group_name = 'Clara Test'
    intial_users = []
    bot = ['@ClaraAssistant_bot']
    more_users = ['@ClaraAssistant_bot', '@pabloleyvasegundo']
    message = "hola familia"
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    print("Connecting to telegram...")
    client = connect_telegram(session_name, app_id, api_hash)

    print("Checking group...")
    group = isGroup(client, group_name)
    
    if not group:
        print("Creating group...")
        group = create_group(client, group_name, intial_users)

    print("adding more users...")
    add_users_to_group(client, group, more_users)

    print("Giving bot permissions...")
    bot_get_admin(client, group, bot)


    chat_id = client.get_entity(group_name) # Gets the basic group id
    chat_id = "-100" + str(chat_id.id) # Add -100 because super group requires it
    
    # Send the message
    print("Sending Message...")
    send_bot_message(bot_token, chat_id, message)
    print(f"Message sent to {group!r}")

    # Clean up
    client.disconnect()