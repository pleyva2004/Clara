from telethon.tl.types import UpdateChatParticipants

def get_chat_id(result):
    for upd in result.updates.updates:
            if isinstance(upd, UpdateChatParticipants):
                chat_id = upd.participants.chat_id
                print("Chat ID (from participants):", chat_id)