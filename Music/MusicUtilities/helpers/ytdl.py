import asyncio
from yt_dlp import YoutubeDL


ytdl = YoutubeDL
async def ytdl(link, str):
    stdout, stderr = await bash(
        f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr

# url
async def ytdl2(url):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "--geo-bypass",
        "-g",
        "-f",
        "[height<=?720][width<=?1280]",
        f"{url}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


ytdl_opts = {
        'format': 'bestaudio[ext=m4a]',
        'geo-bypass': True,
        'noprogress': True,
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; k960n_mt6580_32_n) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        'extractor-args': 'youtube:player_client=all',
        'nocheckcertificate': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quite': True,
    }

