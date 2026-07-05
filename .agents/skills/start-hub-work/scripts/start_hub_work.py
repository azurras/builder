#!/usr/bin/env python3
"""Save a central hub work record."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys


def slugify(value: str) -> str:
    normalized = value.lower().encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized[:80].strip("-") or "hub-work"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Save docs/work/YYYY-MM-DD-title.md.")
    parser.add_argument("--root", default=".", help="Azurras hub root.")
    parser.add_argument("--title", required=True, help="Work title.")
    parser.add_argument("--date", help="Date in YYYY-MM-DD format.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing work record.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2
    date = dt.date.fromisoformat(args.date) if args.date else dt.datetime.now().astimezone().date()
    body = sys.stdin.read().strip()
    if not body:
        print("Work record body is required on stdin", file=sys.stderr)
        return 2
    root = Path(args.root).expanduser().resolve()
    out_dir = root / "docs" / "work"
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
