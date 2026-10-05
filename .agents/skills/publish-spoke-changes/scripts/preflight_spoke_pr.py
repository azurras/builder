#!/usr/bin/env python3
"""Check that a spoke branch is ready to become a pull request backed by published runtime evidence.

Read-only: it never fetches, writes, pushes or calls GitHub. Fetch the spoke and Builder first so the
origin/<branch> refs it reads are current.
"""
import argparse
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from artifact_quality import markdown_sections, project_of, validate_test_report_text
from spoke_registry import Spoke, find_spoke, normalize_remote, resolve_spoke_location
from spoke_state import git, origin_mismatch

REPORT_FOLDER = PurePosixPath("docs/test-reports")
BUILDER_PUBLISHED_REF = "origin/main"
SHORT_SHA_LENGTH = 7
COMMIT_ID_RE = re.compile(rf"\b[0-9a-f]{{{SHORT_SHA_LENGTH},40}}\b")
GIT_FAILURES = (ValueError, OSError, subprocess.TimeoutExpired)


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str


def check_checkout(spoke: Spoke, checkout: Path) -> Check:
    try:
        top_level = Path(git(checkout, "rev-parse", "--show-toplevel")).resolve()
    except GIT_FAILURES as error:
        return Check("checkout", False, f"{checkout} is not a Git checkout: {error}")
    if top_level != checkout.resolve():
        return Check("checkout", False, f"{checkout} is inside {top_level}; pass the checkout root")
    mismatch = origin_mismatch(spoke, checkout)
    if mismatch:
        return Check("checkout", False, mismatch)
    return Check("checkout", True, f"{checkout} with origin matching {spoke.repository}")


def check_branch(spoke: Spoke, checkout: Path) -> Check:
    branch = git(checkout, "branch", "--show-current")
    if not branch:
        return Check("branch", False, "HEAD is detached; switch to a work branch")
    if branch == spoke.default_branch:
        return Check("branch", False, f"on default branch {branch}; commit the change on a work branch")
    return Check("branch", True, branch)


def check_tracked_changes(checkout: Path) -> Check:
    tracked_changes = git(checkout, "status", "--porcelain", "--untracked-files=no")
    if tracked_changes:
        return Check("committed candidate", False,
                     "tracked files are modified or staged, so HEAD is not the verified candidate:\n" + tracked_changes)
    return Check("committed candidate", True, "no modified or staged tracked files")


def check_commits_ahead(spoke: Spoke, checkout: Path) -> Check:
    base_ref = f"origin/{spoke.default_branch}"
    try:
        commits_ahead = int(git(checkout, "rev-list", "--count", f"{base_ref}..HEAD"))
    except GIT_FAILURES as error:
        return Check("commits ahead", False, f"cannot compare with {base_ref}; fetch origin first: {error}")
    if commits_ahead == 0:
        return Check("commits ahead", False, f"HEAD has no commits ahead of {base_ref}")
    return Check("commits ahead", True, f"{commits_ahead} commit(s) ahead of {base_ref}")


def builder_report_path_of(raw_report: str) -> PurePosixPath:
    report_path = PurePosixPath(raw_report.replace("\\", "/"))
    if report_path.parent != REPORT_FOLDER or report_path.suffix != ".md" or report_path.name == "index.md":
        raise ValueError(f"--report must be a dated report under {REPORT_FOLDER}, relative to the Builder root")
    return report_path


def check_report_project(spoke: Spoke, report_text: str) -> Check:
    report_project = project_of(report_text)
    if report_project is None:
        return Check("report project", True, "report predates the Project section")
    return Check("report project", report_project == spoke.slug,
                 f"report Project is {report_project}" if report_project == spoke.slug
                 else f"report Project is {report_project}, not spoke {spoke.slug}")


def check_report(builder_root: Path, spoke: Spoke, report_path: PurePosixPath, candidate_commit: str) -> list[Check]:
    report_file = builder_root / report_path
    try:
        report_text = report_file.read_text(encoding="utf-8")
    except OSError as error:
        return [Check("report", False, f"cannot read {report_path}: {error}")]
    report_errors = validate_test_report_text(report_text, report_file)
    status_lines = markdown_sections(report_text).get("Document Status", "").splitlines() or [""]
    status = status_lines[0].strip().lstrip("-* ").strip("`").lower()
    if status != "complete":
        report_errors.append(f"Document Status is {status or 'missing'}, not complete")
    checks = [Check("report", not report_errors, "; ".join(report_errors) or f"{report_path} is a complete report"),
              check_report_project(spoke, report_text)]
    try:
        published_text = git(builder_root, "show", f"{BUILDER_PUBLISHED_REF}:{report_path}")
    except GIT_FAILURES:
        published_text = None
    if published_text is None:
        checks.append(Check("report published", False, f"{report_path} is not on Builder {BUILDER_PUBLISHED_REF}"))
    elif published_text.replace("\r\n", "\n").strip() != report_text.replace("\r\n", "\n").strip():
        checks.append(Check("report published", False,
                            f"local {report_path} differs from Builder {BUILDER_PUBLISHED_REF}; publish it first"))
    else:
        checks.append(Check("report published", True, f"identical on Builder {BUILDER_PUBLISHED_REF}"))
    named_commits = [commit for commit in COMMIT_ID_RE.findall(report_text) if candidate_commit.startswith(commit)]
    checks.append(Check("report names candidate", bool(named_commits),
                        f"report names {named_commits[0]}" if named_commits
                        else f"report does not name candidate {candidate_commit[:SHORT_SHA_LENGTH]}"))
    return checks


def report_url_of(builder_root: Path, report_path: PurePosixPath) -> str:
    builder_remote = normalize_remote(git(builder_root, "remote", "get-url", "origin"))
    return f"https://{builder_remote}/blob/main/{report_path}"


def preflight(builder_root: Path, spoke: Spoke, checkout: Path, report_path: PurePosixPath) -> tuple[list[Check], str]:
    checkout_check = check_checkout(spoke, checkout)
    if not checkout_check.passed:
        return [checkout_check], ""
    candidate_commit = git(checkout, "rev-parse", "HEAD")
    checks = [checkout_check, check_branch(spoke, checkout), check_tracked_changes(checkout),
              check_commits_ahead(spoke, checkout), *check_report(builder_root, spoke, report_path, candidate_commit)]
    return checks, candidate_commit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spoke", required=True, help="Registered spoke slug from spokes.json")
    parser.add_argument("--path", type=Path, help="Spoke checkout or linked worktree; defaults to the resolved spoke")
    parser.add_argument("--report", required=True, help="Builder test report, e.g. docs/test-reports/<date>-<title>.md")
    parser.add_argument("--root", default=".", help="Builder root containing spokes.json")
    args = parser.parse_args()
    builder_root = Path(args.root).expanduser().resolve()
    try:
        report_path = builder_report_path_of(args.report)
        spoke = find_spoke(builder_root, args.spoke)
        checkout = args.path.expanduser().resolve() if args.path else resolve_spoke_location(builder_root, spoke).path
        checks, candidate_commit = preflight(builder_root, spoke, checkout, report_path)
    except GIT_FAILURES as error:
        print(str(error), file=sys.stderr)
        return 2
    for check in checks:
        print(f"[{'pass' if check.passed else 'FAIL'}] {check.name}: {check.detail}")
    if not all(check.passed for check in checks):
        print("Preflight failed; do not push or open the pull request until every check passes.")
        return 1
    print(f"\nCandidate {candidate_commit} is ready. Add to the pull request body:\n\n"
          f"## Local Verification\nRuntime report for candidate `{candidate_commit[:SHORT_SHA_LENGTH]}`: "
          f"{report_url_of(builder_root, report_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
