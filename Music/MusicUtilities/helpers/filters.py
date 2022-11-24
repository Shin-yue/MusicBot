from typing import List
from typing import Union

from pyrogram import filters
from Music import BOT_USERNAME as buname
from Music.config import COMMAND_PREFIXES as cmd

other_filters = filters.group & ~ filters.edited & \
                ~ filters.via_bot & ~ filters.forwarded
other_filters2 = filters.private & ~ filters.edited \
                 & ~ filters.via_bot & ~ filters.forwarded


def command(commands: Union[str, List[str]]):
    return filters.command(commands, cmd)

# regex
regex_patern = f'^\/(command)+(\@{buname}\w*(_\w+)*)?([ \f\n\r\t\v\u00A0\u2028\u2029].*)?$'
