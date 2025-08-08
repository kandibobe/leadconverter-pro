import logging
import os
from typing import Optional

import stripe


logger = logging.getLogger(__name__)


class BillingService:
    def __init__(self, api_key: Optional[str] = None) -> None:
        stripe.api_key = api_key or os.getenv("STRIPE_API_KEY", "")

    def create_customer(self, email: str) -> stripe.Customer:
        try:
            return stripe.Customer.create(email=email)
        except stripe.error.StripeError as exc:  # pragma: no cover - API errors
            logger.exception("Failed to create Stripe customer", extra={"email": email})
            raise RuntimeError("Stripe service error") from exc

    def create_subscription(self, customer_id: str, price_id: str) -> stripe.Subscription:
        try:
            return stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
            )
        except stripe.error.StripeError as exc:  # pragma: no cover - API errors
            logger.exception(
                "Failed to create Stripe subscription",
                extra={"customer_id": customer_id, "price_id": price_id},
            )
            raise RuntimeError("Stripe service error") from exc

    def cancel_subscription(self, subscription_id: str) -> stripe.Subscription:
        try:
            return stripe.Subscription.delete(subscription_id)
        except stripe.error.StripeError as exc:  # pragma: no cover - API errors
            logger.exception(
                "Failed to cancel Stripe subscription", extra={"subscription_id": subscription_id}
            )
            raise RuntimeError("Stripe service error") from exc


billing = BillingService()
