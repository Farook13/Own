from pyrogram import filters, Client
from bot import app
from info import ADMINS, COMMAND_HANDLER, TMP_DOWNLOAD_DIRECTORY
import os

@app.on_message(filters.command("deletefile", prefixes=COMMAND_HANDLER))
async def delete_file(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply_text("Only admins can delete files!")
        return
    if len(message.command) < 2:
        await message.reply_text("Please provide a filename: /deletefile <filename>")
        return
    
    filename = message.command[1].lower()
    file_path = f"{TMP_DOWNLOAD_DIRECTORY}/{filename}"
    if os.path.exists(file_path):
        os.remove(file_path)
        await message.reply_text(f"Deleted `{filename}` successfully!")
    else:
        await message.reply_text(f"File `{filename}` not found!")