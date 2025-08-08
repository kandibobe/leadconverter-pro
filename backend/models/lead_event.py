from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from app.database import Base


class LeadEvent(Base):
    """Событие, связанное с лидом."""

    __tablename__ = "lead_events"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True, nullable=False)
    lead_id = Column(Integer, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
