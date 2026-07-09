#!/usr/bin/env python3
"""Shared helpers for Builder hub workflow scripts."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import re
import subprocess


HUB_ROOTS = (
    Path("C:/Users/Christopher/Developer/builder"),
    Path("/Users/cbell/Developer/builder"),
)
HUB_ROOT = HUB_ROOTS[0]

DATED_FILE_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.+)\.md$")

STATUS_VALUES = (
    "proposed",
    "active",
    "blocked",
    "in-review",
    "ready-to-close",
    "closed",
)


def resolve_root(root: str | Path = ".") -> Path:
    return Path(root).expanduser().resolve()


def today_local() -> dt.date:
    return dt.datetime.now().astimezone().date()


def timestamp_local() -> str:
    return dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")


def slugify(value: str, fallback: str = "artifact", max_length: int = 80) -> str:
    normalized = value.lower().encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized[:max_length].strip("-") or fallback


def dated_markdown_path(root: Path, directory: str, title: str, date: dt.date | None = None) -> Path:
    artifact_date = date or today_local()
    return root / directory / f"{artifact_date.isoformat()}-{slugify(title)}.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return path


def first_heading(path: Path) -> str:
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except UnicodeDecodeError:
        return path.stem
    return path.stem


def list_markdown(root: Path, directory: str) -> list[Path]:
    target = root / directory
    if not target.exists():
        return []
    return sorted(path for path in target.glob("*.md") if path.is_file())


def parse_dated_file(path: Path) -> tuple[str, str] | None:
    match = DATED_FILE_RE.match(path.name)
    if not match:
        return None
    return match.group("date"), match.group("slug")


def relative_link(from_file: Path, to_file: Path) -> str:
    return to_file.relative_to(from_file.parent).as_posix()


def git_output(repo: Path, *args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def extract_status(markdown: str) -> str | None:
    patterns = (
        r"(?im)^-\s*Status:\s*`?([a-z-]+)`?\s*$",
        r"(?im)^Status:\s*`?([a-z-]+)`?\s*$",
        r"(?im)^##\s+Status\s*\n+([a-z-]+)\s*$",
    )
    for pattern in patterns:
        match = re.search(pattern, markdown)
        if match:
            return match.group(1).strip().lower()
    return None


def markdown_links(markdown: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown)
