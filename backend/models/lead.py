from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, func, text
from app.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        String, index=True, nullable=False, server_default=text("current_setting('app.tenant_id')")
    )
    quiz_id = Column(Integer, nullable=False)
    client_email = Column(String, index=True, nullable=False)
    final_price = Column(Float, nullable=False)
    
    # Используем JSON для гибкого хранения расшифровки ответов
    answers_details = Column(JSON, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
