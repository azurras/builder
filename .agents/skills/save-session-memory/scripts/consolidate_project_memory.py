#!/usr/bin/env python3
"""Consolidate the reviewed legacy Builder corpus; dry-run unless --apply is explicit."""
from __future__ import annotations

import argparse
from collections import Counter
import os
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from memory_migration import Destination, heading_ids, source_anchor, source_section, transform

SOURCE_FOLDERS = {"session-memory", "specs", "spoke-reviews", "spoke-tasks",
                  "spoke-updates", "spokes", "work", "work-closures", "templates"}
BUILDER_JULY9 = {
    "add-builder-artifact-quality-gates", "add-test-report-and-story-issue-loop-skills",
    "complete-builder-spoke-machine-setup", "configure-builder-repo-for-this-computer",
    "enforce-artifact-commit-checkpoints", "expand-implementation-plan-required-sections",
    "install-node-js-lts-on-windows", "require-literal-code-edit-blocks-in-implementation-plans",
    "require-runtime-evidence-in-test-reports", "trust-only-azurras-github-comments",
    "update-implementation-plan-skill-template",
}


def project_for(path: str, body: str) -> str:
    name = Path(path).name
    folder = Path(path).parent.name
    if "personal-computer-cleanup" in name:
        return "personal-computer-cleanup"
    if folder in {"docs", "templates"}:
        return "builder"
    if (name.startswith("2026-07-04-") or "jane-street-code-style-skill" in name
        or "builder-skill" in name or "plan-first-builder-workflow" in name
        or name.removeprefix("2026-07-09-").removesuffix(".md") in BUILDER_JULY9):
        return "builder"
    if folder in {"spoke-reviews", "spoke-tasks", "spoke-updates", "spokes", "work", "work-closures"}:
        return "christopherbell-dev"
    if name in {
        "2026-07-16-command-center-cpu-temperature-selection-and-commit.md",
        "2026-07-29-command-center-configuration-and-durable-power-actions.md",
        "2026-07-29-shared-folder-integrity-retention-issues-1290-1297.md",
        "2026-08-03-wfl-archived-session-recovery.md",
        "2026-08-03-wfl-thumbs-voting.md",
    }:
        return "christopherbell-dev"
    if re.search(r"christopherbell[.-]dev|christopherbell\.dev", name + "\n" + body, re.I):
        return "christopherbell-dev"
    raise ValueError(f"Unreviewed project assignment: {path}")


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True, encoding="utf-8")


def prepare(root: Path, commit: str):
    paths = git(root, "ls-tree", "-r", "--name-only", commit, "--", "docs").splitlines()
    originals = {path: git(root, "show", f"{commit}:{path}") for path in paths if path.endswith(".md")}
    sources = {}
    mapping = {}
    generated = set()
    templates = {
        "docs/templates/test-report.md": root / ".agents/skills/record-runtime-verification/references/template.md",
        "docs/templates/examples/test-report-example.md": root / ".agents/skills/record-runtime-verification/references/example.md",
        "docs/templates/examples/implementation-plan-example.md": root / ".agents/skills/plan-builder-work/references/example.md",
    }
    for path, body in originals.items():
        p = Path(path)
        if path == "docs/active.md" or (p.name == "index.md" and p.parent.name in SOURCE_FOLDERS - {"session-memory"}):
            generated.add(path)
            mapping[(root / path).resolve()] = Destination(root / "docs/session-memory/index.md")
        elif path in templates:
            mapping[(root / path).resolve()] = Destination(templates[path])
        elif p.parent.name in SOURCE_FOLDERS and p.name != "index.md" or path in {"docs/status-model.md", "docs/skill-migration.md"}:
            project = project_for(path, body)
            match = re.search(r"\d{4}-\d{2}-\d{2}", p.name)
            day = match.group() if match else git(root, "log", "-1", "--format=%as", commit, "--", path).strip()
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
                raise ValueError(f"No evidenced date for source: {path}")
            session = f"{day}-{project}"
            sources[path] = session
            mapping[(root / path).resolve()] = Destination(root / f"docs/session-memory/{session}.md", source_anchor(path))
    headings = {(root / path).resolve(): set(heading_ids(body).values()) for path, body in originals.items()}
    outputs = {}
    sections = {}
    summaries = {
        "builder": "Workflow hub configuration, development standards, tooling, and delivery history.",
        "christopherbell-dev": "Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.",
        "personal-computer-cleanup": "Personal computer cleanup requirements and planning history. The imported record does not establish that cleanup was executed.",
    }
    for project in sorted(set(sources.values())):
        output = root / f"docs/session-memory/{project}.md"
        selected = sorted((path for path, owner in sources.items() if owner == project),
                          key=lambda path: (re.search(r"\d{4}-\d{2}-\d{2}", path).group() if re.search(r"\d{4}-\d{2}-\d{2}", path) else "0000", path))
        parts = [f"# {project[:10]} - {project[11:]} Session Memory\n\n{summaries[project[11:]]}\n\n"
                 "## Reading and Updating This Record\n\n"
                 "This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. "
                 "Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. "
                 "Plans and runtime reports remain separate evidence documents. "
                 "Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. "
                 "Use the source navigation or search for an issue, date, or topic rather than loading the entire history.\n\n"
                 "## Imported Source Navigation\n\n"]
        parts.extend(f"- [{path}](#{source_anchor(path)})\n" for path in selected)
        parts.append("\n")
        for path in selected:
            destination = mapping[(root / path).resolve()]
            converted = transform(originals[path], root / path, destination, mapping, headings)
            section = source_section(path, originals[path], converted, commit)
            sections[path] = section
            parts.append(section + "\n")
        outputs[output] = "".join(parts)
    for path, body in originals.items():
        if Path(path).parent.name in {"implementation-plans", "test-reports"} and Path(path).name != "index.md":
            outputs[root / path] = transform(body, root / path, Destination(root / path), mapping, headings)
    for template, target in templates.items():
        if template in originals:
            outputs[target] = transform(originals[template], root / template, Destination(target), mapping, headings)
    removals = set(sources) | generated | (set(templates) & set(originals))
    retained = {path for path in originals if Path(path).parent.name in {"implementation-plans", "test-reports"}}
    retained.add("docs/session-memory/index.md")
    unknown = set(originals) - removals - retained
    if unknown:
        raise ValueError(f"Unaccounted source documents: {sorted(unknown)}")
    return originals, sources, sections, outputs, removals


def verify_sections(root: Path, sources, sections, outputs):
    for source, project in sources.items():
        output = root / f"docs/session-memory/{project}.md"
        text = outputs[output]
        if text.count(f"<!-- migrated-source: {source} -->") != 1 or sections[source] not in text:
            raise ValueError(f"Source preservation failed: {source}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--source-commit", required=True, help="Reviewed pre-migration Git revision")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true", help="Verify imported bodies on disk against the original commit")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    commit = git(root, "rev-parse", args.source_commit).strip()
    originals, sources, sections, outputs, removals = prepare(root, commit)
    verify_sections(root, sources, sections, outputs)
    print(f"Source corpus: {len(sources)} documents; projects: {dict(Counter(sources.values()))}")
    if args.verify:
        actual = {path: path.read_text(encoding="utf-8") for path in outputs}
        verify_sections(root, sources, sections, actual)
        print("Every imported source body matches the full migration transformation.")
        return 0
    if not args.apply:
        print(f"Dry run: {len(outputs)} outputs, {len(removals)} source/generated files to remove.")
        return 0
    # Refuse overwriting unrelated changes or already consolidated memories.
    for path in outputs:
        path.resolve().relative_to(root)
        if path.exists():
            relative = path.relative_to(root).as_posix()
            if relative not in originals or path.read_text(encoding="utf-8") != originals[relative]:
                raise ValueError(f"Destination has unrelated changes: {path}")
    for relative in removals:
        source = root / relative
        source.resolve().relative_to(root / "docs")
        if not source.is_file() or source.read_text(encoding="utf-8") != originals[relative]:
            raise ValueError(f"Source changed since reviewed commit: {relative}")
    # All validation precedes writing; all output readback precedes deletion.
    for path, body in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    actual = {path: path.read_text(encoding="utf-8") for path in outputs}
    if actual != outputs:
        raise ValueError("Output readback differs; originals retained")
    verify_sections(root, sources, sections, actual)
    for relative in sorted(removals):
        (root / relative).unlink()
    # Only remove directories proven empty; no recursive data deletion.
    for folder in SOURCE_FOLDERS - {"session-memory"}:
        target = root / "docs" / folder
        target.resolve().relative_to(root / "docs")
        if target.exists():
            for child in sorted(target.rglob("*"), key=lambda path: len(path.parts), reverse=True):
                child.resolve().relative_to(root / "docs")
                if child.is_dir():
                    child.rmdir()
            target.rmdir()
    print("Migration applied with full source coverage and output readback.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
