import logging
from typing import Dict, Iterable, Tuple

from sqlalchemy.orm import Session

from app.models import quiz as quiz_model
from app.schemas.lead import LeadAnswerIn

logger = logging.getLogger(__name__)

class LeadCalculationError(Exception):
    """Raised when lead price calculation fails."""

class LeadCalculator:
    """Service responsible for calculating lead prices."""

    def __init__(self, log: logging.Logger | None = None) -> None:
        self.logger = log or logger

    def calculate(
        self, db: Session, answers: Iterable[LeadAnswerIn]
    ) -> Tuple[float, Dict[str, str]]:
        """Calculate final price and answer details.

        Args:
            db: SQLAlchemy session.
            answers: Iterable of LeadAnswerIn provided by user.

        Returns:
            Tuple containing final price and mapping of question text to answer text.
        """
        base_price = 0.0
        area_multiplier = 1.0
        answers_details: Dict[str, str] = {}

        try:
            self.logger.debug("Starting calculation for %d answers", len(list(answers)))
        except TypeError:
            # in case answers is a generator consumed later we convert to list once
            answers = list(answers)
            self.logger.debug("Starting calculation for %d answers", len(answers))

        try:
            chosen_option_ids = [a.option_id for a in answers if a.option_id]
            options = (
                db.query(quiz_model.Option)
                .filter(quiz_model.Option.id.in_(chosen_option_ids))
                .all()
            )
            options_map = {opt.id: opt for opt in options}

            question_ids = [a.question_id for a in answers]
            questions = (
                db.query(quiz_model.Question)
                .filter(quiz_model.Question.id.in_(question_ids))
                .all()
            )
            questions_map = {q.id: q for q in questions}

            for ans in answers:
                question = questions_map.get(ans.question_id)
                if not question:
                    continue
                if question.question_type == "slider":
                    try:
                        area_multiplier = float(ans.value)
                        answers_details[question.text] = f"{area_multiplier} м²"
                    except (ValueError, TypeError) as e:
                        self.logger.warning("Invalid area value %r: %s", ans.value, e)
                        area_multiplier = 1.0
                elif ans.option_id in options_map:
                    option = options_map[ans.option_id]
                    base_price += option.price_impact
                    answers_details[question.text] = option.text

            final_price = base_price * area_multiplier
            self.logger.info("Calculated price: %s", final_price)
            return final_price, answers_details
        except Exception as exc:
            self.logger.exception("Failed to calculate price")
            raise LeadCalculationError from exc
