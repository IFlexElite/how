"""
Optional userbot client (Pyrogram) — required only for /names command.
Set USERBOT_SESSION in env to enable.

How to get session string:
  pip install pyrogram TgCrypto
  python -c "from pyrogram import Client; Client('s', api_id=..., api_hash='...').run()"
  # OR use StringSession generator bots: @SessionStringBot
"""
import logging
import config
from pyrogram import Client

logger  = logging.getLogger(__name__)
userbot = None

if config.USERBOT_SESSION:
    try:
        userbot = Client(
            "userbot_session",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.USERBOT_SESSION,
        )
        logger.info("Userbot client created (session string found)")
    except Exception as e:
        logger.warning("Failed to create userbot: %s", e)
        userbot = None
else:
    logger.info("USERBOT_SESSION not set — /names command will be disabled")
