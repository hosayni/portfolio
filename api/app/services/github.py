"""Récupération des dépôts GitHub avec cache mémoire.

Le service est volontairement indépendant de Flask pour être testable seul.
Il applique un cache TTL (1 h par défaut), une liste blanche optionnelle de
dépôts et un repli sur le cache périmé si GitHub est indisponible.
"""

from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib.parse import quote

import requests

GITHUB_API = "https://api.github.com"
USER_AGENT = "portfolio-api"


class GitHubUnavailable(RuntimeError):
    """GitHub n'a pas répondu correctement et aucun cache n'est disponible."""


@dataclass(frozen=True)
class _CacheEntry:
    payload: dict[str, Any]
    expires_at: float


class GitHubService:
    def __init__(
        self,
        username: str,
        token: str = "",
        cache_ttl: int = 3600,
        max_repos: int = 6,
        repos: list[str] | None = None,
        timeout: float = 5.0,
    ) -> None:
        self.username = username
        self._token = token
        self._cache_ttl = max(0, cache_ttl)
        self._max_repos = max(1, max_repos)
        self._repos = [name for name in (repos or []) if name]
        self._timeout = max(1.0, timeout)
        self._lock = threading.Lock()
        self._cache: _CacheEntry | None = None

    def get_projects(self) -> dict[str, Any]:
        """Retourne les projets, depuis le cache ou GitHub.

        Lève ``GitHubUnavailable`` si l'appel échoue sans cache exploitable.
        """

        now = time.monotonic()
        with self._lock:
            if self._cache and now < self._cache.expires_at:
                return {**self._cache.payload, "cached": True, "stale": False}

        try:
            payload = self._fetch_payload()
        except GitHubUnavailable:
            with self._lock:
                if self._cache:
                    return {**self._cache.payload, "cached": True, "stale": True}
            raise

        payload["ttl"] = self._cache_ttl
        with self._lock:
            self._cache = _CacheEntry(payload=payload, expires_at=now + self._cache_ttl)
        return {**payload, "cached": False, "stale": False}

    def _fetch_payload(self) -> dict[str, Any]:
        repositories = self._request(
            f"/users/{quote(self.username, safe='')}/repos",
            params={"per_page": 100, "sort": "pushed", "direction": "desc"},
        )
        if not isinstance(repositories, list):
            raise GitHubUnavailable("github_invalid_response")

        selected = self._select(repositories)
        languages = self._fetch_languages(selected)
        projects = [self._to_project(repo, languages.get(repo["name"], [])) for repo in selected]

        return {
            "projects": projects,
            "fetched_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }

    def _select(self, repositories: list[Any]) -> list[dict[str, Any]]:
        candidates = [
            repo
            for repo in repositories
            if isinstance(repo, dict)
            and repo.get("name")
            and not repo.get("fork")
            and not repo.get("archived")
        ]

        if self._repos:
            by_name = {repo["name"]: repo for repo in candidates}
            selected = [by_name[name] for name in self._repos if name in by_name]
        else:
            selected = sorted(
                candidates,
                key=lambda repo: repo.get("pushed_at") or "",
                reverse=True,
            )

        return selected[: self._max_repos]

    def _fetch_languages(self, repositories: list[dict[str, Any]]) -> dict[str, list[str]]:
        if not repositories:
            return {}

        def fetch(repo: dict[str, Any]) -> tuple[str, list[str]]:
            fallback = [repo["language"]] if repo.get("language") else []
            owner = quote(self.username, safe="")
            name = quote(repo["name"], safe="")
            try:
                data = self._request(f"/repos/{owner}/{name}/languages")
            except GitHubUnavailable:
                return repo["name"], fallback
            if not isinstance(data, dict):
                return repo["name"], fallback
            ordered = sorted(data.items(), key=lambda item: item[1], reverse=True)
            return repo["name"], [name for name, _ in ordered[:3]] or fallback

        with ThreadPoolExecutor(max_workers=min(4, len(repositories))) as pool:
            return dict(pool.map(fetch, repositories))

    @staticmethod
    def _to_project(repo: dict[str, Any], languages: list[str]) -> dict[str, Any]:
        return {
            "name": repo["name"],
            "description": repo.get("description"),
            "languages": languages,
            "stars": int(repo.get("stargazers_count") or 0),
            "updated_at": repo.get("pushed_at"),
            "url": repo.get("html_url"),
            "homepage": repo.get("homepage") or None,
            "topics": repo.get("topics") or [],
        }

    def _request(self, path: str, params: dict[str, Any] | None = None) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        try:
            response = requests.get(
                f"{GITHUB_API}{path}",
                headers=headers,
                params=params,
                timeout=self._timeout,
            )
        except requests.RequestException as exc:  # pragma: no cover - réseau
            raise GitHubUnavailable("github_request_failed") from exc

        if response.status_code != 200:
            raise GitHubUnavailable(f"github_status_{response.status_code}")

        try:
            return response.json()
        except ValueError as exc:
            raise GitHubUnavailable("github_invalid_json") from exc
