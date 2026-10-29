"""Réception des messages de contact."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, current_app, jsonify, request

from app.errors import ApiError
from app.extensions import limiter
from app.services import mail
from app.services.mail import MailDeliveryError, MailNotConfigured
from app.validation import validate_contact

bp = Blueprint("contact", __name__, url_prefix="/api")


def _read_payload() -> dict[str, Any]:
    if request.is_json:
        data = request.get_json(silent=True)
        return data if isinstance(data, dict) else {}
    return request.form.to_dict(flat=True)


@bp.post("/contact")
@limiter.limit(lambda: current_app.config["CONTACT_RATE_LIMIT"])
def contact():
    if not current_app.config.get("CONTACT_ENABLED", True):
        current_app.logger.info(
            "contact_disabled",
            extra={"event": "contact_disabled"},
        )
        raise ApiError(
            "contact_disabled",
            "The contact form is temporarily unavailable.",
            503,
        )

    raw = _read_payload()
    result = validate_contact(raw)

    # Honeypot : réponse neutre, aucun e-mail envoyé, pas d'indice pour le bot.
    if result.honeypot:
        current_app.logger.info("contact_honeypot", extra={"event": "contact_honeypot"})
        return jsonify(status="ok")

    if result.contact is None:
        raise ApiError(
            "validation_error",
            "Some fields are invalid.",
            422,
            fields=result.errors,
        )

    try:
        mail.send_contact_email(current_app.config, result.contact)
    except MailNotConfigured as exc:
        current_app.logger.error(
            "contact_mail_not_configured",
            extra={"event": "contact_mail_not_configured"},
        )
        raise ApiError(
            "mail_unavailable",
            "The contact form is temporarily unavailable.",
            503,
        ) from exc
    except MailDeliveryError as exc:
        raise ApiError(
            "mail_delivery_failed",
            "The message could not be sent. Please try again later.",
            503,
        ) from exc

    return jsonify(status="sent")
