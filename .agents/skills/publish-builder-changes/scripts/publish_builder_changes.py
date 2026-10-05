#!/usr/bin/env python3
"""Commit and push changes to main for only the local builder repository."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


EXPECTED_REMOTE = "https://github.com/azurras/builder.git"
EXPECTED_BRANCH = "main"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish selected Builder changes to origin main."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Must be the top level of the primary Builder checkout, not a linked worktree.",
    )
    parser.add_argument(
        "--message",
        help="Commit message, required when selecting files.",
    )
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--path", action="append", dest="paths", help="Exact repository-relative file to commit; repeat for each file.")
    operation.add_argument("--push-only", action="store_true", help="Push existing main commits without staging or committing files.")
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


def is_in_index(root: Path, path: str) -> bool:
    listed = run_git(root, ["--literal-pathspecs", "ls-files", "-z", "--error-unmatch", "--", path], check=False)
    return listed.returncode == 0 and listed.stdout.split("\0") == [path, ""]


def is_in_head(root: Path, path: str) -> bool:
    """A file in HEAD but not the index is a deletion already staged, such as the old side of git mv. -r keeps a folder from matching."""
    listed = run_git(root, ["--literal-pathspecs", "ls-tree", "-r", "-z", "--name-only", "HEAD", "--", path], check=False)
    return listed.returncode == 0 and listed.stdout.split("\0") == [path, ""]


def paths_needing_staging(root: Path, paths: list[str]) -> list[str]:
    """git add fails on a path whose deletion is already staged, so leave those out."""
    return [path for path in paths if (root / path).is_file() or is_in_index(root, path)]


def selected_paths(root: Path, paths: list[str]) -> list[str]:
    selected: list[str] = []
    for value in paths:
        path = Path(value)
        if path.is_absolute() or path.drive or ".." in path.parts:
            raise ValueError(f"Select an exact repository-relative file: {value!r}")
        candidate = root / path
        if not candidate.resolve().is_relative_to(root):
            raise ValueError(f"Selected path escapes the repository: {value!r}")
        if candidate.is_dir() or candidate.is_symlink() or any(part.lower() in {".git", ".ds_store"} for part in path.parts):
            raise ValueError(f"Directories, symlinks, Git internals, and machine metadata cannot be selected: {value!r}")
        normalized = path.as_posix()
        if not candidate.is_file() and not is_in_index(root, normalized) and not is_in_head(root, normalized):
            raise ValueError(f"Selected file does not exist and is not a tracked deletion: {value!r}")
        if normalized not in selected:
            selected.append(normalized)
    return selected


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    message = (args.message or "").strip()

    if not args.push_only and not message:
        return fail("--message must not be blank")
    if args.push_only and args.message is not None:
        return fail("--push-only does not accept a commit message")

    try:
        top_level = Path(run_git(root, ["rev-parse", "--show-toplevel"]).stdout.strip()).resolve()
        branch = run_git(root, ["branch", "--show-current"]).stdout.strip()
        remote = run_git(root, ["remote", "get-url", "origin"]).stdout.strip()
        git_dir = Path(run_git(root, ["rev-parse", "--absolute-git-dir"]).stdout.strip()).resolve()
        common_dir = Path(root, run_git(root, ["rev-parse", "--git-common-dir"]).stdout.strip()).resolve()
    except subprocess.CalledProcessError as exc:
        return fail(exc.stderr.strip() or "Git validation failed")

    if top_level != root:
        return fail(f"Refusing a path that is not the repository top level: {root} (top level is {top_level})")
    if git_dir != common_dir:
        return fail(f"Refusing to operate in a linked worktree: {root}")
    if branch != EXPECTED_BRANCH:
        return fail(f"Refusing to commit on branch {branch!r}; expected {EXPECTED_BRANCH!r}")
    if remote != EXPECTED_REMOTE:
        return fail(f"Refusing unexpected origin remote: {remote}")

    try:
        print("Repository:", root)
        print("Branch:", branch)
        print("Remote:", remote)
        print("Status:")
        print(run_git(root, ["status", "--short", "--branch"]).stdout.strip())
        if not args.push_only:
            paths = selected_paths(root, args.paths)
            staged = set(filter(None, run_git(root, ["diff", "--cached", "--name-only", "--no-renames", "-z"]).stdout.split("\0")))
            unrelated = staged - set(paths)
            if unrelated:
                return fail(f"Unrelated files are already staged; leave them intact and resolve the selection first: {sorted(unrelated)!r}")
            print("Selected files:", paths)
            print("Commit message:", message)
        else:
            print("Push-only: existing main commits will be pushed; the index and working files are unchanged.")

        if args.dry_run:
            print("Dry run complete; no changes staged, committed, or pushed.")
            return 0

        if not args.push_only:
            paths_to_stage = paths_needing_staging(root, paths)
            if paths_to_stage:
                run_git(root, ["--literal-pathspecs", "add", "--", *paths_to_stage])
            staged = set(filter(None, run_git(root, ["diff", "--cached", "--name-only", "--no-renames", "-z"]).stdout.split("\0")))
            if staged - set(paths):
                return fail("The index changed outside the selected files; refusing to commit. Inspect the index before retrying.")
            if not staged:
                print("No selected changes to commit. To publish existing commits, inspect them and use --push-only.")
                return 0
            commit = run_git(root, ["commit", "-m", message])
            print(commit.stdout.strip())

        commit_hash = run_git(root, ["rev-parse", "--short", "HEAD"]).stdout.strip()
        print(f"Pushing existing commit {commit_hash}; a failed push can be retried with --push-only.")
        push = run_git(root, ["push", "origin", EXPECTED_BRANCH])
        if push.stdout.strip():
            print(push.stdout.strip())
        if push.stderr.strip():
            print(push.stderr.strip())
        print(f"Pushed {commit_hash} to origin {EXPECTED_BRANCH}.")
        return 0
    except ValueError as exc:
        return fail(str(exc))
    except subprocess.CalledProcessError as exc:
        if exc.stdout.strip():
            print(exc.stdout.strip())
        return fail(exc.stderr.strip() or "Git commit/push failed")


if __name__ == "__main__":
    raise SystemExit(main())
