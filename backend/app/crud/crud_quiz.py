from sqlalchemy.orm import Session, selectinload
from app.models.quiz import Quiz, Question, Option
from app.schemas.quiz import QuizCreate

class CRUDQuiz:
    def get(self, db: Session, id: int) -> Quiz | None:
        """
        Получение квиза по ID с принудительной "жадной" загрузкой (eager loading)
        всех связанных вопросов и, для каждого вопроса, всех связанных опций.
        """
        return db.query(Quiz).options(
            selectinload(Quiz.questions).selectinload(Question.options)
        ).filter(Quiz.id == id).first()

    def create(self, db: Session, *, obj_in: QuizCreate) -> Quiz:
        """
        Создание квиза с рекурсивным созданием всех вложенных
        вопросов и вариантов ответов.
        """
        db_quiz = Quiz(
            title=obj_in.title,
            description=obj_in.description
        )
        
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
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    # --- НОВЫЕ МЕТОДЫ ДЛЯ СЧЕТЧИКОВ ---
    def increment_views(self, db: Session, *, quiz_id: int) -> Quiz | None:
        """Увеличивает счетчик просмотров для квиза."""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if quiz:
            quiz.views += 1
            db.commit()
            db.refresh(quiz)
        return quiz

    def increment_starts(self, db: Session, *, quiz_id: int) -> Quiz | None:
        """Увеличивает счетчик начатых расчетов для квиза."""
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if quiz:
            quiz.starts += 1
            db.commit()
            db.refresh(quiz)
        return quiz
    # ------------------------------------

quiz = CRUDQuiz()