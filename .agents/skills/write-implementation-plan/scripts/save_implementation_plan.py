#!/usr/bin/env python3
"""Save a Markdown implementation plan with a dated slug filename."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

LIB = Path(__file__).resolve().parents[3] / "lib"
sys.path.insert(0, str(LIB))

from artifact_io import (dated_markdown_file, parse_optional_date, parse_optional_time, project_prefixed_title,
                         save_dated_markdown)
from artifact_quality import CURRENT_PLAN_FORMAT, plan_format_of, project_of, validate_implementation_plan_text
from builder_hub import BODY_FILE_HELP, read_body_text
from spoke_registry import require_active_project


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Save a Markdown implementation plan to "
            "docs/implementation-plans/YYYY-MM-DD-HH-MM-project-title.md. The project "
            "comes from the plan's Project section."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Builder repository root where docs/implementation-plans should live.",
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
        "--time",
        help="Plan time in HH:MM format for the filename. Defaults to the current local time.",
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Plan title to use for the filename slug.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing plan with the same date and title, whatever its time.",
    )
    parser.add_argument("--body-file", help=BODY_FILE_HELP)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        plan_date = parse_optional_date(args.date)
    except ValueError:
        print("--date must use YYYY-MM-DD format", file=sys.stderr)
        return 2
    try:
        plan_time = parse_optional_time(args.time)
    except ValueError:
        print("--time must use HH:MM format", file=sys.stderr)
        return 2

    title = args.title.strip()
    if not title:
        print("--title must not be blank", file=sys.stderr)
        return 2

    body = read_body_text(args.body_file).strip()
    if not body:
        print("Plan body is required on stdin or in --body-file", file=sys.stderr)
        return 2

    errors = validate_implementation_plan_text(body)
    if errors:
        print("Implementation plan quality checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    builder_root = Path(args.root).expanduser().resolve()
    project = project_of(body)
    filename_title = title if project is None else project_prefixed_title(project, title)
    # Existing plans may be replaced in their own format and without a Project
    # section; new plans use the current format and name their project.
    try:
        plan_file = dated_markdown_file(
            root=builder_root,
            directory=args.plan_dir,
            title=filename_title,
            fallback_slug="implementation-plan",
            artifact_date=plan_date,
            artifact_time=plan_time,
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    is_replacing_existing_plan = args.overwrite and plan_file.exists()
    if plan_format_of(body) != CURRENT_PLAN_FORMAT and not is_replacing_existing_plan:
        print(f"New implementation plans must use Plan Format {CURRENT_PLAN_FORMAT}", file=sys.stderr)
        return 1
    if project is None and not is_replacing_existing_plan:
        print("New implementation plans need a Project section naming builder, a registered spoke "
              "or an active project from spokes.json", file=sys.stderr)
        return 1
    if project is not None:
        try:
            require_active_project(builder_root, project)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1

    try:
        plan_file = save_dated_markdown(
            root=builder_root,
            directory=args.plan_dir,
            title=filename_title,
            body=body,
            fallback_slug="implementation-plan",
            artifact_date=plan_date,
            artifact_time=plan_time,
            overwrite=args.overwrite,
        )
    except FileExistsError as error:
        print(error, file=sys.stderr)
        return 1
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2

    print(plan_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
