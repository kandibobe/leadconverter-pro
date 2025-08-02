from sqlalchemy import Column, Integer, String
from app.db.base import Base

class CompanySettings(Base):
    __tablename__ = "company_settings"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, default="Ваша компания")
    logo_url = Column(String, nullable=True)
    primary_color = Column(String, default="#4CAF50") # Зеленый по умолчанию