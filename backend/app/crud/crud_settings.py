from sqlalchemy.orm import Session
from app.models.settings import CompanySettings
from app.schemas.settings import CompanySettingsUpdate

class CRUDSettings:
    def get(self, db: Session) -> CompanySettings | None:
        return db.query(CompanySettings).first()

    def update(self, db: Session, *, db_obj: CompanySettings, obj_in: CompanySettingsUpdate) -> CompanySettings:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

settings = CRUDSettings()