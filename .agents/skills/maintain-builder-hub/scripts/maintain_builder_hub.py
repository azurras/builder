#!/usr/bin/env python3
"""Check hub artifacts by default; refresh only on explicit request."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

SKILLS = Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("check", "refresh"), default="check")
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    commands = [
        [sys.executable, "-B", str(SKILLS / "update-hub-indexes/scripts/update_hub_indexes.py"), "--root", args.root],
        [sys.executable, "-B", str(SKILLS / "validate-hub-state/scripts/validate_hub_state.py"), "--root", args.root],
    ]
    if args.mode == "check":
        commands[0].append("--check")
    failed = False
    for command in commands:
        result = subprocess.run(command, check=False)
        failed = failed or result.returncode != 0
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
