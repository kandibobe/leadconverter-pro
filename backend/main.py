from fastapi import FastAPI
from app.api.v1.api import api_router
from app.api import leads as lead_api
from app.database import Base, engine

# Создаем таблицы в БД (для первого запуска)
# В продакшене лучше использовать Alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LeadConverter Pro API",
    description="API для интерактивного квиз-калькулятора.",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(api_router, prefix="/api/v1")
app.include_router(lead_api.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to LeadConverter Pro API"}

