import asyncio
import logging
import os
import time
from pyrogram import Client, filters, enums
from info import get_bot_info, COMMAND_HANDLER, TMP_DOWNLOAD_DIRECTORY, API_ID, API_HASH, BOT_TOKEN

# Configure logging
logging.basicConfig(
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your file storage (replace with DB in production)
AVAILABLE_FILES = {
 "movie1": f"{TMP_DOWNLOAD_DIRECTORY}/movie1.mp4",
 "movie2": f"{TMP_DOWNLOAD_DIRECTORY}/movie2.mp4",
}

class MovieBot(Client):
 def __init__(self):
 super().__init__(
 "MovieBot",
 api_id=API_ID,
 api_hash=API_HASH,
 bot_token=BOT_TOKEN,
 plugins=dict(root="plugins"),
 workdir=TMP_DOWNLOAD_DIRECTORY,
 parse_mode=enums.ParseMode.MARKDOWN,
 sleep_threshold=60
 )

app = MovieBot()

@app.on_message(filters.command("start", prefixes=COMMAND_HANDLER))
async def start(client, message):
 start_time = time.time()
 await message.reply_text(get_bot_info())
 logger.info(f"Start command processed in {time.time() - start_time:.3f}s")

@app.on_message(filters.command("getfile", prefixes=COMMAND_HANDLER))
async def get_file(client, message):
 start_time = time.time()
 if len(message.command) < 2:
 await message.reply_text("Please provide a filename: /getfile <filename>")
 return
 
 filename = message.command[1].lower()
 if filename not in AVAILABLE_FILES:
 await message.reply_text(f"File not found! Available files: {', '.join(AVAILABLE_FILES.keys())}")
 return
 
 file_path = AVAILABLE_FILES[filename]
 if not os.path.exists(file_path):
 await message.reply_text("File missing on server!")
 return
 
 try:
 await message.reply_document(
 document=file_path,
 caption=f"Here’s your file: `{filename}`",
 parse_mode=enums.ParseMode.MARKDOWN
 )
 logger.info(f"File { filename} sent in {time.time() - start_time:.3f}s")
 except Exception as e:
 await message.reply_text(f"Error sending file: {str(e)}")
 logger.error(f"Error sending {filename}: {str(e)}")

if __name__ == "__main__":
 app.run()