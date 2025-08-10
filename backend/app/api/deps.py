from typing import Generator
from fastapi import Header, Depends
from sqlalchemy import text
from app.services.lead_calculator import LeadCalculator

from backend.database import SessionLocal

def get_tenant_id(x_tenant_id: str = Header(...)) -> str:
    """Получить идентификатор арендатора из заголовка."""
    return x_tenant_id


def get_db(tenant_id: str = Depends(get_tenant_id)) -> Generator:
    """
    Зависимость, предоставляющая сессию базы данных и устанавливающая контекст арендатора.
    """
    db = SessionLocal()  
    try:
        # Устанавливаем идентификатор арендатора в контекст базы данных
        db.execute(text("SET app.tenant_id = :tenant_id"), {"tenant_id": tenant_id})
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        
def get_lead_calculator() -> LeadCalculator:
    """Provide LeadCalculator service instance."""
    return LeadCalculator()