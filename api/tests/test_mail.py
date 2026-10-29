"""Tests de l'envoi SMTP."""

from __future__ import annotations

import smtplib
from typing import Any, ClassVar

import pytest

from app.services import mail
from app.services.mail import (
    ContactMessage,
    MailDeliveryError,
    MailNotConfigured,
    send_contact_email,
)

CONTACT = ContactMessage(
    name="Camille Martin",
    email="camille@example.com",
    message="Bonjour, ceci est un message de test.",
    lang="fr",
)

BASE_CONFIG: dict[str, Any] = {
    "SMTP_HOST": "smtp.example.com",
    "SMTP_PORT": 587,
    "SMTP_USER": "user",
    "SMTP_PASSWORD": "password",
    "SMTP_USE_TLS": True,
    "SMTP_FROM": "portfolio@example.com",
    "CONTACT_TO": "owner@example.com",
    "SMTP_TIMEOUT": 10,
    "MAIL_SUPPRESS_SEND": False,
}


class FakeSMTP:
    instances: ClassVar[list[FakeSMTP]] = []

    def __init__(self, host: str, port: int, timeout: int | None = None) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.started_tls = False
        self.logged_in: tuple[str, str] | None = None
        self.messages: list[Any] = []
        FakeSMTP.instances.append(self)

    def __enter__(self) -> FakeSMTP:
        return self

    def __exit__(self, *args: object) -> bool:
        return False

    def ehlo(self) -> None:
        pass

    def starttls(self) -> None:
        self.started_tls = True

    def login(self, user: str, password: str) -> None:
        self.logged_in = (user, password)

    def send_message(self, message: Any) -> None:
        self.messages.append(message)


def test_suppressed_mail_is_not_sent(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = FakeSMTP
    fake.instances.clear()
    monkeypatch.setattr(mail.smtplib, "SMTP", fake)

    send_contact_email({**BASE_CONFIG, "MAIL_SUPPRESS_SEND": True}, CONTACT)

    assert fake.instances == []


def test_missing_configuration_raises() -> None:
    with pytest.raises(MailNotConfigured):
        send_contact_email({**BASE_CONFIG, "SMTP_HOST": ""}, CONTACT)


def test_message_is_sent_with_tls(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeSMTP.instances.clear()
    monkeypatch.setattr(mail.smtplib, "SMTP", FakeSMTP)

    send_contact_email(BASE_CONFIG, CONTACT)

    instance = FakeSMTP.instances[0]
    assert instance.host == "smtp.example.com"
    assert instance.port == 587
    assert instance.timeout == 10
    assert instance.started_tls is True
    assert instance.logged_in == ("user", "password")
    assert len(instance.messages) == 1

    message = instance.messages[0]
    assert message["To"] == "owner@example.com"
    assert "Camille Martin" in message["Subject"]
    assert message["Reply-To"] == "Camille Martin <camille@example.com>"
    body = message.get_content()
    assert "camille@example.com" in body
    assert "message de test" in body


def test_implicit_tls_on_port_465(monkeypatch: pytest.MonkeyPatch) -> None:
    instances: list[FakeSMTP] = []

    class FakeSMTPSSL(FakeSMTP):
        def __init__(self, host: str, port: int, timeout: int | None = None) -> None:
            super().__init__(host, port, timeout)
            instances.append(self)

    monkeypatch.setattr(mail.smtplib, "SMTP_SSL", FakeSMTPSSL)

    send_contact_email({**BASE_CONFIG, "SMTP_PORT": 465}, CONTACT)

    assert instances[0].started_tls is False
    assert len(instances[0].messages) == 1


def test_header_injection_is_neutralized(monkeypatch: pytest.MonkeyPatch) -> None:
    FakeSMTP.instances.clear()
    monkeypatch.setattr(mail.smtplib, "SMTP", FakeSMTP)
    contact = ContactMessage(
        name="Camille\r\nBcc: victim@example.com",
        email="camille@example.com",
        message="Bonjour, ceci est un message de test.",
        lang="fr",
    )

    send_contact_email(BASE_CONFIG, contact)

    message = FakeSMTP.instances[0].messages[0]
    subject = str(message["Subject"])
    assert message["Bcc"] is None
    assert "\r" not in subject
    assert "\n" not in subject


def test_smtp_exception_is_wrapped(monkeypatch: pytest.MonkeyPatch) -> None:
    class BrokenSMTP(FakeSMTP):
        def send_message(self, message: Any) -> None:
            raise smtplib.SMTPException("refused")

    monkeypatch.setattr(mail.smtplib, "SMTP", BrokenSMTP)

    with pytest.raises(MailDeliveryError):
        send_contact_email(BASE_CONFIG, CONTACT)
