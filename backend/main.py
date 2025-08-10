# backend/main.py
from __future__ import annotations

import os
import uuid
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import SessionLocal, TENANT_ID

app = FastAPI(title="LeadConverter Pro API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("BACKEND_CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware: прокинуть X-Tenant-ID в contextvar ---
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

# --- DB dependency ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        # при первом SQL начнётся транзакция -> наш after_begin сделает SET LOCAL app.tenant_id
        yield session

# --- Health ---
@app.get("/healthz")
async def healthz():
    return {"ok": True}

# --- Проба БД ---
@app.get("/db-ping")
async def db_ping(db: AsyncSession = Depends(get_db)):
    res = await db.execute(text("select now()"))
    return {"db_time": str(res.scalar_one())}
