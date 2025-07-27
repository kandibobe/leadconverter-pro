from sqlalchemy.orm import Session
from app.models import lead as lead_model, quiz as quiz_model
from app.schemas import lead as lead_schema

class CRUDLead:
    def calculate_price_from_answers(self, db: Session, *, answers_in: list[lead_schema.LeadAnswerIn]) -> float:
        base_price = 0.0
        area_multiplier = 1.0

        chosen_option_ids = [answer.option_id for answer in answers_in if answer.option_id]
        if chosen_option_ids:
            chosen_options = db.query(quiz_model.Option).filter(quiz_model.Option.id.in_(chosen_option_ids)).all()
            options_map = {option.id: option for option in chosen_options}
        else:
            options_map = {}

        for answer in answers_in:
            question = db.query(quiz_model.Question).filter(quiz_model.Question.id == answer.question_id).first()
            if not question: continue

            if question.question_type == 'slider':
                try:
                    area_multiplier = float(answer.value) if answer.value else 1.0
                except (ValueError, TypeError):
                    area_multiplier = 1.0
            elif answer.option_id in options_map:
                base_price += options_map[answer.option_id].price_impact
        
        return base_price * area_multiplier

    def create_with_calculation(self, db: Session, *, obj_in: lead_schema.LeadCreateIn) -> lead_model.Lead:
        final_price = self.calculate_price_from_answers(db=db, answers_in=obj_in.answers)
        
        answers_details = {}
        for answer in obj_in.answers:
            question = db.query(quiz_model.Question).filter(quiz_model.Question.id == answer.question_id).first()
            if not question: continue
            
            if question.question_type == 'slider':
                answers_details[question.text] = f"{answer.value} м²"
            elif answer.option_id:
                option = db.query(quiz_model.Option).filter(quiz_model.Option.id == answer.option_id).first()
                if option:
                    answers_details[question.text] = option.text

        lead_create_data = lead_schema.LeadCreateInternal(
            quiz_id=obj_in.quiz_id,
            client_email=obj_in.client_email,
            final_price=final_price,
            answers_details=answers_details
        )

        db_obj = lead_model.Lead(**lead_create_data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[lead_model.Lead]:
        return db.query(lead_model.Lead).order_by(lead_model.Lead.id.desc()).offset(skip).limit(limit).all()

lead = CRUDLead()