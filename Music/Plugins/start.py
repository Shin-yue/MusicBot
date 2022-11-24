import yt_dlp
from time import time
from datetime import datetime

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Music import app, BOT_USERNAME, BOT_ID, OWNER
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.helpers.formatter import convert_seconds
from Music.MusicUtilities.helpers.inline import pstart_markup
from Music.MusicUtilities.memek.admins import authorized_users_only
from Music.MusicUtilities.helpers.ytdl import ytdl_opts
from Music.config import LOG_GROUP_ID


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@app.on_message(command("ping"))
@authorized_users_only
async def ping_pong(_, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@app.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def start_group(_, message: Message):
    await message.delete()
    chat_id = message.chat.id
    await _.send_message(chat_id, f"""
👋🏻 Hello {message.from_user.mention()}!

💭 __Appoint me as admin in your Group so i can play music, otherwise you can't use my service.__
""",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📚 Commands", url=f"https://telegra.ph/Music-Player---Command-List-01-04"), 
                InlineKeyboardButton("👥 Group", url="https://t.me/AlinaSupportChat"),
            ]
        ]
    ),
)


welcome_captcha_group = 2


@app.on_message(filters.new_chat_members, group=welcome_captcha_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    invite_link = await message.chat.export_invite_link()

    for member in message.new_chat_members:
        try:
            if member.id == BOT_ID:
                await app.send_message(
                    chat_id,
                    f"💭 <b>Hello</> thanks for adding me to this group!\n\n"
                    "📚 Do <b>note</> I need to be <b>promoted</> with proper admin permissions to <b>function properly.</>",
                    parse_mode = "HTML",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("📣 Updates Channel", url="https://t.me/exprojects")]
                        ]
                    )
                )
                return
        except:
            return


@app.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        await app.send_message(message.chat.id,
                               f"""
💭 **Welcome {rpk}**!

📚 @exmusicx_bot **allows you** to play music on groups through the new Telegram's video chats!

🆚 Version**:** __0.8.5__
""",
                               disable_web_page_preview=True,
                               parse_mode="markdown",
                               reply_markup=pstart_markup,
                               )
    elif len(message.command) == 2:
        query = message.text.split(None, 1)[1]
        f1 = (query[0])
        f2 = (query[1])
        f3 = (query[2])
        finxx = (f"{f1}{f2}{f3}")
        if str(finxx) == "inf":
            kontol = await message.reply_text("🔍 Searching Info.. 🔍")
            query = ((str(query)).replace("info_", "", 1))
            query = (f"https://www.youtube.com/watch?v={query}")
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = (x["thumbnail"])
            searched_text = f"""
💡 **Video Track Information :**

🏷️ **Title:** [{x["title"]}]({x["webpage_url"]})  
⏱️ **Duration:** `{convert_seconds(x["duration"])}`
👀 **Views:** `{x["view_count"]}`
📣 **Channel Name:** [{x["uploader"]}]({x["channel_url"]})

⚡️ __Searched by ex music__"""
            link = (x["webpage_url"])
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await kontol.delete()
            await app.send_photo(
               message.chat.id,
               photo=thumb,
               caption=searched_text,
               parse_mode="markdown",
           )


@app.on_message(command(["bug", f"bug@{BOT_USERNAME}"]))
async def bug(bot, message: Message):
    invite_link = await message.chat.export_invite_link()
    if message.chat.username:
        chatusername = (f"{message.chat.username}")
    else:
        chatusername = ("Private group")
    if message.sender_chat:
        return await message.reply_text(
            "you're an __Anonymous Admin__ !\n\n» revert back to user account from admin rights."
        )
        await message.delete()
    else:
        if len(message.command) < 2:
            await message.reply_text(
                "You must specify the bug to report\nexample : `/bug the reason you want to report`"
            )
            return
    await message.reply_text(
        "✅ **Bug reported successfully.**\n__The report has been sent to the support [group](https://t.me/botdiscuss)__",
        disable_web_page_preview=True)
    await bot.send_message(LOG_GROUP_ID, f"""
📣 **New Bug Reporting!** 

**Chat ID:** `{message.chat.id}`
**Place Link:** [{message.chat.title}]({invite_link})
**User Profil:** {message.from_user.mention()}

**Contents of the report:**
{' '.join(message.command[1:])}
""",
      disable_web_page_preview=True,
      reply_markup=InlineKeyboardMarkup(
      [
         [
            InlineKeyboardButton("View Message", url=f"{message.link}"),
         ],
         [
            InlineKeyboardButton("🗑️ Close", callback_data="close2")]]
         ),
      )
