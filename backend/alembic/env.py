import os
import sys
import types
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Определяем корень проекта: /app в контейнере
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Импортируем модуль app (где лежат config и SQLAlchemy Base)
try:
    import app as app_module  # type: ignore
except ModuleNotFoundError:
    app_module = types.ModuleType("app")
    app_module.__path__ = [os.path.join(BASE_DIR, "app")]
    sys.modules["app"] = app_module

try:
    from app.core.config import settings
    from app.database import Base
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(
        "Please ensure that the 'app' directory is correctly structured and that the necessary files exist, including __init__.py files."
    )
    raise

# Alembic Config
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем строку подключения к БД
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск в offline-режиме (без подключения к БД)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск в online-режиме (через engine)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
