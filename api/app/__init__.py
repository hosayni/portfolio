"""Application factory de l'API portfolio."""

from __future__ import annotations

import re
import time
import uuid
from typing import Any

from flask import Flask, g, jsonify, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Config, validate_production_config
from app.errors import register_error_handlers
from app.extensions import limiter
from app.logging_config import configure_logging
from app.routes.contact import bp as contact_bp
from app.routes.health import bp as health_bp
from app.routes.projects import bp as projects_bp
from app.services.github import GitHubService

REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9-]{8,64}$")


def _request_id() -> str:
    candidate = request.headers.get("X-Request-ID", "")
    return candidate if REQUEST_ID_RE.match(candidate) else uuid.uuid4().hex[:12]


def create_app(config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    validate_production_config(app.config)

    app.url_map.strict_slashes = False
    app.json.ensure_ascii = False
    app.config["STARTED_AT"] = time.monotonic()

    if app.config.get("TRUST_PROXY"):
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)  # type: ignore[method-assign]

    configure_logging(app)

    app.config.setdefault("RATELIMIT_HEADERS_ENABLED", True)
    limiter.init_app(app)

    origins = app.config.get("CORS_ORIGINS") or []
    if origins:
        CORS(
            app,
            resources={
                r"/api/*": {
                    "origins": origins,
                    "methods": ["GET", "POST", "OPTIONS"],
                    "allow_headers": ["Content-Type", "X-Request-ID"],
                    "max_age": 600,
                }
            },
            supports_credentials=False,
        )

    app.extensions["github_service"] = GitHubService(
        username=app.config["GITHUB_USERNAME"],
        token=app.config.get("GITHUB_TOKEN", ""),
        cache_ttl=app.config.get("GITHUB_CACHE_TTL", 3600),
        max_repos=app.config.get("GITHUB_MAX_REPOS", 6),
        repos=app.config.get("GITHUB_REPOS") or [],
        timeout=app.config.get("GITHUB_HTTP_TIMEOUT", 5),
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(contact_bp)

    register_error_handlers(app)

    @app.before_request
    def _start_request() -> None:
        g.request_id = _request_id()
        g.request_started_at = time.perf_counter()

    @app.after_request
    def _finalize_response(response):
        elapsed = time.perf_counter() - g.get("request_started_at", time.perf_counter())
        duration_ms = int(elapsed * 1000)
        request_id = g.get("request_id", uuid.uuid4().hex[:12])
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
        )
        if request.is_secure or app.config.get("APP_ENV") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        if request.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
            app.logger.info(
                "request",
                extra={
                    "event": "request",
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.path,
                    "status": response.status_code,
                    "duration_ms": duration_ms,
                },
            )
        return response

    @app.get("/")
    def index():
        return jsonify(
            name="portfolio-api",
            version=app.config.get("VERSION"),
            endpoints=["/api/health", "/api/projects", "/api/contact"],
        )

    return app


__all__ = ["create_app"]
