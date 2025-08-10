# backend/app/db/session.py
from __future__ import annotations

import os
from contextvars import ContextVar

from sqlalchemy import event, text
from sqlalchemy.orm import Session as SyncSession
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# --- DB URL: SQLAlchemy 2.x + psycopg3 ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://lcp_user:lcp_password@db:5432/lcp_db",
)

# Контекстный tenant_id для текущего запроса (ставится в middleware)
TENANT_ID: ContextVar[str | None] = ContextVar("TENANT_ID", default=None)

# --- Async engine / session factory ---
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --- RLS hook: SET LOCAL app.tenant_id в начале транзакции ---
@event.listens_for(SyncSession, "after_begin")
def _set_rls_guc(session: SyncSession, transaction, connection) -> None:
    """
    В async-коде событие вешаем на синхронную Session.
    Колбэк получает sync-connection, на котором безопасно выполняем SET LOCAL.
    """
    tid = TENANT_ID.get()
    if not tid:
        return
    connection.execute(text("SET LOCAL app.tenant_id = :tid"), {"tid": str(tid)})

__all__ = ["engine", "SessionLocal", "TENANT_ID", "AsyncSession"]
