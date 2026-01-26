import os
from yt_dlp import YoutubeDL

# Пути для Windows и Linux
if os.name == 'nt':  # Windows
    FFMPEG_PATH = r"C:\ffmpeg\bin"
    os.environ["PATH"] += os.pathsep + FFMPEG_PATH
else:  # Linux/Unix
    FFMPEG_PATH = "/usr/bin"  # ffmpeg уже в PATH на Linux

DOWNLOAD_DIR = "downloads"

MAX_SIZE = 50 * 1024 * 1024  # 50 MB

def get_qualities(url):
    """
    Получаем список форматов видео и аудио с YouTube
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "format": "best",
        # Используем node.js для JS runtime, чтобы поддерживать новые YouTube форматы
        "js_runtimes": {"node": {}},
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        video_formats = []
        audio_formats = []

        for f in info['formats']:
            if f.get('vcodec') != 'none':  # видео
                video_formats.append(f)
            elif f.get('acodec') != 'none':  # аудио
                audio_formats.append(f)

        # Сортировка по высоте и битрейту
        video_formats.sort(key=lambda x: x.get('height') or 0, reverse=True)
        audio_formats.sort(key=lambda x: x.get('abr') or 0, reverse=True)

    return video_formats, audio_formats


def format_qualities(video_formats, audio_formats):
    """
    Преобразуем форматы в читаемые строки для выбора
    """
    result = []

    for v in video_formats:
        height = v.get("height") or 0
        has_audio = v.get("acodec") != "none"
        label = f"{height}p"
        label += " (с аудио)" if has_audio else " (без аудио)"
        result.append({"id": v["format_id"], "label": label, "size": v.get("filesize") or 0})

    for a in audio_formats:
        abr = a.get("abr") or 0
        label = f"Audio {abr}kbps"
        result.append({"id": a["format_id"], "label": label, "size": a.get("filesize") or 0})

    # Сортируем: видео по высоте, аудио по битрейту
    result.sort(
        key=lambda x: int(x["label"].split("p")[0]) if "p" in x["label"] else x["size"], reverse=True
    )
    return result


def download_video(url, video_id, audio_id=None):
    """
    Скачиваем видео с выбранными видео и аудио форматами
    """
    if audio_id:
        fmt = f"{video_id}+{audio_id}"
    else:
        fmt = f"{video_id}"

    ydl_opts = {
        "format": fmt,
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "quiet": True,
        "ffmpeg_location": FFMPEG_PATH,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def download_audio(url):
    """
    Скачиваем аудио и конвертируем в mp3
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": FFMPEG_PATH,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    filename = ydl.prepare_filename(info)
    filename = filename.rsplit(".", 1)[0] + ".mp3"
    return filename