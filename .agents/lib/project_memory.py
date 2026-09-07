"""Stable project identity and append-only Markdown continuity."""
from __future__ import annotations

import datetime as dt
from pathlib import Path
import re

PROJECT_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")


def project_path(root: Path, project: str) -> Path:
    if not PROJECT_RE.fullmatch(project) or project == "index":
        raise ValueError("--project must be a stable lowercase hyphenated project slug, not index")
    return root.expanduser().resolve() / "docs/session-memory" / f"{project}.md"


def append_entry(root: Path, project: str, title: str, body: str,
                 date: str | None = None, time: str | None = None) -> Path:
    path = project_path(root, project)
    if not title.strip() or not body.strip():
        raise ValueError("Entry title and body must not be blank")
    now = dt.datetime.now().astimezone()
    stamp_date = dt.date.fromisoformat(date) if date else now.date()
    stamp_time = dt.time.fromisoformat(time).strftime("%H:%M") if time else now.strftime("%H:%M %Z")
    previous = path.read_bytes() if path.exists() else b""
    prefix = "\n\n" if previous else f"# {project} Project Memory\n\nAppend dated progress and evidence here; current repository instructions govern workflow.\n\n"
    entry = f"{prefix}## {stamp_date.isoformat()} {stamp_time} - {title.strip()}\n\n{body.strip()}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as stream:
        stream.write(entry.encode("utf-8"))
    return path
