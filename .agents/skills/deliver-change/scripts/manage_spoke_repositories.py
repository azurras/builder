#!/usr/bin/env python3
"""List, register, locate, clone or inspect spoke repositories; optionally snapshot to project memory."""
import argparse
import datetime as dt
import hashlib
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from project_memory import append_entry, project_path
from spoke_registry import Spoke, find_spoke, load_spokes, register_spoke, resolve_spoke_location
from spoke_state import inspect_repository, origin_mismatch


def list_spokes(builder_root: Path) -> int:
    for spoke in load_spokes(builder_root):
        location = resolve_spoke_location(builder_root, spoke)
        state = "present" if location.path.is_dir() else "missing"
        print(f"{spoke.slug}\t{spoke.name}\t{spoke.repository}\t{location.path} ({location.source}, {state})")
    return 0


def locate_spoke(builder_root: Path, spoke: Spoke) -> int:
    location = resolve_spoke_location(builder_root, spoke)
    print(f"- Spoke: `{spoke.slug}` ({spoke.name})\n- Repository: `{spoke.repository}`\n"
          f"- Default branch: `{spoke.default_branch}`\n- Path: `{location.path}` (from {location.source})")
    if not location.path.is_dir():
        print("- State: missing; run clone to create it")
        return 1
    mismatch = origin_mismatch(spoke, location.path)
    print(f"- Origin: {mismatch or 'matches registry'}")
    return 1 if mismatch else 0


def clone_spoke(builder_root: Path, spoke: Spoke) -> int:
    location = resolve_spoke_location(builder_root, spoke)
    if location.path.exists():
        print(f"Refusing to clone into existing path: {location.path}", file=sys.stderr)
        return 1
    location.path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(["git", "clone", "--branch", spoke.default_branch, spoke.repository, str(location.path)],
                            check=False)
    if result.returncode == 0:
        print(location.path)
    return result.returncode


def register_new_spoke(builder_root: Path, arguments: argparse.Namespace) -> int:
    new_spoke = register_spoke(builder_root, slug=arguments.spoke, name=arguments.name,
                               repository=arguments.repository, default_branch=arguments.default_branch,
                               description=arguments.description)
    location = resolve_spoke_location(builder_root, new_spoke)
    print(f"Registered `{new_spoke.slug}` ({new_spoke.name}) from {new_spoke.repository} in spokes.json.\n"
          f"Clone it to {location.path} with: clone --spoke {new_spoke.slug}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("inspect", "snapshot", "list", "register", "locate", "clone"), default="inspect")
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--spoke", help="Registered spoke slug from spokes.json; for register, the new slug")
    target.add_argument("--path", help="Verified repository path when the repository is not a registered spoke")
    parser.add_argument("--root", default=".", help="Builder root containing spokes.json")
    parser.add_argument("--project", help="Memory project slug for snapshot; defaults to the spoke slug")
    parser.add_argument("--name", help="register: display name, usually the repository name")
    parser.add_argument("--repository", help="register: https, ssh or user@host:path remote")
    parser.add_argument("--description", help="register: one sentence; say which instructions own build and run")
    parser.add_argument("--default-branch", default="main", help="register: default branch (default: main)")
    args = parser.parse_args()
    builder_root = Path(args.root).expanduser().resolve()
    try:
        if args.mode == "list":
            return list_spokes(builder_root)
        if args.mode == "register":
            missing = [option for option, value in (("--spoke", args.spoke), ("--name", args.name),
                                                    ("--repository", args.repository),
                                                    ("--description", args.description)) if not value]
            if missing or args.path:
                parser.error("register requires --spoke, --name, --repository and --description, and not --path")
            return register_new_spoke(builder_root, args)
        spoke = find_spoke(builder_root, args.spoke) if args.spoke else None
        if args.mode in {"locate", "clone"}:
            if spoke is None:
                parser.error(f"{args.mode} requires --spoke")
            return locate_spoke(builder_root, spoke) if args.mode == "locate" else clone_spoke(builder_root, spoke)
        if spoke is None and not args.path:
            parser.error(f"{args.mode} requires --spoke or --path")
        checkout = resolve_spoke_location(builder_root, spoke).path if spoke else Path(args.path)
        project = args.project or (spoke.slug if spoke else "")
        day = dt.date.today().isoformat()
        memory_path = project_path(builder_root, project, day) if args.mode == "snapshot" else None
        content, failed = inspect_repository(checkout)
        if spoke and not failed:
            mismatch = origin_mismatch(spoke, checkout)
            if mismatch:
                content += f"- Registry mismatch: {mismatch}\n"
                failed = True
        print(content, end="")
        if memory_path:
            digest = hashlib.sha256(content.encode()).hexdigest()
            previous = memory_path.read_text(encoding="utf-8") if memory_path.exists() else ""
            snapshots = re.findall(r"<!-- git-snapshot: ([a-f0-9]+) -->", previous)
            if not snapshots or snapshots[-1] != digest:
                append_entry(builder_root, project, "Repository inspection",
                             f"<!-- git-snapshot: {digest} -->\n" + content, date=day)
            print(memory_path)
        return 1 if failed else 0
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
