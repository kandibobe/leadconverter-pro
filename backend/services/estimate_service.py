# backend/app/services/estimate_service.py
from sqlalchemy.orm import Session
from app.models import quiz as quiz_model
from app.schemas.estimate import EstimateRequest
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def calculate_estimate(db: Session, payload: EstimateRequest) -> float:
    with tracer.start_as_current_span("calculate_estimate"):
        base_price = 0.0
        area_multiplier = 1.0

        chosen_option_ids = [a.option_id for a in payload.answers if a.option_id]
        options = (
            db.query(quiz_model.Option)
            .filter(quiz_model.Option.id.in_(chosen_option_ids))
            .all()
        )
        options_map = {opt.id: opt for opt in options}

        for ans in payload.answers:
            question = (
                db.query(quiz_model.Question)
                .filter(quiz_model.Question.id == ans.question_id)
                .first()
            )
            if not question:
                continue
            if question.question_type == "slider":
                try:
                    area_multiplier = float(ans.value)
                except (ValueError, TypeError):
                    area_multiplier = 1.0
            elif ans.option_id in options_map:
                base_price += options_map[ans.option_id].price_impact

        return base_price * area_multiplier
