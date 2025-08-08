import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.v1.endpoints.api import api_router
from app.api.v1.endpoints import log_summary

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

load_dotenv()

app = FastAPI(
    title="LeadConverter Pro API",
    description="API для интерактивного квиз-калькулятора.",
    version="1.0.0"
)

# Инициализация OpenTelemetry
resource = Resource.create({"service.name": os.getenv("OTEL_SERVICE_NAME", "leadconverter-pro-backend")})
provider = TracerProvider(resource=resource)

headers: dict[str, str] = {}
headers_env = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
if headers_env:
    for pair in headers_env.split(","):
        if "=" in pair:
            key, value = pair.split("=", 1)
            headers[key.strip()] = value.strip()

otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
    headers=headers,
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

# Подключаем роутеры
app.include_router(api_router, prefix="/api/v1")
app.include_router(log_summary.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to LeadConverter Pro API"}
