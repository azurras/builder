#!/usr/bin/env python3
"""Inspect by default; registration and persisted snapshots require explicit modes."""
from pathlib import Path
import subprocess
import sys

SKILLS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILLS.parent / "lib"))
from spoke_state import main as snapshot


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    mode = args.pop(0) if args and args[0] in {"inspect", "snapshot", "register"} else "inspect"
    if mode == "register":
        return subprocess.run([sys.executable, "-B", str(SKILLS / "register-spoke-repo/scripts/register_spoke_repo.py"), *args], check=False).returncode
    return snapshot([*args, "--inspect"] if mode == "inspect" else args)


if __name__ == "__main__":
    raise SystemExit(main())
