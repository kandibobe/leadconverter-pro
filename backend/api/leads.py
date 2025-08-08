from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from pydantic import BaseModel, EmailStr
from typing import List
import hmac
import hashlib
import json

from app.api import deps
from app.models.lead import Lead
from app.tasks import send_lead_notification

router = APIRouter()

class LeadAnswer(BaseModel):
    question_id: int
    answer: str

class LeadIn(BaseModel):
    email: EmailStr
    utm_source: str | None = None
    answers: List[LeadAnswer]

class LeadResponse(BaseModel):
    lead_id: int
    status: str

def _has_consent(email: str, db: Session) -> bool:
    """Placeholder for double opt-in consent check."""
    return True

@router.post("/lead", response_model=LeadResponse)
def create_lead(lead_in: LeadIn, db: Session = Depends(deps.get_db)):
    if not _has_consent(lead_in.email, db):
        raise HTTPException(status_code=400, detail="Consent required")

    decrypted_email = db.scalar(
        func.pgp_sym_decrypt(text(":email"), text("current_setting('app.pgcrypto_key')")),
        {"email": lead_in.email},
    ) or lead_in.email

    db_lead = Lead(
        client_email=decrypted_email,
        utm_source=lead_in.utm_source,
        final_price=0.0,
        answers_details=[a.model_dump() for a in lead_in.answers],
        quiz_id=0,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    payload = {"lead_id": db_lead.id, "email": decrypted_email, "utm_source": lead_in.utm_source}
    signature = hmac.new(b"secret", json.dumps(payload).encode(), hashlib.sha256).hexdigest()
    send_lead_notification.delay(payload, signature)

    return LeadResponse(lead_id=db_lead.id, status="ok")
