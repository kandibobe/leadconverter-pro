# backend/app/otel.py
import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def setup_otel(app=None, engine=None):
    resource = Resource.create({
        "service.name": "leadconverter",
        "deployment.environment": os.getenv("ENV", "dev"),
    })
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318/v1/traces")
    ))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    if app: FastAPIInstrumentor().instrument_app(app)
    if engine: SQLAlchemyInstrumentor().instrument(engine=engine)
