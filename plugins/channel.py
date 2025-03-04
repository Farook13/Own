from pyrogram import filters
from bot import app  # Import app from bot.py
from info import COMMAND_HANDLER

@app.on_message(filters.command("channel", prefixes=COMMAND_HANDLER))
async def channel_info(client, message):
    await message.reply_text("Channel management commands coming soon!")