#!/usr/bin/env python3
"""Validate the generated static site without third-party packages."""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "index.html",
    "projects/index.html",
    "posts/index.html",
    "wechat/index.html",
    "about/index.html",
    "categories/index.html",
    "tags/index.html",
    "search/index.html",
    "404.html",
    "index.xml",
    "sitemap.xml",
)
FORBIDDEN_TERM = "com" + "sol"


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_depth = 0
        self.title_text: list[str] = []
        self.meta_description = False
        self.canonical = False
        self.references: list[tuple[str, str]] = []
        self.external_assets: list[str] = []
        self.project_slugs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.title_depth += 1
        if tag == "meta" and values.get("name") == "description" and values.get("content"):
            self.meta_description = True
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonical = True
        if "data-project-slug" in values and values["data-project-slug"]:
            self.project_slugs.append(values["data-project-slug"] or "")

        for attribute in ("href", "src"):
            value = values.get(attribute)
            if not value:
                continue
            self.references.append((tag, value))
            if tag in {"script", "img", "source"} and value.startswith(("http://", "https://")):
                self.external_assets.append(value)
            if tag == "link" and "stylesheet" in (values.get("rel") or "") and value.startswith(("http://", "https://")):
                self.external_assets.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)


def local_target(public_dir: Path, source_file: Path, url: str) -> Path | None:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or url.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    if path.startswith("/"):
        target = public_dir / path.lstrip("/")
    else:
        target = source_file.parent / path
    if path.endswith("/"):
        target = target / "index.html"
    elif not target.suffix:
        index_candidate = target / "index.html"
        if index_candidate.exists():
            target = index_candidate
    return target


def validate(public_dir: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (public_dir / relative).is_file():
            errors.append(f"missing required output: {relative}")

    html_files = sorted(public_dir.rglob("*.html"))
    if not html_files:
        return errors + ["no HTML files were generated"]

    project_parser: DocumentParser | None = None
    for html_file in html_files:
        html_text = html_file.read_text(encoding="utf-8")
        if FORBIDDEN_TERM in html_text.casefold():
            errors.append(f"{html_file.relative_to(public_dir)}: contains forbidden product name")
        parser = DocumentParser()
        parser.feed(html_text)
        relative = html_file.relative_to(public_dir)
        if not "".join(parser.title_text).strip():
            errors.append(f"{relative}: missing title")
        if not parser.meta_description:
            errors.append(f"{relative}: missing meta description")
        if not parser.canonical:
            errors.append(f"{relative}: missing canonical URL")
        for asset in parser.external_assets:
            errors.append(f"{relative}: runtime asset is not local: {asset}")
        for _, reference in parser.references:
            target = local_target(public_dir, html_file, reference)
            if target is not None and not target.exists():
                errors.append(f"{relative}: broken local reference {reference}")
        if relative.as_posix() == "projects/index.html":
            project_parser = parser

    if project_parser is not None:
        snapshot = json.loads(
            (ROOT / "data" / "generated" / "github_repos.json").read_text(encoding="utf-8")
        )
        expected = {repo["name"] for repo in snapshot if not repo.get("fork")}
        actual = project_parser.project_slugs
        if len(actual) != len(set(actual)):
            errors.append("projects/index.html: duplicate project cards")
        if set(actual) != expected:
            errors.append(
                "projects/index.html: project set differs from snapshot "
                f"(missing={sorted(expected - set(actual))}, extra={sorted(set(actual) - expected)})"
            )

    for xml_file in sorted(public_dir.rglob("*.xml")):
        if FORBIDDEN_TERM in xml_file.read_text(encoding="utf-8").casefold():
            errors.append(f"{xml_file.relative_to(public_dir)}: contains forbidden product name")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public_dir", nargs="?", type=Path, default=ROOT / "public")
    args = parser.parse_args()
    errors = validate(args.public_dir.resolve())
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"validated static site at {args.public_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
