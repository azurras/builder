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

from artifact_quality import project_of, validate_implementation_plan_text, validate_test_report_text
from project_memory import PROJECT_LINE_RE
from builder_hub import list_markdown, markdown_links, parse_dated_file, read_text
from spoke_registry import REGISTRY_FILE, ProjectStatus, project_statuses_of


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


def validate_claude_skills_link(root: Path, errors: list[str]) -> None:
    """Claude Code reads .claude/skills; it must be a link to the one canonical .agents/skills folder."""
    canonical = root / ".agents" / "skills"
    claude_skills = root / ".claude" / "skills"
    if not canonical.is_dir():
        return
    if not claude_skills.is_symlink() or claude_skills.resolve() != canonical.resolve():
        errors.append(
            f"{claude_skills}: must be a symlink to ../.agents/skills so Claude Code and Codex share one skills folder. "
            "On Windows, enable Developer Mode, run `git config --global core.symlinks true`, then "
            "`git checkout -- .claude/skills` (or re-clone)."
        )


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


def validate_memory_day(path: Path, project_statuses: dict[str, ProjectStatus] | None, errors: list[str]) -> None:
    """A memory file is named for its date alone, and every entry's Project line names a registered project."""
    if not is_iso_date(path.stem):
        errors.append(f"{path}: memory filename must use YYYY-MM-DD.md")
        return
    if project_statuses is None:
        return
    for project in sorted({match.group("project") for match in PROJECT_LINE_RE.finditer(read_text(path))}):
        if project not in project_statuses:
            errors.append(f"{path}: memory project {project!r} is not builder, "
                          f"a registered spoke or a project in {REGISTRY_FILE}")


def is_iso_date(text: str) -> bool:
    try:
        return dt.date.fromisoformat(text).isoformat() == text
    except ValueError:
        return False


def validate_record_project(path: Path, project: str | None, project_statuses: dict[str, ProjectStatus],
                            errors: list[str]) -> None:
    """A labeled plan or report names a registered project, and its filename carries that project."""
    if project is None:
        return
    if project not in project_statuses:
        errors.append(f"{path}: Project {project!r} is not builder, a registered spoke or a project in {REGISTRY_FILE}")
    filename_title = path.stem[len("YYYY-MM-DD-"):]
    if filename_title != project and not filename_title.startswith(f"{project}-"):
        errors.append(f"{path}: filename must start with YYYY-MM-DD-{project}- to match its Project section")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Builder hub state.")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        project_statuses = project_statuses_of(root)
    except ValueError as error:
        errors.append(f"Project registry: {error}")
        project_statuses = None

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
                validate_memory_day(path, project_statuses, errors)
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
        if project_statuses is not None:
            validate_record_project(path, project_of(content), project_statuses, errors)

    for path in list_markdown(root, "docs/test-reports"):
        if path.name == "index.md":
            continue
        content = read_text(path)
        errors.extend(validate_test_report_text(content, path))
        if project_statuses is not None:
            validate_record_project(path, project_of(content), project_statuses, errors)

    validate_skill_frontmatter(root, errors)
    validate_claude_skills_link(root, errors)

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
