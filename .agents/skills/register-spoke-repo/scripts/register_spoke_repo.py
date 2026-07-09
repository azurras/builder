#!/usr/bin/env python3
"""Register or update a spoke repository in docs/spokes/repos.md."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register an Builder spoke repository.")
    parser.add_argument("--root", default=".", help="Builder hub root.")
    parser.add_argument("--name", required=True, help="Human-readable repository name.")
    parser.add_argument("--path", required=True, help="Local filesystem path for the spoke repo.")
    parser.add_argument("--remote", required=True, help="Git remote URL for the spoke repo.")
    parser.add_argument("--default-branch", default="main", help="Default branch for the spoke repo.")
    parser.add_argument("--purpose", required=True, help="What the spoke repo owns.")
    parser.add_argument("--status", default="active", help="Current registry status.")
    parser.add_argument("--guardrails", default="", help="Branch, validation, or ownership rules.")
    parser.add_argument("--notes", default="", help="Additional notes.")
    return parser.parse_args()


def slugify(value: str) -> str:
    normalized = value.lower().encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized[:80].strip("-") or "spoke-repo"


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    registry = root / "docs" / "spokes" / "repos.md"
    registry.parent.mkdir(parents=True, exist_ok=True)

    name = args.name.strip()
    slug = slugify(name)
    section = (
        f"<!-- spoke:{slug} -->\n"
        f"## {name}\n\n"
        f"- Slug: `{slug}`\n"
        f"- Local path: `{Path(args.path).expanduser()}`\n"
        f"- Remote: `{args.remote.strip()}`\n"
        f"- Default branch: `{args.default_branch.strip()}`\n"
        f"- Purpose: {args.purpose.strip()}\n"
        f"- Status: {args.status.strip()}\n"
        f"- Guardrails: {args.guardrails.strip() or 'Not specified'}\n"
        f"- Notes: {args.notes.strip() or 'None'}\n"
        f"<!-- /spoke:{slug} -->"
    )

    if registry.exists():
        content = registry.read_text(encoding="utf-8").rstrip()
    else:
        content = "# Spoke Repositories\n\n"

    pattern = re.compile(
        rf"<!-- spoke:{re.escape(slug)} -->.*?<!-- /spoke:{re.escape(slug)} -->",
        re.DOTALL,
    )
    if pattern.search(content):
        content = pattern.sub(section, content)
    else:
        content = content.rstrip() + "\n\n" + section

    registry.write_text(content.rstrip() + "\n", encoding="utf-8")
    print(registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
