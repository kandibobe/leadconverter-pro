#!/bin/sh
# Немедленно выходить, если команда завершается с ошибкой
set -e

# ЯВНО УСТАНАВЛИВАЕМ PYTHONPATH ДЛЯ ЭТОЙ СЕССИИ
# Это гарантирует, что alembic найдет все модули.
export PYTHONPATH=/app

echo "Waiting for postgres..."
sleep 5

echo "Applying database migrations..."
alembic upgrade head

echo "Starting server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000