#!/usr/bin/env python3
"""Validate Builder implementation plan quality."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

LIB = Path(__file__).resolve().parents[3] / "lib"
sys.path.insert(0, str(LIB))

from artifact_quality import validate_implementation_plan_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate implementation plan Markdown.")
    parser.add_argument("files", nargs="*", help="Plan files. Reads stdin when omitted.")
    args = parser.parse_args()

    errors: list[str] = []
    if args.files:
        for name in args.files:
            path = Path(name)
            errors.extend(validate_implementation_plan_text(path.read_text(encoding="utf-8"), path))
    else:
        errors.extend(validate_implementation_plan_text(sys.stdin.read()))

    if errors:
        print("Implementation plan quality checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Implementation plan quality checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
