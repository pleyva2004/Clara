from telethon.sync import TelegramClient
from telethon.tl.custom.dialog import Dialog
from typing import Optional

def isGroup(client: TelegramClient, group_name: str) -> Optional[Dialog]:
    for dialog in client.iter_dialogs(): # Iterate through all dialogs (groups, channels, etc.) of the user
        if dialog.name == group_name: # Check if the dialog name matches the group name
            print("Group already exists.")
            return dialog
    return None
