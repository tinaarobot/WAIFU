import importlib
from itertools import groupby 
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import InlineQueryHandler,CallbackQueryHandler, ChosenInlineResultHandler
import motor.motor_asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import urllib.request
from pymongo import MongoClient, ReturnDocument
import random
from ROYEDITX import application, SUDO_USERS, collection, db, CHANNEL_ID

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name}, 
        {'$inc': {'sequence_value': 1}}, 
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']

async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        await update.message.reply_text('❖ ᴀsᴋ ᴍʏ ᴏᴡɴᴇʀ...')
        return

    try:
        args = context.args
        if len(args) != 4:
            await update.message.reply_text('❖ ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛᴇ, ᴘʟᴇᴀsᴇ ᴜsᴇ ➥ /upload ɪᴍɢ_ᴜʀʟ, ᴄʜᴀʀᴀᴄᴛᴇʀ-ɴᴀᴍᴇ, ᴀɴɪᴍᴇ-ɴᴀᴍᴇ, ʀᴀʀɪᴛʏ')
            return

        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()

        try:
            urllib.request.urlopen(args[0])
        except:
            await update.message.reply_text('❖ ɪɴᴠᴀʟɪᴅ ᴜʀʟ...')
            return

        rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟡 Legendary", 4: "🟢 Medium"}
        try:
            rarity = rarity_map[int(args[3])]
        except KeyError:
            await update.message.reply_text('❖ ɪɴᴠᴀʟɪᴅ ʀᴀʀɪᴛʏ, ᴘʟᴇᴀsᴇ ᴜsᴇ ➥ 1, 2, 3, ᴏʀ 4')
            return

        id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': args[0],
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': id
        }

        message = await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=args[0],
            caption=f'<b>❖ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴀᴍᴇ ➥</b> {character_name}\n\n<b>● ᴀɴɪᴍᴇ ɴᴀᴍᴇ ➥</b> {anime}\n<b>● ʀᴀʀɪᴛʏ ➥</b> {rarity}\n<b>● ɪᴅ ➥</b> {id}\n\n❖ ᴀᴅᴅᴇᴅ ʙʏ ➥ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
            parse_mode='HTML'
        )

        character['message_id'] = message.message_id
        await collection.insert_one(character)


        await update.message.reply_text('❖ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴅᴅᴇᴅ....')
    except Exception as e:
        await update.message.reply_text(f'❖ ᴜɴsᴜᴄᴄᴇssғᴜʟʟʏ ᴜᴘʟᴏᴀᴅᴇᴅ, ᴇʀʀᴏʀ ➥ {str(e)}')

async def delete(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        await update.message.reply_text('❖ ᴀsᴋ ᴍʏ ᴏᴡɴᴇʀ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅs.')
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('❖ ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛ, ᴘʟᴇᴀsᴇ ᴜsᴇ ➥ /delete ɪᴅ')
            return

        
        character = await collection.find_one_and_delete({'id': args[0]})

        if character:
            
            await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=character['message_id'])
            await update.message.reply_text('✦ ᴅᴏɴᴇ...')
        else:
            await update.message.reply_text('❖ ɴᴏ ᴄʜᴀʀᴀᴄᴛᴇʀ ғᴏᴜɴᴅ ᴡɪᴛʜ ɢɪᴠᴇɴ ɪᴅ.')
    except Exception as e:
        await update.message.reply_text(f'{str(e)}')

async def update(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        await update.message.reply_text("❖ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʀɪɢʜᴛs ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅs.")
        return

    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text('❖ ɪɴᴄᴏʀʀᴇᴄᴛ ғᴏʀᴍᴀᴛᴇ, ᴘʟᴇᴀsᴇ ᴜsᴇ ➥ /update ɪɴ ғɪᴇʟᴅ new_value')
            return

        # Get character by ID
        character = await collection.find_one({'id': args[0]})
        if not character:
            await update.message.reply_text('❖ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ...')
            return

        # Check if field is valid
        valid_fields = ['img_url', 'name', 'anime', 'rarity']
        if args[1] not in valid_fields:
            await update.message.reply_text(f'❖ ɪɴᴠᴀɪʟᴅ ғᴏʀᴍᴀᴛᴇ, ᴘʟᴇᴀsᴇ ᴜsᴇ ᴏɴᴇ ᴏғ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ➥ {", ".join(valid_fields)}')
            return

        # Update field
        if args[1] in ['name', 'anime']:
            new_value = args[2].replace('-', ' ').title()
        elif args[1] == 'rarity':
            rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟡 Legendary", 4: "🟢 Medium"}
            try:
                new_value = rarity_map[int(args[2])]
            except KeyError:
                await update.message.reply_text('❖ ɪɴᴠᴀʟɪᴅ ʀᴀʀɪᴛʏ, ᴘʟᴇᴀsᴇ ᴜsᴇ ➥ 1, 2, 3, ᴏʀ 4')
                return
        else:
            new_value = args[2]

        await collection.find_one_and_update({'id': args[0]}, {'$set': {args[1]: new_value}})

        
        if args[1] == 'img_url':
            await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=character['message_id'])
            message = await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=new_value,
                caption=f'<b>❖ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴀᴍᴇ ➥</b> {character["name"]}\n\n<b>● ᴀɴɪᴍᴇ ɴᴀᴍᴇ ➥</b> {character["anime"]}\n<b>● ʀᴀʀɪᴛʏ ➥</b> {character["rarity"]}\n<b>● ɪᴅ ➥</b> {character["id"]}\n\n❖ ᴜᴘᴅᴀᴛᴇᴅ ʙʏ ➥ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.find_one_and_update({'id': args[0]}, {'$set': {'message_id': message.message_id}})
        else:
            
            await context.bot.edit_message_caption(
                chat_id=CHANNEL_ID,
                message_id=character['message_id'],
                caption=f'<b>❖ ᴄʜᴀʀᴀᴄᴛᴇʀ ɴᴀᴍᴇ ➥</b> {character["name"]}\n\n<b>● ᴀɴɪᴍᴇ ɴᴀᴍᴇ ➥</b> {character["anime"]}\n<b>● ʀᴀʀɪᴛʏ ➥</b> {character["rarity"]}\n<b>● ɪᴅ ➥</b> {character["id"]}\n\n❖ ᴜᴘᴅᴀᴛᴇᴅ ʙʏ ➥ <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )

        await update.message.reply_text('❖ ᴜᴘᴅᴀᴛᴇᴅ ᴅᴏɴᴇ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ, ʙᴜᴛ sᴏᴍᴇᴛɪᴍᴇs ɪᴛ ᴛᴀᴋᴇs ᴛɪᴍᴇ ᴛᴏ ᴇᴅɪᴛ ᴄᴀᴘᴛɪᴏɴ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ, sᴏ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...')
    except Exception as e:
        await update.message.reply_text(f'⬤ ᴇʀʀᴏʀ ➥ {str(e)}')

UPLOAD_HANDLER = CommandHandler('upload', upload, block=False)
application.add_handler(UPLOAD_HANDLER)
DELETE_HANDLER = CommandHandler('delete', delete, block=False)
application.add_handler(DELETE_HANDLER)
UPDATE_HANDLER = CommandHandler('update', update, block=False)
application.add_handler(UPDATE_HANDLER)
