from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import health, quizzes
from app.db import session, init_db
from app.api import deps

# ИМПОРТИРУЕМ МОДЕЛИ ЗДЕСЬ.
# Это гарантирует, что SQLAlchemy "увидит" их до того,
# как мы попросим его создать таблицы. Это разрывает цикл импортов.
from app.models import quiz as quiz_model

# Создаем таблицы в БД.
# Теперь, когда все модели импортированы, Base.metadata знает обо всех таблицах.
session.Base.metadata.create_all(bind=session.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
def on_startup() -> None:
    """
    Выполняется один раз при старте приложения.
    Инициализирует базу данных начальными данными.
    """
    print("Application startup: Initializing DB...")
    db = next(deps.get_db())
    init_db.init_db(db)
    print("Startup complete.")

# Подключаем роутеры API
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(quizzes.router, prefix=f"{settings.API_V1_STR}/quizzes", tags=["Quizzes"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}