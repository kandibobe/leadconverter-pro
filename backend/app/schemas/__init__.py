# Этот файл делает классы из quiz.py доступными на уровне пакета schemas.
# Теперь импорт `from app.schemas import Quiz` будет работать.
from .quiz import Quiz, QuizCreate, Question, QuestionCreate, Option, OptionCreate