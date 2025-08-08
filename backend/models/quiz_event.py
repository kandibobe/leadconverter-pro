from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class QuizEvent(Base):
    __tablename__ = "quiz_events"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    data = Column(JSONB, nullable=False)
