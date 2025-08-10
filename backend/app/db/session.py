# backend/app/db/session.py
from contextvars import ContextVar
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

TENANT_ID: ContextVar[str | None] = ContextVar("TENANT_ID", default=None)

engine = create_async_engine(
    "postgresql+asyncpg://USER:PASS@HOST/DB",
    pool_size=10, max_overflow=10, pool_pre_ping=True,
)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@event.listens_for(AsyncSession, "after_begin")
def _set_rls(session, transaction, connection):
    tid = TENANT_ID.get()
    if tid:
        connection.exec_driver_sql("SET app.tenant_id = %s", (tid,))
