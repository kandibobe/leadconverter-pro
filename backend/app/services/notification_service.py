"""Notification and logging utilities for new leads."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from app.schemas.lead import Lead

logger = logging.getLogger(__name__)


def _mask_email(email: str) -> str:
    """Mask email address for GDPR compliant logging."""
    local, _, domain = email.partition("@");
    if len(local) <= 2:
        masked = local[:1] + "*" * max(len(local) - 1, 0)
    else:
        masked = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked}@{domain}" if domain else masked


class BaseNotifier(ABC):
    """Abstract notifier interface."""

    @abstractmethod
    def send(self, lead_data: Lead) -> Any:
        """Send lead notification."""


class ConsoleNotifier(BaseNotifier):
    """Simple notifier that outputs information to stdout."""

    def send(self, lead_data: Lead) -> None:
        print("=" * 50)
        print("🚀 НОВЫЙ ЛИД ПОЛУЧЕН! 🚀")
        print(f"Email клиента: {lead_data.email}")
        print(f"Итоговая стоимость: {lead_data.final_price} RUB")
        print("Ответы клиента:")
        for key, value in lead_data.answers_data.items():
            print(f"  - {key}: {value}")
        print("=" * 50)


class NotificationService:
    """Service that logs events and delegates sending to a notifier."""

    def __init__(self, notifier: BaseNotifier | None = None) -> None:
        self.notifier = notifier or ConsoleNotifier()

    def send_new_lead_notification(self, lead_data: Lead) -> None:
        """Log sanitized lead info and dispatch notification."""

        logger.info(
            "New lead received email=%s final_price=%.2f",
            _mask_email(lead_data.email),
            lead_data.final_price,
        )
        self.notifier.send(lead_data)


notification = NotificationService()