#!/usr/bin/env python3
"""Compatibility entrypoint for saving a spoke-review record."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from artifact_cli import main

if __name__ == "__main__":
    raise SystemExit(main("spoke-review"))
