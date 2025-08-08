import os
from datetime import datetime

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api import deps
from app.models import Plan, Subscription

router = APIRouter()


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(deps.get_db)):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as exc:  # pragma: no cover - Stripe handles validation
        raise HTTPException(status_code=400, detail="Invalid payload") from exc

    event_type = event.get("type")
    data = event.get("data", {}).get("object", {})

    if event_type in {"customer.subscription.created", "customer.subscription.updated"}:
        sub = (
            db.query(Subscription)
            .filter_by(stripe_subscription_id=data["id"])
            .first()
        )
        if not sub:
            sub = Subscription(stripe_subscription_id=data["id"])
            db.add(sub)
        sub.status = data.get("status")
        price = data.get("items", {}).get("data", [{}])[0].get("price", {})
        plan = db.query(Plan).filter_by(stripe_price_id=price.get("id")).first()
        if plan:
            sub.plan = plan
        sub.current_period_start = datetime.fromtimestamp(data.get("current_period_start", 0))
        sub.current_period_end = datetime.fromtimestamp(data.get("current_period_end", 0))
        db.commit()
    elif event_type == "customer.subscription.deleted":
        sub = (
            db.query(Subscription)
            .filter_by(stripe_subscription_id=data.get("id"))
            .first()
        )
        if sub:
            db.delete(sub)
            db.commit()

    return {"status": "success"}
