from create_connection import connect_telegram
from create_chat import create_group
from add_users import add_users_to_group
from send_messages import send_bot_message
from group_exists import isGroup

if __name__ == "__main__":
    app_id = 24829326
    api_hash = '4bc9bc068c98b8ed0ad8841e410a64a1'
    session_name = 'session_name'
    group_name = 'Clara Test'
    intial_users = ['@liorbiton', '@pabloleyvasegundo']
    more_users = []
    message = "hola familia"
    bot_token = "7787836012:AAEzqQqi1JpCFlKqdn4gBBZIxlFoAgF0ddk"

    print("Connecting to telegram...")
    client = connect_telegram(session_name, app_id, api_hash)

    print("Checking group...")
    group = isGroup(client, group_name)
    
    if group:
        print("adding more users...")
        add_users_to_group(client, group, more_users)
        
    else:
        print("Creating group...")
        group = create_group(client, group_name, intial_users)

    chat_id = client.get_entity(group_name) # Gets the basic group id
    chat_id = "-100" + str(chat_id.id) # Add -100 because super group requires it
    
    # Send the message
    print("Sending Message")
    send_bot_message(bot_token, chat_id, message)
    print(f"Message sent to {group!r}")

    # Clean up
    client.disconnect()