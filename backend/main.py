# backend/app/main.py
from fastapi import FastAPI, Request, Depends, Header
from app.db.session import SessionLocal, TENANT_ID, engine as sa_engine
from app.otel import setup_otel
from sqlalchemy.ext.asyncio import AsyncSession
from app.billing.webhook import router as stripe_webhooks
app.include_router(stripe_webhooks)

app = FastAPI(title="LeadConverter API")
setup_otel(app=app, engine=sa_engine)  # OTel FastAPI/SQLAlchemy

async def get_db(tenant_id: str | None = Header(default=None, alias="X-Tenant-ID")) -> AsyncSession:
    token = None
    if tenant_id:
        token = TENANT_ID.set(tenant_id)
    try:
        async with SessionLocal() as s:
            yield s
    finally:
        if token: TENANT_ID.reset(token)

@app.get("/healthz")
async def healthz(): return {"ok": True}

# простейшая запись лида (event-sourcing lite)
from fastapi import Body
from uuid import uuid4
from sqlalchemy import text

@app.post("/lead/create")
async def lead_create(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    lead_id = body.get("lead_id") or str(uuid4())
    await db.execute(
        text("INSERT INTO lead_events(tenant_id, lead_id, event_type, payload) VALUES(:t,:l,'created',:p)")
        .bindparams(t=TENANT_ID.get(), l=lead_id, p=body))
    await db.commit()
    return {"lead_id": lead_id}
