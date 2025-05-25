from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import Channel
from telethon.errors import UserPrivacyRestrictedError, UserNotMutualContactError
from typing import List

def add_users_to_group(client: TelegramClient, group: Channel, usernames: List[str]) -> None:
    if not usernames:
        print("No usernames provided to add.")
        return

    for username in usernames:
        try:
            user = client.get_input_entity(username)
            client(InviteToChannelRequest(
                channel=group,
                users=[user]  # Important: send as list
            ))
            print(f"Added {username} to group: {group.title}")
        except UserPrivacyRestrictedError:
            print(f"One or more users have privacy settings preventing invites.")
        except UserNotMutualContactError:
            print(f"One or more users must be mutual contacts.")
        except Exception as e:
            print(f"Failed to add users: {e}")
            