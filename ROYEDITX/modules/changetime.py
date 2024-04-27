from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters
from pymongo import MongoClient, ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient 
from ROYEDITX import application 
from ROYEDITX import db, collection, user_totals_collection, user_collection, top_global_groups_collection, top_global_groups_collection, group_user_totals_collection

async def change_time(update: Update, context: CallbackContext) -> None:
    
    user = update.effective_user
    chat = update.effective_chat
    member = await chat.get_member(user.id)

    if member.status not in ('administrator', 'creator'):
        await update.message.reply_text('❖ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ʀɪɢʜᴛsᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴍᴅs.')
        return
    try:
        
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('❖ ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ, ᴘʟᴇᴀsᴇ ᴜsᴇ ➥ /changetime ɴᴜᴍʙᴇʀ')
            return

        
        new_frequency = int(args[0])
        if new_frequency < 1:
            await update.message.reply_text('❖ ᴛʜᴇ ᴍᴇssᴀɢᴇ ғʀᴇǫᴜᴇɴᴄʏ ᴍᴜsᴛ ʙᴇ ɢʀᴇᴀᴛᴇʀ ᴛʜᴀɴ ᴏʀ ᴇǫᴜᴀʟ ᴛᴏ 100.')
            return

        
        chat_frequency = await user_totals_collection.find_one_and_update(
            {'chat_id': str(chat.id)},
            {'$set': {'message_frequency': new_frequency}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        await update.message.reply_text(f'❖ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀᴀɴᴄᴇ ғʀᴇǫᴜᴇɴᴄʏ ᴛᴏ ᴇᴠᴇʀʏ {new_frequency} ᴍᴇssᴀɢᴇ.')
    except Exception as e:
        await update.message.reply_text('❖ ғᴀɪʟᴇᴅ ᴛᴏ ᴄʜᴀɴɢᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀᴀɴᴄᴇ ғʀᴇǫᴜᴇɴᴄʏ.')


application.add_handler(CommandHandler("changetime", change_time, block=False))
