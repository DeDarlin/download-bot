def detect_platform(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "pinterest.com" in url or "pin.it" in url:
        return "pinterest"
    elif "soundcloud.com" in url:
        return "soundcloud"
    elif "tiktok.com" in url or "vt.tiktok.com" in url:
        return "tiktok"
    else:
        return "unknown"
