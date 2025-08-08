from app.models import quiz as quiz_model


def _seed_quiz(db):
    quiz = quiz_model.Quiz(id=1, tenant_id="test-tenant", title="q", description="d")
    slider_q = quiz_model.Question(
        id=1, text="Area", question_type="slider", order=1, quiz=quiz
    )
    option_q = quiz_model.Question(id=2, text="Choice", order=2, quiz=quiz)
    option = quiz_model.Option(id=1, text="A", price_impact=100.0, order=1, question=option_q)
    db.add_all([quiz, slider_q, option_q, option])
    db.commit()


def test_submit_lead_valid(client, db_session):
    _seed_quiz(db_session)
    payload = {
        "quiz_id": 1,
        "client_email": "user@example.com",
        "answers": [
            {"question_id": 1, "value": "10"},
            {"question_id": 2, "option_id": 1},
        ],
    }
    response = client.post(
        "/api/v1/leads/submit",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["final_price"] == 1000.0
    assert data["pdf_url"].endswith(".pdf")


def test_submit_lead_missing_quiz(client):
    payload = {
        "quiz_id": 999,
        "client_email": "user@example.com",
        "answers": [],
    }
    response = client.post(
        "/api/v1/leads/submit",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"},
    )
    assert response.status_code == 404


def test_submit_lead_bad_answer(client, db_session):
    _seed_quiz(db_session)
    payload = {
        "quiz_id": 1,
        "client_email": "user@example.com",
        "answers": [{"question_id": 2, "option_id": 999}],
    }
    response = client.post(
        "/api/v1/leads/submit",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"},
    )
    assert response.status_code == 400

