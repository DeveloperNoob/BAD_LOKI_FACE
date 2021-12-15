from pyrogram import Client, filters

from config import Config


@Client.on_message(
    filters.private
    & filters.command("broadcast")
    & filters.user(Config.ADMINS)
    & filters.reply
)
async def broadcast_(c, m):
    await c.start_broadcast(
        broadcast_message=m.reply_to_message, admin_id=m.from_user.id
    )
