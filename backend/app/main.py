from fastapi import FastAPI

from app.api.v1.endpoints import quiz
from app.db.init_db import init_db
from app.db.session import SessionLocal

app = FastAPI(
    title="LeadConverter Pro API",
    description="API для интерактивного квиз-калькулятора.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize the database on application startup."""
    # Use a context manager so the session always closes
    with SessionLocal() as db:
        init_db(db)

# Подключаем роутеры
app.include_router(quiz.router, prefix="/api/v1", tags=["Quiz & Leads"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LeadConverter Pro API"}