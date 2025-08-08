# backend/api/v1/endpoints/estimate.py
from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from ... import deps
from app.schemas.estimate import EstimateRequest, EstimateResponse
from backend.services.estimate_service import calculate_estimate

router = APIRouter()

@router.post("/", response_model=EstimateResponse)
async def recalc_estimate(
    payload: EstimateRequest,
    db: Session = Depends(deps.get_db),
) -> EstimateResponse:
    cost = await run_in_threadpool(calculate_estimate, db, payload)
    return EstimateResponse(estimated_cost=cost)
