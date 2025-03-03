from pyrogram import filters, Client
from info import SUPPORTED_COMMANDS, COMMAND_HANDLER

@app.on_message(filters.command("help", prefixes=COMMAND_HANDLER))
async def help_command(client, message):
    await message.reply_text(
        "**Available Commands**:\n" + "\n".join(SUPPORTED_COMMANDS),
        parse_mode=enums.ParseMode.MARKDOWN
    )