# credits @levina-lab < https://github.com/levina-lab >

import wget
import yt_dlp
import traceback
import requests
import lyricsgenius

from pyrogram import filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from Music import app, BOT_USERNAME as bn
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import remove_if_exists


@app.on_message(command(["song", f"song@{bn}"]) & ~filters.edited)
async def song_downloader(_, message):
    await message.delete()
    query = " ".join(message.command[1:])
    m = await message.reply("🔎 finding song...")
    ydl_ops = {
        'format': 'bestaudio[ext=m4a]',
        'geo-bypass': True,
        'noprogress': True,
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        'extractor-args': 'youtube:player_client=all',
        'nocheckcertificate': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quite': True,
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        await m.edit("❌ song not found.\n\n» Give me a valid song name !")
        print(str(e))
        return
    await m.edit("📥 downloading song...")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"[{title}]({link})\n• uploader @{bn}"
        host = str(info_dict["uploader"])
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("📤 uploading song...")
        await message.reply_audio(
            audio_file,
            caption=rep,
            performer=host,
            thumb=thumb_name,
            parse_mode="md",
            title=title,
            duration=dur,
        )
        await m.delete()

    except Exception as e:
        await m.edit("❌ error, wait for bot owner to fix")
        print(e)
    try:
        remove_if_exists(audio_file)
        remove_if_exists(thumb_name)
    except Exception as e:
        print(e)


@app.on_message(
    command(["vsong", f"vsong@{bn}", "video", f"video@{bn}"]) & ~filters.edited
)
async def video_downloader(_, message):
    await message.delete()
    ydl_opts = {
        "format": "best",
        "geo-bypass": True,
        "noprogress": True,
        "user-agent": "Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "extractor-args": "youtube:player_client=all",
        "nocheckcertificate": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        await m.edit("❌ video not found.")
        print(str(e))
        return
    try:
        msg = await message.reply("📥 downloading video...")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        traceback.print_exc()
        return await msg.edit(f"🚫 error: `{e}`")
    preview = wget.download(thumbnail)
    await msg.edit("📤 uploading video...")
    text = f"[{title}]({link}) | `video`\n• `{duration}`\n• uploader @{bn}"
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=text,
    )
    try:
        remove_if_exists(file_name)
        await msg.delete()
    except Exception as e:
        print(e)


@app.on_message(command(["lyric", f"lyric@{bn}", "lyrics"]))
async def get_lyric_genius(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**usage:**\n\n/lyrics (song name)")
    return
    m = await message.reply_text("🔍 Searching lyrics...")
    query = message.text.split(None, 1)[1]
    api = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    data = lyricsgenius.Genius(api)
    data.verbose = False
    result = data.search_song(query, get_full_info=False)
    if result is None:
        return await m.edit("❌ `404` lyrics not found")
    xxx = f"""
**Title song:** {query}
**Artist name:** {result.artist}
**Lyrics:**
{result.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**OUTPUT:**\n\n`attached lyrics text`",
            quote=False,
        )
        remove_if_exists(filename)
    else:
        await m.edit(xxx)
