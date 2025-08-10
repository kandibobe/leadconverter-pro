# backend/app/billing/usage.py
from .stripe_client import stripe, METERS
from datetime import datetime, timezone

def record_lead_event(customer_id: str, quantity: int = 1, ts: datetime | None = None):
    return stripe.billing.MeterEvent.create(
        event_name="lead.created",
        payload={"value": quantity, "customer": customer_id, "timestamp": int((ts or datetime.now(timezone.utc)).timestamp())}
    )

def record_ai_tokens(customer_id: str, tokens: int, ts: datetime | None = None):
    return stripe.billing.MeterEvent.create(
        event_name="ai.tokens.used",
        payload={"value": tokens, "customer": customer_id, "timestamp": int((ts or datetime.now(timezone.utc)).timestamp())}
    )
