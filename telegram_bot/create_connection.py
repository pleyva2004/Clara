from telethon.sync import TelegramClient

'''
This function connects to the telegram client and only is used the first time you run the bot.
It will ask for the phone number and the code sent to the telgram app. 
The phone number is off the from +<country_code><number> (e.g. +1234567890)
'''

'''
Parameters:
session: str
    The name of the session file to be created.
id: int
    The application ID from Telegram
hash: str
    The application hash from Telegram
Returns:
    client: TelegramClient
        The connected Telegram client
'''
def connect_telegram(session, id, hash):
    client = TelegramClient(session, id, hash)
    client.start() # this handles login if needed, reuses session otherwise
    return client
