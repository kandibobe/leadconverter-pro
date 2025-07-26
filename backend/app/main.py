from fastapi import FastAPI
from app.api.v1.endpoints import quiz
from app.database import Base, engine
from app.core.config import settings
import logging

# Создаем таблицы в БД (для первого запуска)
# В продакшене лучше использовать Alembic
Base.metadata.create_all(bind=engine)

# Configure logging once at startup
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="LeadConverter Pro API",
    description="API для интерактивного квиз-калькулятора.",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(quiz.router, prefix="/api/v1", tags=["Quiz & Leads"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LeadConverter Pro API"}