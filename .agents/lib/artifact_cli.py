"""Compatibility CLI for the six simple dated Markdown record writers."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from artifact_io import parse_optional_date, save_dated_markdown

RECORDS = {
    "hub-work": "work",
    "spoke-task": "spoke-tasks",
    "spoke-update": "spoke-updates",
    "spoke-review": "spoke-reviews",
    "work-closure": "work-closures",
    "decision": "decisions",
}


def main(kind: str, argv: list[str] | None = None) -> int:
    directory = RECORDS[kind]
    parser = argparse.ArgumentParser(description=f"Save docs/{directory}/YYYY-MM-DD-title.md.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--title", required=True)
    parser.add_argument("--date")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        output = save_dated_markdown(
            root=Path(args.root), directory=f"docs/{directory}", title=args.title,
            body=sys.stdin.read(), fallback_slug=kind,
            artifact_date=parse_optional_date(args.date), overwrite=args.overwrite,
            preserve_truncated_hyphen=kind != "hub-work",
        )
    except FileExistsError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(output)
    return 0
