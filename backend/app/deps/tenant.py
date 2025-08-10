from contextlib import asynccontextmanager
from fastapi import Request, HTTPException
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.models.tenant import Tenant

def _get_slug(request: Request) -> str:
    slug = request.headers.get("X-Tenant-Slug")
    if not slug:
        raise HTTPException(400, "X-Tenant-Slug header is required")
    return slug

@asynccontextmanager
async def tenant_session(request: Request):
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        slug = _get_slug(request)
        tid = await session.scalar(select(Tenant.id).where(Tenant.slug == slug))
        if not tid:
            raise HTTPException(404, "Tenant not found")

        async with session.begin():
            # Делаем RLS-контекст на время транзакции запроса
            await session.execute(text("SET LOCAL app.tenant_id = :tid"), {"tid": str(tid)})
            yield session
