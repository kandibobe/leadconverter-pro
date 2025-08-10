# backend/celery_worker.py
import os
from celery import Celery
from celery.signals import worker_process_init
from opentelemetry.instrumentation.celery import CeleryInstrumentor

app = Celery(
    "lc",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1"),
)

@worker_process_init.connect(weak=False)
def init_tracing(*_a, **_kw):
    CeleryInstrumentor().instrument()  # OTel для celery

@app.task(acks_late=True)
def dummy_task(x):
    return x * 2
