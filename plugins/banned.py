from telegram import Update
from telegram.ext import ContextTypes

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == YOUR_ADMIN_ID:  # Replace with actual admin check
        await update.message.reply_text("User banned!")
