from telethon.sync import TelegramClient
from typing import Optional

def connect_telegram(session: str, id: int, hash: str) -> Optional[TelegramClient]:
    try:
        client = TelegramClient(session, id, hash)
        client.start() # this handles login if needed, reuses session otherwise
        return client
    except Exception as e:
        print(f"Client failed to connect {e}")
        return None
