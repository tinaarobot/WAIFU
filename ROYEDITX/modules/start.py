import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.ext import MessageHandler, filters
from telegram.ext import CommandHandler
from ROYEDITX import application 
from ROYEDITX import db, LOGGER_ID, OWNER_ID 
from ROYEDITX import IMG_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME
import random

#####
AVISHA = [
"https://graph.org/file/eaa3a2602e43844a488a5.jpg",
"https://graph.org/file/b129e98b6e5c4db81c15f.jpg",
"https://graph.org/file/3ccb86d7d62e8ee0a2e8b.jpg",
"https://graph.org/file/df11d8257613418142063.jpg",
"https://graph.org/file/9e23720fedc47259b6195.jpg",
"https://graph.org/file/826485f2d7db6f09db8ed.jpg",
"https://graph.org/file/ff3ad786da825b5205691.jpg",
"https://graph.org/file/52713c9fe9253ae668f13.jpg",
"https://graph.org/file/8f8516c86677a8c91bfb1.jpg",
"https://graph.org/file/6603c3740378d3f7187da.jpg",
"https://graph.org/file/66cb6ec40eea5c4670118.jpg",
"https://graph.org/file/2e3cf4327b169b981055e.jpg",
]

####

collection = db['total_pm_users']


async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        
        await context.bot.send_message(chat_id=LOGGER_ID, text=f"❖ <a href='tg://user?id={user_id}'>{first_name}</a> sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ", parse_mode='HTML')
    else:
        
        if user_data['first_name'] != first_name or user_data['username'] != username:
            
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    

    if update.effective_chat.type== "private":
        
        
        caption = f"""
        ***❖ ʜᴇʏ {update.effective_user.first_name}, ᴡᴇʟᴄᴏᴍᴇ ʙᴀʙʏ ♥︎***
              
***● ɪ'ᴍ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴄᴏʟʟᴇᴄᴛ ʙᴏᴛ.\n\n● ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ɢʀᴏᴜᴘ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ 100 ᴍᴇssᴀɢᴇs ᴀɴᴅ ᴡʜᴏ ɢᴜᴇssᴇᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ's ɴᴀᴍᴇ ᴄᴏʀʀᴇᴄᴛ, ɪ ᴡɪʟʟ ᴀᴅᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪɴ ᴛʜᴀᴛ ᴜsᴇʀ's ᴄᴏʟʟᴇᴄᴛɪᴏɴ. \n\n❖ ᴛᴀᴘ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
               """
        keyboard = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f'https://t.me/HLO_PAPA'),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}')],
            [InlineKeyboardButton("ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(AVISHA)

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(AVISHA)
        keyboard = [
            
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}')],
            
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="❖ ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ !",reply_markup=reply_markup )

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
    ***❖ ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs sᴇᴄᴛɪᴏɴ ❖***
    
***⬤ /guess ➥ ᴛᴏ ɢᴜᴇss ᴄʜᴀʀᴀᴄᴛᴇʀ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘ).***
***⬤ /fav ➥ ᴀᴅᴅ ʏᴏᴜʀ ғᴀᴠʀᴀᴛᴇ.***
***⬤ /trade ➥ ᴛᴏ ᴛʀᴀᴅᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs.***
***⬤ /gift ➥ ɢɪᴠᴇ ᴀɴʏ ᴄʜᴀʀᴀᴄᴛᴇʀ ғʀᴏᴍ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs).***
***⬤ /collection ➥ ᴛᴏ sᴇᴇ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.***
***⬤ /topgroups ➥ sᴇᴇ ᴛᴏᴘ ɢʀᴏᴜᴘs, ᴘᴘʟ ɢᴜᴇssᴇs ᴍᴏsᴛ ɪɴ ᴛʜᴀᴛ ɢʀᴏᴜᴘs.***
***⬤ /top ➥ ᴛᴏᴏ sᴇᴇ ᴛᴏᴘ ᴜsᴇʀs.***
***⬤ /ctop ➥ ʏᴏᴜʀ ᴄʜᴀᴛ ᴛᴏᴘ.***
***⬤ /changetime ➥ ᴄʜᴀɴɢᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀ ᴛɪᴍᴇ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs).***
   """
        help_keyboard = [[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':

        caption = f"""
        ***❖ ʜᴇʏ {update.effective_user.first_name}, ᴡᴇʟᴄᴏᴍᴇ ʙᴀʙʏ ♥︎*** 
        
***● ɪ ᴀᴍ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴄᴏʟʟᴇᴄᴛ ʙᴏᴛ.\n\n● ɪ ᴡɪʟʟ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʜᴀʀᴀᴄᴛᴇʀs ɪɴ ɢʀᴏᴜᴘ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ 100 ᴍᴇssᴀɢᴇs ᴀɴᴅ ᴡʜᴏ ɢᴜᴇssᴇᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ's ɴᴀᴍᴇ ᴄᴏʀʀᴇᴄᴛ, ɪ ᴡɪʟʟ ᴀᴅᴅ ᴛʜᴀᴛ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪɴ ᴛʜᴀᴛ ᴜsᴇʀ's ᴄᴏʟʟᴇᴄᴛɪᴏɴ. \n\n❖ ᴛᴀᴘ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ sᴇᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs.***
        """
        keyboard = [
            [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f'https://t.me/hlo_papa'),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=f'https://t.me/{SUPPORT_CHAT}')],
            [InlineKeyboardButton("ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
      
