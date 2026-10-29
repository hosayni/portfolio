"""Tests de la configuration et de la journalisation."""

from __future__ import annotations

import json
import logging

import pytest
from flask import Flask

from app.config import Config, validate_production_config
from app.logging_config import JsonFormatter, configure_logging


def test_production_requires_secrets() -> None:
    with pytest.raises(RuntimeError) as error:
        validate_production_config(
            {
                "APP_ENV": "production",
                "SECRET_KEY": "change-me-in-production",
                "SMTP_HOST": "",
                "SMTP_FROM": "",
                "CONTACT_TO": "",
                "CORS_ORIGINS": [],
                "MAIL_SUPPRESS_SEND": True,
            }
        )

    message = str(error.value)
    for key in (
        "SECRET_KEY",
        "SMTP_HOST",
        "SMTP_FROM",
        "CONTACT_TO",
        "CORS_ORIGINS",
        "MAIL_SUPPRESS_SEND",
    ):
        assert key in message


def test_development_config_is_not_validated() -> None:
    validate_production_config({"APP_ENV": "development"})


def test_production_without_contact_only_requires_core_secrets() -> None:
    validate_production_config(
        {
            "APP_ENV": "production",
            "SECRET_KEY": "a-long-random-secret",
            "CORS_ORIGINS": ["https://hosayni.com"],
            "CONTACT_ENABLED": False,
            "SMTP_HOST": "",
            "SMTP_FROM": "",
            "CONTACT_TO": "",
            "MAIL_SUPPRESS_SEND": True,
        }
    )


def test_production_with_contact_enabled_requires_smtp() -> None:
    with pytest.raises(RuntimeError) as error:
        validate_production_config(
            {
                "APP_ENV": "production",
                "SECRET_KEY": "a-long-random-secret",
                "CORS_ORIGINS": ["https://hosayni.com"],
                "CONTACT_ENABLED": True,
                "SMTP_HOST": "",
                "SMTP_FROM": "",
                "CONTACT_TO": "",
                "MAIL_SUPPRESS_SEND": True,
            }
        )

    message = str(error.value)
    for key in ("SMTP_HOST", "SMTP_FROM", "CONTACT_TO", "MAIL_SUPPRESS_SEND"):
        assert key in message


def test_environment_defaults_are_sane() -> None:
    assert Config.VERSION
    assert Config.GITHUB_CACHE_TTL > 0
    assert Config.MAX_CONTENT_LENGTH == 16 * 1024


def test_json_formatter_includes_context() -> None:
    record = logging.LogRecord(
        name="app.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="hello",
        args=(),
        exc_info=None,
    )
    record.request_id = "abc12345"
    record.status = 200

    payload = json.loads(JsonFormatter().format(record))

    assert payload["message"] == "hello"
    assert payload["level"] == "INFO"
    assert payload["request_id"] == "abc12345"
    assert payload["status"] == 200


def test_configure_logging_installs_json_handler() -> None:
    root = logging.getLogger()
    previous = root.handlers[:]
    try:
        app = Flask(__name__)
        app.config.update(TESTING=False, LOG_LEVEL="INFO")

        configure_logging(app)

        assert isinstance(root.handlers[0].formatter, JsonFormatter)
    finally:
        root.handlers = previous
