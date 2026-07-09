#!/usr/bin/env python3
"""Save a Markdown project spec under docs/specs with a dated slug filename."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Save a Markdown spec to docs/specs/YYYY-MM-DD-title.md."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Builder repository root where docs/specs should live.",
    )
    parser.add_argument(
        "--spec-dir",
        default="docs/specs",
        help="Spec directory, relative to --root unless absolute.",
    )
    parser.add_argument(
        "--date",
        help="Spec date in YYYY-MM-DD format. Defaults to today's local date.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Spec title to use for the filename slug.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing spec with the same dated title.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    normalized = value.lower().encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized[:80].strip("-") or "spec"


def main() -> int:
    args = parse_args()
    now = dt.datetime.now().astimezone()

    if args.date:
        try:
            spec_date = dt.date.fromisoformat(args.date)
        except ValueError:
            print("--date must use YYYY-MM-DD format", file=sys.stderr)
            return 2
    else:
        spec_date = now.date()

    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2

    body = sys.stdin.read().strip()
    if not body:
        print("Spec body is required on stdin", file=sys.stderr)
        return 2

    root = Path(args.root).expanduser().resolve()
    spec_dir = Path(args.spec_dir).expanduser()
    if not spec_dir.is_absolute():
        spec_dir = root / spec_dir
    spec_dir.mkdir(parents=True, exist_ok=True)

    spec_file = spec_dir / f"{spec_date.isoformat()}-{slugify(title)}.md"
    if spec_file.exists() and not args.overwrite:
        print(
            f"{spec_file} already exists; pass --overwrite to replace it",
            file=sys.stderr,
        )
        return 1

    spec_file.write_text(body + "\n", encoding="utf-8")
    print(spec_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
