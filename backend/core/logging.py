import os
import json
import logging
import contextvars

# Context variable to store request ID
_request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


def set_request_id(request_id: str) -> None:
    """Set the request ID for the current context."""
    _request_id_ctx.set(request_id)


class RequestIdFilter(logging.Filter):
    """Attach request_id from context variable to log records."""

    def filter(self, record: logging.LogRecord) -> bool:  # pragma: no cover - simple filter
        record.request_id = _request_id_ctx.get()
        return True


class JsonFormatter(logging.Formatter):
    """Format logs in JSON with selected fields."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - trivial formatting
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def configure_logging() -> None:
    """Configure root logger with JSON or plain text formatter based on env."""
    log_format = os.getenv("LOG_FORMAT", "json").lower()
    handler = logging.StreamHandler()
    handler.addFilter(RequestIdFilter())

    if log_format == "text":
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(module)s | %(message)s | %(request_id)s"
        )
    else:
        formatter = JsonFormatter()

    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)
