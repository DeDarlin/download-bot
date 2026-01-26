FROM python:3.11-slim

# Установка ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем файлы
COPY . .

# Установка зависимостей
RUN pip install --no-cache-dir aiogram yt-dlp

# Создаем директорию для загрузок
RUN mkdir -p downloads

# Запуск бота
CMD ["python", "main.py"]
