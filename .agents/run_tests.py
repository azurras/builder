#!/usr/bin/env python3
"""Run every Builder test file with the standard library and summarize the results.

Builder's test folders are not importable packages, so `python -m unittest discover` cannot
walk them and `pytest` is not a dependency. Each `test_*.py` under `.agents` runs in its own
process, exactly as a developer would run it by hand.

Usage: python .agents/run_tests.py [name-substring ...]
"""
from pathlib import Path
import subprocess
import sys
import time

AGENTS_ROOT = Path(__file__).resolve().parent
PER_FILE_TIMEOUT_SECONDS = 600


def find_test_files(name_filters: list[str]) -> list[Path]:
    test_files = sorted(
        path for path in AGENTS_ROOT.rglob("test_*.py")
        if "__pycache__" not in path.parts
    )
    if not name_filters:
        return test_files
    return [path for path in test_files if any(name in path.name for name in name_filters)]


def run_test_file(test_file: Path) -> tuple[bool, float, str]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [sys.executable, str(test_file)],
            cwd=AGENTS_ROOT.parent,
            capture_output=True,
            text=True,
            timeout=PER_FILE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return False, time.monotonic() - started, f"timed out after {PER_FILE_TIMEOUT_SECONDS} seconds"
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode == 0, time.monotonic() - started, output


def main() -> int:
    test_files = find_test_files(sys.argv[1:])
    if not test_files:
        print("No test files matched.", file=sys.stderr)
        return 2
    failed_files: list[tuple[Path, str]] = []
    for test_file in test_files:
        passed, elapsed_seconds, output = run_test_file(test_file)
        relative_path = test_file.relative_to(AGENTS_ROOT.parent).as_posix()
        print(f"[{'pass' if passed else 'FAIL'}] {relative_path} ({elapsed_seconds:.1f}s)")
        if not passed:
            failed_files.append((test_file, output))
    for test_file, output in failed_files:
        print(f"\n===== {test_file.relative_to(AGENTS_ROOT.parent).as_posix()} =====\n{output}")
    print(f"\n{len(test_files) - len(failed_files)} of {len(test_files)} test files passed.")
    return 1 if failed_files else 0


if __name__ == "__main__":
    raise SystemExit(main())
