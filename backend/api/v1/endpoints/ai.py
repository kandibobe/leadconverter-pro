from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from app.services import ai

router = APIRouter()


class LeadAIIn(BaseModel):
    client_email: EmailStr | None = None
    final_price: float = 0
    answers_details: Dict[str, Any] = {}


@router.post("/segment")
def segment(lead: LeadAIIn) -> Dict[str, str]:
    return {"segment": ai.auto_segment_lead(lead.model_dump())}


@router.post("/questions")
def questions(lead: LeadAIIn) -> Dict[str, Any]:
    return {"questions": ai.generate_followup_questions(lead.model_dump())}


@router.post("/ltv")
def ltv(lead: LeadAIIn) -> Dict[str, float]:
    return {"ltv": ai.predict_ltv(lead.model_dump())}


@router.post("/insights")
def insights(lead: LeadAIIn) -> Dict[str, Any]:
    data = lead.model_dump()
    return {
        "segment": ai.auto_segment_lead(data),
        "next_questions": ai.generate_followup_questions(data),
        "ltv_prediction": ai.predict_ltv(data),
    }
