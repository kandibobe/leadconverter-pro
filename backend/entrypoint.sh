#!/bin/sh
# Немедленно выходить, если команда завершается с ошибкой
set -e

# Даем Postgres время на запуск
echo "Waiting for postgres..."
sleep 5

# Применяем миграции базы данных
echo "Applying database migrations..."
alembic upgrade head

# Запускаем основной сервер
echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000```

---
### **Шаг 2: Исправление `alembic/env.py`**

Это исправит ошибку импорта. Мы будем импортировать `Base` и пакет `models` напрямую.

**Файл:** `/backend/alembic/env.py`
**Действие:** Заменить

```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- ИЗМЕНЕННАЯ ЧАСТЬ ---
# Импортируем Base, от которого зависят все модели
from app.db.base import Base
# Импортируем пакет models, чтобы Alembic "увидел" все наши таблицы
import app.db.models
# -------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем Alembic на метаданные наших моделей
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()