# it's okay, not everything has to go according to your expectations :)
# https://github.com/riz-ex
import asyncio
import os
import random
import shutil
from os import path
# pyrogram, pytgcalls and other stuff
import yt_dlp
from pyrogram import filters, Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import Voice, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream, InputAudioStream
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from youtubesearchpython import VideosSearch
# repository stuff
from Music import app, converter, BOT_USERNAME, BOT_ID, ASSID, BOT_NAME
from Music.MusicUtilities.database.onoff import is_on_off
from Music.MusicUtilities.database.queue import is_active_chat, add_active_chat, remove_active_chat, music_on
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.formatter import convert_seconds, time_to_seconds
from Music.MusicUtilities.helpers.gets import get_url, themes, remove_if_exists
from Music.MusicUtilities.helpers.inline import play_markup, youtube_markup, search_markup, search_markup2

from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.tgcallsrun.thumbnails2 import kontolmemek_thumb
from Music.MusicUtilities.helpers.ytdl import ytdl_opts, ytdl
from Music.MusicUtilities.memek.youtube import get_audio_direct_link
from Music.MusicUtilities.tgcallsrun import music, convert, download, clear, get, is_empty, put, task_done, ASS_ACC as assistant
from Music.MusicUtilities.memek.permission import require_admins
from Music.MusicUtilities.tgcallsrun.music import smexy
from Music.config import DURATION_LIMIT



@app.on_message(command(["play", f"play@{BOT_USERNAME}"]))
@require_admins
async def play(_, message: Message):
    if message.sender_chat:
        return await message.reply_text(
            "you're an anonymous admin !\n\n» revert back to user account from admin rights."
        )
    chat_id = message.chat.id
    user_id = message.from_user.id

    await message.delete()
    if int(chat_id) == int('-1001771245214'):
        await message.reply_text("⚠️ **The @exmusicx_bot bot in the support group is disabled, to avoid confusion.**\n\n__To avoid spam, you only can safely use it in our group.__",
            disable_web_page_preview=True
        )
        return

    if await is_on_off(1):
        log = "-1001202786293"
        if int(chat_id) != int(log):
            return await message.reply_text(
               f"😕 Sorry, can't play music for now because it's under maintenance.\n\n• we're sorry for the inconveniences**;** for bug & issues report, reach us in support [chat.](https://t.me/botdiscuss)",
               disable_web_page_preview=True,
               reply_markup=InlineKeyboardMarkup(
                  [
                     [
                        InlineKeyboardButton("📣 Official Channel",
                        url="https://t.me/exprojects")
                     ]
                  ]
              )
          )
    try:
        b = await app.get_chat_member(message.chat.id, ASSID)
        if b.status == "banned":
            await app.unban_chat_member(chat_id, ASSID)
            invite_link = await message.chat.export_invite_link()
            if "+" in invite_link:
                group = (invite_link.replace("+", "")).split("t.me/")[1]
                link = f"https://t.me/joinchat/{group}"
            await assistant.join_chat(link)
            await remove_active_chat(chat_id)
            return
    except UserNotParticipant:

        if message.chat.username:
            try:
                await assistant.join_chat(f"{message.chat.username}")
                await remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(f"❌ **Assistant failed to join**\n\nReason: {e}",
                                         reply_markup=InlineKeyboardMarkuo(keyboard))
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    group = (invite_link.replace("+", "")).split("t.me/")[1]
                    link = f"https://t.me/joinchat/{group}"
                await assistant.join_chat(link)
                await remove_active_chat(chat_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(f"__**Assistant failed to join**__\n\n**Reason**:{e}")

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)
    await message.delete()
    if audio:
        mystic = await message.reply_text("📥 process audio...")
        if audio.file_size > 157286400:
            await mystic.edit_text("Audio file size should be less than 150 mb")
            return
        duration = round(audio.duration / 60)
        if duration > DURATION_LIMIT:
            return await mystic.edit_text(
                f"⚠️ __Duration limit error.__\n\n**Allowed duration:** `{DURATION_LIMIT} minute(s)`\n**Received duration:** `{duration} minute(s)`"
                )
        file_name = audio.file_unique_id + '.' + (
            (
                audio.file_name.split('.')[-1]
            ) if (
                not isinstance(audio, Voice)
            ) else 'ogg'
        )
        file_name = path.join(path.realpath('downloads'), file_name)
        file = await convert(
            (
                await message.reply_to_message.download(file_name)
            )
            if (
                not path.isfile(file_name)
            )
            else file_name,
        )
        await mystic.edit("📥 downloading audio...")
        syfa = message.reply_to_message
        if syfa.audio:
            title = audio.title
        elif syfa.voice:
            title = "telegram audio.."
        link = message.reply_to_message.link
        thumbnail = "https://telegra.ph/file/63300139d232dc12452ab.png"
        videoid = "smex1"
        message.chat.title
        if len(message.chat.title) > 10:
            ctitle = message.chat.title[:10] + "..."
        else:
            ctitle = message.chat.title
        ctitle = await CHAT_TITLE(ctitle)
        duration = convert_seconds(audio.duration)
        theme = random.choice(themes)
        userid = message.from_user.id
        thumb = await kontolmemek_thumb(thumbnail, title, userid, theme, ctitle)
        await mystic.delete()

    elif url:
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("🔎 __Searching...__🔎 ")
        ydl_opts = {"format": "bestaudio[ext=m4a]"}

        try:
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                result["title"]
                title = (result["title"])
                duration = (result["duration"])
                views = (result["viewCount"]["short"])
                thumbnail = (result["thumbnails"][0]["url"])
                link = (result["link"])
                idxz = (result["id"])
                videoid = (result["id"])
                userid = message.from_user.id

        except Exception as e:
            return await mystic.edit_text(f"🚫 error: `{e}`")

        buttons = youtube_markup(videoid, duration, user_id)
        await mystic.edit(
            f"🎧 **Result from link:**\n\n1️⃣ **[{title}](https://www.youtube.com/watch?v={videoid})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{videoid})\n └ ⚡ __Powered by {BOT_NAME}__",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
        return
        smex = int(time_to_seconds(duration))
        if smex > DURATION_LIMIT:
            return await mystic.edit_text(
                f"**__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)")
        if duration == "None":
            return await mystic.edit_text("Sorry! Live videos are not Supported")
        if views == "None":
            return await mystic.edit_text("Sorry! Live videos are not Supported")
        semxbabes = (f"Downloading {title[:50]}")
        await mystic.edit(semxbabes)
        theme = random.choice(themes)
        ctitle = message.chat.title
        ctitle = await CHAT_TITLE(ctitle)
        userid = message.from_user.id
        thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)

        loop = asyncio.get_event_loop()
        x = await loop.run_in_executor(None, download, link)
        file = await convert(x)

    else:
        if len(message.command) < 2:
            user_name = message.from_user.first_name
            peler = await message.reply_text(
                f"❌ **Song not found!** Please enter the correct title")
            await asyncio.sleep(10)
            await message.delete()
            await peler.delete()
            return
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("🔍 Searching... 🔍")
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            result[0]["title"]
            if len(result[0]["title"]) > 27:
                title1 = result[0]["title"][:27] + "..."
            else:
                title1 = result[0]["title"]
            duration1 = result[0]["duration"]
            result[1]["title"]
            if len(result[1]["title"]) > 27:
                title2 = result[1]["title"][:27] + "..."
            else:
                title2 = result[1]["title"]
            duration2 = result[1]["duration"]
            result[2]["title"]
            if len(result[2]["title"]) > 27:
                title3 = result[2]["title"][:27] + "..."
            else:
                title3 = result[2]["title"]
            duration3 = result[2]["duration"]
            result[3]["title"]
            if len(result[3]["title"]) > 27:
                title4 = result[3]["title"][:27] + "..."
            else:
                title4 = result[3]["title"]
            duration4 = result[3]["duration"]
            result[4]["title"]
            if len(result[4]["title"]) > 27:
                title5 = result[4]["title"][:27] + "..."
            else:
                title5 = result[4]["title"]
            duration5 = result[4]["duration"]
            ID1 = (result[0]["id"])
            ID2 = (result[1]["id"])
            ID3 = (result[2]["id"])
            ID4 = (result[3]["id"])
            ID5 = (result[4]["id"])
        except Exception as e:
            return await mystic.edit_text(f"🚫 error: `{e}`")
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query)
        await mystic.edit(
            f"• Choose the results to play !\n\n1️⃣ **[{title1}](https://www.youtube.com/watch?v={ID1})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})\n └ ⚡ __Powered by {BOT_NAME}__\n\n2️⃣ **[{title2}](https://www.youtube.com/watch?v={ID2})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})\n └ ⚡ __Powered by {BOT_NAME}__\n\n3️⃣ **[{title3}](https://www.youtube.com/watch?v={ID3})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})\n └ ⚡ __Powered by {BOT_NAME}__\n\n4️⃣ **[{title4}](https://www.youtube.com/watch?v={ID4})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})\n └ ⚡ __Powered by {BOT_NAME}__\n\n5️⃣ **[{title5}](https://www.youtube.com/watch?v={ID5})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})\n └ ⚡ __Powered by {BOT_NAME}__",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
        return
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        buttons = play_markup(_)
        checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        await mystic.delete()
        await message.reply_text(
            "➕ Added to the queue\n📌 Position N°{}\n🎼 [{}]({})".format(position, title, link),
            disable_web_page_preview=True
        )
        remove_if_exists(thumb)
        return

    else:
        try:
            await music.pytgcalls.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception as e:
            await mystic.edit(
                f"⚠️ __error: {e}__"
            )
            return
        _chat_ = ((str(file)).replace("_", "", 1).replace("/", "", 1).replace(".", "", 1))
        checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        buttons = play_markup(_)
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await message.reply_photo(
            photo=thumb,
            caption=f"🏷️ **Name:** [{title}]({link})\n⏱ **Duration:** `{duration}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {checking}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        remove_if_exists(thumb)
        return


@app.on_callback_query(filters.regex(pattern=r"Music"))
async def startyuplay(_, query: CallbackQuery):
    callback_data = query.data.strip()
    chat_id = query.message.chat.id
    chat_title = query.message.chat.title
    callback_request = callback_data.split(None, 1)[1]
    userid = query.from_user.id
    try:
        id, duration, user_id = callback_request.split("|")
    except Exception as e:
        return await query.message.edit(f"❌ error occured\n**possible reason could be**: `{e}`")
    if duration == "None":
        return await query.message.reply_text(f"❌ **sorry** live videos are not supported")
    if query.from_user.id != int(user_id):
        return await query.answer("💡 only the person requesting the song can press the button!", show_alert=True)
    await query.message.delete()
    checking = f"[{query.from_user.first_name}](tg://user?id={userid})"
    url = f"https://www.youtube.com/watch?v={id}"
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    videoid = id
    idx = id
    smex = int(time_to_seconds(duration))
    if smex > DURATION_LIMIT:
        await query.message.reply_text(
            f"⚠️ __Duration limit error.__\n • __Allowed duration: 90 minutes__\n • __Received duration: {duration} minutes__")
        return
    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            x = ytdl.extract_info(url, download=False)
    except Exception as e:
        return await query.message.reply_text(f"⚠️ **Failed to download this video.\n\n» **Reason**: `{e}`")
    x["title"]
    kontol = x["title"]
    if len(x["title"]) > 18:
        memex = x["title"][:18] + "..."
    else:
        memex = x["title"]
    if len(x["title"]) > 27:
        titleq = x["title"][:27] + "..."
    else:
        titleq = x["title"]
    thumbnail = (x["thumbnail"])
    idx = (x["id"])
    videoid = (x["id"])

    loop = asyncio.get_event_loop()
    x = await loop.run_in_executor(None, download, url)
    file = await convert(x)
    theme = random.choice(themes)
    query.message.chat.title
    if len(query.message.chat.title) > 10:
        ctitle = query.message.chat.title[:10] + "..."
    else:
        ctitle = query.message.chat.title
    ctitle = await CHAT_TITLE(ctitle)
    thumb = await gen_thumb(thumbnail, memex, userid, theme, ctitle)
    if await is_active_chat(chat_id):
        position = await put(chat_id, file=file)
        buttons = play_markup(_)
        await query.message.delete()
        await app.send_message(
            chat_id,
            "➕ Added to the queue\n📌 Position N°{}\n🎼 [{}]({})".format(position, kontol, url),
            disable_web_page_preview=True
        )
        remove_if_exists(thumb)
    else:
        peler = await query.message.reply_photo(
            photo=thumb,
            caption=(
            f"🏷️ **Name:** [{kontol}]({url})\n⏱ **Duration:** `{duration}`\n💡 **Status:** `Joining..`\n🎧 **Requested by:** {checking}"),
            reply_markup=InlineKeyboardMarkup(
              [
                 [
                   InlineKeyboardButton("🗑️ Close", callback_data="close2")
                 ]
              ]
           ),
        )
        try:
            await music.pytgcalls.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception as e:
            await asyncio.sleep(3.4)
            await peler.delete()
            await app.send_message(
                chat_id,
                f"⚠️ __error: {e}__"
            )
            return
        await query.message.delete()
        buttons = play_markup(_)
        await music_on(chat_id)
        await add_active_chat(chat_id)
        await peler.edit(
            f"🏷️ **Name:** [{kontol}]({url})\n⏱ **Duration:** `{duration}`\n💡 **Status:** `Playing`\n🎧 **Requested by:** {checking}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        remove_if_exists(thumb)


@app.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_, cb: CallbackQuery):
    callback_data = cb.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    print(callback_request)
    userid = cb.from_user.id
    try:
        id, query, user_id = callback_request.split("|")
    except Exception as e:
        return await cb.message.edit(f"❌ Error Occured\n**Possible reason could be**: `{e}`")
    if cb.from_user.id != int(user_id):
        return await cb.answer("This is not for you! search you own song", show_alert=True)
    i = int(id)
    query = str(query)
    try:
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        result[0]["title"]
        if len(result[0]["title"]) > 27:
            title1 = result[0]["title"][:27] + "..."
        else:
            title1 = result[0]["title"]
        duration1 = result[0]["duration"]
        result[1]["title"]
        if len(result[1]["title"]) > 27:
            title2 = result[1]["title"][:27] + "..."
        else:
            title2 = result[1]["title"]
        duration2 = result[1]["duration"]
        result[2]["title"]
        if len(result[2]["title"]) > 27:
            title3 = result[2]["title"][:27] + "..."
        else:
            title3 = result[2]["title"]
        duration3 = result[2]["duration"]
        result[3]["title"]
        if len(result[3]["title"]) > 27:
            title4 = result[3]["title"][:27] + "..."
        else:
            title4 = result[3]["title"]
        duration4 = result[3]["duration"]
        result[4]["title"]
        if len(result[4]["title"]) > 27:
            title5 = result[4]["title"][:27] + "..."
        else:
            title5 = result[4]["title"]
        duration5 = result[4]["duration"]
        result[5]["title"]
        if len(result[5]["title"]) > 27:
            title6 = result[5]["title"][:27] + "..."
        else:
            title6 = result[5]["title"]
        duration6 = result[5]["duration"]
        result[6]["title"]
        if len(result[6]["title"]) > 27:
            title7 = result[6]["title"][:27] + "..."
        else:
            title7 = result[6]["title"]
        duration7 = result[6]["duration"]
        result[7]["title"]
        if len(result[7]["title"]) > 27:
            title8 = result[7]["title"][:27] + "..."
        else:
            title8 = result[7]["title"]
        duration8 = result[7]["duration"]
        result[8]["title"]
        if len(result[8]["title"]) > 27:
            title9 = result[8]["title"][:27] + "..."
        else:
            title9 = result[8]["title"]
        duration9 = result[8]["duration"]
        result[9]["title"]
        if len(result[9]["title"]) > 27:
            title10 = result[9]["title"][:27] + "..."
        else:
            title10 = result[9]["title"]
        duration10 = result[9]["duration"]
        ID1 = (result[0]["id"])
        ID2 = (result[1]["id"])
        ID3 = (result[2]["id"])
        ID4 = (result[3]["id"])
        ID5 = (result[4]["id"])
        ID6 = (result[5]["id"])
        ID7 = (result[6]["id"])
        ID8 = (result[7]["id"])
        ID9 = (result[8]["id"])
        ID10 = (result[9]["id"])
    except Exception as e:
        return await mystic.edit_text(f"Soung Not Found.\n**Possible Reason:**{e}")
    if i == 1:
        buttons = search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10,
                                 user_id, query)
        await cb.edit_message_text(
            f"\n• Choose the result to play !\n\n6️⃣ **[{title6}](https://www.youtube.com/watch?v={ID6})**\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID6})\n └ ⚡ __Powered by {BOT_NAME}__\n\n7️⃣ **[{title7}](https://www.youtube.com/watch?v={ID7})**\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID7})\n └ ⚡ __Powered by {BOT_NAME}__\n\n8️⃣ **[{title8}](https://www.youtube.com/watch?v={ID8})**\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID8})\n └ ⚡ __Powered by {BOT_NAME}__\n\n9️⃣ **[{title9}](https://www.youtube.com/watch?v={ID9})**\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID9})\n └ ⚡ __Powered by {BOT_NAME}__\n\n🔟 **[{title10}](https://www.youtube.com/watch?v={ID10})**\n ├ 💡 [More Information](https://t.me/{BOT_USERNAME}?start=info_{ID10})\n └ ⚡ __Powered by {BOT_NAME}__\n\n",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
        return
    if i == 2:
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id,
                                query)
        await cb.edit_message_text(
            f"\n• Choose the result to play !\n\n1️⃣ **[{title1}](https://www.youtube.com/watch?v={ID1})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})\n └ ⚡ __Powered by {BOT_NAME}__\n\n2️⃣ **[{title2}](https://www.youtube.com/watch?v={ID2})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})\n └ ⚡ __Powered by {BOT_NAME}__\n\n3️⃣ **[{title3}](https://www.youtube.com/watch?v={ID3})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})\n └ ⚡ __Powered by {BOT_NAME}__\n\n4️⃣ **[{title4}](https://www.youtube.com/watch?v={ID4})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})\n └ ⚡ __Powered by {BOT_NAME}__\n\n5️⃣ **[{title5}](https://www.youtube.com/watch?v={ID5})**\n ├ [💡 More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})\n └ ⚡ __Powered by {BOT_NAME}__",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
        return


@app.on_message(filters.left_chat_member)
async def asisstant(_, message: Message):
    chat_id = message.chat.id
    bot = message.left_chat_member
    if bot == BOT_ID:
        await smexy.leave_chat(chat_id)
        return
