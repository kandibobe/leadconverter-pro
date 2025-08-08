"""Wrapper around lead calculator to compute cost estimates."""
import logging
from sqlalchemy.orm import Session

from app.schemas.estimate import EstimateRequest
from app.services.lead_calculator import LeadCalculator

logger = logging.getLogger(__name__)

def calculate_estimate(
    db: Session, payload: EstimateRequest, calculator: LeadCalculator | None = None
) -> float:
    """Calculate estimated cost using LeadCalculator service."""
    calc = calculator or LeadCalculator()
    price, _ = calc.calculate(db, payload.answers)
    logger.debug("Estimate calculated: %s", price)
    return price
