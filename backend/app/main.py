from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import health, quizzes, leads
from app.api import deps
from app import initial_data # <-- Импортируем наш инициализатор

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
def on_startup() -> None:
    """
    Выполняется один раз при старте приложения.
    Инициализирует базу данных.
    """
    # Получаем сессию и передаем ее в наш единый, правильный инициализатор
    db = next(deps.get_db())
    initial_data.init_db(db)

# Подключаем роутеры API
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(quizzes.router, prefix=f"{settings.API_V1_STR}/quizzes", tags=["Quizzes"])
app.include_router(leads.router, prefix=f"{settings.API_V1_STR}/leads", tags=["Leads"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}