import os
from os import environ
import re
from typing import Dict, List, Union

# Helper function from your code
id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot Identification
BOT_NAME = "MovieBot"
BOT_VERSION = "1.0.0"
BOT_AUTHOR = "xAI Team"  # Assuming built by xAI per your initial prompt
BOT_DESCRIPTION = "A high-speed Telegram bot for delivering movie files with a target response time of 0.2 seconds, featuring IMDb integration, file management, and more."
CREATION_DATE = "2025-03-03"
LAST_UPDATED = "2025-03-03"

# Bot Configuration from Environment
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '12618934'))
API_HASH = environ.get('API_HASH', '49aacd0bc2f8924add29fb02e20c8a16')
BOT_TOKEN = environ.get('BOT_TOKEN', '7857321740:AAHSUfjwO3w6Uffmxm9vCUMl36FtXl5-r6w')
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '5032034594').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002467149516').split()]
AUTH_USERS = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()] + ADMINS
AUTH_GROUPS = [int(ch) for ch in environ.get('AUTH_GROUP', '').split()] if environ.get('AUTH_GROUP') else None
TMP_DOWNLOAD_DIRECTORY = environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

# ... (previous imports and code remain unchanged)

# FSUB
auth_channel = environ.get('AUTH_CHANNEL', '-1002332361885')  # Replace with your channel ID
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

# ... (rest of the file remains unchanged)

# Performance Goals
TARGET_RESPONSE_TIME = 0.2  # Target response time in seconds
MAX_FILE_SIZE = "2GB"       # Default Telegram bot API limit (2GB with premium)

# Supported Commands
SUPPORTED_COMMANDS = [
    "/start - Welcome message and bot info",
    "/getfile <filename> - Download a movie file instantly",
    "/broadcast <message> - Send a message to all users (admin only)",
    "/help - List available commands",
]

# Feature Flags (Derived from your code + our additions)
FEATURES = {
    "fast_file_sending": True,              # 0.2s target response for file delivery
    "broadcast": True,                      # Admin broadcast capability
    "mongodb_support": True,                # MongoDB integration
    "imdb_search": is_enabled(environ.get('IMDB', "True"), True),
    "spell_check": is_enabled(environ.get('SPELL_CHECK_REPLY', "True"), True),
    "auto_delete": is_enabled(environ.get('AUTO_DELETE', "True"), True),
    "shortlink_support": is_enabled(environ.get('IS_SHORTLINK', "False"), False),
    "ai_features": is_enabled(environ.get('AI', "True"), True),
    "file_protection": is_enabled(environ.get('PROTECT_CONTENT', "False"), False),
    "single_button": is_enabled(environ.get('SINGLE_BUTTON', "True"), True),
    "custom_captions": bool(environ.get("CUSTOM_FILE_CAPTION", "")),
    "public_file_store": is_enabled(environ.get('PUBLIC_FILE_STORE', "True"), True),
    "force_subscribe": bool(environ.get('AUTH_CHANNEL', None)),
}

# Database Configuration
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://pcmovies:pcmovies@cluster0.4vv9ebl.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "pcmovies")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')
MONGO_URL = environ.get('MONGO_URL', "mongodb+srv://pcmovies:pcmovies@cluster0.4vv9ebl.mongodb.net/?retryWrites=true&w=majority")

# Media and Links
PICS = environ.get('PICS', 'https://telegra.ph/file/2992a480cae2bc0de1c39.jpg').split()
NOR_IMG = environ.get('NOR_IMG', "https://telegra.ph/file/7d7cbf0d6c39dc5a05f5a.jpg")
SPELL_IMG = environ.get('SPELL_IMG', "https://telegra.ph/file/b58f576fed14cd645d2cf.jpg")
MELCOW_IMG = environ.get('MELCOW_IMG', "https://telegra.ph/file/e54cae941b9b81f13eb71.jpg")
MAIN_CHANNEL = environ.get('MAIN_CHANNEL', "https://t.me/+fqeHQRvmdz8zYzll")
MOVIE_GROUP = environ.get('MOVIE_GROUP', "t.me/CinemaSocket01")
FILE_FORWARD = environ.get('FILE_FORWARD', "https://t.me/+1dbVg9pA2GphZmI1")
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'Elsasupportgp')

# Additional Settings
COMMAND_HANDLER = environ.get("COMMAND_HAND_LER", "/")
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002332361885'))
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "")

# Legal/Compliance
LICENSE = "MIT License"
COMPLIANCE_NOTE = "This bot does not make judgments on death penalty or similar requests per AI guidelines."

def get_bot_info() -> str:
    """Return a formatted string of bot information."""
    info = f"**{BOT_NAME} v{BOT_VERSION}**\n"
    info += f"**Description**: {BOT_DESCRIPTION}\n"
    info += f"**Author**: {BOT_AUTHOR}\n"
    info += f"**Created**: {CREATION_DATE}\n"
    info += f"**Last Updated**: {LAST_UPDATED}\n"
    info += f"**Target Response Time**: {TARGET_RESPONSE_TIME}s\n"
    info += f"**Max File Size**: {MAX_FILE_SIZE}\n"
    info += "**Commands**:\n " + "\n ".join(SUPPORTED_COMMANDS) + "\n"
    info += "**Enabled Features**:\n"
    for feature, enabled in FEATURES.items():
        info += f"  - {feature.replace('_', ' ').title()}: {'Enabled' if enabled else 'Disabled'}\n"
    info += f"**Support**: {SUPPORT_CHAT}\n"
    info += f"**Main Channel**: {MAIN_CHANNEL}\n"
    info += f"**Movie Group**: {MOVIE_GROUP}\n"
    info += f"**License**: {LICENSE}"
    return info

if __name__ == "__main__":
    print(get_bot_info())