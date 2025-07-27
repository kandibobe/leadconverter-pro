 codex/refactor-notification-service-for-gdpr-compliance
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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app import crud, schemas
from app.api import deps
from app.services import pdf_generator # Импортируем наш новый сервис
 main

router = APIRouter()
logger = logging.getLogger(__name__)

 codex/refactor-notification-service-for-gdpr-compliance
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

@router.post("/submit", response_model=schemas.lead.LeadOut)
def submit_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_in: schemas.lead.LeadCreateIn,
) -> Any:
    """
    Принять ответы квиза, рассчитать стоимость, сохранить лид и сгенерировать PDF.
    Это основной эндпоинт для фронтенда.
    """
    # 1. Создаем лид с расчетом цены через CRUD
    created_lead = crud.lead.create_with_calculation(db=db, obj_in=lead_in)

    # 2. Преобразуем созданный объект в Pydantic-схему для ответа
    lead_out_data = schemas.lead.LeadOut.model_validate(created_lead)

    # 3. Генерируем PDF и получаем путь к нему
    # В будущем здесь можно будет вернуть URL для скачивания
    pdf_path = pdf_generator.generate_lead_pdf(lead_out_data)
    lead_out_data.pdf_url = pdf_path # Добавляем путь в ответ API

    # 4. Здесь же можно будет добавить отправку уведомлений в Telegram/Email
    # notification_service.send_new_lead_notification(lead_out_data)

    return lead_out_data


@router.get("/", response_model=List[schemas.lead.LeadOut])
def read_leads(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Получить список всех лидов для админ-панели.
    """
    leads = crud.lead.get_multi(db, skip=skip, limit=limit)
    return leads
 main
