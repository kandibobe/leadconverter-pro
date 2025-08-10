# backend/main.py
from __future__ import annotations

import os
import uuid
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal, TENANT_ID

app = FastAPI(title="LeadConverter Pro API")

# CORS: при allow_credentials=True нельзя ставить '*' — перечисляем явные origin'ы
# (иначе браузер режет запросы). Документация FastAPI/Starlette. 
origins = os.getenv(
    "BACKEND_CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    tid = request.headers.get("X-Tenant-ID")
    token = None
    if tid:
        try:
            uuid.UUID(str(tid))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid X-Tenant-ID")
        token = TENANT_ID.set(str(tid))
    try:
        response = await call_next(request)
    finally:
        if token is not None:
            TENANT_ID.reset(token)
    return response

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@app.get("/healthz")
async def healthz():
    return {"ok": True}

@app.get("/db-ping")
async def db_ping(db: AsyncSession = Depends(get_db)):
    res = await db.execute(text("select now()"))
    return {"db_time": str(res.scalar_one())}

# --- Временные заглушки для фронта ---
@app.get("/api/v1/quizzes")
async def list_quizzes():
    return [{"id": "1", "title": "Demo Quiz"}]

@app.get("/api/v1/quizzes/{quiz_id}")
async def get_quiz(quiz_id: str):
    return {
        "id": str(quiz_id),
        "title": "Demo Quiz",
        "description": "Заглушка API. Замените на реальные данные.",
        "questions": [
            {"id": "q1", "type": "radio", "text": "Какой язык?", "options": ["Python", "TS", "Go"], "required": True},
            {"id": "q2", "type": "text", "text": "Ваш домен?", "required": False},
        ],
    }
