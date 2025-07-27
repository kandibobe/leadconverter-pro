# backend/Dockerfile

FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код всего backend (а не только app) в образ
COPY backend/ .

EXPOSE 8000

# Контейнер запускается без явной команды, т.к. команда задаётся в compose‑файле
