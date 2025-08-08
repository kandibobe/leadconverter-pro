from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class LeadEvent(Base):
    __tablename__ = "lead_events"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data = Column(JSONB, nullable=False)
