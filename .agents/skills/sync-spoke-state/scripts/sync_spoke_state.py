#!/usr/bin/env python3
"""Snapshot registered spoke repository Git state."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import subprocess


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    ).stdout.strip()


def parse_registry(registry: Path) -> list[dict[str, str]]:
    if not registry.exists():
        return []
    content = registry.read_text(encoding="utf-8")
    entries = []
    for block in re.findall(r"<!-- spoke:[^>]+ -->(.*?)<!-- /spoke:[^>]+ -->", content, re.DOTALL):
        name_match = re.search(r"^##\s+(.+)$", block, re.MULTILINE)
        path_match = re.search(r"- Local path: `([^`]+)`", block)
        remote_match = re.search(r"- Remote: `([^`]+)`", block)
        branch_match = re.search(r"- Default branch: `([^`]+)`", block)
        if name_match and path_match:
            entries.append(
                {
                    "name": name_match.group(1).strip(),
                    "path": path_match.group(1).strip(),
                    "remote": remote_match.group(1).strip() if remote_match else "",
                    "default_branch": branch_match.group(1).strip() if branch_match else "",
                }
            )
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Write docs/spokes/state.md from registered spoke repos.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    registry = root / "docs" / "spokes" / "repos.md"
    state_file = root / "docs" / "spokes" / "state.md"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")

    lines = [f"# Spoke Repository State", "", f"Snapshot: {now}", ""]
    entries = parse_registry(registry)
    if not entries:
        lines.extend(["No spoke repositories are registered.", ""])
    for entry in entries:
        repo = Path(entry["path"]).expanduser()
        lines.extend([f"## {entry['name']}", "", f"- Path: `{repo}`", f"- Registered remote: `{entry['remote'] or 'unknown'}`"])
        if not repo.exists():
            lines.extend(["- State: path missing", ""])
            continue
        if not (repo / ".git").exists():
            lines.extend(["- State: not a Git repository", ""])
            continue
        branch = git(repo, "branch", "--show-current") or "detached"
        head = git(repo, "rev-parse", "--short", "HEAD") or "unknown"
        remote = git(repo, "remote", "get-url", "origin") or "unknown"
        status = git(repo, "status", "--short") or "clean"
        lines.extend(
            [
                f"- Branch: `{branch}`",
                f"- HEAD: `{head}`",
                f"- Origin: `{remote}`",
                "- Status:",
                "```text",
                status,
                "```",
                "",
            ]
        )
    state_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(state_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
