from pyrogram import filters
from bot import app  # Import app from bot.py
from info import ADMINS, COMMAND_HANDLER
from database.users_chats_db import UsersChatsDB

@app.on_message(filters.command("broadcast", prefixes=COMMAND_HANDLER))
async def broadcast(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("Only admins can broadcast!")
        return
    if len(message.command) < 2:
        await message.reply_text("Please provide a message to broadcast!")
        return
    
    text = " ".join(message.command[1:])
    db = UsersChatsDB()
    users = await db.collection.find().to_list(None)  # Get all users
    
    for user in users:
        try:
            await client.send_message(user["user_id"], text)
        except Exception as e:
            print(f"Failed to send to {user['user_id']}: {e}")
    await message.reply_text(f"Broadcast sent to {len(users)} users!")