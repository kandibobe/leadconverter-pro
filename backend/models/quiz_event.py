from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from app.database import Base


class QuizEvent(Base):
    """Событие, связанное с квизом."""

    __tablename__ = "quiz_events"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True, nullable=False)
    quiz_id = Column(Integer, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
