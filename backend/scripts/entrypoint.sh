#!/bin/sh
set -e

echo "Waiting for postgres..."
# ждём доступность порта 5432 на хосте db
until nc -z db 5432; do
  sleep 1
done

echo "Applying database migrations..."
alembic -c backend/alembic.ini upgrade head || {
  echo "Alembic upgrade failed"; exit 1;
}
