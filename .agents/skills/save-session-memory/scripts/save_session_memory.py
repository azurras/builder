#!/usr/bin/env python3
"""Append a project-tagged entry to the one session record for its date."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from builder_hub import BODY_FILE_HELP, read_body_text
from project_memory import append_entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--project", required=True, help="Project slug the entry is tagged with, e.g. builder or christopherbell-dev")
    parser.add_argument("--title", required=True, help="Entry title; the file is named for the date alone")
    parser.add_argument("--date")
    parser.add_argument("--time")
    parser.add_argument("--body-file", help=BODY_FILE_HELP)
    args = parser.parse_args()
    try:
        print(append_entry(Path(args.root), args.project, args.title, read_body_text(args.body_file), args.date, args.time))
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
