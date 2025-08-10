FROM python:3.11-slim

# Системные библиотеки (WeasyPrint + компоновка шрифтов и т.д.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Сначала копируем только requirements для более стабильного кеша сборки
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/backend/requirements.txt

# Теперь — исходники backend и скрипт старта
COPY backend /app/backend
COPY scripts /app/backend/scripts

# Чтобы импорты вида "from app..." работали
ENV PYTHONPATH=/app/backend

# Гарантируем права на entrypoint
RUN chmod +x /app/backend/scripts/entrypoint.sh
