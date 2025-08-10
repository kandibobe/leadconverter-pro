# backend/alembic/env.py
import os
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

# Логи Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata ваших моделей
target_metadata = Base.metadata

# Протаскиваем DATABASE_URL из .env / окружения в alembic.ini в рантайме
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline():
    """Запуск в offline-режиме — генерирует SQL без подключения к БД."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Онлайн-режим — нормальные миграции с подключением."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
