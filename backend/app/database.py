from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """ORM Base, без engine/session (важно для Alembic)."""
    pass
