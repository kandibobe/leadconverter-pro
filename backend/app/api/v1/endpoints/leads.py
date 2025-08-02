from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Any
from app import crud, schemas
from app.api import deps
from app.services import pdf_generator, email_service

router = APIRouter()

@router.post("/submit", response_model=schemas.LeadOut)
async def submit_lead(
    *,
    db: Session = Depends(deps.get_db),
    lead_in: schemas.LeadCreateIn,
    background_tasks: BackgroundTasks
) -> Any:
    created_lead = crud.lead.create_with_calculation(db=db, obj_in=lead_in)
    lead_out_data = schemas.LeadOut.model_validate(created_lead)
    
    pdf_path = pdf_generator.generate_lead_pdf(lead_out_data)
    lead_out_data.pdf_url = pdf_path
    
    # Добавляем отправку email в фоновую задачу
    background_tasks.add_task(
        email_service.send_lead_confirmation_email, lead_out_data, pdf_path
    )
    
    return lead_out_data

@router.get("/", response_model=List[schemas.LeadOut])
def read_leads(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    leads = crud.lead.get_multi(db, skip=skip, limit=limit)
    return leads

@router.patch("/{lead_id}", response_model=schemas.LeadOut)
def update_lead_status(
    *,
    db: Session = Depends(deps.get_db),
    lead_id: int,
    lead_in: schemas.LeadUpdate,
):
    """
    Обновить статус лида.
    """
    lead = crud.lead.get(db=db, id=lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead = crud.lead.update(db=db, db_obj=lead, obj_in=lead_in)
    return lead