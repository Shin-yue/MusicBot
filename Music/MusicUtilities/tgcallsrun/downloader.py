from os import path

from yt_dlp import YoutubeDL


def download(url: str) -> str:
    x = YoutubeDL(
        {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
        },
    )
    info = x.extract_info(url, download=False)
    x.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")
