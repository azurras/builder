#!/usr/bin/env python3
"""Save a Markdown test report with a dated slug filename."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

LIB = Path(__file__).resolve().parents[3] / "lib"
sys.path.insert(0, str(LIB))

from artifact_io import parse_optional_date, save_dated_markdown
from artifact_quality import validate_test_report_text


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


def main() -> int:
    args = parse_args()

    try:
        report_date = parse_optional_date(args.date)
    except ValueError:
        print("--date must use YYYY-MM-DD format", file=sys.stderr)
        return 2

    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2

    body = sys.stdin.read().strip()
    if not body:
        print("Report body is required on stdin", file=sys.stderr)
        return 2

    errors = validate_test_report_text(body)
    if errors:
        print("Test report quality checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    try:
        report_file = save_dated_markdown(
            root=Path(args.root),
            directory=args.report_dir,
            title=title,
            body=body,
            fallback_slug="test-report",
            artifact_date=report_date,
            overwrite=args.overwrite,
        )
    except FileExistsError as error:
        print(error, file=sys.stderr)
        return 1
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2

    print(report_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
