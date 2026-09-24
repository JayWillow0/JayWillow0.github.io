from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "fetch_github_repos.py"
SPEC = importlib.util.spec_from_file_location("fetch_github_repos", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FakeResponse:
    def __init__(self, payload, link=None):
        self.payload = payload
        self.headers = {"Link": link} if link else {}

    def read(self):
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def repo(name, *, fork=False, archived=False):
    return {
        "name": name,
        "html_url": f"https://github.com/JayWillow0/{name}",
        "description": None,
        "language": "Python",
        "topics": [],
        "stargazers_count": 2,
        "forks_count": 1,
        "updated_at": "2026-09-24T00:00:00Z",
        "fork": fork,
        "archived": archived,
    }


class FetchRepositoriesTests(unittest.TestCase):
    def test_filter_excludes_forks_and_archived_repositories(self):
        result = MODULE.filter_original(
            [repo("Owned"), repo("Fork", fork=True), repo("Old", archived=True)]
        )
        self.assertEqual([item["name"] for item in result], ["Owned"])
        self.assertEqual(result[0]["description"], "")

    def test_fetch_follows_pagination(self):
        responses = iter(
            [
                FakeResponse([repo("First")], '<https://api.github.com/page=2>; rel="next"'),
                FakeResponse([repo("Second")]),
            ]
        )

        def opener(*_, **__):
            return next(responses)

        result = MODULE.fetch_all_repos("JayWillow0", opener=opener)
        self.assertEqual([item["name"] for item in result], ["First", "Second"])

    def test_refresh_uses_existing_snapshot_on_api_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "repos.json"
            MODULE.write_snapshot(path, MODULE.filter_original([repo("Cached")]))

            def failing_fetcher(*_):
                raise urllib.error.URLError("offline")

            result, refreshed = MODULE.refresh(path, "JayWillow0", None, failing_fetcher)
            self.assertFalse(refreshed)
            self.assertEqual(result[0]["name"], "Cached")

    def test_unknown_original_is_kept_in_fallback_partition(self):
        repos = MODULE.filter_original([repo("Curated"), repo("NewResearch")])
        curated, fallback = MODULE.partition_projects(repos, ["Curated"])
        self.assertEqual([item["name"] for item in curated], ["Curated"])
        self.assertEqual([item["name"] for item in fallback], ["NewResearch"])

    def test_snapshot_rejects_duplicate_names(self):
        records = MODULE.filter_original([repo("Duplicate")])
        with self.assertRaises(MODULE.SnapshotError):
            MODULE.validate_snapshot(records + records)


if __name__ == "__main__":
    unittest.main()
