import os
from logging.config import fileConfig
from pathlib import Path
from alembic import context
from sqlalchemy import engine_from_config, pool

# .env из backend/ или корня – чтобы не зависеть от окружения терминала
try:
    from dotenv import load_dotenv
    for p in [Path(__file__).resolve().parent.parent / ".env.docker",
              Path(__file__).resolve().parent.parent / ".env",
              Path(__file__).resolve().parents[2] / ".env.local"]:
        if p.exists():
            load_dotenv(p)
            break
except Exception:
    pass

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.database import Base
import app.models  # noqa: F401

target_metadata = Base.metadata

db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata,
                      literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
