#!/usr/bin/env python3
"""Validate Builder hub state conventions."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re
import sys

LIB = Path(__file__).resolve().parents[3] / "lib"
sys.path.insert(0, str(LIB))

from artifact_quality import validate_implementation_plan_text, validate_test_report_text
from project_memory import PROJECT_RE
from builder_hub import list_markdown, markdown_links, parse_dated_file, read_text


# Historical pre-schema plans remain warnings; all other plans must validate.
LEGACY_PLAN_NAMES = frozenset({
    '2026-07-08-complete-christopherbell-dev-issues-1105-1109.md',
    '2026-07-09-issue-1090-production-jwt-secret-fallback.md',
    '2026-07-09-issue-1091-trusted-client-ip-resolution.md',
    '2026-07-09-issue-1092-request-body-size-enforcement.md',
    '2026-07-09-issue-1093-password-reset-token-logging.md',
    '2026-07-09-issue-1094-generic-controller-exception-fallback.md',
    '2026-07-09-issue-1095-endpoint-aware-rate-limits.md',
    '2026-07-09-issue-1096-bean-validation-request-dto.md',
})


ARTIFACT_DIRS = ("docs/session-memory", "docs/implementation-plans", "docs/test-reports")
INDEX_FILES = tuple(f"{directory}/index.md" for directory in ARTIFACT_DIRS)
SPECIAL_DOC_NAMES = {"index.md"}


def validate_skill_frontmatter(root: Path, errors: list[str]) -> None:
    for skill in sorted((root / ".agents" / "skills").glob("*/SKILL.md")):
        content = read_text(skill)
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            errors.append(f"{skill}: missing valid frontmatter")
            continue
        fields: dict[str, str] = {}
        for line in match.group(1).splitlines():
            if ":" not in line:
                errors.append(f"{skill}: invalid frontmatter line {line!r}")
                continue
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        if set(fields) != {"name", "description"}:
            errors.append(f"{skill}: frontmatter must contain only name and description")
        if not re.match(r"^[a-z0-9-]+$", fields.get("name", "")):
            errors.append(f"{skill}: invalid skill name")
        if not fields.get("description"):
            errors.append(f"{skill}: missing description")


def validate_links(path: Path, root: Path, errors: list[str]) -> None:
    for link in markdown_links(read_text(path)):
        if "://" in link or link.startswith("#") or link.startswith("mailto:"):
            continue
        target = (path.parent / link.split("#", 1)[0]).resolve()
        try:
            target.relative_to(root)
        except ValueError:
            continue
        if not target.exists():
            errors.append(f"{path}: broken local link {link}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Builder hub state.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    docs = root / "docs"
    allowed = {Path(directory).name for directory in ARTIFACT_DIRS}
    if docs.exists():
        for entry in docs.iterdir():
            if not entry.is_dir() or entry.name not in allowed:
                errors.append(f"Unexpected docs entry: {entry}")
    for index in INDEX_FILES:
        if not (root / index).is_file():
            errors.append(f"Missing index: {index}")

    for directory in ARTIFACT_DIRS:
        for path in list_markdown(root, directory):
            if path.name in SPECIAL_DOC_NAMES:
                continue
            if directory == "docs/session-memory":
                parsed = parse_dated_file(path)
                try:
                    dt.date.fromisoformat(path.name[:10])
                    valid = parsed and PROJECT_RE.fullmatch(path.stem[11:])
                except ValueError:
                    valid = False
                if not valid:
                    errors.append(f"{path}: memory filename must use YYYY-MM-DD-project.md")
            elif not parse_dated_file(path):
                errors.append(f"{path}: filename must use YYYY-MM-DD-title.md")
            validate_links(path, root, errors)

    for path in list_markdown(root, "docs/implementation-plans"):
        if path.name == "index.md":
            continue
        content = read_text(path)
        if path.name in LEGACY_PLAN_NAMES and "#### Code Edit" not in content and "## Plan Format" not in content:
            warnings.append(f"{path}: historical implementation plan predates the quality schema")
        else:
            errors.extend(validate_implementation_plan_text(content, path))

    for path in list_markdown(root, "docs/test-reports"):
        if path.name == "index.md":
            continue
        errors.extend(validate_test_report_text(read_text(path), path))

    validate_skill_frontmatter(root, errors)

    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Hub state validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
