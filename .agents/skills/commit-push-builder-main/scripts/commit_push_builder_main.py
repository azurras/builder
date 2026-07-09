#!/usr/bin/env python3
"""Commit and push changes to main for only the local builder repository."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


EXPECTED_ROOTS = (
    "C:/Users/Christopher/Developer/builder",
    "/Users/cbell/Developer/builder",
)
EXPECTED_REMOTE = "https://github.com/azurras/builder.git"
EXPECTED_BRANCH = "main"


def expected_roots_display() -> str:
    return ", ".join(EXPECTED_ROOTS)


def normalize_root(root: Path) -> str:
    return str(root.resolve()).replace("\\", "/")


def is_expected_root(root: Path) -> bool:
    return normalize_root(root) in EXPECTED_ROOTS


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Commit and push the builder repository to origin main."
    )
    parser.add_argument(
        "--root",
        default=".",
        help=f"Repository root. Must resolve to one of: {expected_roots_display()}.",
    )
    parser.add_argument(
        "--message",
        required=True,
        help="Commit message.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and show intended actions without changing Git state.",
    )
    return parser.parse_args()


def run_git(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    message = args.message.strip()

    if not is_expected_root(root):
        return fail(f"Refusing to operate outside configured builder roots ({expected_roots_display()}): {root}")
    if not message:
        return fail("--message must not be blank")

    try:
        top_level = Path(run_git(root, ["rev-parse", "--show-toplevel"]).stdout.strip()).resolve()
        branch = run_git(root, ["branch", "--show-current"]).stdout.strip()
        remote = run_git(root, ["remote", "get-url", "origin"]).stdout.strip()
    except subprocess.CalledProcessError as exc:
        return fail(exc.stderr.strip() or "Git validation failed")

    if not is_expected_root(top_level):
        return fail(f"Refusing unexpected Git root: {top_level}")
    if branch != EXPECTED_BRANCH:
        return fail(f"Refusing to commit on branch {branch!r}; expected {EXPECTED_BRANCH!r}")
    if remote != EXPECTED_REMOTE:
        return fail(f"Refusing unexpected origin remote: {remote}")

    status = run_git(root, ["status", "--short"]).stdout.strip()
    if not status:
        print("No changes to commit.")
        return 0

    print("Repository:", root)
    print("Branch:", branch)
    print("Remote:", remote)
    print("Status:")
    print(status)
    print("Commit message:", message)

    if args.dry_run:
        print("Dry run complete; no changes staged, committed, or pushed.")
        return 0

    try:
        run_git(root, ["add", "--all"])
        run_git(root, ["reset", "--", ".DS_Store", "docs/.DS_Store"], check=False)
        staged = run_git(root, ["diff", "--cached", "--name-only"]).stdout.strip()
        if not staged:
            print("No staged changes to commit after exclusions.")
            return 0

        commit = run_git(root, ["commit", "-m", message])
        print(commit.stdout.strip())

        commit_hash = run_git(root, ["rev-parse", "--short", "HEAD"]).stdout.strip()
        push = run_git(root, ["push", "origin", EXPECTED_BRANCH])
        if push.stdout.strip():
            print(push.stdout.strip())
        if push.stderr.strip():
            print(push.stderr.strip())
        print(f"Pushed {commit_hash} to origin {EXPECTED_BRANCH}.")
        return 0
    except subprocess.CalledProcessError as exc:
        if exc.stdout.strip():
            print(exc.stdout.strip())
        return fail(exc.stderr.strip() or "Git commit/push failed")


if __name__ == "__main__":
    raise SystemExit(main())
