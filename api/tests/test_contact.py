"""Tests de l'endpoint de contact et de la validation."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app.services import mail
from app.services.mail import ContactMessage, MailDeliveryError, MailNotConfigured
from app.validation import validate_contact

VALID_PAYLOAD: dict[str, Any] = {
    "name": "Camille Martin",
    "email": "camille@example.com",
    "message": "Bonjour, je souhaite discuter d'un projet avec vous.",
    "consent": True,
    "lang": "fr",
    "website": "",
}


def post_contact(client: FlaskClient, **overrides: Any):
    payload = {**VALID_PAYLOAD, **overrides}
    return client.post("/api/contact", json=payload)


def test_valid_message_is_sent(client: FlaskClient, monkeypatch: pytest.MonkeyPatch) -> None:
    sent: list[ContactMessage] = []
    monkeypatch.setattr(mail, "send_contact_email", lambda config, contact: sent.append(contact))

    response = post_contact(client)

    assert response.status_code == 200
    assert response.get_json() == {"status": "sent"}
    assert len(sent) == 1
    assert sent[0].name == "Camille Martin"
    assert sent[0].email == "camille@example.com"
    assert sent[0].lang == "fr"


def test_form_encoded_message_is_accepted(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    sent: list[ContactMessage] = []
    monkeypatch.setattr(mail, "send_contact_email", lambda config, contact: sent.append(contact))

    response = client.post(
        "/api/contact",
        data={
            "name": "Camille",
            "email": "camille@example.com",
            "message": "Message suffisamment long pour passer la validation.",
            "consent": "on",
            "lang": "en",
        },
    )

    assert response.status_code == 200
    assert sent[0].lang == "en"


def test_honeypot_is_silently_ignored(client: FlaskClient, monkeypatch: pytest.MonkeyPatch) -> None:
    called = False

    def fail_if_called(config: dict, contact: ContactMessage) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(mail, "send_contact_email", fail_if_called)

    response = post_contact(client, website="https://spam.example")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
    assert called is False


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("name", "", "required"),
        ("name", "A", "length"),
        ("name", "A" * 121, "length"),
        ("email", "", "required"),
        ("email", "not-an-email", "invalid"),
        ("email", f"{'a' * 250}@example.com", "invalid"),
        ("message", "", "required"),
        ("message", "trop court", "too_short"),
        ("message", "x" * 5001, "too_long"),
        ("consent", False, "required"),
    ],
)
def test_validation_errors(client: FlaskClient, field: str, value: Any, error: str) -> None:
    response = post_contact(client, **{field: value})

    assert response.status_code == 422
    body = response.get_json()
    assert body["error"] == "validation_error"
    assert body["fields"][field] == error


def test_invalid_json_body_is_rejected(client: FlaskClient) -> None:
    response = client.post(
        "/api/contact",
        data="{not json",
        content_type="application/json",
    )

    assert response.status_code == 422
    assert response.get_json()["error"] == "validation_error"


def test_rate_limit_returns_json_429(make_app: Callable[..., Flask]) -> None:
    app = make_app(CONTACT_RATE_LIMIT="1 per hour")
    client = app.test_client()

    first = post_contact(client)
    second = post_contact(client)

    assert first.status_code == 200
    assert second.status_code == 429
    assert second.get_json()["error"] == "rate_limited"
    assert "Retry-After" in second.headers


def test_mail_not_configured_returns_503(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def unavailable(config: dict, contact: ContactMessage) -> None:
        raise MailNotConfigured("missing")

    monkeypatch.setattr(mail, "send_contact_email", unavailable)

    response = post_contact(client)

    assert response.status_code == 503
    assert response.get_json()["error"] == "mail_unavailable"


def test_disabled_contact_returns_503_without_sending(
    make_app: Callable[..., Flask], monkeypatch: pytest.MonkeyPatch
) -> None:
    called = False

    def fail_if_called(config: dict, contact: ContactMessage) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(mail, "send_contact_email", fail_if_called)

    app = make_app(CONTACT_ENABLED=False)
    response = post_contact(app.test_client())

    assert response.status_code == 503
    assert response.get_json()["error"] == "contact_disabled"
    assert called is False


def test_mail_delivery_failure_returns_503(
    client: FlaskClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def failing(config: dict, contact: ContactMessage) -> None:
        raise MailDeliveryError("smtp down")

    monkeypatch.setattr(mail, "send_contact_email", failing)

    response = post_contact(client)

    assert response.status_code == 503
    assert response.get_json()["error"] == "mail_delivery_failed"


def test_payload_too_large_returns_json_413(client: FlaskClient) -> None:
    response = client.post(
        "/api/contact",
        data="x" * (17 * 1024),
        content_type="text/plain",
    )

    assert response.status_code == 413
    assert response.get_json()["error"] == "payload_too_large"


def test_validation_normalizes_language_and_trims_values() -> None:
    result = validate_contact(
        {
            "name": "  Camille  ",
            "email": "  camille@example.com ",
            "message": "  Un message assez long pour être accepté.  ",
            "consent": "true",
            "lang": "de",
        }
    )

    assert result.contact is not None
    assert result.contact.name == "Camille"
    assert result.contact.email == "camille@example.com"
    assert result.contact.lang == "fr"
    assert result.errors == {}


def test_validation_handles_non_string_values() -> None:
    result = validate_contact({"name": 42, "email": None, "message": [], "consent": False})

    assert result.contact is None
    assert set(result.errors) == {"name", "email", "message", "consent"}
