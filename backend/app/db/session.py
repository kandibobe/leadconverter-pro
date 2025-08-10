import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

db_url_sync = os.getenv("DATABASE_URL")  # postgresql+psycopg://...
if not db_url_sync:
    raise RuntimeError("DATABASE_URL is not set")

db_url_async = db_url_sync.replace("postgresql+psycopg", "postgresql+asyncpg")
engine_async = create_async_engine(db_url_async, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(engine_async, expire_on_commit=False,
                                       class_=AsyncSession)
