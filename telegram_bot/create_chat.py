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
    result.chat[0]:
        Returns the group chat object
'''
def create_group(client, group_name, usernames):
    for dialog in client.iter_dialogs(): # Iterate through all dialogs (groups, channels, etc.) of the user
        if dialog.name == group_name: # Check if the dialog name matches the group name
            print("Group already exists.")
            return dialog
    
    # Get the users
    users = []
    for username in usernames:
        try:
            user = client.get_input_entity(username)
            users.append(user)
        except Exception as e:
            print(f"Error: {e}") # If username not found ect.

    if not users: # If no users are found
        print("No valid users found.")
        return None
    
    result = client(CreateChatRequest(
        users=users,
        title=group_name
    ))
    
    # Find and return the new group dialog
    for dialog in client.iter_dialogs():
        if dialog.name == group_name:
            return dialog

    print("Group created but not found in dialogs.")
    return None 