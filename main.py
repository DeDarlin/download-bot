import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import TOKEN, LOCAL_API_SERVER
from handlers.messages import router

async def main():
    # Если указан локальный API сервер - используем его
    if LOCAL_API_SERVER:
        bot = Bot(
            token=TOKEN,
            default=DefaultBotProperties(parse_mode="HTML")
        )
        bot.session.api.base = LOCAL_API_SERVER
        print(f"Бот запущен с локальным API: {LOCAL_API_SERVER}")
        print("Поддержка файлов до 2000 МБ включена")
    else:
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
        print("Бот запущен")
        print("Лимит файлов: 50 МБ (для больших файлов настройте LOCAL_API_SERVER)")
    
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
