"""Configuration de l'API, lue depuis l'environnement.

Aucune valeur secrète n'est stockée ici : les valeurs par défaut servent
uniquement au développement local. La factory refuse de démarrer en production
si les secrets indispensables sont absents ou restés à leur valeur d'exemple.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

API_DIR = Path(__file__).resolve().parents[1]

# Charge `api/.env` puis la racine du dépôt, sans écraser les variables déjà
# définies par l'environnement (Docker, CI, production).
load_dotenv(API_DIR / ".env")
load_dotenv(API_DIR.parent / ".env")


def _as_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _as_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _as_list(name: str, default: tuple[str, ...] = ()) -> list[str]:
    raw = os.getenv(name)
    if raw is None:
        return list(default)
    return [item.strip() for item in raw.split(",") if item.strip()]


class Config:
    APP_ENV = os.getenv("APP_ENV", "development")
    VERSION = os.getenv("APP_VERSION", "0.1.0")
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    SITE_URL = os.getenv("SITE_URL", "http://localhost:4321")
    SITE_NAME = os.getenv("SITE_NAME", "Mohamed Hosayni")
    CORS_ORIGINS = _as_list(
        "CORS_ORIGINS",
        ("http://localhost:4321", "https://hosayni.com"),
    )

    CONTACT_ENABLED = _as_bool("CONTACT_ENABLED", True)
    CONTACT_RATE_LIMIT = os.getenv("CONTACT_RATE_LIMIT", "5 per hour")
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
    RATELIMIT_ENABLED = _as_bool("RATELIMIT_ENABLED", True)

    GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "hosayni")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_CACHE_TTL = _as_int("GITHUB_CACHE_TTL", 3600)
    GITHUB_MAX_REPOS = _as_int("GITHUB_MAX_REPOS", 6)
    GITHUB_REPOS = _as_list("GITHUB_REPOS")
    GITHUB_HTTP_TIMEOUT = _as_int("GITHUB_HTTP_TIMEOUT", 5)

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = _as_int("SMTP_PORT", 587)
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_USE_TLS = _as_bool("SMTP_USE_TLS", True)
    SMTP_FROM = os.getenv("SMTP_FROM", "")
    CONTACT_TO = os.getenv("CONTACT_TO", "")
    MAIL_SUPPRESS_SEND = _as_bool("MAIL_SUPPRESS_SEND", APP_ENV != "production")
    SMTP_TIMEOUT = _as_int("SMTP_TIMEOUT", 10)

    # À activer uniquement derrière Caddy/nginx : fait confiance à un proxy
    # pour X-Forwarded-For/Proto. Indispensable au rate limiting par IP réelle.
    TRUST_PROXY = _as_bool("TRUST_PROXY", APP_ENV == "production")

    MAX_CONTENT_LENGTH = 16 * 1024


def validate_production_config(config: dict) -> None:
    """Échoue vite plutôt que de servir une API mal configurée."""

    if config.get("APP_ENV") != "production":
        return

    problems: list[str] = []

    if config.get("SECRET_KEY") in (None, "", "change-me-in-production"):
        problems.append("SECRET_KEY")
    if not config.get("CORS_ORIGINS"):
        problems.append("CORS_ORIGINS")

    # Le formulaire peut rester désactivé tant qu'aucun SMTP n'est configuré :
    # l'API démarre alors sans dépendre d'un serveur mail, et /api/contact
    # répond 503. Dès que CONTACT_ENABLED=true, SMTP devient obligatoire.
    if config.get("CONTACT_ENABLED", True):
        if not config.get("SMTP_HOST"):
            problems.append("SMTP_HOST")
        if not config.get("SMTP_FROM"):
            problems.append("SMTP_FROM")
        if not config.get("CONTACT_TO"):
            problems.append("CONTACT_TO")
        if config.get("MAIL_SUPPRESS_SEND"):
            problems.append("MAIL_SUPPRESS_SEND")

    if problems:
        joined = ", ".join(problems)
        raise RuntimeError(f"Configuration de production incomplète : {joined}")
