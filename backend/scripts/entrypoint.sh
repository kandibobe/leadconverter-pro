#!/bin/sh
set -e

echo "Waiting for postgres..."
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-lcp_user}"; do
  sleep 1
done

echo "Applying database migrations..."
if [ -f "/app/alembic.ini" ]; then
  alembic -c /app/alembic.ini upgrade head || echo "Alembic failed, continuing..."
else
  echo "No /app/alembic.ini found, skipping migrations"
fi

exec "$@"
