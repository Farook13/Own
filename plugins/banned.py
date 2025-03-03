from pyrogram import filters, Client
from info import ADMINS, COMMAND_HANDLER

@app.on_message(filters.command("ban", prefixes=COMMAND_HANDLER))
async def ban_user(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("Only admins can ban users!")
        return
    if not message.reply_to_message:
        await message.reply_text("Reply to a user’s message to ban them!")
        return
    user_id = message.reply_to_message.from_user.id
    # Add ban logic (e.g., update database)
    await message.reply_text(f"User {user_id} banned!")