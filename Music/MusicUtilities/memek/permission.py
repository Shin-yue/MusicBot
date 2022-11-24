from Music import BOT_ID, app


def require_admins(mystic):
    async def wrapper(_, message):
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "📌 **To use me I need to be an admin with permissions:**\n"
                + "❌ __can_manage_voice_chats__\n"
                + "❌ __can_delete_messages__\n"
                + "❌ __can_invite_users__\n"
                + "If so, then type `/reload`"
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "📌 **To use me I need to be an admin with permissions:**\n"
                + "❌ __Manage voice chats__\n"
                + "If so, then type `/reload`"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "📌 **To use me I need to be an admin with permissions:**\n"
                + "❌  __Delete messages__\n"
                + "If so, then type `/reload`"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "📌 **To use me I need to be an admin with permissions:**\n"
                + "❌  __Invite user via link__\n"
                + "If so, then type `/reload`"
            )
            return
        return await mystic(_, message)

    return wrapper
