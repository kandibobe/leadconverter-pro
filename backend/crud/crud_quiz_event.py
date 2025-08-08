from sqlalchemy.orm import Session
from app.models import QuizEvent
from app.schemas import QuizEventCreate


class CRUDQuizEvent:
    def create(
        self,
        db: Session,
        *,
        obj_in: QuizEventCreate,
        tenant_id: str,
    ) -> QuizEvent:
        db_obj = QuizEvent(tenant_id=tenant_id, **obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_quiz(
        self,
        db: Session,
        *,
        quiz_id: int,
        tenant_id: str,
    ) -> list[QuizEvent]:
        return (
            db.query(QuizEvent)
            .filter(QuizEvent.tenant_id == tenant_id, QuizEvent.quiz_id == quiz_id)
            .order_by(QuizEvent.created_at.asc())
            .all()
        )


quiz_event = CRUDQuizEvent()
