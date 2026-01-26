# Download Bot - Telegram бот для скачивания видео

Telegram бот для скачивания видео с YouTube, Pinterest, TikTok и аудио с SoundCloud.

## Возможности

- **YouTube** - скачивание видео с выбором качества (144p - 4K)
- **Pinterest** - скачивание видео
- **TikTok** - скачивание видео без водяных знаков
- **SoundCloud** - скачивание аудио в MP3

## Поддержка больших файлов

| Режим | Максимальный размер |
|-------|---------------------|
| Стандартный | 50 МБ |
| С локальным Bot API | 2000 МБ (2 ГБ) |

## Быстрый старт

### Локальный запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-username/download-bot.git
cd download-bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте `.env` файл:
```bash
cp .env.example .env
```

4. Добавьте токен бота в `.env`:
```
BOT_TOKEN=ваш_токен_от_BotFather
```

5. Запустите:
```bash
python main.py
```

### Деплой на хостинг

**См. подробную инструкцию:** [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

Рекомендуемые хостинги:
- **Railway.app** - поддержка файлов до 2 ГБ
- **Render.com** - простой деплой (до 50 МБ)
- **Fly.io** - расширенные возможности

## 🔧 Настройка для файлов >50 МБ

Для отправки файлов больше 50 МБ нужен локальный Bot API сервер.

### Через Docker Compose:

1. Получите API_ID и API_HASH на https://my.telegram.org
2. Добавьте в `.env`:
```
TELEGRAM_API_ID=ваш_api_id
TELEGRAM_API_HASH=ваш_api_hash
```
3. Запустите:
```bash
docker-compose up -d
```

**Подробнее:** [SETUP_BIG_FILES.md](SETUP_BIG_FILES.md)

## Требования

- Python 3.11+
- ffmpeg (для обработки видео)
- Docker (опционально, для файлов >50 МБ)

## Установка ffmpeg

### Windows:
1. Скачайте: https://ffmpeg.org/download.html
2. Распакуйте в `C:\ffmpeg`
3. Добавьте `C:\ffmpeg\bin` в PATH

### Linux:
```bash
sudo apt-get install ffmpeg
```

### macOS:
```bash
brew install ffmpeg
```

## Получение токена бота

1. Напишите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

## Команды бота

- `/start` - Начало работы
- `/help` - Справка по использованию

## Структура проекта

```
download-bot/
├── handlers/          # Обработчики команд и сообщений
├── downloaders/       # Модули для скачивания с разных платформ
├── keyboards/         # Клавиатуры Telegram
├── utils/            # Вспомогательные функции
├── downloads/        # Временные файлы (автоматически очищается)
├── main.py           # Точка входа
├── config.py         # Конфигурация
└── requirements.txt  # Зависимости
```

## Решение проблем

### Ошибка "ffmpeg not found"
**Решение:** Установите ffmpeg (см. раздел "Установка ffmpeg")

### Файл >50 МБ не отправляется
**Решение:** Настройте локальный Bot API (см. SETUP_BIG_FILES.md)

### Бот не отвечает
**Проверьте:**
1. Правильность токена в `.env`
2. Запущен ли бот (`python main.py`)
3. Есть ли ошибки в консоли

## Лицензия

MIT License - используйте свободно!

## Вклад в проект

Pull requests приветствуются! Для больших изменений сначала откройте issue.

## Поддержка

Возникли вопросы? Создайте [Issue](https://github.com/ваш-username/download-bot/issues)
