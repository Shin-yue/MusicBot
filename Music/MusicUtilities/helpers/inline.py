# button inline

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def play_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text="❌ Cancel", callback_data="endvc"),
            InlineKeyboardButton(text="🗑 Close", callback_data=f'close')
        ],
    ]
    return buttons


def search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query):
    buttons = [
        [
            InlineKeyboardButton(text="1️⃣", callback_data=f'Music2 {ID1}|{duration1}|{user_id}'),
            InlineKeyboardButton(text="2️⃣", callback_data=f'Music2 {ID2}|{duration2}|{user_id}'),
            InlineKeyboardButton(text="3️⃣", callback_data=f'Music2 {ID3}|{duration3}|{user_id}')
        ],
        [
            InlineKeyboardButton(text="4️⃣", callback_data=f'Music2 {ID4}|{duration4}|{user_id}'),
            InlineKeyboardButton(text="5️⃣", callback_data=f'Music2 {ID5}|{duration5}|{user_id}')
        ],
        [

            InlineKeyboardButton(text="➡️", callback_data=f'popat 1|{query[:14]}|{user_id}'),
        ],
        [
            InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}")
        ],
    ]
    return buttons


def search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10, user_id, query):
    buttons = [
        [
            InlineKeyboardButton(text="6️⃣", callback_data=f'Music2 {ID6}|{duration6}|{user_id}'),
            InlineKeyboardButton(text="7️⃣", callback_data=f'Music2 {ID7}|{duration7}|{user_id}'),
            InlineKeyboardButton(text="8️⃣", callback_data=f'Music2 {ID8}|{duration8}|{user_id}')
        ],
        [
            InlineKeyboardButton(text="9️⃣", callback_data=f'Music2 {ID9}|{duration9}|{user_id}'),
            InlineKeyboardButton(text="🔟", callback_data=f'Music2 {ID10}|{duration10}|{user_id}')
        ],
        [

            InlineKeyboardButton(text="⬅️", callback_data=f'popat 2|{query[:14]}|{user_id}'),
        ],
        [
            InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}")
        ],
    ]
    return buttons



def youtube_markup(videoid, duration, user_id):
    buttons = [
        [
            InlineKeyboardButton(text="1️⃣", callback_data=f"Music2 {videoid}|{duration}|{user_id}"),
        ],
        [
            InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}")
        ],
    ]
    return buttons
# button for start in pm
pstart_markup = InlineKeyboardMarkup(
    [
        [
           InlineKeyboardButton("➕ Add me to your group ➕", url="https://t.me/exmusicx_bot?startgroup=True"), 
        ],
        [
           InlineKeyboardButton("❤️ Donate", url="https://t.me/InfoDonate/8"),
           InlineKeyboardButton("📚 Command", url="https://telegra.ph/Music-Player---Command-List-01-04")
        ],
        [
           InlineKeyboardButton("👥 Official Group", url="t.me/AlinaSupportChat"),
           InlineKeyboardButton("📣 Official Channel", url="t.me/exprojects")
        ]
    ]
)
