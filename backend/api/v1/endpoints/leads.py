import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app import crud, schemas
from app.api import deps
from app.services import pdf_generator  # Импортируем наш новый сервис


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/submit", response_model=schemas.lead.LeadOut)
def submit_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_in: schemas.lead.LeadCreateIn,
) -> Any:
    """Принять ответы квиза, рассчитать стоимость, сохранить лид и сгенерировать PDF."""
    logger.info("Submitting lead: %s", lead_in.model_dump())
    try:
        logger.debug("Creating lead with calculation")
        created_lead = crud.lead.create_with_calculation(db=db, obj_in=lead_in)
    except Exception:
        logger.exception("Failed to create lead")
        raise HTTPException(status_code=500, detail="Failed to create lead")

    logger.debug("Validating created lead data for response")
    lead_out_data = schemas.lead.LeadOut.model_validate(created_lead)

    try:
        logger.debug("Generating PDF for lead %s", created_lead.id)
        pdf_path = pdf_generator.generate_lead_pdf(lead_out_data)
    except Exception:
        logger.exception("Failed to generate PDF for lead %s", created_lead.id)
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

    lead_out_data.pdf_url = pdf_path  # Добавляем путь в ответ API
    logger.info("Lead %s processed successfully", lead_out_data.id)

    # 4. Здесь же можно будет добавить отправку уведомлений в Telegram/Email
    # notification_service.send_new_lead_notification(lead_out_data)

    return lead_out_data


@router.get("/", response_model=List[schemas.lead.LeadOut])
def read_leads(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Получить список всех лидов для админ-панели."""
    logger.debug("Fetching leads: skip=%s limit=%s", skip, limit)
    leads = crud.lead.get_multi(db, skip=skip, limit=limit)
    return leads
