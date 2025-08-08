"""Centralized logging configuration for the backend application."""

from __future__ import annotations

import logging
import logging.config
import os


def setup_logging() -> None:
    """Configure root logger using settings from environment.

    The log level can be controlled via the ``LOG_LEVEL`` environment variable.
    All module loggers should obtain their logger via ``logging.getLogger`` and
    rely on this configuration.
    """

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            }
        },
        "root": {
            "level": log_level,
            "handlers": ["console"],
        },
    }

    logging.config.dictConfig(logging_config)


__all__ = ["setup_logging"]

