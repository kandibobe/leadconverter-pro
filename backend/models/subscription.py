from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    stripe_subscription_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)

    plan = relationship("Plan", back_populates="subscriptions")
    user = relationship("User", back_populates="subscriptions")
    organization = relationship("Organization", back_populates="subscriptions")
