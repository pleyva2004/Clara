import requests

def send_bot_message(bot_token: str, chat_id: int, message: str) -> None:

    if not message.strip():
        print("Message is empty, Nothing was sent.")
        return
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print("Failed to send message:", response.text)
    except requests.RequestException as e:
        print(f"Request failed: {e}")