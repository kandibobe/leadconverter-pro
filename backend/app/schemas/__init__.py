from .quiz import Quiz, QuizCreate, Question, QuestionCreate, Option, OptionCreate
from .lead import (
    LeadOut as Lead,           # схема ответа API
    LeadCreateIn as LeadCreate,  # схема входящих данных
    LeadCreateInternal         # используется в CRUD
)
