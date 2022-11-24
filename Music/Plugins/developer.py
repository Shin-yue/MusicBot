import os
import re
import subprocess
import psutil
import sys
import traceback

from time import time
from datetime import datetime
from sys import version as pyver
from inspect import getfullargspec
from io import StringIO

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import Message

from Music import ex, app, OWNER, BOT_NAME as buname
from Music.MusicUtilities.database.functions import start_restart_stage
from Music.MusicUtilities.database import get_served_chats
from Music.MusicUtilities.database.onoff import add_on, add_off
from Music.MusicUtilities.database.queue import get_active_chats, remove_active_chat
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.formatter import get_readable_time
from Music.MusicUtilities.tgcallsrun import pytgcalls
from Music.helpers.sys import bot_sys_stats


@app.on_message(command("update") & filters.user(OWNER))
@errors
async def update(_, message: Message):
    m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if str(m[0]) != "A":
        x = await message.reply_text("Found Updates! Pushing Now.")
        await start_restart_stage(x.chat.id, x.message_id)
        os.execvp("python3", ["python3", "-m", "Music"])
    else:
        await message.reply_text("Already Upto Date")


@app.on_message(command("send") & filters.user(OWNER))
async def send_group(_, m: Message):
    args = " ".join(m.command[1:])
    try:
        chat_id = str(args[0])
        del args[0]
    except:
        await m.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            await app.send_message(int(chat_id), str(to_send))
        except Exception as e:
            await m.reply_text(
                "• error**:** {}".format(e)
            )
    else:
        m.reply_text(
            "Where should i send??\nGive me the chat id!"
        )


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_message(
    filters.user(OWNER)
    & ~filters.forwarded
    & ~filters.via_bot
    & command(["p", "evalx"])
)
async def executor(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="» Give a command to execute !")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "SUCCESS"
    final_output = f"`OUTPUT:`\n\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳", callback_data=f"runtime {t2-t1} seconds"
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"`INPUT:`\n`{cmd[0:980]}`\n\n`OUTPUT:`\n`attached document`",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2-t1, 3)} seconds",
                    )
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_message(
    filters.user(OWNER)
    & ~filters.forwarded
    & ~filters.via_bot
    & command(["pler", "sh"]),
)
async def shellrunner(client, message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="**usage:**\n\n» /sh echo hello world")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await edit_or_reply(message, text=f"`ERROR:`\n```{err}```")
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"`ERROR:`\n```{''.join(errors)}```"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`Output`",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"`OUTPUT:`\n```{output}```")
    else:
        await edit_or_reply(message, text="`OUTPUT:`\n`no output`")


@app.on_message(command("Musicp") & filters.user(OWNER))
async def smex(_, message):
    usage = "**Usage:**\n/Musicp [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("Music Enabled for Maintenance")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("Maintenance Mode Disabled")
    else:
        await message.reply_text(usage)


@app.on_message(command("stp") & filters.user(OWNER))
async def sls_skfs(_, message):
    usage = "**Usage:**\n/st [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 2
        await add_on(user_id)
        await message.reply_text("Speedtest Enabled")
    elif state == "disable":
        user_id = 2
        await add_off(user_id)
        await message.reply_text("Speedtest Disabled")
    else:
        await message.reply_text(usage)


@app.on_message(command("restart") & filters.user(OWNER))
async def theme_func(_, message):
    a = "downloads"
    b = "raw_files"
    shutil.rmtree(a)
    shutil.rmtree(b)
    os.mkdir(a)
    os.mkdir(b)
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        pass
    for x in served_chats:
        try:
            await app.send_message(
                x,
               "💭 music has just restarted herself. sorry for the issues.\n\nstart playing after 10-15 seconds again."
            )
        except Exception:
            pass
    served_chatss = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chatss.append(int(chat["chat_id"]))
    except Exception as e:
        pass
    for served_chat in served_chatss:
        try:
            await remove_active_chat(served_chat)
        except Exception as e:
            await message.reply_text(f"{e}")
            pass
    x = await message.reply_text("restarting music player..")
    await start_restart_stage(x.chat.id, x.message_id)
    os.execvp(f"python{str(pyver.split(' ')[0])[:3]}", [
        f"python{str(pyver.split(' ')[0])[:3]}", "-m", "Music"])


@app.on_message(command("system") & filters.user(OWNER))
async def bot_stats(_, message: Message):
    chat_id = message.chat.id
    uptime = await bot_sys_stats()
    start = datetime.now()
    msg = await app.send_message(
        chat_id,
        f"🔄 __Processing...__"
    )
    end = datetime.now()
    chats = len(await get_served_chats())

    resp = (end - start).microseconds / 1000

    text = "{}".format(uptime)

    if pytgcalls.active_calls:
        text += "\n ├ __Served Chats: {}__\n └ __Calls active: {}__".format(chats, len(pytgcalls.active_calls))
    if not pytgcalls.active_calls:
        text += "\n └ __Served Chats: {}__".format(chats)

    await msg.edit_text(text)
    return
   
     

