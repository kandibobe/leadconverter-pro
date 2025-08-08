import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app import crud, schemas
from app.api import deps

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
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
    logger.info("API: Request received for quiz_id: %s", quiz_id)
    logger.debug("API: Fetching quiz from database")
    quiz = crud.quiz.get(db=db, id=quiz_id)
    
    if not quiz:
        logger.warning(f"API: Quiz with id {quiz_id} not found in DB.")
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )
    
    logger.info(
        "API: Returning quiz '%s' with %s questions.",
        quiz.title,
        len(quiz.questions),
    )
    return quiz
