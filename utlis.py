import logging

logger = logging.getLogger(__name__)

async def log_action(action: str):
    logger.info(f"Action performed: {action}")
