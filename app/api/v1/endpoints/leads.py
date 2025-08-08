from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from app import crud, schemas
from app.api import deps
from app.services import pdf_generator

router = APIRouter()


@router.post("/submit", response_model=schemas.lead.LeadOut)
def submit_lead(
    *,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
    lead_in: schemas.lead.LeadCreateIn,
) -> Any:
    """Принять ответы квиза, рассчитать стоимость, сохранить лид и сгенерировать PDF."""
    quiz = crud.quiz.get(db, id=lead_in.quiz_id, tenant_id=tenant_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    question_map = {q.id: q for q in quiz.questions}
    for ans in lead_in.answers:
        question = question_map.get(ans.question_id)
        if not question:
            raise HTTPException(status_code=400, detail="Invalid question")
        if question.question_type != "slider":
            option_ids = {opt.id for opt in question.options}
            if ans.option_id not in option_ids:
                raise HTTPException(status_code=400, detail="Invalid option")

    created_lead = crud.lead.create_with_calculation(
        db=db, obj_in=lead_in, tenant_id=tenant_id
    )

    lead_out_data = schemas.lead.LeadOut.model_validate(created_lead)
    pdf_path = pdf_generator.generate_lead_pdf(lead_out_data)
    lead_out_data.pdf_url = pdf_path

    return lead_out_data


@router.get("/", response_model=List[schemas.lead.LeadOut])
def read_leads(
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Получить список всех лидов для админ-панели."""
    leads = crud.lead.get_multi(db, tenant_id=tenant_id, skip=skip, limit=limit)
    return leads

