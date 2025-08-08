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
# Run Uvicorn bound to a Unix Domain Socket
exec uvicorn main:app --uds /tmp/uvicorn.sock
