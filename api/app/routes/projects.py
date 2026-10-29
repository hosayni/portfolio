"""Liste des dépôts GitHub mis en avant."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify

from app.errors import ApiError
from app.services.github import GitHubService, GitHubUnavailable

bp = Blueprint("projects", __name__, url_prefix="/api")


@bp.get("/projects")
def list_projects():
    service: GitHubService | None = current_app.extensions.get("github_service")
    if service is None:  # pragma: no cover - configuration impossible
        raise ApiError("github_unavailable", "GitHub integration is not configured.", 503)

    try:
        payload = service.get_projects()
    except GitHubUnavailable as exc:
        current_app.logger.warning(
            "github_unavailable",
            extra={"event": "github_unavailable", "reason": str(exc)},
        )
        raise ApiError(
            "github_unavailable",
            "GitHub is temporarily unavailable. Please try again later.",
            503,
        ) from exc

    return jsonify(payload)
