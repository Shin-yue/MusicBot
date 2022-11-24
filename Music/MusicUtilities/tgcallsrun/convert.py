import asyncio
from os import listdir, mkdir, path

if "raw_files" not in listdir():
    mkdir("raw_files")


async def convert(file_path: str) -> str:
    out = path.join("raw_files", path.basename(f"{file_path}.raw"))
    if path.isfile(out):
        return out
    proc = await asyncio.create_subprocess_shell(
        cmd=(
            "ffmpeg "
            "-y -i "
            f"{file_path} "
            "-f s16le "
            "-ac 1 "
            "-ar 48000 "
            "-acodec pcm_s16le "
            f"{out}"
        ),
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()
    return out


class FFmpegReturnCodeError(Exception):
    pass
