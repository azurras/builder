#!/usr/bin/env python3
"""Append a completed-request memory entry to a dated Markdown file."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create or append session memory in "
            "docs/session-memory/YYYY-MM-DD-short-description.md."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root where the session-memory directory should live.",
    )
    parser.add_argument(
        "--memory-dir",
        default="docs/session-memory",
        help="Memory directory, relative to --root unless absolute.",
    )
    parser.add_argument(
        "--date",
        help="Entry date in YYYY-MM-DD format. Defaults to today's local date.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Short title for the completed request.",
    )
    parser.add_argument(
        "--file-description",
        help="Short description to use in the filename. Defaults to --title.",
    )
    parser.add_argument(
        "--time",
        help="Entry time in HH:MM format. Defaults to current local time.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    normalized = value.lower().encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized[:80].strip("-") or "session-memory"


def main() -> int:
    args = parse_args()
    now = dt.datetime.now().astimezone()

    if args.date:
        try:
            entry_date = dt.date.fromisoformat(args.date)
        except ValueError:
            print("--date must use YYYY-MM-DD format", file=sys.stderr)
            return 2
    else:
        entry_date = now.date()

    entry_time = args.time or now.strftime("%H:%M")
    body = sys.stdin.read().strip()
    if not body:
        print("Memory body is required on stdin", file=sys.stderr)
        return 2

    root = Path(args.root).expanduser().resolve()
    memory_dir = Path(args.memory_dir).expanduser()
    if not memory_dir.is_absolute():
        memory_dir = root / memory_dir
    memory_dir.mkdir(parents=True, exist_ok=True)

    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2

    file_description = (args.file_description or title).strip()
    if not file_description:
        print("--file-description must not be blank when provided", file=sys.stderr)
        return 2

    file_slug = slugify(file_description)
    memory_file = memory_dir / f"{entry_date.isoformat()}-{file_slug}.md"
    if memory_file.exists():
        existing = memory_file.read_text(encoding="utf-8").rstrip()
        prefix = existing + "\n\n"
    else:
        prefix = f"# {entry_date.isoformat()} - {file_description.strip()}\n\n"

    entry = f"## {entry_time} - {title}\n\n{body}\n"
    memory_file.write_text(prefix + entry, encoding="utf-8")
    print(memory_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
