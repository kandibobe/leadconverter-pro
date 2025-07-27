from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(deps.get_db)):
    quiz = crud.quiz.get(db=db, id=quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/calculate", response_model=float)
def calculate_price(
    *,
    db: Session = Depends(deps.get_db),
    calculation_data: schemas.LeadCreateIn
):
    """
    Рассчитывает предварительную стоимость в реальном времени.
    """
    price = crud.lead.calculate_price_from_answers(db=db, answers_in=calculation_data.answers)
    return price