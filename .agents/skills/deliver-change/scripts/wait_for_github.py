#!/usr/bin/env python3
"""Wait, within a bound, for a pull request to pass CI (and optionally merge it) or for a deploy to go live.

Agents use this to watch their own work instead of handing the wait to the user.

  pr    Polls `gh pr view` until the PR is merged, a check fails, or the timeout passes. A check
        that CI infrastructure cancelled or never started (CANCELLED, STARTUP_FAILURE) gets one
        `gh run rerun --failed` per run. With --merge, the head observed green is merged with
        --match-head-commit.
        A branch that falls behind the base is updated once per head.
  live  Polls a URL until its body contains the expected text, such as a deployed commit SHA.
  deployed
        For a spoke that declares autoDeploy in spokes.json, polls until production serves the given
        commit or a later commit that contains it (production may skip commits it was too slow for).
  queue For an autoDeploy spoke, merges PRs one at a time. Each PR is released only once production
        serves the default branch's head, so back-to-back merges cannot starve the deployment, and
        the queue ends when production serves the last merge. --timeout-minutes bounds each PR.

Exit codes: 0 done (merged, green, or live), 1 failed (check failed, PR closed, merge refused),
2 timed out or unusable input. Run it in the background for long waits.
"""
import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Callable
import urllib.error
import urllib.request

BUILDER_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(BUILDER_ROOT / ".agents" / "lib"))

from spoke_registry import AutoDeploy, find_spoke, normalize_remote  # noqa: E402

REPOSITORY_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/[A-Za-z0-9._-]+")
COMMIT_RE = re.compile(r"[0-9a-fA-F]{7,40}")
RUN_ID_RE = re.compile(r"/actions/runs/(?P<run_id>\d+)")
PASSING_CONCLUSIONS = {"SUCCESS", "NEUTRAL", "SKIPPED"}
INFRASTRUCTURE_CONCLUSIONS = {"CANCELLED", "STARTUP_FAILURE", "STALE"}
MERGE_METHODS = ("squash", "merge", "rebase")
# GitHub compare statuses meaning the live commit is the expected commit or descends from it.
LIVE_COMPARE_STATUSES = {"identical", "ahead"}

CommandRunner = Callable[[list[str]], subprocess.CompletedProcess]


@dataclass(frozen=True)
class WaitOutcome:
    exit_code: int
    message: str
    merge_commit: str = ""


@dataclass(frozen=True)
class CheckSummary:
    pending_names: list[str]
    failed_names: list[str]
    infrastructure_run_ids: dict[str, str]


def run_gh(arguments: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *arguments], capture_output=True, text=True, encoding="utf-8",
                          timeout=120, check=False)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "builder-wait-for-github"})
    with urllib.request.urlopen(request, timeout=15) as response:  # noqa: S310 - caller-supplied https URL
        return response.read().decode("utf-8", errors="replace")


def summarize_checks(status_check_rollup: list[dict]) -> CheckSummary:
    """Classifies GitHub check runs and commit statuses by what the waiter should do next."""
    pending_names: list[str] = []
    failed_names: list[str] = []
    infrastructure_run_ids: dict[str, str] = {}
    for check in status_check_rollup:
        name = str(check.get("name") or check.get("context") or "unnamed check")
        if check.get("__typename") == "StatusContext":
            state = str(check.get("state") or "PENDING").upper()
            if state in {"PENDING", "EXPECTED"}:
                pending_names.append(name)
            elif state != "SUCCESS":
                failed_names.append(name)
            continue
        if str(check.get("status") or "").upper() != "COMPLETED":
            pending_names.append(name)
            continue
        conclusion = str(check.get("conclusion") or "").upper()
        if conclusion in PASSING_CONCLUSIONS:
            continue
        run_match = RUN_ID_RE.search(str(check.get("detailsUrl") or ""))
        if conclusion in INFRASTRUCTURE_CONCLUSIONS and run_match:
            infrastructure_run_ids[name] = run_match.group("run_id")
        else:
            failed_names.append(name)
    return CheckSummary(pending_names, failed_names, infrastructure_run_ids)


def read_pull_request(repository: str, number: int, run_command: CommandRunner) -> dict:
    completed = run_command(["pr", "view", str(number), "--repo", repository, "--json",
                             "state,headRefOid,mergeCommit,mergeStateStatus,statusCheckRollup"])
    if completed.returncode:
        raise ValueError(f"gh pr view {number} failed: {completed.stderr.strip()}")
    return json.loads(completed.stdout)


def wait_for_pull_request(repository: str, number: int, *, merge_method: str | None, timeout_seconds: float,
                          interval_seconds: float, run_command: CommandRunner = run_gh,
                          sleep: Callable[[float], None] = time.sleep,
                          clock: Callable[[], float] = time.monotonic) -> WaitOutcome:
    deadline = clock() + timeout_seconds
    rerun_run_ids: set[str] = set()
    updated_heads: set[str] = set()
    last_error = ""
    while True:
        try:
            pull_request = read_pull_request(repository, number, run_command)
        except (ValueError, json.JSONDecodeError) as error:
            pull_request, last_error = None, str(error)
        if pull_request is not None:
            state = str(pull_request.get("state") or "").upper()
            head_commit = str(pull_request.get("headRefOid") or "")
            if state == "MERGED":
                merge_commit = (pull_request.get("mergeCommit") or {}).get("oid", "")
                return WaitOutcome(0, f"PR #{number} merged as {merge_commit or 'an unknown commit'}.",
                                   merge_commit)
            if state == "CLOSED":
                return WaitOutcome(1, f"PR #{number} was closed without merging.")
            is_behind = str(pull_request.get("mergeStateStatus") or "").upper() == "BEHIND"
            if is_behind and head_commit not in updated_heads:
                update = run_command(["pr", "update-branch", str(number), "--repo", repository])
                updated_heads.add(head_commit)
                print(f"PR #{number} was behind its base; branch update "
                      f"{'requested' if update.returncode == 0 else 'refused: ' + update.stderr.strip()}.",
                      flush=True)
            checks = summarize_checks(list(pull_request.get("statusCheckRollup") or []))
            for check_name, run_id in checks.infrastructure_run_ids.items():
                if run_id in rerun_run_ids:
                    checks.failed_names.append(f"{check_name} (cancelled again after a re-run)")
                    continue
                rerun = run_command(["run", "rerun", run_id, "--failed", "--repo", repository])
                rerun_run_ids.add(run_id)
                print(f"Re-ran run {run_id} for {check_name}: "
                      f"{'requested' if rerun.returncode == 0 else rerun.stderr.strip()}", flush=True)
            if checks.failed_names:
                return WaitOutcome(1, f"PR #{number} has failing checks: {', '.join(sorted(checks.failed_names))}.")
            is_green = (not checks.pending_names and not checks.infrastructure_run_ids
                        and bool(pull_request.get("statusCheckRollup")))
            if is_green and merge_method is None:
                return WaitOutcome(0, f"PR #{number} checks passed on {head_commit[:7]}; not merged.")
            if is_green and not is_behind:
                merge = run_command(["pr", "merge", str(number), "--repo", repository, f"--{merge_method}",
                                     "--match-head-commit", head_commit])
                if merge.returncode:
                    return WaitOutcome(1, f"Merging PR #{number} at {head_commit[:7]} was refused: "
                                          f"{merge.stderr.strip() or merge.stdout.strip()}")
                print(f"Merge requested for PR #{number} at {head_commit[:7]}.", flush=True)
        if clock() >= deadline:
            detail = f" Last error: {last_error}" if last_error else ""
            return WaitOutcome(2, f"Timed out waiting for PR #{number}.{detail}")
        sleep(interval_seconds)


def wait_for_live_text(url: str, expected_text: str, *, timeout_seconds: float, interval_seconds: float,
                       fetch: Callable[[str], str] = fetch_text, sleep: Callable[[float], None] = time.sleep,
                       clock: Callable[[], float] = time.monotonic) -> WaitOutcome:
    deadline = clock() + timeout_seconds
    last_problem = "no response yet"
    while True:
        try:
            body = fetch(url)
            if expected_text in body:
                return WaitOutcome(0, f"{url} now contains {expected_text}.")
            last_problem = f"body did not contain {expected_text} (starts {body[:120]!r})"
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_problem = f"request failed: {error}"
        if clock() >= deadline:
            return WaitOutcome(2, f"Timed out waiting for {url}: {last_problem}.")
        sleep(interval_seconds)


def github_repository_of(repository_url: str) -> str:
    """The owner/name of a registered GitHub remote."""
    host, _, path = normalize_remote(repository_url).partition("/")
    if host != "github.com" or not REPOSITORY_RE.fullmatch(path):
        raise ValueError(f"{repository_url} is not a GitHub repository.")
    return path


def live_commit_of(auto_deploy: AutoDeploy, fetch: Callable[[str], str]) -> str:
    body = fetch(auto_deploy.live_commit_url)
    match = auto_deploy.live_commit_pattern.search(body)
    if match is None:
        raise ValueError(f"{auto_deploy.live_commit_url} did not show a commit (starts {body[:120]!r})")
    return match.group(1).lower()


def default_branch_head_of(repository: str, branch: str, run_command: CommandRunner) -> str:
    completed = run_command(["api", f"repos/{repository}/commits/{branch}", "--jq", ".sha"])
    if completed.returncode:
        raise ValueError(f"reading {branch} failed: {completed.stderr.strip()}")
    return completed.stdout.strip().lower()


def is_commit_in_live(repository: str, commit: str, live_commit: str, run_command: CommandRunner) -> bool:
    """True when the live commit is the given commit or a descendant of it."""
    if live_commit.startswith(commit.lower()):
        return True
    completed = run_command(["api", f"repos/{repository}/compare/{commit}...{live_commit}", "--jq", ".status"])
    if completed.returncode:
        raise ValueError(f"comparing {commit[:7]} with {live_commit[:7]} failed: {completed.stderr.strip()}")
    return completed.stdout.strip() in LIVE_COMPARE_STATUSES


def wait_for_deployed_commit(repository: str, auto_deploy: AutoDeploy, commit: str, *, timeout_seconds: float,
                             interval_seconds: float, run_command: CommandRunner = run_gh,
                             fetch: Callable[[str], str] = fetch_text, sleep: Callable[[float], None] = time.sleep,
                             clock: Callable[[], float] = time.monotonic) -> WaitOutcome:
    deadline = clock() + timeout_seconds
    last_problem = "no response yet"
    while True:
        try:
            live_commit = live_commit_of(auto_deploy, fetch)
            if is_commit_in_live(repository, commit, live_commit, run_command):
                return WaitOutcome(0, f"Production serves {live_commit[:7]}, which contains {commit[:7]}.")
            last_problem = f"production still serves {live_commit[:7]}"
        except (ValueError, urllib.error.URLError, TimeoutError, OSError) as error:
            last_problem = str(error)
        if clock() >= deadline:
            return WaitOutcome(2, f"Timed out waiting for {commit[:7]} to be live: {last_problem}.")
        sleep(interval_seconds)


def wait_for_default_branch_live(repository: str, branch: str, auto_deploy: AutoDeploy, *, timeout_seconds: float,
                                 interval_seconds: float, run_command: CommandRunner, fetch: Callable[[str], str],
                                 sleep: Callable[[float], None], clock: Callable[[], float]) -> WaitOutcome:
    deadline = clock() + timeout_seconds
    last_problem = "no response yet"
    while True:
        try:
            head = default_branch_head_of(repository, branch, run_command)
            live_commit = live_commit_of(auto_deploy, fetch)
            if live_commit == head:
                return WaitOutcome(0, f"Production serves {branch} head {head[:7]}.")
            last_problem = f"production serves {live_commit[:7]} but {branch} is at {head[:7]}"
        except (ValueError, urllib.error.URLError, TimeoutError, OSError) as error:
            last_problem = str(error)
        if clock() >= deadline:
            return WaitOutcome(2, f"Timed out waiting for production to serve {branch}: {last_problem}.")
        sleep(interval_seconds)


def merge_queue(repository: str, branch: str, auto_deploy: AutoDeploy, numbers: list[int], *, merge_method: str,
                timeout_seconds: float, interval_seconds: float, run_command: CommandRunner = run_gh,
                fetch: Callable[[str], str] = fetch_text, sleep: Callable[[float], None] = time.sleep,
                clock: Callable[[], float] = time.monotonic) -> WaitOutcome:
    """Merges each PR in order, releasing it only when production serves the default branch's head."""
    timing = {"timeout_seconds": timeout_seconds, "interval_seconds": interval_seconds,
              "run_command": run_command, "sleep": sleep, "clock": clock}
    last_merge_commit = ""
    for number in numbers:
        released = wait_for_default_branch_live(repository, branch, auto_deploy, fetch=fetch, **timing)
        print(released.message, flush=True)
        if released.exit_code:
            return WaitOutcome(released.exit_code, f"PR #{number} was not released: {released.message}")
        merged = wait_for_pull_request(repository, number, merge_method=merge_method, **timing)
        print(merged.message, flush=True)
        if merged.exit_code:
            return merged
        last_merge_commit = merged.merge_commit
    if not last_merge_commit:
        return WaitOutcome(1, "The last PR merged without a readable merge commit.")
    deployed = wait_for_deployed_commit(repository, auto_deploy, last_merge_commit, fetch=fetch, **timing)
    return WaitOutcome(deployed.exit_code, f"Merged PRs {', '.join(f'#{n}' for n in numbers)}. {deployed.message}",
                       last_merge_commit)


def auto_deploy_spoke(slug: str) -> tuple[str, str, AutoDeploy]:
    """The GitHub repository, default branch and deployment declaration of a registered spoke."""
    spoke = find_spoke(BUILDER_ROOT, slug)
    if spoke.auto_deploy is None:
        raise ValueError(f"Spoke {slug!r} does not declare autoDeploy in spokes.json.")
    return github_repository_of(spoke.repository), spoke.default_branch, spoke.auto_deploy


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modes = parser.add_subparsers(dest="mode", required=True)
    pr_parser = modes.add_parser("pr", help="Wait for a pull request's checks, optionally merging it")
    pr_parser.add_argument("--repo", required=True, help="owner/name")
    pr_parser.add_argument("--number", type=int, required=True)
    pr_parser.add_argument("--merge", choices=MERGE_METHODS, help="Merge the head observed green with this method")
    live_parser = modes.add_parser("live", help="Wait for a URL to serve expected text")
    live_parser.add_argument("--url", required=True)
    live_parser.add_argument("--expect", required=True, help="Text the body must contain, such as a commit SHA")
    deployed_parser = modes.add_parser("deployed", help="Wait for an autoDeploy spoke to serve a commit")
    deployed_parser.add_argument("--spoke", required=True, help="Registered spoke slug")
    deployed_parser.add_argument("--commit", required=True, help="Commit SHA that production must contain")
    queue_parser = modes.add_parser("queue", help="Merge PRs one at a time behind an autoDeploy spoke's deployment")
    queue_parser.add_argument("--spoke", required=True, help="Registered spoke slug")
    queue_parser.add_argument("--numbers", type=int, nargs="+", required=True, help="PR numbers in merge order")
    queue_parser.add_argument("--merge", choices=MERGE_METHODS, required=True)
    for mode_parser in (pr_parser, live_parser, deployed_parser, queue_parser):
        mode_parser.add_argument("--timeout-minutes", type=float, default=60.0)
        mode_parser.add_argument("--interval-seconds", type=float, default=60.0)
    args = parser.parse_args()
    if args.timeout_minutes <= 0 or args.interval_seconds < 5:
        print("--timeout-minutes must be positive and --interval-seconds at least 5.", file=sys.stderr)
        return 2
    timeout_seconds = args.timeout_minutes * 60
    if args.mode == "pr":
        if not REPOSITORY_RE.fullmatch(args.repo):
            print("--repo must be owner/name.", file=sys.stderr)
            return 2
        outcome = wait_for_pull_request(args.repo, args.number, merge_method=args.merge,
                                        timeout_seconds=timeout_seconds, interval_seconds=args.interval_seconds)
    elif args.mode == "live":
        if not args.url.startswith(("https://", "http://")):
            print("--url must be an http(s) URL.", file=sys.stderr)
            return 2
        outcome = wait_for_live_text(args.url, args.expect, timeout_seconds=timeout_seconds,
                                     interval_seconds=args.interval_seconds)
    else:
        try:
            repository, branch, auto_deploy = auto_deploy_spoke(args.spoke)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 2
        if args.mode == "deployed" and not COMMIT_RE.fullmatch(args.commit):
            print("--commit must be a 7 to 40 character hexadecimal SHA.", file=sys.stderr)
            return 2
        if args.mode == "deployed":
            outcome = wait_for_deployed_commit(repository, auto_deploy, args.commit, timeout_seconds=timeout_seconds,
                                               interval_seconds=args.interval_seconds)
        else:
            outcome = merge_queue(repository, branch, auto_deploy, args.numbers, merge_method=args.merge,
                                  timeout_seconds=timeout_seconds, interval_seconds=args.interval_seconds)
    print(outcome.message)
    return outcome.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
