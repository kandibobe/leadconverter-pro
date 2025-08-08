import sys
from pathlib import Path

import pytest
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.database import Base  # noqa: E402


# Stub models required for SQLAlchemy mapper configuration
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal = sessionmaker(bind=engine)

    from app.models import quiz as quiz_model
    from app.models import lead as lead_model

    for table in [
        User.__table__,
        Organization.__table__,
        Plan.__table__,
        quiz_model.Quiz.__table__,
        quiz_model.Question.__table__,
        quiz_model.Option.__table__,
        lead_model.Lead.__table__,
    ]:
        table.create(bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session, tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.api import deps
    from app.main import app

    def get_test_db():
        try:
            yield db_session
        finally:
            pass

    def get_tenant():
        return "test-tenant"

    app.dependency_overrides[deps.get_db] = get_test_db
    app.dependency_overrides[deps.get_tenant_id] = get_tenant

    # Avoid heavy PDF generation during API tests
    def fake_pdf(lead_data):
        path = tmp_path / f"lead_{lead_data.id}.pdf"
        path.write_text("dummy")
        return str(path)

    monkeypatch.setattr("app.services.pdf_generator.generate_lead_pdf", fake_pdf)

    return TestClient(app)

