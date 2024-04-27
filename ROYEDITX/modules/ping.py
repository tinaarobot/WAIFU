import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters

from datetime import datetime, timedelta
import time
from ROYEDITX import application, SUDO_USERS

async def ping(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        update.message.reply_text("✦ ɴᴏ ʙᴀʙʏ, ᴛʜɪs ᴄᴍᴅ ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs..")
        return
    start_time = time.time()
    message = await update.message.reply_text('⬤ ᴘɪɴɢ ᴘᴏɴɢ...')
    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 3)
    await message.edit_text(f'❖ ᴘɪɴɢ sᴛᴀᴛs ➥ {elapsed_time} ᴍs')

application.add_handler(CommandHandler("ping", ping))
