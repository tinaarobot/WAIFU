from itertools import groupby
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultPhoto, InputTextMessageContent, InputMediaPhoto
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from telegram import Update
from motor.motor_asyncio import AsyncIOMotorClient 
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, filters
from telegram.ext import CallbackQueryHandler
from pymongo import MongoClient, ReturnDocument
import urllib.request
from ROYEDITX import application 
from ROYEDITX import db, collection, user_totals_collection, user_collection, top_global_groups_collection, top_global_groups_collection, group_user_totals_collection
from ROYEDITX import IMG_URL, OWNER_ID
from ROYEDITX import SUDO_USERS as SUDO_USERS 
import random
import json
import html
import re

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

async def global_leaderboard(update: Update, context: CallbackContext) -> None:
    
    cursor = top_global_groups_collection.aggregate([
        {"$project": {"group_name": 1, "count": 1}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>❖ ᴛᴏᴘ 10 ɢʟᴏʙᴀʟ ɢʀᴏᴜᴘs ❖</b>\n\n"

    for i, group in enumerate(leaderboard_data, start=1):
        group_name = html.escape(group.get('group_name', 'Unknown'))

        if len(group_name) > 10:
            group_name = group_name[:15] + '...'
        count = group['count']
        leaderboard_message += f'{i}. <b>{group_name}</b> ➥ <b>{count}</b>\n'
    
    
    photo_url = random.choice(AVISHA)

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

async def ctop(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    cursor = group_user_totals_collection.aggregate([
        {"$match": {"group_id": chat_id}},
        {"$project": {"username": 1, "first_name": 1, "character_count": "$count"}},
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>❖ ᴛᴏᴘ 10 ᴜsᴇʀs ᴡɪᴛʜ ᴍᴏsᴛ ᴄʜᴀʀᴀᴄᴛᴇʀsɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➥ <b>{character_count}</b>\n'
    
    photo_url = random.choice(AVISHA)

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')


async def leaderboard(update: Update, context: CallbackContext) -> None:
    
    cursor = user_collection.aggregate([
        {"$project": {"username": 1, "first_name": 1, "character_count": {"$size": "$characters"}}},
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>❖ ᴛᴏᴘ 10 ᴜsᴇʀs ᴡɪᴛʜ ᴍᴏsᴛ ᴄʜᴀʀᴀᴄᴛᴇʀs ❖</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➥ <b>{character_count}</b>\n'
    
    photo_url = random.choice(AVISHA)

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')


async def broadcast(update: Update, context: CallbackContext) -> None:
    
    if str(update.effective_user.id) == OWNER_ID:
        
        if update.message.reply_to_message is None:
            await update.message.reply_text('❖ ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.')
            return

        
        all_users = await user_collection.find({}).to_list(length=None)
        all_groups = await group_user_totals_collection.find({}).to_list(length=None)
        
        unique_user_ids = set(user['id'] for user in all_users)
        unique_group_ids = set(group['group_id'] for group in all_groups)

        total_sent = 0
        total_failed = 0

        
        for user_id in unique_user_ids:
            try:
                await context.bot.forward_message(chat_id=user_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        
        for group_id in unique_group_ids:
            try:
                await context.bot.forward_message(chat_id=group_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'❖ ʙʀᴏᴀᴅᴄᴀsᴛ ʀᴇᴘᴏʀᴛ ❖\n\n● ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ➥ {total_sent}\n● ᴛᴏᴛᴀʟ ғᴀɪʟᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇɴᴅ ➥ {total_failed}'
        )
    else:
        await update.message.reply_text('❖ ᴏɴʟʏ ᴍᴜʀᴀᴛ ᴄᴀɴ ᴜsᴇ...')


async def stats(update: Update, context: CallbackContext) -> None:
    
    if str(update.effective_user.id) not in OWNER_ID:
        update.message.reply_text('❖ ᴏɴʟʏ ғᴏʀ sᴜᴅᴏ ᴜsᴇʀs...')
        return

    
    user_count = await user_collection.count_documents({})


    group_count = await group_user_totals_collection.distinct('group_id')


    await update.message.reply_text(f'❖ ᴍʏ ᴀɴɪᴍᴇ ʙᴏᴛ sᴛᴀᴛs ⏤͟͟͞͞★\n\n● ᴛᴏᴛᴀʟ ᴜsᴇʀs ➥ {user_count}\n● ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs ➥ {len(group_count)}\n\n❖ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➥ 『ɴʏᴋᴀᴀ』x³『ᴀɴɪᴍᴇ』♡゙')




async def send_users_document(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('❖ ᴏɴʟʏ ғᴏʀ sᴜᴅᴏ ᴜsᴇʀs...')
        return
    cursor = user_collection.find({})
    users = []
    async for document in cursor:
        users.append(document)
    user_list = ""
    for user in users:
        user_list += f"❖ {user['first_name']}\n"
    with open('users.txt', 'w') as f:
        f.write(user_list)
    with open('users.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('users.txt')

async def send_groups_document(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('❖ ᴏɴʟʏ ғᴏʀ sᴜᴅᴏ ᴜsᴇʀs...')
        return
    cursor = top_global_groups_collection.find({})
    groups = []
    async for document in cursor:
        groups.append(document)
    group_list = ""
    for group in groups:
        group_list += f"❖ {group['group_name']}\n"
        group_list += "\n"
    with open('groups.txt', 'w') as f:
        f.write(group_list)
    with open('groups.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('groups.txt')


application.add_handler(CommandHandler('ctop', ctop, block=False))
application.add_handler(CommandHandler('stats', stats, block=False))
application.add_handler(CommandHandler('TopGroups', global_leaderboard, block=False))

application.add_handler(CommandHandler('list', send_users_document, block=False))
application.add_handler(CommandHandler('groups', send_groups_document, block=False))


application.add_handler(CommandHandler('top', leaderboard, block=False))
application.add_handler(CommandHandler('broadcast', broadcast, block=False))

