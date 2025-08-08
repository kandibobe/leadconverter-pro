from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stripe_price_id = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    subscriptions = relationship("Subscription", back_populates="plan")
