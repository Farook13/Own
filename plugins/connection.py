from telegram import Update
from telegram.ext import ContextTypes

async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Connected to chat!")
