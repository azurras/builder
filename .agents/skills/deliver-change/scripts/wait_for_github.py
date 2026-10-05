#!/usr/bin/env python3
"""Wait, within a bound, for a pull request to pass CI (and optionally merge it) or for a deploy to go live.

Agents use this to watch their own work instead of handing the wait to the user.

  pr    Polls `gh pr view` until the PR is merged, a check fails, or the timeout passes. A check
        that CI infrastructure cancelled or never started (CANCELLED, STARTUP_FAILURE) gets one
        `gh run rerun --failed` per run. With --merge, the head observed green is merged with
        --match-head-commit.
  live  Polls a URL until its body contains the expected text, such as a deployed commit SHA.

Exit codes: 0 done (merged, green, or live), 1 failed (check failed, PR closed, merge refused),
2 timed out or unusable input. Run it in the background for long waits.
"""
import argparse
from dataclasses import dataclass
import json
import re
import subprocess
import sys
import time
from typing import Callable
import urllib.error
import urllib.request

REPOSITORY_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/[A-Za-z0-9._-]+")
RUN_ID_RE = re.compile(r"/actions/runs/(?P<run_id>\d+)")
PASSING_CONCLUSIONS = {"SUCCESS", "NEUTRAL", "SKIPPED"}
INFRASTRUCTURE_CONCLUSIONS = {"CANCELLED", "STARTUP_FAILURE", "STALE"}
MERGE_METHODS = ("squash", "merge", "rebase")

CommandRunner = Callable[[list[str]], subprocess.CompletedProcess]


@dataclass(frozen=True)
class WaitOutcome:
    exit_code: int
    message: str


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
                             "state,headRefOid,mergeCommit,statusCheckRollup"])
    if completed.returncode:
        raise ValueError(f"gh pr view {number} failed: {completed.stderr.strip()}")
    return json.loads(completed.stdout)


def wait_for_pull_request(repository: str, number: int, *, merge_method: str | None, timeout_seconds: float,
                          interval_seconds: float, run_command: CommandRunner = run_gh,
                          sleep: Callable[[float], None] = time.sleep,
                          clock: Callable[[], float] = time.monotonic) -> WaitOutcome:
    deadline = clock() + timeout_seconds
    rerun_run_ids: set[str] = set()
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
                return WaitOutcome(0, f"PR #{number} merged as {merge_commit or 'an unknown commit'}.")
            if state == "CLOSED":
                return WaitOutcome(1, f"PR #{number} was closed without merging.")
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
            if is_green:
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
    for mode_parser in (pr_parser, live_parser):
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
    else:
        if not args.url.startswith(("https://", "http://")):
            print("--url must be an http(s) URL.", file=sys.stderr)
            return 2
        outcome = wait_for_live_text(args.url, args.expect, timeout_seconds=timeout_seconds,
                                     interval_seconds=args.interval_seconds)
    print(outcome.message)
    return outcome.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
