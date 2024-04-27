import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.ext import MessageHandler, filters
from telegram.ext import CommandHandler
from ROYEDITX import application 
from ROYEDITX import db, LOGGER_ID, OWNER_ID 
from ROYEDITX import IMG_URL, SUPPORT_CHAT, UPDATE_CHAT 
import random
collection = db['total_pm_users']


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        
        await context.bot.send_message(chat_id=LOGGER_ID, text=f"๏ <a href='tg://user?id={user_id}'>{first_name}</a> sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ", parse_mode='HTML')
    else:
        
        if user_data['first_name'] != first_name or user_data['username'] != username:
            
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    

    if update.effective_chat.type== "private":
        
        
        caption = f"""
        ***๏ ʜᴇʏ {update.effective_user.first_name}, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ᴜʜʜ !***
              
***๏ ɪ'ᴍ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴄᴏʟʟᴇᴄᴛ ʙᴏᴛ.\n\n๏ ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ɢʀᴏᴜᴘ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ 100 ᴍᴇssᴀɢᴇs ᴀɴᴅ ᴡʜᴏ ɢᴜᴇssᴇᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ's ɴᴀᴍᴇ ᴄᴏʀʀᴇᴄᴛ, ɪ ᴡɪʟʟ ᴀᴅᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪɴ ᴛʜᴀᴛ ᴜsᴇʀ's ᴄᴏʟʟᴇᴄᴛɪᴏɴ. \n\n๏ ᴛᴀᴘ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
               """
        keyboard = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f'http://t.me/Collect_emAll_Bot?startgroup=new')],
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url=f'https://t.me/{UPDATE_CHAT}'),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}')],
            [InlineKeyboardButton("ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(PHOTO_URL)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(PHOTO_URL)
        keyboard = [
            
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}')],
            
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="๏ ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !",reply_markup=reply_markup )

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    ***✦ ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs sᴇᴄᴛɪᴏɴ ✦***
    
***๏ /guess ➠ ᴛᴏ ɢᴜᴇss ᴄʜᴀʀᴀᴄᴛᴇʀ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘ).***
***๏ /fav ➠ ᴀᴅᴅ ʏᴏᴜʀ ғᴀᴠʀᴀᴛᴇ.***
***๏ /trade ➠ ᴛᴏ ᴛʀᴀᴅᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs.***
***๏ /gift ➠ ɢɪᴠᴇ ᴀɴʏ ᴄʜᴀʀᴀᴄᴛᴇʀ ғʀᴏᴍ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs).***
***๏ /collection ➠ ᴛᴏ sᴇᴇ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.***
***๏ /topgroups ➠ sᴇᴇ ᴛᴏᴘ ɢʀᴏᴜᴘs, ᴘᴘʟ ɢᴜᴇssᴇs ᴍᴏsᴛ ɪɴ ᴛʜᴀᴛ ɢʀᴏᴜᴘs.***
***๏ /top ➠ ᴛᴏᴏ sᴇᴇ ᴛᴏᴘ ᴜsᴇʀs.***
***๏ /ctop ➠ ʏᴏᴜʀ ᴄʜᴀᴛ ᴛᴏᴘ.***
***๏ /changetime ➠ ᴄʜᴀɴɢᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀ ᴛɪᴍᴇ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs).***
   """
        help_keyboard = [[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':

        caption = f"""
        ***๏ ʜᴇʏ {update.effective_user.first_name}, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ᴜʜʜ !*** 
        
***๏ ɪ ᴀᴍ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴄᴏʟʟᴇᴄᴛ ʙᴏᴛ.\n\n๏ ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ɢʀᴏᴜᴘ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ 100 ᴍᴇssᴀɢᴇs ᴀɴᴅ ᴡʜᴏ ɢᴜᴇssᴇᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ's ɴᴀᴍᴇ ᴄᴏʀʀᴇᴄᴛ, ɪ ᴡɪʟʟ ᴀᴅᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪɴ ᴛʜᴀᴛ ᴜsᴇʀ's ᴄᴏʟʟᴇᴄᴛɪᴏɴ. \n\n๏ ᴛᴀᴘ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
        """
        keyboard = [
            [InlineKeyboardButton("↻ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ↻", url=f'http://t.me/Collect_emAll_Bot?startgroup=new')],
            [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url=f'https://t.me/{UPDATE_CHAT}'),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}')],
            [InlineKeyboardButton("ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
      
