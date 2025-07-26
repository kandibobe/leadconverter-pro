import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app import crud, schemas
from app.api import deps

# Настраиваем базовый логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(
    quiz_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Получить полную структуру квиза по его ID.
    """
    logger.info(f"API: Request received for quiz_id: {quiz_id}")
    quiz = crud.quiz.get(db=db, id=quiz_id)
    
    if not quiz:
        logger.warning(f"API: Quiz with id {quiz_id} not found in DB.")
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )
    
    logger.info(f"API: Returning quiz '{quiz.title}' with {len(quiz.questions)} questions.")
    return quiz
