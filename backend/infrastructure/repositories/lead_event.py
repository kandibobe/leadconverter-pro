from sqlalchemy.orm import Session
from app.infrastructure.models import LeadEvent
from app.domain.lead_event import LeadEventCreate


class CRUDLeadEvent:
    def create(
        self,
        db: Session,
        *,
        obj_in: LeadEventCreate,
        tenant_id: str,
    ) -> LeadEvent:
        db_obj = LeadEvent(tenant_id=tenant_id, **obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_lead(
        self,
        db: Session,
        *,
        lead_id: int,
        tenant_id: str,
    ) -> list[LeadEvent]:
        return (
            db.query(LeadEvent)
            .filter(LeadEvent.tenant_id == tenant_id, LeadEvent.lead_id == lead_id)
            .order_by(LeadEvent.created_at.asc())
            .all()
        )


lead_event = CRUDLeadEvent()
