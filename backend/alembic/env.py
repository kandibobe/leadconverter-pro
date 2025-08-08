from logging.config import fileConfig
import sys
import types
import importlib.util
from pathlib import Path

from alembic import context

# Add application path and create a fake 'app' package so that
# imports like `from app.database import Base` work even though the
# project code lives directly in `backend/`.
BASE_DIR = Path(__file__).resolve().parent.parent
app_package = types.ModuleType("app")
app_package.__path__ = [str(BASE_DIR)]
sys.modules.setdefault("app", app_package)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module

# Load database configuration and models
_database = _load_module("app.database", BASE_DIR / "database.py")
_load_module("app.models", BASE_DIR / "models.py")

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", _database.DATABASE_URL)

target_metadata = _database.Base.metadata


def run_migrations_offline() -> None:
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
    connectable = _database.engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
