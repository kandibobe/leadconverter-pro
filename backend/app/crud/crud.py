# В файле backend/app/crud.py

# ... (существующие функции get_quiz, create_lead)

from sqlalchemy import func
from . import models

def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).offset(skip).limit(limit).all()

def get_dashboard_metrics(db: Session):
    total_leads = db.query(models.Lead).count()
    average_check_query = db.query(func.avg(models.Lead.final_price)).scalar()
    # Обработка случая, когда лидов еще нет
    average_check = float(average_check_query) if average_check_query is not None else 0.0
    
    return {"total_leads": total_leads, "average_check": average_check}