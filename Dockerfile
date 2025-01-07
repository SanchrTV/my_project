# Используем базовый образ Python
FROM python:3.9-slim

# Перепроверка установлен ли pip
RUN apt-get update && apt-get install -y python3-pip

# Установка зависимостей и SQLite
RUN apt-get update && apt-get install -y sqlite3 supervisor && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы с зависимостями
COPY app/requirements.txt /app/

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY app /app

# Создаем директорию для базы данных
RUN mkdir -p /app/data

# Инициализация SQLite базы данных
RUN sqlite3 /app/data/app.db "VACUUM;"

# Открываем порт 80
EXPOSE 80

# Объявляем том для базы данных
VOLUME /app/data

# Копируем конфигурацию supervisord
COPY app/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Запускаем supervisord для управления несколькими процессами
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
