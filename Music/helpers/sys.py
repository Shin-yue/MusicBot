import time
import psutil

from Music import Music_START_TIME
from Music.MusicUtilities.helpers.formatter import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - Music_START_TIME)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f'''
🌐 **Statstic of bot:**
 ├ __Cpu: {cpu}%__
 ├ __Ram: {mem}%__
 ├ __Disk: {disk}%__
 ├ __Uptime: {get_readable_time((bot_uptime))}__'''
    return stats
