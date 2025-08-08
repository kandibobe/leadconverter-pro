from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api import deps
from app.models import lead as lead_model

router = APIRouter()


@router.get("/metrics")
def get_metrics(
    db: Session = Depends(deps.get_db),
    tenant_id: str = Depends(deps.get_tenant_id),
):
    """Return simple dashboard metrics for the current tenant."""
    total_leads, average_check = db.query(
        func.count(lead_model.Lead.id),
        func.coalesce(func.avg(lead_model.Lead.final_price), 0.0),
    ).filter(lead_model.Lead.tenant_id == tenant_id).one()

    return {"total_leads": total_leads, "average_check": average_check}

