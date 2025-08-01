from sqlalchemy.orm import Session
from . import models, schemas

def get_quiz(db: Session, quiz_id: int):
    """Получение квиза со всеми вопросами и вариантами ответов."""
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

def create_lead(db: Session, lead_data: schemas.LeadCreate) -> models.Lead:
    """Создание лида на основе ответов."""
    
    # Рассчитываем итоговую стоимость
    total_cost = 0.0
    details_answers = {}
    for answer in lead_data.answers:
        option = db.query(models.Option).filter(models.Option.id == answer.option_id).first()
        if option:
            total_cost += option.value
            question_text = option.question.text
            details_answers[question_text] = option.text

    # Создаем запись в БД
    db_lead = models.Lead(
        client_email=lead_data.client_email,
        estimated_cost=total_cost,
        details={
            "quiz_id": lead_data.quiz_id,
            "answers": details_answers
        }
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead