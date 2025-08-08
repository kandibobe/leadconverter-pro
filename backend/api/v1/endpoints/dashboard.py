from fastapi import APIRouter

router = APIRouter()

@router.get("/metrics")
def metrics() -> dict[str, float]:
    return {"total_leads": 0, "average_check": 0.0}
