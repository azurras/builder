#!/usr/bin/env python3
"""Run every Builder test file with the standard library and summarize the results.

Builder's test folders are not importable packages, so `python -m unittest discover` cannot
walk them and `pytest` is not a dependency. Each `test_*.py` under `.agents` is loaded by
unittest in its own process, whether or not the file has a `__main__` block, and a file in
which no test ran counts as a failure.

Usage: python .agents/run_tests.py [name-substring ...]
"""
from pathlib import Path
import re
import subprocess
import sys
import time

AGENTS_ROOT = Path(__file__).resolve().parent
PER_FILE_TIMEOUT_SECONDS = 600
# Imports the file as a module from its own folder (so sibling fixtures resolve) and runs its tests.
UNITTEST_BOOTSTRAP = (
    "import sys, unittest; from pathlib import Path; test_file = Path(sys.argv[1]); "
    "sys.path.insert(0, str(test_file.parent)); "
    "unittest.main(module=test_file.stem, argv=[sys.argv[0]], verbosity=1)"
)
TESTS_RAN_RE = re.compile(r"^Ran (?P<count>\d+) tests? in ", re.MULTILINE)


def find_test_files(name_filters: list[str]) -> list[Path]:
    test_files = sorted(
        path for path in AGENTS_ROOT.rglob("test_*.py")
        if "__pycache__" not in path.parts
    )
    if not name_filters:
        return test_files
    return [path for path in test_files if any(name in path.name for name in name_filters)]


def run_test_file(test_file: Path) -> tuple[bool, int, float, str]:
    """Returns whether the file passed, how many tests ran, the elapsed seconds and the combined output."""
    started = time.monotonic()
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-c", UNITTEST_BOOTSTRAP, str(test_file)],
            cwd=AGENTS_ROOT.parent,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=PER_FILE_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return False, 0, time.monotonic() - started, f"timed out after {PER_FILE_TIMEOUT_SECONDS} seconds"
    output = (completed.stdout + completed.stderr).strip()
    ran_match = TESTS_RAN_RE.search(output)
    tests_ran = int(ran_match.group("count")) if ran_match else 0
    return completed.returncode == 0 and tests_ran > 0, tests_ran, time.monotonic() - started, output


def main() -> int:
    test_files = find_test_files(sys.argv[1:])
    if not test_files:
        print("No test files matched.", file=sys.stderr)
        return 2
    failed_files: list[tuple[Path, str]] = []
    total_tests_ran = 0
    for test_file in test_files:
        passed, tests_ran, elapsed_seconds, output = run_test_file(test_file)
        total_tests_ran += tests_ran
        relative_path = test_file.relative_to(AGENTS_ROOT.parent).as_posix()
        print(f"[{'pass' if passed else 'FAIL'}] {relative_path}: {tests_ran} tests ({elapsed_seconds:.1f}s)")
        if not passed:
            failed_files.append((test_file, output or "no output"))
    for test_file, output in failed_files:
        print(f"\n===== {test_file.relative_to(AGENTS_ROOT.parent).as_posix()} =====\n{output}")
    print(f"\n{len(test_files) - len(failed_files)} of {len(test_files)} test files passed; "
          f"{total_tests_ran} tests ran.")
    return 1 if failed_files else 0


if __name__ == "__main__":
    raise SystemExit(main())
