import asyncio
import os
import random
import time as sedtime
from asyncio import QueueEmpty

import yt_dlp
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
# repository stuff
from Music import app, OWNER, BOT_USERNAME as buname, ASSID as asid, client as user, admins
from Music.MusicUtilities.memek.youtube import get_audio_direct_link
from Music.MusicUtilities.database.queue import is_active_chat, remove_active_chat, music_on, is_music_playing, music_off
from Music.MusicUtilities.helpers.filters import command, other_filters
from Music.MusicUtilities.helpers.formatter import convert_seconds
from Music.MusicUtilities.helpers.gets import themes
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.MusicUtilities.memek.admins import authorized_users_only
from Music.MusicUtilities.tgcallsrun import music, convert, download, clear, get, is_empty, task_done

flex = {}


@app.on_message(command(["cleandb", f"cleandb@{buname}"]))
@authorized_users_only
async def stop_cmd(_, message):
    chat_id = message.chat.id
    await message.delete()
    try:
        clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)
    try:
        await music.pytgcalls.leave_group_call(chat_id)
    except:
        pass
    await app.send_message(
        chat_id,
        f"""
✅ __Erased queues in {message.chat.title}__
│
╰ Database cleaned by {message.from_user.mention()}"""
    )


@app.on_message(command(["reload", f"reload@{buname}"]) & other_filters)
@authorized_users_only
async def update_admin(_, message):
    chat_id = message.chat.id
    global admins
    new_admins = []
    new_ads = await app.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    msg = await app.send_message(
        chat_id,
        "✅ Bot restarted\n✅ Admin list updated"
    )
    await asyncio.sleep(10)
    await msg.delete()


@app.on_message(command(["pause", f"pause@{buname}"]))
@authorized_users_only
async def pause_cmd(_, message):
    await message.delete()
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text("❌ no songs playing can paused for a moment.")
    elif not await is_music_playing(message.chat.id):
        return await message.reply_text("❌ Tracks is already paused...")
        await message.delete()
    await music_off(chat_id)
    await music.pytgcalls.pause_stream(chat_id)
    msg = await _.send_message(chat_id, f"⏸ Music paused!\n\n• To resume the music playback, use **command » /resume**")
    await asyncio.sleep(10)
    await msg.delete()


@app.on_message(command(["resume", f"resume@{buname}"]))
@authorized_users_only
async def stop_cmd(_, message):
    await message.delete()
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        await message.reply_text("❌ **not playing music in voice chat**")
        return
    else:
        await music_on(chat_id)
        await music.pytgcalls.resume_stream(chat_id)
        msg = await _.send_message(chat_id, f"⏸ Music resumed!\n\n• To pause the music playback, use **command » /pause**")
        await asyncio.sleep(10)
        await msg.delete()


@app.on_message(command(["end", f"end@{buname}"]))
@authorized_users_only
async def stop_cmd(_, message):
    await message.delete()
    chat_id = message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await music.pytgcalls.leave_group_call(chat_id)
        await _.send_message(chat_id, f"✅ __The userbot has disconnected from the voice chat__")
    else:
        msg = await message.reply_text("❌ **not playing music in voice chat**")
        await asyncio.sleep(10)
        await msg.delete()
        return


@app.on_message(command(["skip", f"skip@{buname}"]))
@authorized_users_only
async def stop_cmd(_, message):
    await message.delete()
    chat_id = message.chat.id
    chat_title = message.chat.title
    if not await is_active_chat(chat_id):
        await message.reply_text("❌ **not playing music in voice chat**")
    else:
        task_done(chat_id)
        if is_empty(chat_id):
            await message.reply_text(
                f"💡 Song **queue** is empty, can't skip song. or it can be **stopped** by pressing the button below.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("✔️ Yes", callback_data="endvc"),
                            InlineKeyboardButton("🗑️ Close", callback_data="closememek")
                        ]
                    ]
                ),
            )
            return
        else:
            afk = get(chat_id)['file']
            await music.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            afk,
                        ),
                    ),
                )
            _chat_ = ((str(afk)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1))
            msv = await _.send_message(
                chat_id, 
                "⏭️ __You've skipped to the next track__"
            )
            await asyncio.sleep(10)
            await msv.delete()
            return


# assistant cmd 
@app.on_message(command("userbotjoin"))
@authorized_users_only
async def userbot_join_(_, m: Message):
    chat_id = m.chat.id
    invite_link = await m.chat.export_invite_link()
    try:
        await user.join_chat(invite_link)
    except UserAlreadyParticipant:
        admin = await m.chat.get_member((await user.get_me()).id)
        if not admin.can_manage_voice_chats:
            return
    await _.promote_chat_member(chat_id, asid)
    return await user.send_message(chat_id, "👋 **hello** I joined here as a music player assistant.")


@app.on_message(command("userbotleave"))
@authorized_users_only
async def ubot_leave_(_, m: Message):
    chat_id = m.chat.id
    try:
        await user.leave_chat(chat_id)
        return await _.send_message(
            chat_id,
            "✅ __Music Assistant successfully left the group__"
        )
    except UserNotParticipant:
        return await _.send_message(
            chat_id,
            "» music assistant is not in this group."
        )
