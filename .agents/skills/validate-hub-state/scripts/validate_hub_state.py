#!/usr/bin/env python3
"""Validate Builder hub state conventions."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

LIB = Path(__file__).resolve().parents[3] / "lib"
sys.path.insert(0, str(LIB))

from artifact_quality import validate_implementation_plan_text, validate_test_report_text
from builder_hub import STATUS_VALUES, extract_status, list_markdown, markdown_links, parse_dated_file, read_text


ARTIFACT_DIRS = (
    "docs/session-memory",
    "docs/specs",
    "docs/implementation-plans",
    "docs/test-reports",
    "docs/spokes",
    "docs/work",
    "docs/spoke-tasks",
    "docs/spoke-updates",
    "docs/spoke-reviews",
    "docs/decisions",
    "docs/work-closures",
)

INDEX_FILES = (
    "docs/active.md",
    "docs/work/index.md",
    "docs/spokes/index.md",
    "docs/decisions/index.md",
    "docs/specs/index.md",
    "docs/implementation-plans/index.md",
    "docs/test-reports/index.md",
    "docs/spoke-tasks/index.md",
    "docs/spoke-updates/index.md",
    "docs/spoke-reviews/index.md",
    "docs/work-closures/index.md",
    "docs/session-memory/index.md",
)

TEMPLATE_FILES = (
    "docs/templates/work-record.md",
    "docs/templates/spoke-task.md",
    "docs/templates/spoke-update.md",
    "docs/templates/spoke-review.md",
    "docs/templates/decision-record.md",
    "docs/templates/work-closure.md",
    "docs/templates/test-report.md",
)

SPECIAL_DOC_NAMES = {"index.md", "state.md", "repos.md", "active.md", "status-model.md"}


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

    for directory in ARTIFACT_DIRS:
        if not (root / directory).exists():
            warnings.append(f"Missing artifact directory: {directory}")

    for template in TEMPLATE_FILES:
        if not (root / template).exists():
            errors.append(f"Missing template: {template}")

    for index in INDEX_FILES:
        if not (root / index).exists():
            errors.append(f"Missing index: {index}")

    for directory in ARTIFACT_DIRS:
        for path in list_markdown(root, directory):
            if path.name in SPECIAL_DOC_NAMES:
                continue
            if not parse_dated_file(path):
                errors.append(f"{path}: filename must use YYYY-MM-DD-title.md")
            validate_links(path, root, errors)

    for path in list_markdown(root, "docs/work"):
        if path.name == "index.md":
            continue
        status = extract_status(read_text(path))
        if status and status not in STATUS_VALUES:
            errors.append(f"{path}: invalid status {status!r}")
        if not status:
            warnings.append(f"{path}: missing explicit status")

    for path in list_markdown(root, "docs/implementation-plans"):
        if path.name == "index.md":
            continue
        content = read_text(path)
        if "#### Code Edit" in content:
            errors.extend(validate_implementation_plan_text(content, path))
        else:
            warnings.append(f"{path}: legacy implementation plan missing quality-gated Code Edit blocks")

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
