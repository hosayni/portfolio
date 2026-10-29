"""Point d'entrée WSGI pour Gunicorn et Flask CLI."""

from __future__ import annotations

from app import create_app

app = create_app()

if __name__ == "__main__":  # pragma: no cover - confort local
    app.run(host="127.0.0.1", port=8000, debug=True)
