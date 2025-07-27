from fastapi import APIRouter
from app.api.v1.endpoints import quizzes, leads, dashboard

api_router = APIRouter()

# Подключаем роутер для квизов
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])

# Подключаем роутер для лидов
api_router.include_router(leads.router, prefix="/leads", tags=["Leads"])

# Подключаем роутер для дашборда
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])