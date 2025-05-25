import requests

'''
This function connects to the telegram server to send the chat
'''

'''
Parameters:

bot_token: str
    Token of the clara bot
chat_id: str
    Id of the chat to send
message: str
    Message to send to chat via bot
'''


def send_bot_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.text)