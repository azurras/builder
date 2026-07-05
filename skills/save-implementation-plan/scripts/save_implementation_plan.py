#!/usr/bin/env python3
"""Save a Markdown implementation plan with a dated slug filename."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Save a Markdown implementation plan to "
            "docs/implementation-plans/YYYY-MM-DD-title.md."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Azurras repository root where docs/implementation-plans should live.",
    )
    parser.add_argument(
        "--plan-dir",
        default="docs/implementation-plans",
        help="Plan directory, relative to --root unless absolute.",
    )
    parser.add_argument(
        "--date",
        help="Plan date in YYYY-MM-DD format. Defaults to today's local date.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Plan title to use for the filename slug.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing plan with the same dated title.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    normalized = value.lower().encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized[:80].strip("-") or "implementation-plan"


def main() -> int:
    args = parse_args()
    now = dt.datetime.now().astimezone()

    if args.date:
        try:
            plan_date = dt.date.fromisoformat(args.date)
        except ValueError:
            print("--date must use YYYY-MM-DD format", file=sys.stderr)
            return 2
    else:
        plan_date = now.date()

    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2

    body = sys.stdin.read().strip()
    if not body:
        print("Plan body is required on stdin", file=sys.stderr)
        return 2

    root = Path(args.root).expanduser().resolve()
    plan_dir = Path(args.plan_dir).expanduser()
    if not plan_dir.is_absolute():
        plan_dir = root / plan_dir
    plan_dir.mkdir(parents=True, exist_ok=True)

    plan_file = plan_dir / f"{plan_date.isoformat()}-{slugify(title)}.md"
    if plan_file.exists() and not args.overwrite:
        print(
            f"{plan_file} already exists; pass --overwrite to replace it",
            file=sys.stderr,
        )
        return 1

    plan_file.write_text(body + "\n", encoding="utf-8")
    print(plan_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
