import asyncio
import logging
from aiohttp import web
from telegram import Update, constants
from telegram.ext import Application, CommandHandler, ContextTypes

import config
from client import pbot
from userbot import userbot
from info      import chat_info_handler, user_info_handler, id_handler, members_handler
from translate import translate_handler
from telegraph import telegraph_handler
from sangmata  import names_handler

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ─── /start ──────────────────────────────────────────────────────────────────
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "<b>ɪɴꜰᴏ ʙᴏᴛ — ʙʏ SayaProject</b>\n"
        "<b>━━━━━━━━━━━━━━━━</b>\n"
        "<b>/user</b> <code>@username</code>  — ᴜꜱᴇʀ ɪɴꜰᴏ\n"
        "<b>/chat</b> <code>-100xxx</code>   — ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ ɪɴꜰᴏ\n"
        "<b>/id</b>                          — ɢᴇᴛ ɪᴅꜱ (ᴜꜱᴇʀ, ᴄʜᴀᴛ, ᴍꜱɢ, ᴍᴇᴅɪᴀ)\n"
        "<b>/members</b>                     — ʟɪꜱᴛ ᴀʟʟ ᴜꜱᴇʀ ɪᴅꜱ ɪɴ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ\n"
        "<b>/tr</b> <code>hi</code>          — ᴛʀᴀɴꜱʟᴀᴛᴇ ʀᴇᴘʟɪᴇᴅ ᴍꜱɢ (ʀᴇᴘʟʏ ʀᴇǫᴜɪʀᴇᴅ)\n"
        "<b>/tr</b> <code>en//hi</code>      — ꜰᴏʀᴄᴇ ꜱᴏᴜʀᴄᴇ → ᴛᴀʀɢᴇᴛ\n"
        "<b>/tl</b>                          — ᴜᴘʟᴏᴀᴅ ʀᴇᴘʟɪᴇᴅ ᴍᴇᴅɪᴀ ᴛᴏ ᴄᴀᴛʙᴏx.ᴍᴏᴇ\n"
        "<b>/names</b> <code>@user</code>    — ɴᴀᴍᴇ/ᴜꜱᴇʀɴᴀᴍᴇ ʜɪꜱᴛᴏʀʏ\n"
        "<b>━━━━━━━━━━━━━━━━</b>",
        parse_mode=constants.ParseMode.HTML,
    )


# ─── HEALTH SERVER ────────────────────────────────────────────────────────────
async def run_health_server():
    _ok = lambda r: web.Response(text="OK")
    for port in [config.PORT, config.PORT + 1, 8080, 8443, 5000]:
        try:
            app = web.Application()
            app.router.add_get("/",       _ok)
            app.router.add_get("/health", _ok)
            runner = web.AppRunner(app)
            await runner.setup()
            await web.TCPSite(runner, "0.0.0.0", port).start()
            logger.info("Health server: port %d", port)
            return
        except OSError:
            continue
    logger.warning("No free port for health server")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
async def main():
    # start Pyrogram bot client
    await pbot.start()
    logger.info("Pyrogram bot OK")

    # start optional userbot (for /names)
    if userbot:
        await userbot.start()
        logger.info("Userbot OK")

    # build PTB app
    app = Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",                         start_handler))
    app.add_handler(CommandHandler(["user", "info"],                user_info_handler))
    app.add_handler(CommandHandler(["chat", "ginfo"],               chat_info_handler))
    app.add_handler(CommandHandler("id",                            id_handler))
    app.add_handler(CommandHandler("members",                       members_handler))
    app.add_handler(CommandHandler("tr",                            translate_handler))
    app.add_handler(CommandHandler(["tgm", "tgt", "telegraph", "tl"], telegraph_handler))
    app.add_handler(CommandHandler("names",                         names_handler))

    await run_health_server()
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    logger.info("Bot live — polling")

    try:
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        if userbot:
            await userbot.stop()
        await pbot.stop()


if __name__ == "__main__":
    asyncio.run(main())
