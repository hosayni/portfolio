"""Tests de l'endpoint de santé et des réponses transverses."""

from __future__ import annotations

from collections.abc import Callable

from flask import Flask
from flask.testing import FlaskClient


def test_health_returns_status_and_version(client: FlaskClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "ok"
    assert body["version"] == "0.1.0-test"
    assert body["environment"] == "test"
    assert body["uptime_seconds"] >= 0


def test_health_security_headers(client: FlaskClient) -> None:
    response = client.get("/api/health")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "default-src 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers["Cache-Control"] == "no-store"


def test_request_id_is_echoed_when_valid(client: FlaskClient) -> None:
    response = client.get("/api/health", headers={"X-Request-ID": "abc12345"})

    assert response.headers["X-Request-ID"] == "abc12345"


def test_request_id_is_replaced_when_invalid(client: FlaskClient) -> None:
    response = client.get("/api/health", headers={"X-Request-ID": "bad id"})

    assert response.headers["X-Request-ID"] != "bad id"
    assert len(response.headers["X-Request-ID"]) == 12


def test_index_lists_endpoints(client: FlaskClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "/api/health" in response.get_json()["endpoints"]


def test_unknown_endpoint_returns_json_404(client: FlaskClient) -> None:
    response = client.get("/api/unknown")

    assert response.status_code == 404
    body = response.get_json()
    assert body["error"] == "not_found"
    assert "message" in body


def test_wrong_method_returns_json_405(client: FlaskClient) -> None:
    response = client.get("/api/contact")

    assert response.status_code == 405
    assert response.get_json()["error"] == "method_not_allowed"


def test_allowed_cors_origin(client: FlaskClient) -> None:
    response = client.get("/api/health", headers={"Origin": "https://hosayni.com"})

    assert response.headers["Access-Control-Allow-Origin"] == "https://hosayni.com"


def test_disallowed_cors_origin(client: FlaskClient) -> None:
    response = client.get("/api/health", headers={"Origin": "https://evil.example"})

    assert "Access-Control-Allow-Origin" not in response.headers


def test_proxy_headers_are_trusted_when_enabled(
    make_app: Callable[..., Flask],
) -> None:
    app = make_app(TRUST_PROXY=True)
    client = app.test_client()

    response = client.get(
        "/api/health",
        headers={"X-Forwarded-Proto": "https", "X-Forwarded-For": "203.0.113.10"},
    )

    assert response.headers["Strict-Transport-Security"].startswith("max-age=31536000")
