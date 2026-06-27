"""
/names @username | /names reply
Fetches name/username change history via @SangMata_BOT using the optional userbot.
Requires USERBOT_SESSION env var.
"""
import asyncio
import logging
from telegram import constants
from userbot import userbot

logger       = logging.getLogger(__name__)
SANGMATA_BOT = "@SangMata_BOT"


async def names_handler(update, context):
    m = update.effective_message

    # ── userbot not configured ──────────────────────────────────────────────
    if not userbot:
        await m.reply_text(
            "<b>ᴜꜱᴇʀʙᴏᴛ ɴᴏᴛ ᴄᴏɴꜰɪɢᴜʀᴇᴅ.</b>\n\n"
            "ᴛᴏ ᴇɴᴀʙʟᴇ <b>/names</b>:\n"
            "1. Get session string via @SessionStringBot\n"
            "2. Add to Railway Variables:\n"
            "   <code>USERBOT_SESSION = &lt;your session string&gt;</code>",
            parse_mode=constants.ParseMode.HTML,
        )
        return

    # ── resolve target user ─────────────────────────────────────────────────
    user_id = None

    if m.reply_to_message:
        ru = m.reply_to_message.from_user
        if ru:
            user_id = ru.id
        elif m.reply_to_message.sender_chat:
            await m.reply_text("ᴄᴀɴɴᴏᴛ ꜰᴇᴛᴄʜ ʜɪsᴛᴏʀʏ ꜰᴏʀ ᴄʜᴀɴɴᴇʟs.")
            return
    elif len(m.text.split()) > 1:
        arg = m.text.split()[1].strip()
        if arg.lstrip("-").isdigit():
            user_id = int(arg)
        else:
            try:
                chat = await context.bot.get_chat(arg.lstrip("@"))
                user_id = chat.id
            except Exception:
                await m.reply_text("ᴄᴏᴜʟᴅɴ'ᴛ ꜰɪɴᴅ ᴜꜱᴇʀ.")
                return
    else:
        await m.reply_text(
            "ᴜꜱᴀɢᴇ: <code>/names @username</code>\n"
            "ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ's ᴍᴇssᴀɢᴇ ᴡɪᴛʜ <code>/names</code>",
            parse_mode=constants.ParseMode.HTML,
        )
        return

    status = await m.reply_text(
        "<code>ꜰᴇᴛᴄʜɪɴɢ ɴᴀᴍᴇ ʜɪsᴛᴏʀʏ...</code>",
        parse_mode=constants.ParseMode.HTML,
    )

    try:
        # send user ID to SangMata and immediately delete our message
        sent = await userbot.send_message(SANGMATA_BOT, str(user_id))
        await sent.delete()
        await asyncio.sleep(2)

        # read SangMata's response (most recent message in that chat)
        result = None
        async for msg in userbot.get_chat_history(SANGMATA_BOT, limit=10):
            if msg.text and msg.text.strip():
                result = msg.text
                break

        if result:
            await status.edit_text(result)
        else:
            await status.edit_text("ɴᴏ ɴᴀᴍᴇ ʜɪsᴛᴏʀʏ ꜰᴏᴜɴᴅ ꜰᴏʀ ᴛʜɪs ᴜsᴇʀ.")

        # clean up chat history with SangMata (no traces left)
        try:
            from pyrogram.raw.functions.messages import DeleteHistory
            peer = await userbot.resolve_peer(SANGMATA_BOT)
            await userbot.invoke(DeleteHistory(peer=peer, max_id=0, revoke=True))
        except Exception:
            pass

    except Exception as e:
        logger.exception("names_handler error")
        await status.edit_text(
            f"<b>ᴇʀʀᴏʀ:</b> <code>{e}</code>",
            parse_mode=constants.ParseMode.HTML,
        )
