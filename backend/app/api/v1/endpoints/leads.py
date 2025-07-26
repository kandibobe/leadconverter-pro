from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app import crud, schemas
from app.api import deps
from app.services import pdf_generator # Импортируем наш новый сервис

router = APIRouter()

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