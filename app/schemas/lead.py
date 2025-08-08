from pydantic import BaseModel, EmailStr, Field
from typing import List, Dict, Any, Optional

# Схема для одного ответа, который присылает фронтенд
class LeadAnswerIn(BaseModel):
    question_id: int
    option_id: Optional[int] = None # Необязательно для слайдера
    value: Optional[str | int | float] = None # Для слайдера или текстового поля

# Схема для создания лида (то, что мы ждем от фронтенда)
class LeadCreateIn(BaseModel):
    quiz_id: int
    client_email: EmailStr
    answers: List[LeadAnswerIn]

# Схема для внутреннего использования при создании в CRUD
class LeadCreateInternal(BaseModel):
    quiz_id: int
    client_email: EmailStr
    final_price: float
    answers_details: Dict[str, Any]
    tenant_id: str

# Финальная схема для ответа API (то, что мы возвращаем фронтенду)
class LeadOut(BaseModel):
    id: int
    client_email: EmailStr
    final_price: float = Field(..., description="Итоговая рассчитанная стоимость")
    answers_details: Dict[str, Any] = Field(..., description="Детализация ответов")
    pdf_url: Optional[str] = Field(None, description="Ссылка на сгенерированный PDF")
    tenant_id: str

    class Config:
        from_attributes = True
