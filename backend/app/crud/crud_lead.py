from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate

class CRUDLead:
    def create(self, db: Session, *, obj_in: LeadCreate) -> Lead:
        db_obj = Lead(
            email=obj_in.email,
            final_price=obj_in.final_price,
            answers_data=obj_in.answers_data
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

lead = CRUDLead()