from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """Provide a transactional database session."""
    with SessionLocal() as db:
        yield db
