"""Tests du service GitHub (hors réseau)."""

from __future__ import annotations

from typing import Any

import pytest
import requests

from app.services import github
from app.services.github import GitHubService, GitHubUnavailable


class FakeResponse:
    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def json(self) -> Any:
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


def repo(
    name: str,
    pushed_at: str = "2026-01-01T00:00:00Z",
    *,
    fork: bool = False,
    archived: bool = False,
    language: str = "Python",
) -> dict[str, Any]:
    return {
        "name": name,
        "description": f"Description de {name}",
        "language": language,
        "stargazers_count": 12,
        "pushed_at": pushed_at,
        "html_url": f"https://github.com/hosayni/{name}",
        "homepage": "",
        "topics": ["astro", "flask"],
        "fork": fork,
        "archived": archived,
    }


def test_projects_are_filtered_sorted_and_enriched(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        calls.append(url)
        if url.endswith("/repos"):
            return FakeResponse(
                [
                    repo("old", "2025-01-01T00:00:00Z"),
                    repo("new", "2026-05-01T00:00:00Z"),
                    repo("forked", fork=True),
                    repo("archived", archived=True),
                ]
            )
        if url.endswith("/old/languages"):
            return FakeResponse({"Python": 1000, "HTML": 200, "CSS": 50, "Shell": 5})
        return FakeResponse({"Python": 500})

    monkeypatch.setattr(github.requests, "get", fake_get)
    service = GitHubService("hosayni", max_repos=2)

    payload = service.get_projects()

    assert payload["cached"] is False
    assert payload["stale"] is False
    assert payload["ttl"] == 3600
    assert [project["name"] for project in payload["projects"]] == ["new", "old"]
    assert payload["projects"][0]["languages"] == ["Python"]
    assert payload["projects"][1]["languages"] == ["Python", "HTML", "CSS"]
    assert payload["projects"][0]["stars"] == 12
    assert payload["projects"][0]["url"].endswith("/new")
    assert payload["projects"][0]["homepage"] is None
    assert len(calls) == 3


def test_allowlist_preserves_configured_order(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        if url.endswith("/repos"):
            return FakeResponse([repo("a"), repo("b"), repo("c")])
        return FakeResponse({"Python": 1})

    monkeypatch.setattr(github.requests, "get", fake_get)
    service = GitHubService("hosayni", repos=["c", "a", "missing"])

    payload = service.get_projects()

    assert [project["name"] for project in payload["projects"]] == ["c", "a"]


def test_cache_avoids_second_network_call(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        nonlocal calls
        calls += 1
        if url.endswith("/repos"):
            return FakeResponse([repo("only")])
        return FakeResponse({"Python": 1})

    monkeypatch.setattr(github.requests, "get", fake_get)
    service = GitHubService("hosayni")

    first = service.get_projects()
    second = service.get_projects()

    assert first["cached"] is False
    assert second["cached"] is True
    assert second["stale"] is False
    assert calls == 2


def test_stale_cache_is_used_when_github_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    def working_get(url: str, **kwargs: Any) -> FakeResponse:
        if url.endswith("/repos"):
            return FakeResponse([repo("cached")])
        return FakeResponse({"Python": 1})

    monkeypatch.setattr(github.requests, "get", working_get)
    service = GitHubService("hosayni", cache_ttl=0)
    first = service.get_projects()
    assert first["projects"][0]["name"] == "cached"

    def failing_get(url: str, **kwargs: Any) -> FakeResponse:
        raise requests.ConnectionError("offline")

    monkeypatch.setattr(github.requests, "get", failing_get)
    stale = service.get_projects()

    assert stale["cached"] is True
    assert stale["stale"] is True
    assert stale["projects"][0]["name"] == "cached"


def test_github_failure_without_cache_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    def failing_get(url: str, **kwargs: Any) -> FakeResponse:
        raise requests.Timeout("timed out")

    monkeypatch.setattr(github.requests, "get", failing_get)
    service = GitHubService("hosayni")

    with pytest.raises(GitHubUnavailable, match="github_request_failed"):
        service.get_projects()


@pytest.mark.parametrize(
    ("response", "reason"),
    [
        (FakeResponse({}, status_code=403), "github_status_403"),
        (FakeResponse([], status_code=500), "github_status_500"),
        (FakeResponse(ValueError("bad json")), "github_invalid_json"),
        (FakeResponse({"message": "not a list"}), "github_invalid_response"),
    ],
)
def test_invalid_github_responses_raise(
    monkeypatch: pytest.MonkeyPatch, response: FakeResponse, reason: str
) -> None:
    monkeypatch.setattr(github.requests, "get", lambda *args, **kwargs: response)
    service = GitHubService("hosayni")

    with pytest.raises(GitHubUnavailable, match=reason):
        service.get_projects()


def test_language_failure_falls_back_to_primary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        if url.endswith("/repos"):
            return FakeResponse([repo("fallback", language="Rust")])
        raise requests.ConnectionError("languages unavailable")

    monkeypatch.setattr(github.requests, "get", fake_get)
    service = GitHubService("hosayni")

    payload = service.get_projects()

    assert payload["projects"][0]["languages"] == ["Rust"]


def test_empty_repository_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github.requests, "get", lambda *args, **kwargs: FakeResponse([]))
    service = GitHubService("hosayni")

    payload = service.get_projects()

    assert payload["projects"] == []
    assert payload["cached"] is False


def test_token_is_sent_as_bearer(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        captured.update(kwargs)
        return FakeResponse([])

    monkeypatch.setattr(github.requests, "get", fake_get)
    GitHubService("hosayni", token="secret-token").get_projects()

    assert captured["headers"]["Authorization"] == "Bearer secret-token"
    assert captured["timeout"] == 5.0
