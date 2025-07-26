# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# НЕ ИСПОЛЬЗУЕМ БОЛЬШЕ Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
 codex/add-newline-at-eof-for-project-files
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

    return {"message": "Welcome to LeadConverter Pro API"}
 main
