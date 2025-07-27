# Этот файл собирает все Pydantic модели (схемы) в одном месте.

# Импортируем все схемы, связанные с квизами
from .quiz import Quiz, QuizCreate, Question, QuestionCreate, Option, OptionCreate

# Импортируем все схемы, связанные с лидами
from .lead import LeadOut, LeadCreateIn, LeadCreateInternal, LeadAnswerIn

# Импортируем схемы для дашборда
from .dashboard import DashboardMetrics