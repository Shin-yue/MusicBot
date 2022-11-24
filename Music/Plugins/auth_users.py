from time import time
from pyrogram import filters
from pyrogram.types import Message

from Music import app
from Music.MusicUtilities.database import get_authuser_names, save_authuser, delete_authuser, extract_user
from Music.MusicUtilities.memek.admins import auth_user
from Music.MusicUtilities.memek.changers import int_to_alpha


# authusers can used admins conmand without admin permissions
admins_in_chat = {}


async def list_admins(chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in app.iter_chat_members(
                chat_id, filter="administrators"
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


@app.on_message(filters.command("auth") & filters.group)
@auth_user
async def auth(_, message: Message):
    chat_id = message.chat.id
    userid = await extract_user(message)
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "😕 I'm sorry, **I couldn't** find this user!\n\n» try to give me the id or username of the user"
            )
        if userid in (await list_admins(message.chat.id)):
            return await app.send_message(
                chat_id,
                "👮 __Users is administrators on this chat.__"
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = 0 
        for smex in _check:
            count += 1
        if int(count) == 20:
            return await message.reply_text(
                "😕 You can only have 20 Users in your groups **uuthorised** users list."
            )
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            await save_authuser(message.chat.id, token, assis)
            mention = user.mention
            await message.reply_text(
                f"🧙 **added** {mention} to the **authorized users list**, from now on he'll be able to **use** my **commands.**"
            )
            return
        else:
            return await message.reply_text(
                f"{mention} already in the **authorized users list** and he can use my **commands.**")
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(
            "😕 You can only have 20 Users in your groups **authorised users list.**"
        )
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        await save_authuser(message.chat.id, token, assis)
        await message.reply_text(
            f"🧙 **added** {message.reply_to_message.from_user.mention} to the **authorized users list**, from now on he'll be able to **use** my **commands.**"
        )
        return
    else:
        return await message.reply_text(
            f"{message.reply_to_message.from_user.mention} already in the **authorized users list** and he can use my **commands.**")


@app.on_message(filters.command("unauth") & filters.group)
@auth_user
async def whitelist_chat_func(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "😕 I'm sorry, **I couldn't** find this user!\n\n» try to give me the id or username of the user"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        mention = user.mention
        if deleted:
            return await message.reply_text(
                f"🧙 {mention} removed from the **authorized users list**, from now on he'll no longer be able to **use** my **commands.**"
            )
        else:
            return await message.reply_text(f"😕 {mention} not an authorised user.")
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if deleted:
        return await message.reply_text(
            f"🧙 removed {message.reply_to_message.from_user.mention} from the **authorized users list**, from now on he'll no longer be able to **use** my **commands.**"
        )
    else:
        return await message.reply_text(f"😕 not an authorised user.")
