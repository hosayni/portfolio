"""Tests de la route /api/projects avec un service simulé."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from flask import Flask

from app.services.github import GitHubUnavailable

PROJECTS_PAYLOAD: dict[str, Any] = {
    "projects": [
        {
            "name": "portfolio",
            "description": "Mon portfolio",
            "languages": ["Python", "Astro"],
            "stars": 3,
            "updated_at": "2026-05-01T00:00:00Z",
            "url": "https://github.com/hosayni/portfolio",
            "homepage": None,
            "topics": [],
        }
    ],
    "fetched_at": "2026-05-01T10:00:00+00:00",
    "ttl": 3600,
    "cached": False,
    "stale": False,
}


class StubService:
    def __init__(self, payload: dict[str, Any] | None = None, error: bool = False) -> None:
        self._payload = payload
        self._error = error

    def get_projects(self) -> dict[str, Any]:
        if self._error:
            raise GitHubUnavailable("github_status_500")
        assert self._payload is not None
        return self._payload


def test_projects_route_returns_payload(make_app: Callable[..., Flask]) -> None:
    app = make_app()
    app.extensions["github_service"] = StubService(PROJECTS_PAYLOAD)

    response = app.test_client().get("/api/projects")

    assert response.status_code == 200
    body = response.get_json()
    assert body["projects"][0]["name"] == "portfolio"
    assert body["cached"] is False


def test_projects_route_returns_503_when_github_fails(
    make_app: Callable[..., Flask],
) -> None:
    app = make_app()
    app.extensions["github_service"] = StubService(error=True)

    response = app.test_client().get("/api/projects")

    assert response.status_code == 503
    assert response.get_json()["error"] == "github_unavailable"
