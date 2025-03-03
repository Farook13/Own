import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import time

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store files in a simple dictionary (in production, use a database)
AVAILABLE_FILES = {
    "movie1": "path/to/movie1.mp4",
    "movie2": "path/to/movie2.mp4",
    # Add more files as needed
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command with fast response."""
    start_time = time.time()
    await update.message.reply_text('Welcome to Movie Bot! Use /getfile <filename> to download.')
    logger.info(f"Start command processed in {time.time() - start_time:.3f} seconds")

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send requested file with minimal delay."""
    start_time = time.time()
    
    # Get filename from command
    if not context.args:
        await update.message.reply_text("Please provide a filename: /getfile <filename>")
        return
    
    filename = context.args[0].lower()
    
    # Check if file exists in our dictionary
    if filename not in AVAILABLE_FILES:
        await update.message.reply_text("File not found! Available files: " + ", ".join(AVAILABLE_FILES.keys()))
        return
    
    file_path = AVAILABLE_FILES[filename]
    
    # Verify file exists on disk
    if not os.path.exists(file_path):
        await update.message.reply_text("Sorry, file is missing on the server!")
        return
    
    # Send file asynchronously
    try:
        with open(file_path, 'rb') as file:
            await update.message.reply_document(
                document=file,
                filename=os.path.basename(file_path),
                caption=f"Here's your file: {filename}"
            )
        logger.info(f"File {filename} sent in {time.time() - start_time:.3f} seconds")
    except Exception as e:
        await update.message.reply_text(f"Error sending file: {str(e)}")
        logger.error(f"Error sending file: {str(e)}")

async def main():
    """Main bot setup with optimized configuration."""
    # Replace 'YOUR_BOT_TOKEN' with your actual Telegram bot token
    application = Application.builder().token('YOUR_BOT_TOKEN').build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getfile", get_file))
    
    # Start the bot with polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling(
        drop_pending_updates=True,  # Skip old updates for faster startup
        poll_interval=0.1,         # Check for updates frequently
        timeout=10                 # Quick timeout for requests
    )

if __name__ == '__main__':
    asyncio.run(main())
