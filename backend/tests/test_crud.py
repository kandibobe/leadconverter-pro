from app.crud import quiz as crud_quiz, lead as crud_lead
from app.schemas.quiz import QuizCreate, QuestionCreate, OptionCreate
from app.schemas.lead import LeadCreate


def test_create_quiz(db_session):
    quiz_in = QuizCreate(
        title="Test Quiz",
        description="desc",
        questions=[
            QuestionCreate(
                text="Q1",
                question_type="single-choice",
                order=1,
                options=[
                    OptionCreate(text="Opt1", price_impact=1.0, order=1)
                ],
            )
        ],
    )
    db_quiz = crud_quiz.create(db=db_session, obj_in=quiz_in)
    assert db_quiz.id is not None
    assert db_quiz.questions[0].options[0].text == "Opt1"


def test_create_lead(db_session):
    lead_in = LeadCreate(
        email="user@example.com",
        final_price=100.0,
        answers_data={"q1": "a1"},
    )
    db_lead = crud_lead.create(db=db_session, obj_in=lead_in)
    assert db_lead.id is not None
    assert db_lead.email == "user@example.com"
