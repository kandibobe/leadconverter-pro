# В файле backend/app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ... (существующие схемы)

class LeadOut(BaseModel):
    id: int
    email: str
    final_price: float
    created_at: datetime

    class Config:
        orm_mode = True

class DashboardMetrics(BaseModel):
    total_leads: int
    average_check: float