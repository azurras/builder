"""Read registered repositories without changing their Git state."""
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import subprocess
import sys


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}, timeout=30, check=False,
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(args)} failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout.strip()


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



def render_state(registry: Path) -> tuple[str, bool]:
    if not registry.is_file():
        raise ValueError(f"Spoke registry is missing: {registry}")
    entries = parse_registry(registry)
    # An empty registry is legitimate; malformed blocks must not hide registered work.
    marker_count = registry.read_text(encoding="utf-8").count("<!-- spoke:")
    if len(entries) != marker_count:
        raise ValueError(f"Malformed spoke registry: {registry}")
    lines = ["# Spoke Repository State", ""]
    failed = False
    if not entries:
        lines.extend(["No spoke repositories are registered.", ""])
    for entry in entries:
        repo = Path(entry["path"]).expanduser()
        lines.extend([f"## {entry['name']}", "", f"- Path: `{repo}`",
                      f"- Registered remote: `{entry['remote'] or 'unknown'}`"])
        try:
            top = Path(git(repo, "rev-parse", "--show-toplevel")).resolve()
            if top != repo.resolve():
                raise ValueError("Registered path is not the repository root")
            branch = git(repo, "branch", "--show-current") or "detached"
            head = git(repo, "rev-parse", "--short", "HEAD")
            remotes = git(repo, "remote").splitlines()
            remote = git(repo, "remote", "get-url", "origin") if "origin" in remotes else "not configured"
            status = git(repo, "status", "--short") or "clean"
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            failed = True
            lines.extend([f"- State: error: {str(exc).replace(chr(10), ' ')}", ""])
            continue
        lines.extend([f"- Branch: `{branch}`", f"- HEAD: `{head}`",
                      f"- Origin: `{remote}`", "- Status:", "```text", status, "```", ""])
    return "\n".join(lines).rstrip() + "\n", failed


def semantic_content(content: str) -> str:
    return re.sub(r"^Snapshot:.*\n\n?", "", content, count=1, flags=re.MULTILINE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Snapshot registered Git state; --inspect prints without writing.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    try:
        content, failed = render_state(root / "docs/spokes/repos.md")
        if args.inspect:
            print(content, end="")
        else:
            state = root / "docs/spokes/state.md"
            old = state.read_text(encoding="utf-8") if state.exists() else ""
            if semantic_content(old) != content:
                now = dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
                state.write_text(content.replace("\n\n", f"\n\nSnapshot: {now}\n\n", 1), encoding="utf-8")
            print(state)
        return 1 if failed else 0
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
