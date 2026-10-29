"""Fixtures partagées par les tests de l'API."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import suppress
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.extensions import limiter

BASE_CONFIG: dict[str, Any] = {
    "TESTING": True,
    "APP_ENV": "test",
    "VERSION": "0.1.0-test",
    "SECRET_KEY": "test-secret",
    "CORS_ORIGINS": ["http://localhost:4321", "https://hosayni.com"],
    "CONTACT_RATE_LIMIT": "100 per hour",
    "GITHUB_USERNAME": "hosayni",
    "GITHUB_TOKEN": "",
    "GITHUB_REPOS": [],
    "GITHUB_CACHE_TTL": 3600,
    "MAIL_SUPPRESS_SEND": True,
    "TRUST_PROXY": False,
    "RATELIMIT_ENABLED": True,
    "RATELIMIT_STORAGE_URI": "memory://",
}


@pytest.fixture
def make_app() -> Iterator[Callable[..., Flask]]:
    apps: list[Flask] = []

    def factory(**overrides: Any) -> Flask:
        app = create_app({**BASE_CONFIG, **overrides})
        apps.append(app)
        return app

    yield factory

    for app in apps:
        with suppress(Exception), app.app_context():
            limiter.reset()


@pytest.fixture
def app(make_app: Callable[..., Flask]) -> Flask:
    return make_app()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
