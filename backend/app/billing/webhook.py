# backend/app/billing/webhook.py
import os, stripe
from fastapi import APIRouter, Request, HTTPException
router = APIRouter(prefix="/webhooks/stripe", tags=["stripe"])
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("")
async def handle(request: Request):
    payload = await request.body()
    sig = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig, WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # TODO: обработка checkout.session.completed, invoice.finalized и т.д.
    return {"received": True}
