from telethon.sync import TelegramClient
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import Channel, ChatAdminRights
from typing import List

def bot_get_admin(client: TelegramClient, group: Channel, bot: List[str]) -> None:
    if group:
        try:
            # Define admin rights
            rights = ChatAdminRights(
                post_messages=True,
                add_admins=False,
                invite_users=True,
                change_info=False,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                manage_call=True,
                anonymous=False,
                manage_topics=True
            )

            bot = client.get_input_entity("@ClaraAssistant_bot")
            client(EditAdminRequest(
                channel=group,
                user_id=bot,
                admin_rights=rights,
                rank="Bot"
            ))
            print("Bot promoted to admin.")
        except Exception as e:
            print(f"Admin Promotion Error: {e}")
