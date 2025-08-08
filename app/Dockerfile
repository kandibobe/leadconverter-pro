# app/Dockerfile (ИСПРАВЛЕННАЯ ВЕРСИЯ)

# --- Этап 1: Сборка зависимостей ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем файл зависимостей, указывая путь от корня проекта
COPY app/requirements.txt .

# Устанавливаем зависимости
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- Этап 2: Финальный образ ---
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Копируем скомпилированные зависимости из сборщика
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Копируем код нашего приложения, указывая путь от корня проекта
COPY ./app /app
# Копируем точку входа отдельно и размещаем её вне тома проекта,
# чтобы избежать проблем с правами и окончанием строк на Windows
COPY app/entrypoint.sh /entrypoint.sh
# Обеспечиваем корректные окончания строк и права на выполнение
RUN sed -i 's/\r$//' /entrypoint.sh \
    && chmod +x /entrypoint.sh

# Открываем порт
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]