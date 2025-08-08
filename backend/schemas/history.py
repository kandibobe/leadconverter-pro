from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel


class LeadEvent(BaseModel):
    id: int
    lead_id: int
    timestamp: datetime
    data: Dict[str, Any]

    class Config:
        from_attributes = True


class QuizEvent(BaseModel):
    id: int
    quiz_id: int
    timestamp: datetime
    data: Dict[str, Any]

    class Config:
        from_attributes = True
