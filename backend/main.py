from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.v1.endpoints.api import api_router
from app.api.v1.endpoints import log_summary
from app.database import init_db

load_dotenv()
init_db()

app = FastAPI(
    title="LeadConverter Pro API",
    description="API для интерактивного квиз-калькулятора.",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(api_router, prefix="/api/v1")
app.include_router(log_summary.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to LeadConverter Pro API"}
