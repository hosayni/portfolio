"""Routes de l'API."""

from __future__ import annotations

import time

from flask import Blueprint, current_app, jsonify

bp = Blueprint("health", __name__, url_prefix="/api")


@bp.get("/health")
def health():
    started = current_app.config.get("STARTED_AT", 0.0)
    return jsonify(
        status="ok",
        version=current_app.config.get("VERSION", "0.0.0"),
        environment=current_app.config.get("APP_ENV", "development"),
        contact_enabled=bool(current_app.config.get("CONTACT_ENABLED", True)),
        uptime_seconds=max(0, int(time.monotonic() - started)),
    )
