from telethon.sync import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest


def create_group(id, hash, session, users, title):
    with TelegramClient(session, id, hash) as client:
        result = client(CreateChatRequest(
            users = users,
            title = title,
        ))
        print("Group created:", result.chats[0].title)

