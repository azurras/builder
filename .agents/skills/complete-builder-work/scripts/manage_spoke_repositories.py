#!/usr/bin/env python3
"""Inspect a repository or append its snapshot to project memory."""
import argparse
import datetime as dt
import hashlib
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from project_memory import append_entry, project_path
from spoke_state import inspect_repository


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("inspect", "snapshot"), default="inspect")
    parser.add_argument("--path", required=True, help="Verified repository path from project memory or inspection")
    parser.add_argument("--root", default=".")
    parser.add_argument("--project", help="Required for snapshot persistence")
    args = parser.parse_args()
    day = dt.date.today().isoformat()
    try:
        target = project_path(Path(args.root), args.project or "", day) if args.mode == "snapshot" else None
        content, failed = inspect_repository(Path(args.path))
        print(content, end="")
        if target:
            digest = hashlib.sha256(content.encode()).hexdigest()
            previous = target.read_text(encoding="utf-8") if target.exists() else ""
            snapshots = re.findall(r"<!-- git-snapshot: ([a-f0-9]+) -->", previous)
            if not snapshots or snapshots[-1] != digest:
                append_entry(Path(args.root), args.project, "Repository inspection",
                             f"<!-- git-snapshot: {digest} -->\n" + content, date=day)
            print(target)
        return 1 if failed else 0
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
