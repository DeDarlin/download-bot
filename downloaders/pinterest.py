import yt_dlp

# Укажи путь к ffmpeg, пример для Windows:
FFMPEG_PATH = r"C:\\ffmpeg\\bin\\ffmpeg.exe"

def download_pinterest(url, format_id="best"):
    """
    Скачивает видео с Pinterest.
    format_id: 'best', '144p', '240p', '360p', '480p', '720p', '1080p'
    """
    # Параметры yt-dlp
    ydl_opts = {
        'format': f'bestvideo[ext=mp4][height<={format_id}]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ffmpeg_location': FFMPEG_PATH,
        'quiet': False,
        'noplaylist': True,
        'nocheckcertificate': True,
    }

    # Если выбрали "звук", скачиваем только аудио
    if format_id.lower() == "audio":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename
