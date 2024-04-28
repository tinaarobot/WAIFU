from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient 
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultPhoto, InputTextMessageContent
from collections import Counter
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import enums
from ROYEDITX import db, collection, top_global_groups_collection, group_user_totals_collection, user_collection, user_totals_collection
from ROYEDITX import ROY




pending_trades = {}


@ROY.on_message(filters.command("trade"))
async def trade(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("❖ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀᴅᴇ ᴀ ᴄʜᴀʀᴀᴄᴛᴇʀ.")
        return

    receiver_id = message.reply_to_message.from_user.id

    if sender_id == receiver_id:
        await message.reply_text("❖ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴛʀᴀᴅᴇ ᴀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴡɪᴛʜ ʏᴏᴜʀsᴇʟғ.")
        return

    if len(message.command) != 3:
        await message.reply_text("❖ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴛᴡᴏ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ,s.")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    sender = await user_collection.find_one({'id': sender_id})
    receiver = await user_collection.find_one({'id': receiver_id})

    sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
    receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

    if not sender_character:
        await message.reply_text("❖ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ʏᴏᴜ'ʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴛʀᴀᴅᴇ.")
        return

    if not receiver_character:
        await message.reply_text("❖ ᴛʜᴇ ᴏᴛʜᴇʀ ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ, ᴛʜᴇʏ ᴀʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴛʀᴀᴅᴇ.")
        return

    # Rest of your code...




    if len(message.command) != 3:
        await message.reply_text("❖  ➥ /trade [ʏᴏᴜʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ] [ᴏᴛʜᴇʀ ᴜsᴇʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ]")
        return

    sender_character_id, receiver_character_id = message.command[1], message.command[2]

    # Add the trade offer to the pending trades
    pending_trades[(sender_id, receiver_id)] = (sender_character_id, receiver_character_id)

    # Create a confirmation button
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ᴄᴏɴғɪʀᴍ ᴛʀᴀᴅᴇ", callback_data="confirm_trade")],
            [InlineKeyboardButton("ᴄᴀɴᴄᴇʟ ᴛʀᴀᴅᴇ", callback_data="cancel_trade")]
        ]
    )

    await message.reply_text(f"❖ {message.reply_to_message.from_user.mention}, ᴅᴏ ʏᴏᴜ ᴀᴄᴄᴇᴘᴛ ᴛʜɪs ᴛʀᴀᴅᴇ ?", reply_markup=keyboard)


@ROY.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_trade", "cancel_trade"]))
async def on_callback_query(client, callback_query):
    receiver_id = callback_query.from_user.id

    # Find the trade offer
    for (sender_id, _receiver_id), (sender_character_id, receiver_character_id) in pending_trades.items():
        if _receiver_id == receiver_id:
            break
    else:
        await callback_query.answer("❖ ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ.", show_alert=True)
        return

    if callback_query.data == "confirm_trade":
        # Perform the trade
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        sender_character = next((character for character in sender['characters'] if character['id'] == sender_character_id), None)
        receiver_character = next((character for character in receiver['characters'] if character['id'] == receiver_character_id), None)

        # Remove the characters from the users' collections
        sender['characters'].remove(sender_character)
        receiver['characters'].remove(receiver_character)

        # Update the users' collections in the database
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        # Add the characters to the other users' collections
        sender['characters'].append(receiver_character)
        receiver['characters'].append(sender_character)

        # Update the users' collections in the database again
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})
        await user_collection.update_one({'id': receiver_id}, {'$set': {'characters': receiver['characters']}})

        # Remove the trade offer from the pending trades
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"❖ ʏᴏᴜ ʜᴀᴠᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴛʀᴀᴅᴇ ʏᴏᴜʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴡɪᴛʜ ➥ {callback_query.message.reply_to_message.from_user.mention} !")

    elif callback_query.data == "cancel_trade":
        # Remove the trade offer from the pending trades
        del pending_trades[(sender_id, receiver_id)]

        await callback_query.message.edit_text("❌️ ᴄᴀɴᴄᴇʟʟᴇᴅ...")



# This dictionary will hold the gift offers until they are confirmed or cancelled
pending_gifts = {}


@ROY.on_message(filters.command("gift"))
async def gift(client, message):
    sender_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text("❖ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴀ ᴜsᴇʀs's ᴍᴇssᴀɢᴇ ᴛᴏ ɢɪғᴛ ᴀ ᴄʜᴀʀᴀᴄᴛᴇʀ.")
        return

    receiver_id = message.reply_to_message.from_user.id
    receiver_username = message.reply_to_message.from_user.username
    receiver_first_name = message.reply_to_message.from_user.first_name

    if sender_id == receiver_id:
        await message.reply_text("❖ ʏᴏᴜ ᴄᴀɴ'ᴛ ɢɪғᴛ ᴀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴛᴏ ʏᴏᴜʀsᴇʟғ.")
        return

    if len(message.command) != 2:
        await message.reply_text("❖ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ.")
        return

    character_id = message.command[1]

    sender = await user_collection.find_one({'id': sender_id})

    character = next((character for character in sender['characters'] if character['id'] == character_id), None)

    if not character:
        await message.reply_text("❖ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜɪs ᴄʜᴀʀᴀᴄᴛᴇʀ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")
        return

    # Add the gift offer to the pending gifts
    pending_gifts[(sender_id, receiver_id)] = {
        'character': character,
        'receiver_username': receiver_username,
        'receiver_first_name': receiver_first_name
    }

    # Create a confirmation button
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ᴄᴏɴғɪʀᴍ ɢɪғᴛ", callback_data="confirm_gift")],
            [InlineKeyboardButton("ᴄᴀɴᴄᴇʟ ɢɪғᴛ", callback_data="cancel_gift")]
        ]
    )

    await message.reply_text(f"❖ ᴅᴏ ʏᴏᴜ ʀᴇᴀʟʟʏ ᴡᴀɴɴᴀ ᴛᴏ ɢɪғᴛ ➥ {message.reply_to_message.from_user.mention}?", reply_markup=keyboard)

@ROY.on_callback_query(filters.create(lambda _, __, query: query.data in ["confirm_gift", "cancel_gift"]))
async def on_callback_query(client, callback_query):
    sender_id = callback_query.from_user.id

    # Find the gift offer
    for (_sender_id, receiver_id), gift in pending_gifts.items():
        if _sender_id == sender_id:
            break
    else:
        await callback_query.answer("❖ ᴛʜɪs ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ.", show_alert=True)
        return

    if callback_query.data == "confirm_gift":
        # Perform the gift
        sender = await user_collection.find_one({'id': sender_id})
        receiver = await user_collection.find_one({'id': receiver_id})

        # Remove the character from the sender's collection
        sender['characters'].remove(gift['character'])
        await user_collection.update_one({'id': sender_id}, {'$set': {'characters': sender['characters']}})

        # Add the character to the receiver's collection
        if receiver:
            await user_collection.update_one({'id': receiver_id}, {'$push': {'characters': gift['character']}})
        else:
            # Create new user document
            await user_collection.insert_one({
                'id': receiver_id,
                'username': gift['receiver_username'],
                'first_name': gift['receiver_first_name'],
                'characters': [gift['character']],
            })

        # Remove the gift offer from the pending gifts
        del pending_gifts[(sender_id, receiver_id)]

        await callback_query.message.edit_text(f"❖ ʏᴏᴜ ʜᴀᴠᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ɢɪғᴛᴇᴅ ʏᴏᴜʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴛᴏ ➥ [{gift['receiver_first_name']}](tg://user?id={receiver_id})")


