from telethon.sync import TelegramClient

def connect_telegram(session: str, id: int, hash: str) -> TelegramClient:
    client = TelegramClient(session, id, hash)
    client.start() # this handles login if needed, reuses session otherwise
    return client
