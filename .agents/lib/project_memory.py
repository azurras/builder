"""Dated session records: one append-only file per date, each entry tagged with its project."""
from __future__ import annotations

import datetime as dt
from pathlib import Path, PurePosixPath
import re

from spoke_registry import require_active_project

PROJECT_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
MEMORY_DIRECTORY = PurePosixPath("docs/session-memory")
# The tag under every entry heading; the hub check and snapshot lookups read it.
PROJECT_LINE_RE = re.compile(r"^\*\*Project:\*\* (?P<project>\S+)$", re.MULTILINE)
ENTRY_HEADING_RE = re.compile(r"^## ", re.MULTILINE)
# A Markdown link target naming a former per-project memory file, before any anchor.
PROJECT_MEMORY_LINK_RE = re.compile(
    r"\]\((?P<folder>(?:[^()\s#]*/)?)(?P<date>\d{4}-\d{2}-\d{2})-[a-z][a-z0-9-]*\.md(?P<anchor>#[^()\s]*)?\)")


def memory_day_path(root: Path, date: str | None = None) -> Path:
    day = dt.date.fromisoformat(date) if date else dt.date.today()
    return root.expanduser().resolve() / MEMORY_DIRECTORY / f"{day.isoformat()}.md"


def append_entry(root: Path, project: str, title: str, body: str,
                 date: str | None = None, time: str | None = None) -> Path:
    if not PROJECT_RE.fullmatch(project) or project == "index":
        raise ValueError("--project must be a stable lowercase hyphenated project slug, not index")
    if not title.strip() or not body.strip():
        raise ValueError("Entry title and body must not be blank")
    builder_root = root.expanduser().resolve()
    require_active_project(builder_root, project)
    now = dt.datetime.now().astimezone()
    stamp_date = dt.date.fromisoformat(date) if date else now.date()
    path = memory_day_path(builder_root, stamp_date.isoformat())
    stamp_time = dt.time.fromisoformat(time).strftime("%H:%M") if time else now.strftime("%H:%M %Z")
    previous = path.read_bytes() if path.exists() else b""
    if not previous:
        prefix = (f"# {stamp_date.isoformat()} Session Memory\n\n"
                  "Work, decisions, events, and evidence for every project on this date.\n\n")
    else:
        prefix = "\n" if previous.endswith(b"\n") else "\n\n"
    entry = (f"{prefix}## {stamp_date.isoformat()} {stamp_time} - {title.strip()}\n\n"
             f"**Project:** {project}\n\n{body.strip()}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("ab") as stream:
        stream.write(entry.encode("utf-8"))
    return path


def project_entries(day_text: str, project: str) -> list[str]:
    """The `## ` entries of a dated file whose Project line names the project, in file order."""
    entries = ENTRY_HEADING_RE.split(day_text)[1:]
    return [f"## {entry}" for entry in entries
            if any(match.group("project") == project for match in PROJECT_LINE_RE.finditer(entry))]


def retarget_merged_memory_links(text: str, linking_directory: str) -> str:
    """Point links at former `YYYY-MM-DD-project.md` memory files to the merged `YYYY-MM-DD.md`.

    Only links that resolve into docs/session-memory from the linking file's directory change.
    """
    linking_folder = PurePosixPath(linking_directory)

    def retarget(link: re.Match[str]) -> str:
        folder = link.group("folder")
        if not resolves_to_memory_directory(linking_folder, folder):
            return link.group(0)
        return f"]({folder}{link.group('date')}.md{link.group('anchor') or ''})"

    return PROJECT_MEMORY_LINK_RE.sub(retarget, text)


def resolves_to_memory_directory(linking_folder: PurePosixPath, relative_folder: str) -> bool:
    if "://" in relative_folder:
        return False
    parts = list(linking_folder.parts)
    for part in PurePosixPath(relative_folder).parts if relative_folder else ():
        if part == "..":
            if not parts:
                return False
            parts.pop()
        elif part != ".":
            parts.append(part)
    return PurePosixPath(*parts) == MEMORY_DIRECTORY if parts else False
