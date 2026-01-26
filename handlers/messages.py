from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import FSInputFile
import os

from utils.detect import detect_platform
from downloaders.youtube import get_qualities, download_audio, download_video
from downloaders.pinterest import download_pinterest
from downloaders.soundcloud import download_soundcloud_audio
from downloaders.tiktok import download_tiktok
from keyboards.quality import quality_keyboard

router = Router()
user_urls = {}

# ---------- /start ----------
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я скачиваю видео и аудио 📥\n\n"
        "Поддержка:\n"
        "• YouTube (качество + звук)\n"
        "• Pinterest (видео)\n"
        "• SoundCloud (аудио)\n\n"
        "Просто отправь ссылку 🔗"
    )

# ---------- /help ----------
@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "ℹ️ Как пользоваться:\n\n"
        "1️⃣ Отправь ссылку\n"
        "2️⃣ Если YouTube — выбери качество\n"
        "3️⃣ Получи файл\n\n"
        "📦 Видео >50 МБ отправляются как документ\n"
        "⚠️ Максимальный размер: 2 ГБ"
    )

# ---------- ссылки ----------
@router.message(F.text)
async def link_handler(message: Message):
    url = message.text.strip()
    platform = detect_platform(url)

    if platform == "youtube":
        user_urls[message.from_user.id] = url

        try:
            videos, audios = get_qualities(url)

            if not videos or not audios:
                await message.answer("❌ Не удалось получить форматы")
                return

            best_audio = audios[0]["format_id"]

            await message.answer(
                "🎥 Выбери качество видео:",
                reply_markup=quality_keyboard(videos, best_audio)
            )
        except Exception as e:
            await message.answer(f"❌ Ошибка при получении форматов: {str(e)}")

    elif platform == "pinterest":
        try:
            await message.answer("⏳ Скачиваю видео с Pinterest...")
            path = download_pinterest(url)

            size = os.path.getsize(path)
            size_mb = size / (1024 * 1024)
            
            if size > 50 * 1024 * 1024:
                await message.answer_document(
                    document=FSInputFile(path),
                    caption=f"🎥 Pinterest видео ({size_mb:.1f} МБ)"
                )
            else:
                await message.answer_video(video=FSInputFile(path))
            
            os.remove(path)
        except Exception as e:
            await message.answer(f"❌ Ошибка при скачивании с Pinterest: {str(e)}")
            if 'path' in locals() and os.path.exists(path):
                os.remove(path)

    elif platform == "soundcloud":
        try:
            await message.answer("🎵 Скачиваю аудио с SoundCloud...")
            path = download_soundcloud_audio(url)

            await message.answer_audio(audio=FSInputFile(path))
            os.remove(path)
        except Exception as e:
            await message.answer(f"❌ Ошибка при скачивании с SoundCloud: {str(e)}")
            if 'path' in locals() and os.path.exists(path):
                os.remove(path)

    elif platform == "tiktok":
        try:
            await message.answer("⏳ Скачиваю видео с TikTok...")
            path = download_tiktok(url)

            size = os.path.getsize(path)
            size_mb = size / (1024 * 1024)
            
            if size > 50 * 1024 * 1024:
                await message.answer_document(
                    document=FSInputFile(path),
                    caption=f"🎥 TikTok видео ({size_mb:.1f} МБ)"
                )
            else:
                await message.answer_video(video=FSInputFile(path))
            
            os.remove(path)
        except Exception as e:
            await message.answer(f"❌ Ошибка при скачивании с TikTok: {str(e)}")
            if 'path' in locals() and os.path.exists(path):
                os.remove(path)

    else:
        await message.answer("❌ Платформа не поддерживается")


# ---------- callbacks ---------- 
@router.callback_query(F.data.startswith("q:"))
async def video_handler(call: CallbackQuery):
    await call.answer()  # Убираем часики на кнопке
    
    url = user_urls.get(call.from_user.id)
    
    if not url:
        await call.message.answer("❌ Ошибка: ссылка не найдена. Отправьте ссылку заново.")
        return

    data = call.data.split(":")[1]
    video_id, audio_id = data.split("|")
    
    # Уведомляем пользователя о начале скачивания
    status_msg = await call.message.answer("⏳ Скачиваю видео...")

    try:
        path = download_video(url, video_id, audio_id)

        size = os.path.getsize(path)
        size_mb = size / (1024 * 1024)
        
        # Отправляем файл (с локальным Bot API можно до 2000 МБ)
        if size > 2000 * 1024 * 1024:
            await status_msg.edit_text(
                f"❌ Файл слишком большой ({size_mb:.1f} МБ)\n"
                f"Максимум 2000 МБ. Выберите качество пониже."
            )
        elif size > 50 * 1024 * 1024:
            # Большие файлы отправляем как документ
            await status_msg.edit_text(f"📤 Отправляю как документ ({size_mb:.1f} МБ)...")
            await call.message.answer_document(
                document=FSInputFile(path),
                caption=f"🎥 Видео ({size_mb:.1f} МБ)"
            )
            await status_msg.delete()
        else:
            # Маленькие файлы как видео
            await status_msg.edit_text("📤 Отправляю видео...")
            await call.message.answer_video(video=FSInputFile(path))
            await status_msg.delete()

        if os.path.exists(path):
            os.remove(path)
            
    except Exception as e:
        error_msg = str(e)
        try:
            if "Request Entity Too Large" in error_msg or "file is too big" in error_msg.lower():
                await status_msg.edit_text(
                    f"❌ Файл слишком большой ({size_mb:.1f} МБ)\n\n"
                    f"Для отправки файлов >50 МБ нужен локальный Bot API сервер.\n"
                    f"Инструкция: запустите бота с флагом --local-api\n"
                    f"Или выберите качество пониже."
                )
            else:
                await status_msg.edit_text(f"❌ Ошибка: {error_msg}")
        except:
            await call.message.answer(f"❌ Ошибка: {error_msg}")
        
        if 'path' in locals() and os.path.exists(path):
            os.remove(path)


@router.callback_query(F.data == "audio")
async def audio_handler(call: CallbackQuery):
    await call.answer()
    
    url = user_urls.get(call.from_user.id)
    
    if not url:
        await call.message.answer("❌ Ошибка: ссылка не найдена. Отправьте ссылку заново.")
        return
    
    status_msg = await call.message.answer("🎵 Скачиваю аудио...")
    
    try:
        path = download_audio(url)
        await status_msg.delete()
        await call.message.answer_audio(audio=FSInputFile(path))
        os.remove(path)
    except Exception as e:
        await status_msg.edit_text(f"❌ Ошибка при скачивании: {str(e)}")
        if 'path' in locals() and os.path.exists(path):
            os.remove(path)