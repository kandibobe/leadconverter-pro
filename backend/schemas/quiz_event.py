from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel


class QuizEventBase(BaseModel):
    quiz_id: int
    event_type: str
    payload: Dict[str, Any]


class QuizEventCreate(QuizEventBase):
    pass


class QuizEventOut(QuizEventBase):
    id: int
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True
