from sqlalchemy.orm import Session, selectinload
from app.models.quiz import Quiz, Question, Option
from app.models.quiz_event import QuizEvent
from app.schemas.quiz import QuizCreate, Quiz as QuizSchema

class CRUDQuiz:
    def get(self, db: Session, id: int, tenant_id: str) -> Quiz | None:
        """
        Получение квиза по ID с принудительной "жадной" загрузкой (eager loading)
        всех связанных вопросов и, для каждого вопроса, всех связанных опций.
        Это решает проблему ленивой загрузки и гарантирует, что Pydantic получит полные данные.
        """
        return (
            db.query(Quiz)
            .options(selectinload(Quiz.questions).selectinload(Question.options))
            .filter(Quiz.id == id, Quiz.tenant_id == tenant_id)
            .first()
        )

    def create(self, db: Session, *, obj_in: QuizCreate, tenant_id: str) -> Quiz:
        """
        Создание квиза с рекурсивным созданием всех вложенных
        вопросов и вариантов ответов.
        """
        db_quiz = Quiz(
            title=obj_in.title,
            description=obj_in.description,
            tenant_id=tenant_id,
        )
        
        # Мы больше не добавляем объекты в сессию по одному.
        # SQLAlchemy 1.4+ достаточно умен, чтобы обработать каскадное сохранение,
        # если отношения настроены правильно (а они настроены).
        
        if obj_in.questions:
            for question_in in obj_in.questions:
                db_question = Question(
                    text=question_in.text,
                    description=question_in.description,
                    question_type=question_in.question_type,
                    order=question_in.order
                )
                if question_in.options:
                    for option_in in question_in.options:
                        db_option = Option(
                            text=option_in.text,
                            price_impact=option_in.price_impact,
                            order=option_in.order
                        )
                        db_question.options.append(db_option)
                db_quiz.questions.append(db_question)
        
        db.add(db_quiz)
        db.flush()

        snapshot = QuizSchema.model_validate(db_quiz).model_dump()
        db_event = QuizEvent(quiz_id=db_quiz.id, data=snapshot)
        db.add(db_event)

        db.commit()
        db.refresh(db_quiz)
        return db_quiz

# Создаем экземпляр нашего CRUD-класса для использования в API
quiz = CRUDQuiz()
