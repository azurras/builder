#!/usr/bin/env python3
"""Save a spoke task brief."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys


def slugify(value: str) -> str:
    value = value.lower().encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-{2,}", "-", value).strip("-")[:80] or "spoke-task"


def main() -> int:
    parser = argparse.ArgumentParser(description="Save docs/spoke-tasks/YYYY-MM-DD-title.md.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--title", required=True)
    parser.add_argument("--date")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2
    date = dt.date.fromisoformat(args.date) if args.date else dt.datetime.now().astimezone().date()
    body = sys.stdin.read().strip()
    if not body:
        print("Task brief body is required on stdin", file=sys.stderr)
        return 2
    out_dir = Path(args.root).expanduser().resolve() / "docs" / "spoke-tasks"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{date.isoformat()}-{slugify(title)}.md"
    if out_file.exists() and not args.overwrite:
        print(f"{out_file} already exists; pass --overwrite to replace it", file=sys.stderr)
        return 1
    out_file.write_text(body + "\n", encoding="utf-8")
    print(out_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
