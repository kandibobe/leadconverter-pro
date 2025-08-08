from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app import crud, schemas
from app.api import deps
from app.models import lead as lead_model
from app.models.lead_event import LeadEvent as LeadEventModel
from app.services import pdf_generator  # Импортируем наш новый сервис

router = APIRouter()

@router.post("/submit", response_model=schemas.lead.LeadOut)
def submit_lead(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
    lead_in: schemas.lead.LeadCreateIn,
) -> Any:
    """
    Принять ответы квиза, рассчитать стоимость, сохранить лид и сгенерировать PDF.
    Это основной эндпоинт для фронтенда.
    """
    # 1. Создаем лид с расчетом цены через CRUD
    created_lead = crud.lead.create_with_calculation(
        db=db, obj_in=lead_in, tenant_id=tenant_id
    )

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
    tenant_id: str = Depends(deps.get_tenant_id),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Получить список всех лидов для админ-панели.
    """
    leads = crud.lead.get_multi(db, tenant_id=tenant_id, skip=skip, limit=limit)
    return leads


@router.get("/{lead_id}/history", response_model=List[schemas.LeadEvent])
def lead_history(
    lead_id: int,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
) -> Any:
    events = (
        db.query(LeadEventModel)
        .join(lead_model.Lead, LeadEventModel.lead_id == lead_model.Lead.id)
        .filter(LeadEventModel.lead_id == lead_id, lead_model.Lead.tenant_id == tenant_id)
        .order_by(LeadEventModel.timestamp.desc())
        .all()
    )
    return events


@router.post("/{lead_id}/rollback/{event_id}", response_model=schemas.lead.LeadOut)
def lead_rollback(
    lead_id: int,
    event_id: int,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
) -> Any:
    lead_obj = (
        db.query(lead_model.Lead)
        .filter(lead_model.Lead.id == lead_id, lead_model.Lead.tenant_id == tenant_id)
        .first()
    )
    if not lead_obj:
        raise HTTPException(status_code=404, detail="Lead not found")

    event = (
        db.query(LeadEventModel)
        .filter(LeadEventModel.id == event_id, LeadEventModel.lead_id == lead_id)
        .first()
    )
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for field, value in event.data.items():
        if field == "id":
            continue
        setattr(lead_obj, field, value)

    db.add(lead_obj)
    db_event = LeadEventModel(lead_id=lead_obj.id, data=event.data)
    db.add(db_event)
    db.commit()
    db.refresh(lead_obj)
    return lead_obj
