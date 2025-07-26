from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Lead)
def create_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_in: schemas.LeadCreate,
):
    """
    Создать новый лид.
    """
    # ИМПОРТ ВНУТРИ ФУНКЦИИ:
    # Это разрывает любые циклы на уровне модулей и является более надежным паттерном.
    from app.services.notification_service import notification

    lead = crud.lead.create(db=db, obj_in=lead_in)
    
    # "Отправляем" уведомление
    notification.send_new_lead_notification(lead)
    
    return lead