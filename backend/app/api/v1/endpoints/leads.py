# backend/app/api/v1/endpoints/leads.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.LeadOut])
def read_leads(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all leads.
    """
    leads = crud.get_leads(db, skip=skip, limit=limit)
    return leads