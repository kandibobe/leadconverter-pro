# backend/Dockerfile (ИСПРАВЛЕННАЯ ВЕРСИЯ)

# --- Этап 1: Сборка зависимостей ---
FROM python:3.11-slim as builder

WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем файл зависимостей, указывая путь от корня проекта
COPY backend/requirements.txt .

# Устанавливаем зависимости
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- Этап 2: Финальный образ ---
FROM python:3.11-slim

WORKDIR /app

# Копируем скомпилированные зависимости из сборщика
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем код нашего приложения, указывая путь от корня проекта
COPY ./backend/app /app

# Открываем порт
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
