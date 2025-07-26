# backend/app/api/v1/endpoints/leads.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.LeadOut])
def read_leads(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Retrieve all leads.
    """

    # ИМПОРТ ВНУТРИ ФУНКЦИИ:
    # Это разрывает любые циклы на уровне модулей и является более надежным паттерном.
    from app.services.notification_service import notification

    lead = crud.lead.create(db=db, obj_in=lead_in)
    
    # "Отправляем" уведомление
    notification.send_new_lead_notification(lead)
    
    return lead

    leads = crud.get_leads(db, skip=skip, limit=limit)
    return leads
 main
