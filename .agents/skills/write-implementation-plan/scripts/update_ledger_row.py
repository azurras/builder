#!/usr/bin/env python3
"""Replace text in one row of an umbrella plan's ledger table.

An umbrella plan tracks its child plans in a Markdown table whose first cell identifies each row.
This helper finds the one table row whose first cell equals --row and replaces the single
occurrence of --replace in it with --with, for example to turn
"in progress: [plan](child.md)" into "done: [plan](child.md), PR #12 `abc1234`".
Every other byte, including line endings, is kept. The plan is validated before writing and left
unchanged when the row or text is missing or ambiguous or validation fails.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

LIB = Path(__file__).resolve().parents[3] / "lib"
sys.path.insert(0, str(LIB))

from artifact_quality import validate_implementation_plan_text  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plan", required=True, help="Umbrella implementation plan Markdown file.")
    parser.add_argument("--row", required=True, help="Exact first-cell value of the ledger row, such as 19.")
    parser.add_argument("--replace", required=True, help="Text that occurs exactly once in that row.")
    parser.add_argument("--with", dest="replacement", required=True, help="Replacement text.")
    return parser.parse_args()


def first_cell_of(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return stripped[1:].split("|", 1)[0].strip()


def replace_in_ledger_row(plan_text: str, row: str, old_text: str, new_text: str) -> str:
    """plan_text with old_text replaced in the one table row whose first cell is row."""
    lines = plan_text.splitlines(keepends=True)
    row_indexes = [index for index, line in enumerate(lines) if first_cell_of(line) == row]
    if len(row_indexes) != 1:
        raise ValueError(f"expected one ledger row {row!r}, found {len(row_indexes)}")
    row_line = lines[row_indexes[0]]
    occurrences = row_line.count(old_text)
    if occurrences != 1:
        raise ValueError(f"ledger row {row!r} contains the text to replace {occurrences} times, not once")
    if "\n" in new_text or "\r" in new_text:
        raise ValueError("the replacement must stay on one line")
    lines[row_indexes[0]] = row_line.replace(old_text, new_text)
    return "".join(lines)


def main() -> int:
    args = parse_args()
    plan_file = Path(args.plan)
    if not plan_file.is_file():
        print(f"{plan_file} does not exist", file=sys.stderr)
        return 1
    # Read and write without newline translation so untouched bytes stay identical.
    with plan_file.open(encoding="utf-8", newline="") as plan_stream:
        original_plan = plan_stream.read()
    try:
        updated_plan = replace_in_ledger_row(original_plan, args.row, args.replace, args.replacement)
    except ValueError as error:
        print(f"{plan_file}: {error}; plan left unchanged", file=sys.stderr)
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
