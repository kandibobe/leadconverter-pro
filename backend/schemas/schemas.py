from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional, Any

from .quiz import QuestionType

# --- Схемы для отображения квиза ---

class Option(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: int
    text: str
    question_type: QuestionType
    options: List[Option]

    class Config:
        orm_mode = True

class Quiz(BaseModel):
    id: int
    name: str
    description: str
    questions: List[Question]

    class Config:
        orm_mode = True

# --- Схемы для создания лида ---

class LeadAnswer(BaseModel):
    question_id: int
    option_id: int

class LeadCreate(BaseModel):
    quiz_id: int
    client_email: EmailStr
    answers: List[LeadAnswer]

class Lead(BaseModel):
    id: int
    client_email: EmailStr
    estimated_cost: float
    details: Dict[str, Any]

    class Config:
        orm_mode = True

