# /backend/initial_data.py

from app.db.session import SessionLocal
# --- ИЗМЕНЕННЫЙ ИМПОРТ ---
from app.db.models import Quiz, Question, Option

def seed_data():
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже квизы, чтобы не создавать дубликаты
        if db.query(Quiz).count() == 0:
            print("База данных пуста. Начинаю наполнение...")

            # --- Создаем Квиз "Ремонт квартир" ---
            quiz = Quiz(
                title="Калькулятор ремонта квартиры", # Поле было name, меняем на title
                description="Ответьте на несколько вопросов и получите предварительную смету на ремонт вашей мечты."
            )
            db.add(quiz)
            db.commit()
            db.refresh(quiz)

            # --- Вопрос 1: Тип жилья ---
            q1 = Question(text="Какой у вас тип жилья?", quiz_id=quiz.id, order=1)
            db.add(q1)
            db.commit()
            db.refresh(q1)
            o1_1 = Option(text="Новостройка", price_impact=5000, question_id=q1.id, order=1)
            o1_2 = Option(text="Вторичное жилье", price_impact=15000, question_id=q1.id, order=2) # Демонтаж дороже
            db.add_all([o1_1, o1_2])

            # --- Вопрос 2: Площадь ---
            q2 = Question(text="Укажите площадь помещения (м²)?", question_type="slider", quiz_id=quiz.id, order=2)
            db.add(q2)
            db.commit()
            db.refresh(q2)
            # Для слайдера опции не нужны, логика расчета в другом месте

            # --- Вопрос 3: Тип ремонта ---
            q3 = Question(text="Какой тип ремонта планируете?", quiz_id=quiz.id, order=3)
            db.add(q3)
            db.commit()
            db.refresh(q3)
            o3_1 = Option(text="Косметический", price_impact=20000, question_id=q3.id, order=1)
            o3_2 = Option(text="Капитальный", price_impact=100000, question_id=q3.id, order=2)
            o3_3 = Option(text="Дизайнерский", price_impact=250000, question_id=q3.id, order=3)
            db.add_all([o3_1, o3_2, o3_3])

            db.commit()
            print("Данные для квиза 'Ремонт квартир' успешно созданы.")
        else:
            print("В базе данных уже есть данные. Наполнение не требуется.")

    finally:
        db.close()

if __name__ == "__main__":
    print("Запуск наполнения базы данных начальными данными...")
    seed_data()