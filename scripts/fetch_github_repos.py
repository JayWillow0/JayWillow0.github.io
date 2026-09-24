#!/usr/bin/env python3
"""Refresh the deterministic snapshot used by the project gallery."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = ROOT / "data" / "generated" / "github_repos.json"
DEFAULT_USERNAME = "JayWillow0"
USER_AGENT = "LiuYang-Lab-site-builder/1.0"


class SnapshotError(RuntimeError):
    """Raised when the repository snapshot does not satisfy its contract."""


def normalize_repo(repo: dict[str, Any]) -> dict[str, Any]:
    """Keep only the stable public fields consumed by Hugo."""
    name = repo.get("name")
    url = repo.get("html_url") or repo.get("url")
    if not isinstance(name, str) or not name.strip():
        raise SnapshotError("repository is missing a non-empty name")
    if not isinstance(url, str) or not url.startswith("https://github.com/"):
        raise SnapshotError(f"{name}: invalid GitHub URL")

    topics = repo.get("topics") or []
    if not isinstance(topics, list) or not all(isinstance(item, str) for item in topics):
        raise SnapshotError(f"{name}: topics must be a list of strings")

    return {
        "name": name,
        "url": url,
        "description": repo.get("description") or "",
        "language": repo.get("language") or "",
        "topics": topics,
        "stars": int(repo.get("stargazers_count", repo.get("stars", 0)) or 0),
        "forks": int(repo.get("forks_count", repo.get("forks", 0)) or 0),
        "updated_at": repo.get("updated_at") or "",
        "fork": bool(repo.get("fork", False)),
    }


def filter_original(repos: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize repositories and retain only original, non-archived work."""
    originals = []
    for repo in repos:
        if repo.get("fork") or repo.get("archived"):
            continue
        originals.append(normalize_repo(repo))
    return sorted(originals, key=lambda item: item["name"].casefold())


def _next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for chunk in link_header.split(","):
        parts = [part.strip() for part in chunk.split(";")]
        if len(parts) >= 2 and parts[1] == 'rel="next"':
            return parts[0].strip("<>")
    return None


def fetch_all_repos(
    username: str,
    token: str | None = None,
    opener: Callable[..., Any] = urllib.request.urlopen,
) -> list[dict[str, Any]]:
    """Fetch every public repository, following GitHub pagination links."""
    quoted_user = urllib.parse.quote(username, safe="")
    url = (
        f"https://api.github.com/users/{quoted_user}/repos"
        "?per_page=100&type=owner&sort=updated"
    )
    raw_repos: list[dict[str, Any]] = []

    while url:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers)
        with opener(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, list):
                raise SnapshotError("GitHub API response must be a list")
            raw_repos.extend(payload)
            url = _next_link(response.headers.get("Link"))

    return filter_original(raw_repos)


def validate_snapshot(repos: Any) -> list[dict[str, Any]]:
    if not isinstance(repos, list) or not repos:
        raise SnapshotError("snapshot must contain at least one repository")
    normalized = [normalize_repo(repo) for repo in repos]
    names = [repo["name"] for repo in normalized]
    if len(names) != len(set(names)):
        raise SnapshotError("snapshot contains duplicate repository names")
    if any(repo["fork"] for repo in normalized):
        raise SnapshotError("snapshot must not contain forked repositories")
    return sorted(normalized, key=lambda item: item["name"].casefold())


def read_snapshot(path: Path) -> list[dict[str, Any]]:
    try:
        return validate_snapshot(json.loads(path.read_text(encoding="utf-8")))
    except FileNotFoundError as error:
        raise SnapshotError(f"snapshot does not exist: {path}") from error
    except json.JSONDecodeError as error:
        raise SnapshotError(f"snapshot is not valid JSON: {error}") from error


def write_snapshot(path: Path, repos: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(repos, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temporary_path = Path(handle.name)
    temporary_path.replace(path)


def partition_projects(
    repos: Iterable[dict[str, Any]], curated_slugs: Iterable[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return curated and fallback projects without dropping unknown originals."""
    curated_names = set(curated_slugs)
    curated, fallback = [], []
    for repo in repos:
        (curated if repo["name"] in curated_names else fallback).append(repo)
    return curated, fallback


def refresh(
    snapshot_path: Path,
    username: str,
    token: str | None,
    fetcher: Callable[[str, str | None], list[dict[str, Any]]] = fetch_all_repos,
) -> tuple[list[dict[str, Any]], bool]:
    """Refresh data, returning the old snapshot if GitHub is unavailable."""
    try:
        repos = validate_snapshot(fetcher(username, token))
    except (OSError, urllib.error.URLError, TimeoutError, SnapshotError) as error:
        fallback = read_snapshot(snapshot_path)
        print(
            f"warning: GitHub refresh failed; using snapshot ({error})",
            file=sys.stderr,
        )
        return fallback, False
    write_snapshot(snapshot_path, repos)
    return repos, True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="validate the committed snapshot without accessing the network",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.offline:
            repos = read_snapshot(args.snapshot)
            refreshed = False
        else:
            repos, refreshed = refresh(
                args.snapshot,
                args.username,
                os.environ.get("GITHUB_TOKEN"),
            )
    except SnapshotError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    state = "refreshed" if refreshed else "validated"
    print(f"{state} {len(repos)} original repositories in {args.snapshot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
