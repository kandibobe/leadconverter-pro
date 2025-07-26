# Этап 1: Установка зависимостей
FROM python:3.11-slim AS builder

WORKDIR /app

# Устанавливаем переменные окружения, чтобы pip не кэшировал и не выводил лишнего
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Этап 2: Сборка финального образа
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости из builder'а
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем исходный код приложения
COPY ./app /app

# Команда для запуска будет передана через docker-compose
