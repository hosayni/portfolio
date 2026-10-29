"""Envoi des messages de contact par SMTP."""

from __future__ import annotations

import logging
import smtplib
from dataclasses import dataclass
from datetime import UTC, datetime
from email.message import EmailMessage
from email.utils import format_datetime, formataddr

logger = logging.getLogger(__name__)


class MailNotConfigured(RuntimeError):
    """SMTP n'est pas configuré alors que l'envoi est requis."""


class MailDeliveryError(RuntimeError):
    """Le serveur SMTP a refusé ou n'a pas pu recevoir le message."""


@dataclass(frozen=True)
class ContactMessage:
    name: str
    email: str
    message: str
    lang: str


def _clean_header(value: str) -> str:
    return " ".join(value.replace("\r", " ").replace("\n", " ").split())


def _build_message(config: dict, contact: ContactMessage) -> EmailMessage:
    sender = config["SMTP_FROM"]
    recipient = config["CONTACT_TO"]

    message = EmailMessage()
    message["Subject"] = f"[Portfolio] Nouveau message de {_clean_header(contact.name)}"
    message["From"] = sender
    message["To"] = recipient
    message["Reply-To"] = formataddr((_clean_header(contact.name), contact.email))
    message["Date"] = format_datetime(datetime.now(UTC))

    body = (
        "Nouveau message depuis le portfolio\n"
        "\n"
        f"Nom : {contact.name}\n"
        f"E-mail : {contact.email}\n"
        f"Langue : {contact.lang}\n"
        f"Date : {datetime.now(UTC).isoformat(timespec='seconds')}\n"
        "\n"
        "Message :\n"
        f"{contact.message}\n"
    )
    message.set_content(body, charset="utf-8")
    return message


def send_contact_email(config: dict, contact: ContactMessage) -> None:
    if config.get("MAIL_SUPPRESS_SEND"):
        logger.info("contact_mail_suppressed", extra={"event": "contact_mail_suppressed"})
        return

    if not config.get("SMTP_HOST") or not config.get("SMTP_FROM") or not config.get("CONTACT_TO"):
        raise MailNotConfigured("smtp_not_configured")

    message = _build_message(config, contact)
    host = config["SMTP_HOST"]
    port = int(config.get("SMTP_PORT", 587))
    timeout = int(config.get("SMTP_TIMEOUT", 10))

    try:
        if port == 465:
            client = smtplib.SMTP_SSL(host, port, timeout=timeout)
        else:
            client = smtplib.SMTP(host, port, timeout=timeout)

        with client as smtp:
            smtp.ehlo()
            if port != 465 and config.get("SMTP_USE_TLS", True):
                smtp.starttls()
                smtp.ehlo()
            if config.get("SMTP_USER") and config.get("SMTP_PASSWORD"):
                smtp.login(config["SMTP_USER"], config["SMTP_PASSWORD"])
            smtp.send_message(message)
    except (smtplib.SMTPException, OSError) as exc:
        logger.warning(
            "contact_mail_failed",
            extra={"event": "contact_mail_failed", "reason": type(exc).__name__},
        )
        raise MailDeliveryError("smtp_delivery_failed") from exc
