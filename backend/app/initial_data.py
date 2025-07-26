import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base, session # <-- Импортируем base и session
# Импортируем все модели, чтобы Base знал о них перед созданием таблиц
from app.models.quiz import Quiz
from app.models.lead import Lead

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """
    Инициализация базы данных.
    1. Создает все таблицы.
    2. Наполняет данными, если их нет.
    """
    # ИСПРАВЛЕНИЕ: Используем правильный путь base.Base
    logger.info("Creating database tables...")
    base.Base.metadata.create_all(bind=session.engine)
    logger.info("Tables created.")

    # Наполнение данными
    quiz = crud.quiz.get(db, id=1)
    if not quiz:
        logger.info("Seeding initial quiz data...")
        initial_quiz_data = schemas.QuizCreate(
            title="Калькулятор ремонта в новостройке",
            description="Ответьте на несколько вопросов и получите примерную стоимость вашего ремонта.",
            questions=[
                schemas.QuestionCreate(
                    text="Какой тип ремонта вы планируете?",
                    question_type="single-choice",
                    order=1,
                    options=[
                        schemas.OptionCreate(text="Косметический", price_impact=5000, order=1),
                        schemas.OptionCreate(text="Капитальный (White box)", price_impact=15000, order=2),
                        schemas.OptionCreate(text="Дизайнерский", price_impact=30000, order=3),
                    ]
                ),
                schemas.QuestionCreate(
                    text="Укажите площадь вашей квартиры, м²",
                    description="Итоговая стоимость будет умножена на площадь.",
                    question_type="slider",
                    order=2,
                    options=[]
                ),
                schemas.QuestionCreate(
                    text="Нужна ли перепланировка?",
                    question_type="single-choice",
                    order=3,
                    options=[
                        schemas.OptionCreate(text="Да, требуется снос и возведение стен", price_impact=80000, order=1),
                        schemas.OptionCreate(text="Нет, планировка остается прежней", price_impact=0, order=2),
                    ]
                ),
            ]
        )
        crud.quiz.create(db=db, obj_in=initial_quiz_data)
        logger.info("Seeding complete.")
    else:
        logger.info("Quiz data already exists. Skipping seeding.")
