# backend/app/api/v1/endpoints/dashboard.py
import logging
import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/metrics", response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """Get key metrics for the dashboard."""
    logger.info("Fetching dashboard metrics")
    try:
        metrics = crud.get_dashboard_metrics(db)
    except Exception:
        logger.exception("Failed to fetch dashboard metrics")
        raise
    return metrics
