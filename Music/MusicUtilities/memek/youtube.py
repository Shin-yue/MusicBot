from yt_dlp import YoutubeDL


# audio direct link
def get_audio_direct_link(url: str) -> str:
    with YoutubeDL({"format": "ba*"}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]
