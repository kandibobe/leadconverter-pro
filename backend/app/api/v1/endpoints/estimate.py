# backend/app/api/v1/endpoints/estimate.py
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from ... import deps
from app.schemas.estimate import EstimateRequest, EstimateResponse
from app.services.lead_calculator import LeadCalculator
from app.services.estimate_service import calculate_estimate

router = APIRouter()

@router.post("/", response_model=EstimateResponse)
async def recalc_estimate(
    payload: EstimateRequest,
    db: Session = Depends(deps.get_db),
    calculator: LeadCalculator = Depends(deps.get_lead_calculator),
) -> EstimateResponse:
   price = await run_in_threadpool(calculate_estimate, db, payload, calculator)
   return EstimateResponse(estimated_cost=price)
