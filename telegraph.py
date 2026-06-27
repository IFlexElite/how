"""
/tgm  /tgt  /telegraph  /tl
Reply to any media → uploads to catbox.moe → returns permanent link.
Max file size: 200 MB.
"""
import os
import logging
import aiohttp
from telegram import constants, InlineKeyboardButton, InlineKeyboardMarkup
from client import pbot

logger    = logging.getLogger(__name__)
MAX_BYTES = 200 * 1024 * 1024          # 200 MB
CATBOX    = "https://catbox.moe/user/api.php"


async def _upload_catbox(path: str) -> tuple:
    """Upload file to catbox.moe. Returns (success: bool, url_or_error: str)."""
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=120)
        ) as sess:
            form = aiohttp.FormData()
            form.add_field("reqtype", "fileupload")
            with open(path, "rb") as f:
                form.add_field(
                    "fileToUpload", f,
                    filename=os.path.basename(path),
                    content_type="application/octet-stream",
                )
                async with sess.post(CATBOX, data=form) as r:
                    text = await r.text()
                    if r.status == 200 and text.startswith("http"):
                        return True, text.strip()
                    return False, f"HTTP {r.status}: {text[:200]}"
    except Exception as e:
        return False, str(e)


async def telegraph_handler(update, context):
    m = update.effective_message

    if not m.reply_to_message:
        await m.reply_text("❍ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇᴅɪᴀ ᴛᴏ ᴜᴘʟᴏᴀᴅ")
        return

    media     = m.reply_to_message
    file_id   = None
    file_size = 0
    file_name = "upload"

    if media.photo:
        p         = media.photo[-1]          # largest photo
        file_id   = p.file_id
        file_size = p.file_size or 0
        file_name = f"photo_{p.file_unique_id}.jpg"
    elif media.video:
        file_id   = media.video.file_id
        file_size = media.video.file_size or 0
        file_name = media.video.file_name or f"video_{media.video.file_unique_id}.mp4"
    elif media.document:
        file_id   = media.document.file_id
        file_size = media.document.file_size or 0
        file_name = media.document.file_name or f"doc_{media.document.file_unique_id}"
    elif media.audio:
        file_id   = media.audio.file_id
        file_size = media.audio.file_size or 0
        file_name = media.audio.file_name or f"audio_{media.audio.file_unique_id}.mp3"
    elif media.voice:
        file_id   = media.voice.file_id
        file_size = media.voice.file_size or 0
        file_name = f"voice_{media.voice.file_unique_id}.ogg"
    elif media.animation:
        file_id   = media.animation.file_id
        file_size = media.animation.file_size or 0
        file_name = media.animation.file_name or f"gif_{media.animation.file_unique_id}.mp4"
    elif media.sticker:
        file_id   = media.sticker.file_id
        file_size = media.sticker.file_size or 0
        file_name = f"sticker_{media.sticker.file_unique_id}.webp"
    else:
        await m.reply_text("❍ ɴᴏ sᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ ꜰᴏᴜɴᴅ ɪɴ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.")
        return

    if file_size > MAX_BYTES:
        await m.reply_text("❍ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴍᴇᴅɪᴀ ꜰɪʟᴇ ᴜɴᴅᴇʀ 200MB.")
        return

    status     = await m.reply_text("❍ ᴘʀᴏᴄᴇssɪɴɢ...")
    local_path = None

    try:
        # ── download via Pyrogram (handles large files reliably) ──
        _last = [-1]

        async def _progress(current, total):
            pct = int(current * 100 / total)
            if pct % 10 == 0 and pct != _last[0]:
                _last[0] = pct
                try:
                    await status.edit_text(
                        f"❍ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ... {pct}%",
                        parse_mode=constants.ParseMode.HTML,
                    )
                except Exception:
                    pass

        local_path = await pbot.download_media(
            file_id,
            file_name=f"/tmp/{file_name}",
            progress=_progress,
        )

        await status.edit_text("❍ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴄᴀᴛʙᴏx...")

        ok, result = await _upload_catbox(local_path)

        if ok:
            await status.edit_text(
                f"❍ ᴜᴘʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇ",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("❍ ᴏᴘᴇɴ ʟɪɴᴋ", url=result)
                ]]),
            )
        else:
            await status.edit_text(f"❍ ᴜᴘʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ\n<code>{result}</code>",
                                   parse_mode=constants.ParseMode.HTML)

    except Exception as e:
        logger.exception("telegraph_handler error")
        try:
            await status.edit_text(
                f"❍ ᴇʀʀᴏʀ: <code>{e}</code>",
                parse_mode=constants.ParseMode.HTML,
            )
        except Exception:
            pass
    finally:
        if local_path and os.path.exists(local_path):
            try:
                os.remove(local_path)
            except Exception:
                pass
