"""Validation stricte des messages de contact."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from app.services.mail import ContactMessage

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
NAME_MIN, NAME_MAX = 2, 120
MESSAGE_MIN, MESSAGE_MAX = 20, 5000
EMAIL_MAX = 254
CONSENT_VALUES = {True, "1", "true", "True", "on"}


@dataclass(frozen=True)
class ContactValidation:
    contact: ContactMessage | None
    errors: dict[str, str]
    honeypot: bool


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def validate_contact(raw: dict[str, Any]) -> ContactValidation:
    """Valide et normalise les champs, sans jamais faire confiance au client."""

    name = _text(raw.get("name"))
    email = _text(raw.get("email"))
    message = _text(raw.get("message"))
    lang = _text(raw.get("lang"))
    honeypot = bool(_text(raw.get("website")))

    errors: dict[str, str] = {}

    if not name:
        errors["name"] = "required"
    elif not NAME_MIN <= len(name) <= NAME_MAX:
        errors["name"] = "length"

    if not email:
        errors["email"] = "required"
    elif len(email) > EMAIL_MAX or not EMAIL_RE.match(email):
        errors["email"] = "invalid"

    if not message:
        errors["message"] = "required"
    elif len(message) < MESSAGE_MIN:
        errors["message"] = "too_short"
    elif len(message) > MESSAGE_MAX:
        errors["message"] = "too_long"

    if raw.get("consent") not in CONSENT_VALUES:
        errors["consent"] = "required"

    if errors:
        return ContactValidation(contact=None, errors=errors, honeypot=honeypot)

    contact = ContactMessage(
        name=name,
        email=email,
        message=message,
        lang=lang if lang in {"fr", "en"} else "fr",
    )
    return ContactValidation(contact=contact, errors={}, honeypot=honeypot)
