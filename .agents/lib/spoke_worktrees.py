"""Find and remove a spoke's stale linked worktrees whose work is already on the default branch.

A worktree is stale only when every condition holds, so live or unmerged work is never touched:
it sits in the checkout's own `<checkout>-worktrees` or `<checkout>.worktrees` folder, it is not
locked, its HEAD is already contained in origin/<default>, it has no tracked change beyond line
endings and no untracked file Git does not ignore, and Git has recorded no activity in it for the
minimum age. Ignored files such as build output are discarded with the worktree.

With pull request heads supplied, a worktree whose HEAD is exactly the head of a merged pull request
also counts as contained, because its content reached the default branch through that merge.
"""
from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from spoke_registry import normalize_remote
from spoke_state import git

REMOVE_TIMEOUT_SECONDS = 600
SECONDS_PER_DAY = 86_400


@dataclass(frozen=True)
class LinkedWorktree:
    path: Path
    head: str
    branch: str | None
    is_locked: bool


@dataclass(frozen=True)
class PullRequestHead:
    number: int
    state: str
    head_commit: str
    url: str


@dataclass(frozen=True)
class WorktreeDecision:
    worktree: LinkedWorktree
    is_stale: bool
    reason: str


def git_succeeds(repo: Path, *args: str) -> bool:
    completed = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8",
                               env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}, timeout=120, check=False)
    return completed.returncode == 0


def owned_worktree_folders(checkout: Path) -> list[Path]:
    return [checkout.parent / f"{checkout.name}-worktrees", checkout.parent / f"{checkout.name}.worktrees"]


def linked_worktrees_of(checkout: Path) -> list[LinkedWorktree]:
    """Parses `git worktree list --porcelain`, leaving out the primary checkout."""
    worktrees = []
    for record in git(checkout, "worktree", "list", "--porcelain").replace("\r\n", "\n").split("\n\n"):
        fields = [line.split(" ", 1) for line in record.splitlines() if line]
        values = {field[0]: (field[1] if len(field) > 1 else "") for field in fields}
        if "worktree" not in values or "bare" in values:
            continue
        path = Path(values["worktree"]).resolve()
        if path == checkout.resolve():
            continue
        branch = values.get("branch", "").removeprefix("refs/heads/") or None
        worktrees.append(LinkedWorktree(path, values.get("HEAD", ""), branch, "locked" in values))
    return worktrees


def is_contained_in(checkout: Path, commit: str, base_ref: str) -> bool:
    """True when the commit is an ancestor of base_ref, or merging it into base_ref changes nothing (squash merges)."""
    if git_succeeds(checkout, "merge-base", "--is-ancestor", commit, base_ref):
        return True
    try:
        merged_tree = git(checkout, "merge-tree", "--write-tree", base_ref, commit)
    except ValueError:
        return False
    return merged_tree.splitlines()[0] == git(checkout, "rev-parse", f"{base_ref}^{{tree}}")


def github_repository_of(repository_url: str) -> str:
    """owner/name for a github.com remote; other hosts have no pull requests to read."""
    host, _, path = normalize_remote(repository_url).partition("/")
    if host != "github.com" or path.count("/") != 1:
        raise ValueError(f"{repository_url} is not a github.com repository")
    return path


def pull_requests_by_branch(repository: str, limit: int = 1000) -> dict[str, list[PullRequestHead]]:
    """Every pull request of the repository, newest first, keyed by head branch name."""
    completed = subprocess.run(["gh", "pr", "list", "--repo", repository, "--state", "all", "--limit", str(limit),
                                "--json", "number,state,headRefName,headRefOid,url"],
                               capture_output=True, text=True, encoding="utf-8", timeout=120, check=False)
    if completed.returncode:
        raise ValueError(f"gh pr list failed: {completed.stderr.strip()}")
    pull_requests: dict[str, list[PullRequestHead]] = {}
    for entry in json.loads(completed.stdout):
        pull_requests.setdefault(entry["headRefName"], []).append(
            PullRequestHead(int(entry["number"]), str(entry["state"]).upper(), entry["headRefOid"], entry["url"]))
    return pull_requests


def merged_heads_of(pull_requests: dict[str, list[PullRequestHead]]) -> frozenset[str]:
    return frozenset(head.head_commit for heads in pull_requests.values() for head in heads if head.state == "MERGED")


def pull_request_summary(worktree: LinkedWorktree, pull_requests: dict[str, list[PullRequestHead]]) -> str:
    """What GitHub knows about the worktree's branch, for a person deciding whether to keep it."""
    heads = pull_requests.get(worktree.branch or "", [])
    if not heads:
        return "no pull request: never published"
    newest = heads[0]
    if newest.state == "MERGED" and newest.head_commit != worktree.head:
        return f"PR #{newest.number} merged, but the worktree has commits after it"
    if newest.state == "CLOSED":
        return f"PR #{newest.number} closed without merging"
    return f"PR #{newest.number} {newest.state.lower()}"


def days_since_last_activity(worktree_path: Path, now_seconds: float) -> float:
    git_folder = Path(git(worktree_path, "rev-parse", "--absolute-git-dir"))
    activity_times = [(git_folder / name).stat().st_mtime for name in ("HEAD", "index", "logs/HEAD")
                      if (git_folder / name).exists()]
    return (now_seconds - max(activity_times, default=0.0)) / SECONDS_PER_DAY


def decide(checkout: Path, worktree: LinkedWorktree, base_ref: str, minimum_age_days: float,
           now_seconds: float, merged_pull_request_heads: frozenset[str] = frozenset()) -> WorktreeDecision:
    if not any(worktree.path.is_relative_to(folder.resolve()) for folder in owned_worktree_folders(checkout)):
        return WorktreeDecision(worktree, False, "outside the checkout's worktree folders")
    if worktree.is_locked:
        return WorktreeDecision(worktree, False, "locked")
    if not worktree.path.is_dir():
        return WorktreeDecision(worktree, False, "folder is missing; git worktree prune clears it")
    merged_by_pull_request = worktree.head in merged_pull_request_heads
    if not merged_by_pull_request and not is_contained_in(checkout, worktree.head, base_ref):
        return WorktreeDecision(worktree, False, f"HEAD {worktree.head[:7]} is not on {base_ref}")
    status_lines = git(worktree.path, "status", "--porcelain", "--untracked-files=all").splitlines()
    untracked_files = [line[3:] for line in status_lines if line.startswith("??")]
    if untracked_files:
        return WorktreeDecision(worktree, False, f"{len(untracked_files)} untracked file(s), e.g. {untracked_files[0]}")
    if git(worktree.path, "diff", "HEAD", "--ignore-cr-at-eol", "--name-only"):
        return WorktreeDecision(worktree, False, "tracked changes")
    idle_days = days_since_last_activity(worktree.path, now_seconds)
    if idle_days < minimum_age_days:
        return WorktreeDecision(worktree, False, f"active {idle_days:.1f} day(s) ago")
    merge_route = "by a merged pull request" if merged_by_pull_request else f"into {base_ref}"
    return WorktreeDecision(worktree, True, f"merged {merge_route}, clean, idle {idle_days:.0f} day(s)")


def stale_worktree_decisions(checkout: Path, default_branch: str, minimum_age_days: float,
                             now_seconds: float | None = None,
                             merged_pull_request_heads: frozenset[str] = frozenset()) -> list[WorktreeDecision]:
    checkout = checkout.resolve()
    if Path(git(checkout, "rev-parse", "--show-toplevel")).resolve() != checkout:
        raise ValueError(f"{checkout} is not a repository root")
    if Path(git(checkout, "rev-parse", "--absolute-git-dir")).resolve() != (checkout / ".git").resolve():
        raise ValueError(f"{checkout} is a linked worktree; pass the primary checkout")
    now_seconds = time.time() if now_seconds is None else now_seconds
    base_ref = f"origin/{default_branch}"
    return [decide(checkout, worktree, base_ref, minimum_age_days, now_seconds, merged_pull_request_heads)
            for worktree in linked_worktrees_of(checkout)]


def remove_worktree(checkout: Path, worktree: LinkedWorktree, default_branch: str) -> str:
    """Removes one stale worktree and its local branch; returns what was done."""
    removal = subprocess.run(["git", "worktree", "remove", "--force", str(worktree.path)], cwd=checkout,
                             capture_output=True, text=True, encoding="utf-8", timeout=REMOVE_TIMEOUT_SECONDS,
                             check=False)
    if removal.returncode and worktree.path.exists():
        long_path = f"\\\\?\\{worktree.path}" if os.name == "nt" else str(worktree.path)
        shutil.rmtree(long_path)
    git(checkout, "worktree", "prune")
    if worktree.branch and worktree.branch != default_branch:
        git(checkout, "branch", "-D", worktree.branch)
        return f"removed worktree and branch {worktree.branch}"
    return "removed worktree"
