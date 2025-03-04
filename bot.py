import asyncio
import logging
import os
import time
from pyrogram import Client, filters, enums
from info import get_bot_info, COMMAND_HANDLER, TMP_DOWNLOAD_DIRECTORY, API_ID, API_HASH, BOT_TOKEN, AUTH_CHANNEL
from aiohttp import web
from database.files_mdb import FilesDB

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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
            sleep_threshold=60,
            in_memory=True
        )
        self.files_db = FilesDB()  # Initialize database connection
        logger.info("Initialized with in-memory storage and MongoDB")

app = MovieBot()

# Force subscription check
async def check_subscription(user_id):
    """Check if the user is subscribed to AUTH_CHANNEL."""
    if not AUTH_CHANNEL:
        return True  # No force sub required if AUTH_CHANNEL is None
    try:
        member = await app.get_chat_member(AUTH_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

@app.on_message(filters.command("start", prefixes=COMMAND_HANDLER))
async def start(client, message):
    start_time = time.time()
    user_id = message.from_user.id
    if not await check_subscription(user_id):
        await message.reply_text(
            f"Please join our channel first: {AUTH_CHANNEL}\nThen send /start again.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    await message.reply_text(get_bot_info())
    logger.info(f"Start command processed in {time.time() - start_time:.3f}s")

@app.on_message(filters.document & ~filters.command([], prefixes=COMMAND_HANDLER))
async def index_file(client, message):
    """Index any document sent to the bot."""
    start_time = time.time()
    user_id = message.from_user.id
    if not await check_subscription(user_id):
        await message.reply_text(
            f"Please join our channel first: {AUTH_CHANNEL}",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    file = message.document
    file_id = file.file_id
    file_name = file.file_name or f"unnamed_{file_id[:10]}"
    
    await app.files_db.add_file(file_id, file_name)
    await message.reply_text(f"Indexed file: `{file_name}`")
    logger.info(f"Indexed file {file_name} in {time.time() - start_time:.3f}s")

@app.on_message(filters.text & ~filters.command([], prefixes=COMMAND_HANDLER))
async def search_file(client, message):
    """Search for a file by name when text is sent."""
    start_time = time.time()
    user_id = message.from_user.id
    if not await check_subscription(user_id):
        await message.reply_text(
            f"Please join our channel first: {AUTH_CHANNEL}",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    filename = message.text.strip().lower()
    file_data = await app.files_db.get_file(filename)
    
    if not file_data:
        await message.reply_text(f"File `{filename}` not found in database!")
        return
    
    file_id = file_data["file_id"]
    try:
        await message.reply_document(
            document=file_id,
            caption=f"Here’s your file: `{filename}`",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        logger.info(f"File {filename} sent in {time.time() - start_time:.3f}s")
    except Exception as e:
        await message.reply_text(f"Error sending file: {str(e)}")
        logger.error(f"Error sending {filename}: {str(e)}")

# Minimal web server for Heroku health check
async def health_check(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    port = int(os.environ.get("PORT", 8000))
    web_app = web.Application()
    web_app.add_routes([web.get('/', health_check)])
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Web server started on port {port}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    app.run()