from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

# Теперь этот импорт корректно найдет все, что нам нужно
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(
    quiz_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Получить полную структуру квиза по его ID.
    """
    quiz = crud.quiz.get(db=db, id=quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )
    return quiz