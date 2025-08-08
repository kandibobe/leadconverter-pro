from sqlalchemy.orm import Session
from app.crud.crud_quiz import quiz as crud_quiz
from app.schemas import quiz as quiz_schema

def init_db(db: Session) -> None:
    """
    Инициализация базы данных.
    Проверяет наличие квиза и, если его нет, создает его.
    """
    quiz = crud_quiz.get(db, id=1)
    if quiz:
        print("Quiz data already exists. Skipping seeding.")
        return

    print("Seeding initial quiz data...")
    
    initial_quiz_data = quiz_schema.QuizCreate(
        title="Калькулятор ремонта в новостройке",
        description="Ответьте на несколько вопросов и получите примерную стоимость вашего ремонта.",
        questions=[
            quiz_schema.QuestionCreate(
                text="Какой тип ремонта вы планируете?",
                question_type="single-choice",
                order=1,
                options=[
                    quiz_schema.OptionCreate(text="Косметический", price_impact=5000, order=1),
                    quiz_schema.OptionCreate(text="Капитальный (White box)", price_impact=15000, order=2),
                    quiz_schema.OptionCreate(text="Дизайнерский", price_impact=30000, order=3),
                ]
            ),
            quiz_schema.QuestionCreate(
                text="Укажите площадь вашей квартиры, м²",
                description="Итоговая стоимость будет умножена на площадь.",
                question_type="slider",
                order=2,
                options=[]
            ),
            quiz_schema.QuestionCreate(
                text="Нужна ли перепланировка?",
                question_type="single-choice",
                order=3,
                options=[
                    quiz_schema.OptionCreate(text="Да, требуется снос и возведение стен", price_impact=80000, order=1),
                    quiz_schema.OptionCreate(text="Нет, планировка остается прежней", price_impact=0, order=2),
                ]
            ),
        ]
    )
    
    # Вызываем новую, полноценную CRUD-функцию
    crud_quiz.create(db=db, obj_in=initial_quiz_data)
    print("Seeding complete.")