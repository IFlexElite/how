"""
/tr handler — powered by gpytranslate (Google Translate, no API key needed).

Usage:
  /tr hi           → auto-detect source, translate to Hindi
  /tr en           → auto-detect source, translate to English
  /tr en//hi       → force source=English, translate to Hindi
  (reply to a message while using the command)
"""
import logging
from gpytranslate import Translator

logger = logging.getLogger(__name__)

_trans = Translator()


async def translate_handler(update, context):
    m         = update.effective_message
    reply_msg = m.reply_to_message

    if not reply_msg:
        await m.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ !")
        return

    to_translate = (reply_msg.caption or reply_msg.text or "").strip()
    if not to_translate:
        await m.reply_text("ɴᴏ ᴛᴇxᴛ ꜰᴏᴜɴᴅ ɪɴ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.")
        return

    # parse args
    parts = m.text.split()
    try:
        arg = parts[1].lower() if len(parts) > 1 else None
        if arg and "//" in arg:
            source, dest = arg.split("//", 1)
        elif arg:
            source = await _trans.detect(to_translate)
            dest   = arg
        else:
            source = await _trans.detect(to_translate)
            dest   = "en"
    except (IndexError, Exception):
        source = await _trans.detect(to_translate)
        dest   = "en"

    try:
        translation = await _trans(to_translate, sourcelang=source, targetlang=dest)
        reply = (
            f"ᴛʀᴀɴsʟᴀᴛᴇᴅ ꜰʀᴏᴍ <b>{source}</b> ᴛᴏ <b>{dest}</b>:\n\n"
            f"{translation.text}"
        )
        from telegram import constants
        await m.reply_text(reply, parse_mode=constants.ParseMode.HTML)
    except Exception as e:
        logger.exception("Translation failed")
        await m.reply_text(f"ᴛʀᴀɴsʟᴀᴛɪᴏɴ ꜰᴀɪʟᴇᴅ: {e}")
