import asyncio

from Music.MusicUtilities.database.queue import is_active_chat
from Music.MusicUtilities.tgcallsrun.music import smexy
from Music.config import AUTO_LEAVE, LOG_GROUP_ID


async def auto_leave():
    if AUTO_LEAVE == str(True):
        while not await asyncio.sleep(AUTO_LEAVE):
            async for i in smexy.iter_dialogs():
                chat_type = i.chat.type
                if chat_type in [
                    "supergroup",
                    "group",
                ]:
                    chat_id = i.chat.id
                    if (
                        chat_id != LOG_GROUP_ID
                        and chat_id != -1001627221128
                        and chat_id != -1001665437027
                        and chat_id != -1001202786293
                    ):
                        if not await is_active_chat(chat_id):
                            try:
                                await smexy.leave_chat(
                                    chat_id
                                )
                            except:
                               continue


asyncio.create_task(auto_leave())
