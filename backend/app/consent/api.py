from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from uuid import UUID
from app.db.session import TENANT_ID
router = APIRouter(prefix="/consent", tags=["consent"])

@router.post("/event")
async def store_consent(ev: dict, req: Request, db: AsyncSession = Depends()):
    q = text("""
      INSERT INTO consent_events(tenant_id, user_agent, ip, consent_id, policy_version, choice)
      VALUES(:t,:ua,:ip,:cid,:pv,:ch)
    """)
    await db.execute(q.bindparams(
        t=TENANT_ID.get(),
        ua=req.headers.get("User-Agent"),
        ip=req.client.host,
        cid=UUID(ev["consent_id"]),
        pv=ev["policy_version"],
        ch=ev["choice"],
    ))
    await db.commit()
    return {"ok": True}
