from sqlalchemy.orm import Session
from app.models import lead as lead_model
from app.models import quiz as quiz_model
from app.models.lead_event import LeadEvent
from app.schemas import lead as lead_schema

class CRUDLead:
    def create_with_calculation(
        self, db: Session, *, obj_in: lead_schema.LeadCreateIn, tenant_id: str
    ) -> lead_model.Lead:
        """
        Создает лид, производя расчеты на основе ответов.
        Это - сердце бизнес-логики.
        """
        base_price = 0.0
        area_multiplier = 1.0
        answers_details = {}

        # 1. Получаем все опции, которые выбрал пользователь, одним запросом
        chosen_option_ids = [answer.option_id for answer in obj_in.answers if answer.option_id]
        chosen_options = db.query(quiz_model.Option).filter(quiz_model.Option.id.in_(chosen_option_ids)).all()
        options_map = {option.id: option for option in chosen_options}

        # 2. Обрабатываем ответы
        for answer in obj_in.answers:
            question = db.query(quiz_model.Question).filter(quiz_model.Question.id == answer.question_id).first()
            if not question:
                continue

            # Если это вопрос типа "слайдер" (площадь)
            if question.question_type == 'slider':
                try:
                    area_multiplier = float(answer.value)
                    answers_details[question.text] = f"{area_multiplier} м²"
                except (ValueError, TypeError):
                    area_multiplier = 1.0
            # Для всех остальных вопросов (радио, чекбоксы)
            elif answer.option_id in options_map:
                option = options_map[answer.option_id]
                base_price += option.price_impact
                answers_details[question.text] = option.text
        
        # 3. Рассчитываем итоговую стоимость
        final_price = base_price * area_multiplier

        # 4. Создаем объект для сохранения в БД
        lead_create_data = lead_schema.LeadCreateInternal(
            quiz_id=obj_in.quiz_id,
            client_email=obj_in.client_email,
            final_price=final_price,
            answers_details=answers_details,
            tenant_id=tenant_id,
        )

        db_obj = lead_model.Lead(**lead_create_data.model_dump())
        db.add(db_obj)
        db.flush()

        event_data = lead_create_data.model_dump()
        event_data["id"] = db_obj.id
        db_event = LeadEvent(lead_id=db_obj.id, data=event_data)
        db.add(db_event)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, *, tenant_id: str, skip: int = 0, limit: int = 100
    ) -> list[lead_model.Lead]:
        return (
            db.query(lead_model.Lead)
            .filter(lead_model.Lead.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


lead = CRUDLead()
