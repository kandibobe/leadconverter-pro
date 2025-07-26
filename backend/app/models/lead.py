from sqlalchemy import Column, Integer, String, Float, JSON
from app.db.base import Base

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    final_price = Column(Float, nullable=False)
    # Используем JSON для гибкого хранения ответов
    answers_data = Column(JSON, nullable=False)