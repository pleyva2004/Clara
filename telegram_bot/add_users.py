from telethon.tl.functions.messages import AddChatUserRequest
from telethon.errors import UserPrivacyRestrictedError, UserNotMutualContactError

'''
This function adds users to a group in Telegram.

Parameters:
client: The return value from connect_telegram function (The connection)
group_name: str
    The name of the group to which users will be added.
usernames: list
    A list of usernames to be added to the group. Usernames should be in the format '@username'.
Returns:
    None
'''
def add_users_to_group(client, group, usernames):
    if not usernames:
        print("No usernames provided to add.")
        return
    
    # Iterarte through the usernames and add them to the group
    for username in usernames:
        try:
            user = client.get_entity(username) 
            client(AddChatUserRequest(
                chat_id=group.id,
                user_id=user,
                fwd_limit=0
            ))
            print(f"Added {username} to '{group.title}'")
        except UserPrivacyRestrictedError:
            print(f"{username} has privacy settings preventing adding.")
        except UserNotMutualContactError:
            print(f"{username} must be a mutual contact.")
        except Exception as e:
            print(f"Failed to add {username}: {e}")