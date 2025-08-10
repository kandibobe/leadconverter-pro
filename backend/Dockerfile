FROM python:3.11-slim

# Системные либы (WeasyPrint и пр.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Кладём requirements из КОРНЯ репо (у тебя он так и лежит)
COPY requirements.txt /app/requirements.txt

# Ставим зависимости (важно: psycopg v3, НЕТ psycopg2-binary)
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /app/requirements.txt

# Кладём исходники backend
COPY backend/ /app/backend/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

WORKDIR /app/backend

# Запускаем uvicorn по TCP (а не через Unix socket)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
