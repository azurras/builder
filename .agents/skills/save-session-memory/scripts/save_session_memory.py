#!/usr/bin/env python3
"""Append a dated entry to one stable project memory file."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from project_memory import append_entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--project", required=True, help="Stable project slug, e.g. builder or christopherbell-dev")
    parser.add_argument("--title", required=True, help="Entry title; does not determine filename")
    parser.add_argument("--date")
    parser.add_argument("--time")
    args = parser.parse_args()
    try:
        print(append_entry(Path(args.root), args.project, args.title, sys.stdin.read(), args.date, args.time))
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
