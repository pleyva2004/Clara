import requests

def send_bot_message(bot_token: str, chat_id: int, message: str) -> int:

    if not message.strip():
        print("Message is empty, Nothing was sent.")
        return None
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            message_id = data["result"]["message_id"]
            print(f"Message sent successfully! Message ID: {message_id}")
            return message_id
        else:
            print("Failed to send message:", response.text)
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None