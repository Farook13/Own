from telegram import Update
from telegram.ext import ContextTypes

async def channel_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Channel management commands coming soon!")
