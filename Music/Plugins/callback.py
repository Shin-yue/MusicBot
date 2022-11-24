# Copyright by https://github.com/riz-ex
# At some point, i used to wish i would disappear from this world. The whole world seemed so dark and i cried every night
import asyncio
import os
import random
import re
from asyncio import QueueEmpty
# try with your ability.
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
# repository stuff
from Music import app
from Music import aiohttpsession as session
from Music.MusicUtilities.database.queue import is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off
from Music.MusicUtilities.tgcallsrun import music, convert, download, clear, get, is_empty, put, task_done


pattern = re.compile(
    r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$"
)

flex = {}


async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False


@app.on_callback_query(filters.regex(pattern=r"ppcl"))
async def closesmex(_, query: CallbackQuery):
    callback_data = query.data.strip()
    chat_id = query.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = query.from_user.id
    try:
        smex, user_id = callback_request.split("|")
    except Exception as e:
        await query.message.edit(f"❌ an error occured\n\n**reason:** `{e}`")
        return
    if query.from_user.id != int(user_id):
        await query.answer("💡 sorry this is not your request", show_alert=True)
        return
    await query.message.delete()


@app.on_callback_query(filters.regex("pausevc"))
async def pausevc(_, query: CallbackQuery):
    a = await app.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "you don't have the required permission to perform this action.\npermission: manage voice chats",
            show_alert=True)
    checking = query.from_user.first_name
    chat_id = query.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await music.pytgcalls.pause_stream(chat_id)
            await music_off(chat_id)
            await query.answer(f"music is paused")
        else:
            await query.answer(f"no music playing!")
            return
    else:
        await query.answer(f"nothing's playing on music!")


@app.on_callback_query(filters.regex(pattern=r"other"))
async def closesmex(_, query: CallbackQuery):
    callback_data = query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    await query.answer("menu opened")
    userid = query.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = others_markup(videoid, user_id)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(pattern=r"goback"))
async def goback(_, query: CallbackQuery):
    callback_data = query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    await query.answer("menu closed")
    userid = query.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = play_markup(videoid, user_id)
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(pattern=r"good"))
async def good(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id
    videoid, user_id = callback_request.split("|")
    buttons = gets(videoid, user_id)
    await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("close"))
async def close_admin(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
          "💡 Only admin with manage video chat permission that can tap this button !", show_alert=True
        )
    await query.message.delete()


@app.on_callback_query(filters.regex("ngentod"))
async def ngentod(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex(pattern=r"down"))
async def down(_, CallbackQuery):
    await CallbackQuery.answer()


@app.on_callback_query(filters.regex("endvc"))
async def endvc(_, query: CallbackQuery):
    a = await app.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer(
            "You don't have the required permission to perform this action.\nPermissions: manage voice chats",
            show_alert=True)
    checking = query.from_user.first_name
    chat_id = query.message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        try:
            await music.pytgcalls.leave_group_call(chat_id)
        except Exception as e:
            pass
        await remove_active_chat(chat_id)
        await query.answer(f"️✅ music has ended")
    else:
        await query.answer(f"sorry, nothing's playing on music!", show_alert=True)
