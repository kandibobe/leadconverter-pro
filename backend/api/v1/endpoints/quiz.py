import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas
from app.database import get_db


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/quizzes/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Получить структуру квиза по его ID.
    Это то, что фронтенд будет запрашивать для отображения опросника.
    """
    logger.info("Fetching quiz %s", quiz_id)
    db_quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if db_quiz is None:
        logger.warning("Quiz %s not found", quiz_id)
        raise HTTPException(status_code=404, detail="Quiz not found")
    logger.info("Quiz %s retrieved successfully", quiz_id)
    return db_quiz

@router.post("/leads", response_model=schemas.Lead)
def submit_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    """Принять ответы квиза, рассчитать стоимость и сохранить лид."""
    logger.info("Submitting lead: %s", lead.model_dump())
    try:
        created_lead = crud.create_lead(db=db, lead_data=lead)
    except Exception:
        logger.exception("Failed to create lead")
        raise HTTPException(status_code=500, detail="Failed to create lead")
    logger.info("Lead %s created successfully", created_lead.id)
    return created_lead

