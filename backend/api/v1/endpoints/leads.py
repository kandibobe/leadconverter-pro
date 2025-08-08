from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app.api import deps
from app.application.services import pdf_generator  # Генерация PDF
from app.domain import lead as lead_schema, lead_event as lead_event_schema
from app.infrastructure.repositories import lead as lead_repo, lead_event as lead_event_repo

router = APIRouter()


@router.post("/submit", response_model=lead_schema.LeadOut)
def submit_lead(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
    lead_in: lead_schema.LeadCreateIn,
) -> Any:
    """
    Принять ответы квиза, рассчитать стоимость, сохранить лид и сгенерировать PDF.
    Это основной эндпоинт для фронтенда.
    """
    # 1. Создаем лид с расчетом цены через репозиторий
    created_lead = lead_repo.create_with_calculation(
        db=db, obj_in=lead_in, tenant_id=tenant_id
    )

    lead_event_repo.create(
        db=db,
        obj_in=lead_event_schema.LeadEventCreate(
            lead_id=created_lead.id,
            event_type="created",
            payload={
                "final_price": created_lead.final_price,
                "answers_details": created_lead.answers_details,
            },
        ),
        tenant_id=tenant_id,
    )

    # 2. Преобразуем созданный объект в Pydantic-схему для ответа
    lead_out_data = lead_schema.LeadOut.model_validate(created_lead)

    # 3. Генерируем PDF и получаем путь к нему
    # В будущем здесь можно будет вернуть URL для скачивания
    pdf_path = pdf_generator.generate_lead_pdf(lead_out_data)
    lead_out_data.pdf_url = pdf_path  # Добавляем путь в ответ API

    # 4. Здесь же можно будет добавить отправку уведомлений в Telegram/Email
    # notification_service.send_new_lead_notification(lead_out_data)

    return lead_out_data


@router.get("/", response_model=List[lead_schema.LeadOut])
def read_leads(
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Получить список всех лидов для админ-панели.
    """
    leads = lead_repo.get_multi(db, tenant_id=tenant_id, skip=skip, limit=limit)
    return leads


@router.get("/{lead_id}/events", response_model=List[lead_event_schema.LeadEventOut])
def read_lead_events(
    lead_id: int,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
) -> Any:
    """Получить историю событий для лида."""
    events = lead_event_repo.get_multi_by_lead(
        db=db, lead_id=lead_id, tenant_id=tenant_id
    )
    return events
