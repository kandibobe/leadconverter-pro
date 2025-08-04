# backend/app/api/v1/endpoints/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.crud.crud_lead import lead as crud_lead
from app.database import get_db


class DashboardMetrics(BaseModel):
    total_leads: int


router = APIRouter()


@router.get("/metrics", response_model=DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Get key metrics for the dashboard."""
    leads = crud_lead.get_multi(db)
    return DashboardMetrics(total_leads=len(leads))
