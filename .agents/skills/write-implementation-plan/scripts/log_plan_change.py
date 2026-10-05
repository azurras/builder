#!/usr/bin/env python3
"""Append a dated Implementation Log entry to a plan and optionally move its status."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

LIB = Path(__file__).resolve().parents[3] / "lib"
sys.path.insert(0, str(LIB))

from artifact_io import parse_optional_date
from artifact_quality import PLAN_STATUSES, validate_implementation_plan_text

LOG_HEADING = "## Implementation Log"
SECTION_HEADING_PATTERN = r"(?m)^##[ \t]+\S"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Append a dated entry to a plan's Implementation Log. "
            "The entry body (Change, Reason and Impact lines) is read from stdin."
        )
    )
    parser.add_argument("--plan", required=True, help="Implementation plan Markdown file to update.")
    parser.add_argument("--title", required=True, help="Short title for the log entry.")
    parser.add_argument(
        "--date",
        help="Entry date in YYYY-MM-DD format. Defaults to today's local date.",
    )
    parser.add_argument(
        "--status",
        choices=sorted(PLAN_STATUSES),
        help="Also set the plan's Document Status to this value.",
    )
    return parser.parse_args()


def with_log_entry(plan_text: str, log_entry: str, newline: str) -> str:
    """Return plan_text with log_entry added at the end of the Implementation Log."""
    log_heading = re.search(rf"(?m)^{re.escape(LOG_HEADING)}[ \t]*(?=\r?$)", plan_text)
    if not log_heading:
        new_section = f"{LOG_HEADING}{newline}{newline}{log_entry}{newline}{newline}"
        outcome_heading = re.search(r"(?m)^##[ \t]+Outcome[ \t]*(?=\r?$)", plan_text)
        if outcome_heading:
            return plan_text[:outcome_heading.start()] + new_section + plan_text[outcome_heading.start():]
        return plan_text.rstrip() + newline + newline + new_section

    next_section = re.compile(SECTION_HEADING_PATTERN).search(plan_text, log_heading.end())
    log_end = next_section.start() if next_section else len(plan_text)
    log_body = plan_text[log_heading.end():log_end]
    has_entries = re.search(r"(?m)^###[ \t]+", log_body)
    # A log with no entries holds only a placeholder such as "No entries yet."
    kept_log_body = log_body.rstrip() if has_entries else ""
    updated_log = f"{kept_log_body}{newline}{newline}{log_entry}{newline}"
    if next_section:
        updated_log += newline
    return plan_text[:log_heading.end()] + updated_log + plan_text[log_end:]


def with_document_status(plan_text: str, status: str) -> str:
    status_line = re.search(r"(?m)^##[ \t]+Document Status[ \t]*\r?\n(?:[ \t]*\r?\n)*(?P<value>[^\r\n]*)", plan_text)
    if not status_line:
        raise ValueError("plan has no Document Status section")
    return plan_text[:status_line.start("value")] + status + plan_text[status_line.end("value"):]


def main() -> int:
    args = parse_args()

    try:
        entry_date = parse_optional_date(args.date)
    except ValueError:
        print("--date must use YYYY-MM-DD format", file=sys.stderr)
        return 2

    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2

    entry_body = sys.stdin.read().strip()
    if not entry_body:
        print("Log entry body is required on stdin", file=sys.stderr)
        return 2

    plan_file = Path(args.plan)
    if not plan_file.is_file():
        print(f"{plan_file} does not exist", file=sys.stderr)
        return 1

    # Read and write without newline translation so untouched bytes stay identical.
    with plan_file.open(encoding="utf-8", newline="") as plan_stream:
        original_plan = plan_stream.read()
    newline = "\r\n" if "\r\n" in original_plan else "\n"
    log_entry = f"### {entry_date.isoformat()} - {title}{newline}{newline}" + newline.join(entry_body.splitlines())

    updated_plan = with_log_entry(original_plan, log_entry, newline)
    if args.status:
        try:
            updated_plan = with_document_status(updated_plan, args.status)
        except ValueError as error:
            print(f"{plan_file}: {error}", file=sys.stderr)
            return 1

    errors = validate_implementation_plan_text(updated_plan, plan_file)
    if errors:
        print("Implementation plan quality checks failed; plan left unchanged:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    with plan_file.open("w", encoding="utf-8", newline="") as plan_stream:
        plan_stream.write(updated_plan)
    print(plan_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
