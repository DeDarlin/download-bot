from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def quality_keyboard(videos, audio_id):
    buttons = []

    for v in videos:
        # Используем height вместо quality
        height = v.get('height') or 0
        buttons.append([
            InlineKeyboardButton(
                text=f"🎥 {height}p",
                callback_data=f"q:{v['format_id']}|{audio_id}"
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
