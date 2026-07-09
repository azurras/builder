#!/usr/bin/env python3
"""Save a Markdown test report with a dated slug filename."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Save a Markdown test report to docs/test-reports/YYYY-MM-DD-title.md."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Builder repository root where docs/test-reports should live.",
    )
    parser.add_argument(
        "--report-dir",
        default="docs/test-reports",
        help="Report directory, relative to --root unless absolute.",
    )
    parser.add_argument(
        "--date",
        help="Report date in YYYY-MM-DD format. Defaults to today's local date.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Report title to use for the filename slug.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing report with the same dated title.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    normalized = value.lower().encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized[:80].strip("-") or "test-report"


def main() -> int:
    args = parse_args()
    now = dt.datetime.now().astimezone()

    if args.date:
        try:
            report_date = dt.date.fromisoformat(args.date)
        except ValueError:
            print("--date must use YYYY-MM-DD format", file=sys.stderr)
            return 2
    else:
        report_date = now.date()

    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2

    body = sys.stdin.read().strip()
    if not body:
        print("Report body is required on stdin", file=sys.stderr)
        return 2

    root = Path(args.root).expanduser().resolve()
    report_dir = Path(args.report_dir).expanduser()
    if not report_dir.is_absolute():
        report_dir = root / report_dir
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"{report_date.isoformat()}-{slugify(title)}.md"
    if report_file.exists() and not args.overwrite:
        print(
            f"{report_file} already exists; pass --overwrite to replace it",
            file=sys.stderr,
        )
        return 1

    report_file.write_text(body + "\n", encoding="utf-8")
    print(report_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
