from pydantic import BaseModel, Field
from typing import List, Optional


# --- Схемы для Вариантов Ответов (Option) ---
class OptionBase(BaseModel):
    text: str
    price_impact: float = 0.0
    order: int


class OptionCreate(OptionBase):
    pass


class Option(OptionBase):
    id: int

    class Config:
        from_attributes = True  # Раньше называлось orm_mode


# --- Схемы для Вопросов (Question) ---
class QuestionBase(BaseModel):
    text: str
    description: Optional[str] = None
    question_type: str
    order: int


class QuestionCreate(QuestionBase):
    options: List[OptionCreate]


class Question(QuestionBase):
    id: int
    options: List[Option] = Field(default_factory=list)

    class Config:
        from_attributes = True


# --- Схемы для Квиза (Quiz) ---
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None


class QuizCreate(QuizBase):
    questions: List[QuestionCreate]


# Эта схема будет использоваться для ответа API: полный квиз со всеми вопросами и вариантами
class Quiz(QuizBase):
    id: int
    questions: List[Question] = Field(default_factory=list)

    class Config:
        from_attributes = True
