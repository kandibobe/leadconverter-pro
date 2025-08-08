from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_quiz import quiz as crud_quiz
from app.crud.crud_lead import lead as crud_lead
from app.schemas.quiz import Quiz
from app.schemas.lead import LeadCreateIn, LeadOut
from app.database import get_db

router = APIRouter()

@router.get("/quizzes/{quiz_id}", response_model=Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Получить структуру квиза по его ID.
    Это то, что фронтенд будет запрашивать для отображения опросника.
    """
    db_quiz = crud_quiz.get(db, id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.post("/leads", response_model=LeadOut)
def submit_lead(lead: LeadCreateIn, db: Session = Depends(get_db)):
    """
    Принять ответы квиза, рассчитать стоимость и сохранить лид.
    Возвращает созданный лид с итоговой ценой.
    """
    # Здесь можно добавить логику для отправки PDF и уведомлений в будущем
    created_lead = crud_lead.create_with_calculation(db=db, obj_in=lead)
    return LeadOut.model_validate(created_lead)