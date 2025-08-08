from app.schemas.estimate import EstimateRequest
from app.schemas.lead import LeadAnswerIn
from app.models import quiz as quiz_model
from app.services.estimate_service import calculate_estimate


def _create_questions(db):
    quiz = quiz_model.Quiz(id=1, tenant_id="test-tenant", title="t", description="d")
    slider_q = quiz_model.Question(
        id=1, text="Area", question_type="slider", order=1, quiz=quiz
    )
    option_q = quiz_model.Question(id=2, text="Option", order=2, quiz=quiz)
    option = quiz_model.Option(id=1, text="A", price_impact=100.0, order=1, question=option_q)
    db.add_all([quiz, slider_q, option_q, option])
    db.commit()


def test_calculate_estimate_slider_and_option(db_session):
    _create_questions(db_session)
    payload = EstimateRequest(
        quiz_id=1,
        answers=[
            LeadAnswerIn(question_id=1, value="10"),
            LeadAnswerIn(question_id=2, option_id=1),
        ],
    )
    cost = calculate_estimate(db_session, payload)
    assert cost == 1000.0


def test_calculate_estimate_invalid_slider(db_session):
    _create_questions(db_session)
    payload = EstimateRequest(
        quiz_id=1,
        answers=[
            LeadAnswerIn(question_id=1, value="abc"),
            LeadAnswerIn(question_id=2, option_id=1),
        ],
    )
    cost = calculate_estimate(db_session, payload)
    assert cost == 100.0


def test_calculate_estimate_missing_option(db_session):
    _create_questions(db_session)
    payload = EstimateRequest(
        quiz_id=1,
        answers=[
            LeadAnswerIn(question_id=1, value="10"),
            LeadAnswerIn(question_id=2, option_id=999),
        ],
    )
    cost = calculate_estimate(db_session, payload)
    assert cost == 0.0

