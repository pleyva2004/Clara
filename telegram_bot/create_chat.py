from telethon.sync import TelegramClient
from telethon.tl.functions.channels import CreateChannelRequest, InviteToChannelRequest
from telethon.tl.types import Channel
from typing import List, Optional

def create_group(client: TelegramClient, group_name: str, usernames: List[str]) -> Optional[Channel]:

    try:
        result = client(CreateChannelRequest(
            title=group_name,
            about="Group created by bot",
            megagroup=True  #makes it a supergroup
        ))
        group = result.chats[0]  # This is the new supergroup

        print(f"Supergroup '{group.title}' created.")

        if not usernames:
            print("No usernames provided to invite.")
            return group # Still return the group if creation was successful
        
        # Get the users
        users = []
        for username in usernames:
            try:
                user = client.get_input_entity(username)
                users.append(user)
            except Exception as e:
                print(f"User Error for '{username}': {e}") # If username not found ect.

        if users:
            client(InviteToChannelRequest(channel=group, users=users))
            print(f"Invited {len(users)} users.")
        else:
            print("No valid useres to invite")
        
        return group
    
    except Exception as e:
        print(f"Chat Creation Error: {e}")
        return None
