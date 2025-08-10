import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql+psycopg://...

# alembic использует sync-драйвер, а приложение — async. Это нормально (best practice).
engine = create_async_engine(DATABASE_URL.replace("postgresql+psycopg", "postgresql+asyncpg"), echo=False)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
