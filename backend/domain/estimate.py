# backend/domain/estimate.py
from pydantic import BaseModel
from typing import List
from app.domain.lead import LeadAnswerIn

class EstimateRequest(BaseModel):
    quiz_id: int
    answers: List[LeadAnswerIn]

class EstimateResponse(BaseModel):
    estimated_cost: float
