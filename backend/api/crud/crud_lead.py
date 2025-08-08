import logging
from sqlalchemy.orm import Session
from app.models import lead as lead_model
from app.schemas import lead as lead_schema
from app.services.lead_calculator import LeadCalculator, LeadCalculationError

logger = logging.getLogger(__name__)

class CRUDLead:
    def create_with_calculation(
    self,
        db: Session,
        *,
        obj_in: lead_schema.LeadCreateIn,
        tenant_id: str,
        calculator: LeadCalculator | None = None,
    ) -> lead_model.Lead:
         
         """Create lead and calculate price using LeadCalculator."""
        calc = calculator or LeadCalculator()
        try:
            final_price, answers_details = calc.calculate(db, obj_in.answers)
        except LeadCalculationError:
            logger.exception("Lead calculation failed")
            raise


        lead_create_data = lead_schema.LeadCreateInternal(
            quiz_id=obj_in.quiz_id,
            client_email=obj_in.client_email,
            final_price=final_price,
            answers_details=answers_details,
            tenant_id=tenant_id,
        )

        db_obj = lead_model.Lead(**lead_create_data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, tenant_id: str, skip: int = 0, limit: int = 100
    ) -> list[lead_model.Lead]:
        return (
            db.query(lead_model.Lead)
            .filter(lead_model.Lead.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


lead = CRUDLead()
