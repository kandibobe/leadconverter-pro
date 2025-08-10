# backend/app/api/leads.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from app.deps.tenant import tenant_session

router = APIRouter()

@router.get("/_debug/tenants")
async def debug_tenants(request: Request, session = Depends(tenant_session)):
    rows = (await session.execute(text("select * from tenants order by created_at desc"))).mappings().all()
    return {"items": list(rows)}
