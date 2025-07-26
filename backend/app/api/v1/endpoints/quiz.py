from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/quizzes/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(deps.get_db)):
    """
    Получить структуру квиза по его ID.
    Это то, что фронтенд будет запрашивать для отображения опросника.
    """
    db_quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.post("/leads", response_model=schemas.Lead)
def submit_lead(lead: schemas.LeadCreate, db: Session = Depends(deps.get_db)):
    """
    Принять ответы квиза, рассчитать стоимость и сохранить лид.
    Возвращает созданный лид с итоговой ценой.
    """
    # Здесь можно добавить логику для отправки PDF и уведомлений в будущем
    return crud.create_lead(db=db, lead_data=lead)