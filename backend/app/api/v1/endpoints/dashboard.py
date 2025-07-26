# backend/app/api/v1/endpoints/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/metrics", response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(deps.get_db)):
    """
    Get key metrics for the dashboard.
    """
    metrics = crud.get_dashboard_metrics(db)
    return metrics