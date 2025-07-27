# Этап 1: "Строитель" - установка зависимостей
FROM python:3.11-slim as builder

# Устанавливаем ПОЛНЫЙ набор системных зависимостей, необходимых для сборки WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-cffi \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./backend/requirements.txt .

# Создаем "колеса" для всех зависимостей
RUN pip wheel --wheel-dir /app/wheels -r requirements.txt


# Этап 2: Финальный образ
FROM python:3.11-slim

# Устанавливаем только те системные зависимости, что нужны для ЗАПУСКА WeasyPrint
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем предустановленные "колеса" из "строителя"
COPY --from=builder /app/wheels /wheels
COPY ./backend/requirements.txt .

# Устанавливаем зависимости из локальных "колес"
RUN pip install --no-index --find-links=/wheels -r requirements.txt

# Копируем весь код бэкенда в контейнер
COPY ./backend/ /app

# Указываем команду для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]