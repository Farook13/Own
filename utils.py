import logging
from pyrogram import Client

logger = logging.getLogger(__name__)

async def log_action(client: Client, action: str):
    logger.info(f"Action performed: {action}")