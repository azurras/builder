#!/usr/bin/env python3
"""Legacy snapshot command; add --inspect for read-only output."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from spoke_state import main

if __name__ == "__main__":
    raise SystemExit(main())
