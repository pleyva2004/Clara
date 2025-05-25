# Clara ( Conversational Language AI Response Assistant )

# Telgram-bot Branch

This repository was made with the intentions of assisting on Campus Organizations with email management. Allowing students to focus on academics and influence.

## `connect_telegram(session: str, id: int, hash: str) -> TelegramClient`

Connects to the Telegram client using a saved session or prompts for login if it’s the first run.

**Parameters:**
1. session (str): Name of the session file (e.g., 'session_name').
2. id (int): Your Telegram API ID from [my.telegram.org](my.telegram.org).
3. hash (str): Your Telegram API hash.

**Returns: TelegramClient – A connected Telethon client instance.**

## `isGroup(client: TelegramClient, group_name: str) -> Optional[Dialog]`
Checks if a group with the given name already exists in the account’s dialog list.

**Parameters:**
1. client (TelegramClient): A connected Telethon client.
2. group_name (str): The name of the group to search for.

**Returns: Optional[Dialog] – The group dialog if it exists, otherwise None.**

## `create_group(client: TelegramClient, group_name: str, usernames: List[str]) -> Optional[Channel]`
Creates a supergroup and optionally invites a list of users.

**Parameters:**
1. client (TelegramClient): A connected Telethon client.
2. group_name (str): Title of the supergroup to be created.
3. usernames (List[str]): A list of @usernames to invite.

**Returns: Optional[Channel] – The created supergroup or None if creation fails.**

## `add_users_to_group(client: TelegramClient, group: Channel, usernames: List[str]) -> None:`
Invites a list of users to an existing supergroup.

**Parameters:**
1. client (TelegramClient): A connected Telethon client.
2. group (Channel): The supergroup where users will be invited.
3. usernames (List[str]): A list of @usernames to invite.

**Returns: None.**

## `bot_get_admin(client: TelegramClient, group: Channel, bot: List[str]) -> None:`
Gives a Telegram bot admin role in a supergroup with specific permissions.

**Parameters:**
1. client (TelegramClient): A connected Telethon client.
2. group (Channel): The target supergroup.
3. bot (List[str]): A list containing the bot’s username (e.g., ['@ClaraAssistant_bot']).

**Returns: None.**

## `send_bot_message(bot_token: str, chat_id: int, message: str) -> None`
Sends a message to a Telegram chat using the HTTP Bot API.

**Parameters:**
1. bot_token (str): The bot's API token from [@BotFather](https://telegram.me/BotFather).
2. chat_id (int): The unique ID of the target chat (e.g., -1001234567890).
3. message (str): The message to send.

**Returns: None.**

