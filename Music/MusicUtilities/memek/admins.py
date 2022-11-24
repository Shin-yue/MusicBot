from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Music import SUDO_USERS, app
from Music.MusicUtilities.database import get_authuser_names, is_nonadmin_chat
from Music.MusicUtilities.memek.changers import int_to_alpha

keyboard = [
    [
        InlineKeyboardButton("🗑️ Close", callback_data="close2")
    ],
]


def authorized_users_only(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "You're an __anonymous admin__\n\n» revert back to user account."
            )
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            member = await app.get_chat_member(
                message.chat.id, message.from_user.id
            )
            if not member.can_manage_voice_chats:
                if message.from_user.id not in SUDO_USERS:
                    token = await int_to_alpha(message.from_user.id)
                    _check = await get_authuser_names(message.chat.id)
                    if token not in _check:
                        return await message.reply(
                            f"Hi {message.from_user.mention()} this command only for admin with **permission:**\n\n» __requies admin with manage vc rights__",
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
        return await mystic(_, message)

    return wrapper


def auth_user(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "you're an __anonymous admin__\n\n» revert back to user account."
            )
        member = await app.get_chat_member(
            message.chat.id, message.from_user.id
        )
        if not member.can_manage_voice_chats:
            return await message.reply(
                f"Hi {message.from_user.mention()} this command only for admin with **permission:**\n\n» __requires admin with manage vc rights__",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        return await mystic(_, message)

    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(_, CallbackQuery):
        a = await app.get_chat_member(
            CallbackQuery.message.chat.id, CallbackQuery.from_user.id
        )
        if not a.can_manage_voice_chats:
            return await CallbackQuery.answer(
                "You don't have the required permission to perform this action.\nPermission: Manage voice chats",
                show_alert=True,
            )
        return await mystic(_, CallbackQuery)

    return wrapper
