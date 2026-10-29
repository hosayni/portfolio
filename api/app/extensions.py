"""Extensions partagées par l'application."""

from __future__ import annotations

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Le stockage est fixé par la factory à partir de RATELIMIT_STORAGE_URI.
limiter = Limiter(key_func=get_remote_address)
