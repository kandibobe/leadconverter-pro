# backend/app/billing/stripe_client.py
import stripe, os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_version = "2025-06-30"  # актуальный стабильный

# ID ваших meters/price/product положите в ENV
METERS = {
    "leads": os.getenv("STRIPE_METER_LEADS"),
    "ai_tokens": os.getenv("STRIPE_METER_AI_TOKENS"),
}
