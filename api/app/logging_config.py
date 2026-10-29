"""Journalisation structurée en JSON, sans donnée personnelle."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime

from flask import Flask

LOG_FIELDS = (
    "event",
    "request_id",
    "method",
    "path",
    "status",
    "duration_ms",
    "reason",
    "version",
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in LOG_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(app: Flask) -> None:
    if app.config.get("TESTING"):
        app.logger.setLevel(logging.CRITICAL)
        return

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(app.config.get("LOG_LEVEL", "INFO"))

    app.logger.handlers.clear()
    app.logger.propagate = True
