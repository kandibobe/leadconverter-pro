# backend/app/api/v1/endpoints/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.dashboard import get_dashboard_metrics
from app.schemas.dashboard import DashboardMetrics
from app.database import get_db

router = APIRouter()

@router.get("/metrics", response_model=DashboardMetrics)
def read_dashboard_metrics(db: Session = Depends(get_db)):
    """Get key metrics for the dashboard."""
    return get_dashboard_metrics(db)
