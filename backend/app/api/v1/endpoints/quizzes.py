from fastapi import APIRouter, Depends, HTTPException, Response, status
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

# --- НОВЫЕ ЭНДПОИНТЫ ДЛЯ ТРЕКИНГА ---
@router.post("/{quiz_id}/view", status_code=status.HTTP_204_NO_CONTENT)
def track_quiz_view(quiz_id: int, db: Session = Depends(deps.get_db)):
    """
    Регистрирует один просмотр квиза.
    Вызывается фронтендом при загрузке страницы с квизом.
    """
    quiz = crud.quiz.increment_views(db=db, quiz_id=quiz_id)
    if not quiz:
        # Не бросаем 404, чтобы не ломать фронтенд, если квиз удалили
        # Просто ничего не делаем
        pass
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{quiz_id}/start", status_code=status.HTTP_204_NO_CONTENT)
def track_quiz_start(quiz_id: int, db: Session = Depends(deps.get_db)):
    """
    Регистрирует начало взаимодействия с квизом.
    Вызывается фронтендом при первом ответе пользователя.
    """
    quiz = crud.quiz.increment_starts(db=db, quiz_id=quiz_id)
    if not quiz:
        pass
    return Response(status_code=status.HTTP_204_NO_CONTENT)
# ------------------------------------