import asyncio
import os
import random
import contextlib
from asyncio import QueueEmpty

import yt_dlp
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputStream, InputAudioStream

from Music import app, config
from Music.MusicUtilities.memek.youtube import get_audio_direct_link
from Music.MusicUtilities.database.queue import remove_active_chat
from Music.MusicUtilities.helpers.gets import themes
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.MusicUtilities.tgcallsrun import convert, download
from Music.MusicUtilities.tgcallsrun import queues


flex = {}
smexy = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)

pytgcalls = PyTgCalls(
    smexy,
    cache_duration=100,
    overload_quiet_mode=True,
)


@pytgcalls.on_kicked()
async def on_kicked(_: PyTgCalls, chat_id: int) -> None:
    with contextlib.suppress(QueueEmpty):
        queues.clear(chat_id)
    await remove_active_chat(chat_id)


@pytgcalls.on_closed_voice_chat()
async def on_closed(_: PyTgCalls, chat_id: int) -> None:
    with contextlib.suppress(QueueEmpty):
        queues.clear(chat_id)
    await remove_active_chat(chat_id)


@pytgcalls.on_stream_end()
async def on_stream_end(_: PyTgCalls, update: Update) -> None:
    chat_id = update.chat_id
    try:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await pytgcalls.leave_group_call(chat_id)
        else:
            afk = queues.get(chat_id)["file"]
            await pytgcalls.change_stream(
                chat_id,
                InputStream(
                    InputAudioStream(
                        afk,
                    ),
                ),
            )
    except Exception as e:
        print(e)


run = pytgcalls.start
