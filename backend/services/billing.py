import os
from typing import Optional

import stripe


class BillingService:
    def __init__(self, api_key: Optional[str] = None) -> None:
        stripe.api_key = api_key or os.getenv("STRIPE_API_KEY", "")

    def create_customer(self, email: str) -> stripe.Customer:
        return stripe.Customer.create(email=email)

    def create_subscription(self, customer_id: str, price_id: str) -> stripe.Subscription:
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
        )

    def cancel_subscription(self, subscription_id: str) -> stripe.Subscription:
        return stripe.Subscription.delete(subscription_id)


billing = BillingService()
