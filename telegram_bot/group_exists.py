
'''
This checks to see if the group was created or not. If it was not created then return None otherwise return the chat dialog object
'''

'''
Parameters:
client: TelegramObject
    The return value from connect_telegram function (The connection)
group_name: str
    The name of the Telegram Group
Returns:
    client: Dialog Object or None
'''

def isGroup(client, group_name):
    for dialog in client.iter_dialogs(): # Iterate through all dialogs (groups, channels, etc.) of the user
        if dialog.name == group_name: # Check if the dialog name matches the group name
            print("Group already exists.")
            return dialog
    return None