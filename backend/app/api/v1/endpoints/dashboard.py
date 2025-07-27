from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/metrics", response_model=schemas.DashboardMetrics)
def get_dashboard_metrics(db: Session = Depends(deps.get_db)):
    """
    Получить ключевые метрики для дашборда.
    """
    metrics = crud.dashboard(db) # Теперь вызываем crud.dashboard
    return metrics