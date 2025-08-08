# /backend/initial_data.py

from backend.database import SessionLocal
from backend.models import Quiz, Question, Option

def seed_data():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже квизы, чтобы не создавать дубликаты
        if db.query(Quiz).count() == 0:
            print("База данных пуста. Начинаю наполнение...")

            # --- Создаем Квиз "Ремонт квартир" ---
            quiz = Quiz(
                name="Калькулятор ремонта квартиры",
                description="Ответьте на несколько вопросов и получите предварительную смету на ремонт вашей мечты."
            )
            db.add(quiz)
            db.commit()
            db.refresh(quiz)

            # --- Вопрос 1: Тип жилья ---
            q1 = Question(text="Какой у вас тип жилья?", quiz_id=quiz.id)
            db.add(q1)
            db.commit()
            db.refresh(q1)
            o1_1 = Option(text="Новостройка", value=5000, question_id=q1.id)
            o1_2 = Option(text="Вторичное жилье", value=15000, question_id=q1.id) # Демонтаж дороже
            db.add_all([o1_1, o1_2])

            # --- Вопрос 2: Площадь ---
            q2 = Question(text="Укажите площадь помещения (м²)?", question_type="slider", quiz_id=quiz.id)
            db.add(q2)
            db.commit()
            db.refresh(q2)
            # Для слайдера можно задать цену за единицу (например, за м²)
            o2_1 = Option(text="Площадь", value=3000, question_id=q2.id) # 3000 за м²
            db.add(o2_1)

            # --- Вопрос 3: Тип ремонта ---
            q3 = Question(text="Какой тип ремонта планируете?", quiz_id=quiz.id)
            db.add(q3)
            db.commit()
            db.refresh(q3)
            o3_1 = Option(text="Косметический", value=20000, question_id=q3.id)
            o3_2 = Option(text="Капитальный", value=100000, question_id=q3.id)
            o3_3 = Option(text="Дизайнерский", value=250000, question_id=q3.id)
            db.add_all([o3_1, o3_2, o3_3])

            db.commit()
            print("Данные для квиза 'Ремонт квартир' успешно созданы.")
        else:
            print("В базе данных уже есть данные. Наполнение не требуется.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
