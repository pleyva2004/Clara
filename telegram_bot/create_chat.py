from telethon.tl.functions.messages import CreateChatRequest

'''
This function greates a group chat
Parameters:
client: The return value from connect_telegram function (The connection)
group_name: str
    The name of the group to which users will be added.
usernames: list
    A list of usernames to be added to the group. Usernames should be in the format '@username'.
Returns:
    None or Dialog:
        Returns the Dialog object
'''
def create_group(client, group_name, usernames):
    # Get the users
    users = []
    for username in usernames:
        try:
            user = client.get_input_entity(username)
            users.append(user)
        except Exception as e:
            print(f"User Error: {e}") # If username not found ect.

    if not users: # If no users are found
        print("No valid users found.")
        return None
    try:
        result = client(CreateChatRequest(
            users=users,
            title=group_name
        ))

        # Find and return the new group dialog
        for dialog in client.iter_dialogs():
            if dialog.name == group_name:
                return dialog
    except Exception as e:
        print(f"Chat Creation Error: {e}")
        return None
