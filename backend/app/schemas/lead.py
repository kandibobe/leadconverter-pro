from pydantic import BaseModel, EmailStr
from typing import Dict, Any

class LeadBase(BaseModel):
    email: EmailStr
    final_price: float
    answers_data: Dict[str, Any]

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    class Config:
        from_attributes = True