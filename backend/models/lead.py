from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, func
from app.db.base import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, nullable=False)
    client_email = Column(String, index=True, nullable=False)
    final_price = Column(Float, nullable=False)
    
    # Используем JSON для гибкого хранения расшифровки ответов
    answers_details = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
