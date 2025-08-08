import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, List
from app import crud, schemas
from app.api import deps
from app.models.quiz_event import QuizEvent as QuizEventModel
from app.models.quiz import Quiz, Question, Option

# Настраиваем базовый логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(
    quiz_id: int,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
) -> Any:
    """
    Получить полную структуру квиза по его ID.
    """
    logger.info(f"API: Request received for quiz_id: {quiz_id}")
    quiz = crud.quiz.get(db=db, id=quiz_id, tenant_id=tenant_id)
    
    if not quiz:
        logger.warning(f"API: Quiz with id {quiz_id} not found in DB.")
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )
    
    logger.info(f"API: Returning quiz '{quiz.title}' with {len(quiz.questions)} questions.")
    return quiz


@router.get("/{quiz_id}/history", response_model=List[schemas.QuizEvent])
def quiz_history(
    quiz_id: int,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
) -> Any:
    events = (
        db.query(QuizEventModel)
        .join(Quiz, QuizEventModel.quiz_id == Quiz.id)
        .filter(QuizEventModel.quiz_id == quiz_id, Quiz.tenant_id == tenant_id)
        .order_by(QuizEventModel.timestamp.desc())
        .all()
    )
    return events


@router.post("/{quiz_id}/rollback/{event_id}", response_model=schemas.Quiz)
def quiz_rollback(
    quiz_id: int,
    event_id: int,
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
) -> Any:
    quiz_obj = (
        db.query(Quiz)
        .filter(Quiz.id == quiz_id, Quiz.tenant_id == tenant_id)
        .first()
    )
    if not quiz_obj:
        raise HTTPException(status_code=404, detail="Quiz not found")

    event = (
        db.query(QuizEventModel)
        .filter(QuizEventModel.id == event_id, QuizEventModel.quiz_id == quiz_id)
        .first()
    )
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    data = event.data
    for question in list(quiz_obj.questions):
        db.delete(question)

    quiz_obj.title = data.get("title", quiz_obj.title)
    quiz_obj.description = data.get("description")

    for q in data.get("questions", []):
        db_question = Question(
            text=q["text"],
            description=q.get("description"),
            question_type=q.get("question_type", "single-choice"),
            order=q.get("order", 0),
        )
        for op in q.get("options", []):
            db_option = Option(
                text=op["text"],
                price_impact=op.get("price_impact", 0.0),
                order=op.get("order", 0),
            )
            db_question.options.append(db_option)
        quiz_obj.questions.append(db_question)

    db.add(quiz_obj)
    snapshot = schemas.Quiz.model_validate(quiz_obj).model_dump()
    db_event = QuizEventModel(quiz_id=quiz_obj.id, data=snapshot)
    db.add(db_event)
    db.commit()
    db.refresh(quiz_obj)
    return quiz_obj
