# backend/app/api/v1/endpoints/leads.py
"""API endpoints for working with leads."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.models.lead import Lead
from app.services.notification_service import notification
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[schemas.Lead])
def read_leads(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Retrieve leads from the database."""

    leads = db.query(Lead).offset(skip).limit(limit).all()
    logger.debug("Returning %s leads", len(leads))
    return leads


@router.post("/", response_model=schemas.Lead)
def create_lead(lead_in: schemas.LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead and send notification."""

    db_obj = crud.lead.create(db=db, obj_in=lead_in)
    notification.send_new_lead_notification(db_obj)
    return db_obj