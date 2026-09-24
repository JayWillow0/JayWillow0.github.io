from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProjectContractTests(unittest.TestCase):
    def test_forbidden_product_name_is_absent_from_site_sources(self):
        forbidden = "com" + "sol"
        roots = [
            ROOT / "hugo.yaml",
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / "archetypes",
            ROOT / "content",
            ROOT / "data",
            ROOT / "docs",
            ROOT / "layouts",
            ROOT / "scripts",
            ROOT / "static",
        ]
        offenders: list[str] = []
        for source in roots:
            files = [source] if source.is_file() else source.rglob("*")
            for path in files:
                if not path.is_file() or path.suffix.lower() not in {
                    ".css", ".html", ".js", ".json", ".md", ".py", ".svg", ".txt", ".xml", ".yaml", ".yml"
                }:
                    continue
                if forbidden in path.read_text(encoding="utf-8").casefold():
                    offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_current_original_repositories_are_curated(self):
        snapshot = json.loads(
            (ROOT / "data" / "generated" / "github_repos.json").read_text(encoding="utf-8")
        )
        overrides = (ROOT / "data" / "project_overrides.yaml").read_text(encoding="utf-8")
        curated = set(re.findall(r"^\s+- slug:\s*(.+?)\s*$", overrides, re.MULTILINE))
        originals = {repo["name"] for repo in snapshot if not repo.get("fork")}
        self.assertTrue(curated.issubset(originals))
        self.assertEqual(len(curated), 8)

    def test_project_covers_follow_asset_convention(self):
        overrides = (ROOT / "data" / "project_overrides.yaml").read_text(encoding="utf-8")
        covers = re.findall(r"^\s+cover:\s*(.+?)\s*$", overrides, re.MULTILINE)
        self.assertEqual(len(covers), 8)
        for cover in covers:
            self.assertTrue(cover.startswith("images/projects/"))
            self.assertTrue((ROOT / "assets" / cover).is_file(), cover)


if __name__ == "__main__":
    unittest.main()
