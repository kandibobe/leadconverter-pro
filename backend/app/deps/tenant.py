from contextlib import asynccontextmanager
from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app.db.session import async_session_maker  # см. ниже
from app.models.tenant import Tenant

def _extract_slug(request: Request) -> str:
    slug = request.headers.get("X-Tenant-Slug")
    if not slug:
        raise HTTPException(400, "X-Tenant-Slug header is required")
    return slug

@asynccontextmanager
async def tenant_session(request: Request):
    async with async_session_maker() as session:  # type: AsyncSession
        slug = _extract_slug(request)
        tenant_id = await session.scalar(select(Tenant.id).where(Tenant.slug == slug))
        if not tenant_id:
            raise HTTPException(404, "Tenant not found")

        # ВАЖНО: SET LOCAL — только внутри транзакции текущего запроса
        async with session.begin():
            await session.execute(text("SET LOCAL app.tenant_id = :tid"), {"tid": str(tenant_id)})
            yield session
