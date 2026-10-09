#!/usr/bin/env python3
"""Record runtime evidence as it happens, then render it as a test report.

  run    Runs a local command and records its arguments, exit code, stdout and stderr.
  http   Sends one HTTP request and records the request, status, headers and body.
  render Turns the recorded cases into a complete report body for save_test_report.py.

Each recorded case is appended as one JSON line to --evidence, a scratch file outside the
repositories. Secrets in headers and common token shapes are masked before anything is written.
`run` and `http` exit 0 when the case passed, 1 when it was recorded but failed, 2 on bad input.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

MAX_OUTPUT_CHARACTERS = 20_000
COLLAPSE_AFTER_LINES = 30
SECRET_HEADERS = {"authorization", "cookie", "set-cookie", "proxy-authorization", "x-api-key"}
SECRET_PATTERNS = (
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]+"), "[REDACTED_TOKEN]"),
    (re.compile(r"\bgh[opsur]_[A-Za-z0-9]{16,}"), "[REDACTED_TOKEN]"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"), "[REDACTED_JWT]"),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]+"), "Bearer [REDACTED]"),
    (re.compile(r"(?i)\b(mongodb(?:\+srv)?|postgres(?:ql)?)://[^/\s@]+@"), r"\1://[REDACTED]@"),
    (re.compile(r"(?i)\b(password|passwd|secret|api[_-]?key|token)(\s*[=:]\s*)[^\s,;&\"]+"), r"\1\2[REDACTED]"),
)


@dataclass(frozen=True)
class RecordedCase:
    case: str
    kind: str
    started_at: str
    elapsed_ms: int
    sent: str
    received: str
    passed: bool
    expectation: str
    working_directory: str
    candidate_commit: str | None


def masked(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def bounded(text: str) -> str:
    if len(text) <= MAX_OUTPUT_CHARACTERS:
        return text
    return text[:MAX_OUTPUT_CHARACTERS] + f"\n... [{len(text) - MAX_OUTPUT_CHARACTERS} more characters not recorded]"


def candidate_commit_of(checkout: Path) -> str | None:
    completed = subprocess.run(["git", "rev-parse", "HEAD"], cwd=checkout, capture_output=True, text=True,
                               timeout=30, check=False)
    return completed.stdout.strip() if completed.returncode == 0 else None


def now_stamp() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def record_command(case: str, command: list[str], working_directory: Path, expected_exit_code: int,
                   timeout_seconds: float) -> RecordedCase:
    started_at, started = now_stamp(), time.monotonic()
    try:
        completed = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, encoding="utf-8",
                                   errors="replace", timeout=timeout_seconds, check=False)
        exit_code, stdout, stderr = completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired as error:
        exit_code = None
        stdout = error.stdout if isinstance(error.stdout, str) else ""
        stderr = f"timed out after {timeout_seconds:g} seconds"
    except OSError as error:
        exit_code, stdout, stderr = None, "", f"could not start: {error}"
    elapsed_ms = int((time.monotonic() - started) * 1000)
    received = f"exit code: {exit_code if exit_code is not None else 'none'}\n--- stdout ---\n{stdout.rstrip()}"
    if stderr.strip():
        received += f"\n--- stderr ---\n{stderr.rstrip()}"
    return RecordedCase(case, "command", started_at, elapsed_ms, masked(subprocess.list2cmdline(command)),
                        masked(bounded(received)), exit_code == expected_exit_code,
                        f"exit code {expected_exit_code}", str(working_directory), candidate_commit_of(working_directory))


def record_http(case: str, method: str, url: str, headers: dict[str, str], body: str | None,
                expected_status: int | None, expected_text: str | None, checkout: Path,
                timeout_seconds: float) -> RecordedCase:
    request = urllib.request.Request(url, method=method, headers=headers,
                                     data=body.encode("utf-8") if body is not None else None)
    shown_headers = "".join(f"{name}: {'[REDACTED]' if name.lower() in SECRET_HEADERS else value}\n"
                            for name, value in headers.items())
    sent = f"{method} {url}\n{shown_headers}" + (f"\n{body}" if body is not None else "")
    started_at, started = now_stamp(), time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - local candidate URL
            status, reason, response_headers = response.status, response.reason, response.headers
            response_body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        status, reason, response_headers = error.code, error.reason, error.headers
        response_body = error.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        status, reason, response_headers, response_body = None, str(error), {}, ""
    elapsed_ms = int((time.monotonic() - started) * 1000)
    header_lines = "".join(f"{name}: {'[REDACTED]' if name.lower() in SECRET_HEADERS else value}\n"
                           for name, value in response_headers.items())
    received = f"HTTP {status if status is not None else 'no response'} {reason}\n{header_lines}\n{response_body}"
    status_ok = (status == expected_status) if expected_status is not None else (status is not None and status < 400)
    text_ok = expected_text is None or expected_text in response_body
    expectation = (f"status {expected_status}" if expected_status is not None else "status below 400") + (
        f" and body containing {expected_text!r}" if expected_text is not None else "")
    return RecordedCase(case, "http", started_at, elapsed_ms, masked(sent.rstrip()), masked(bounded(received.rstrip())),
                        status_ok and text_ok, expectation, str(checkout), candidate_commit_of(checkout))


def append_case(evidence_file: Path, recorded_case: RecordedCase) -> None:
    evidence_file.parent.mkdir(parents=True, exist_ok=True)
    with evidence_file.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(asdict(recorded_case)) + "\n")


def read_cases(evidence_file: Path) -> list[RecordedCase]:
    lines = evidence_file.read_text(encoding="utf-8").splitlines()
    return [RecordedCase(**json.loads(line)) for line in lines if line.strip()]


def fenced(text: str, language: str) -> str:
    fence = "````" if "```" in text else "```"
    block = f"{fence}{language}\n{text}\n{fence}"
    if text.count("\n") + 1 <= COLLAPSE_AFTER_LINES:
        return block
    return f"<details><summary>{text.count(chr(10)) + 1} lines</summary>\n\n{block}\n\n</details>"


def render_report(cases: list[RecordedCase], *, title: str, story: str, branch: str, project: str,
                  environment: list[str], cleanup: str) -> str:
    if not cases:
        raise ValueError("the evidence file has no recorded cases")
    commits = {recorded_case.candidate_commit for recorded_case in cases if recorded_case.candidate_commit}
    candidate = next(iter(commits))[:7] if len(commits) == 1 else "mixed: " + ", ".join(sorted(c[:7] for c in commits))
    passed_count = sum(recorded_case.passed for recorded_case in cases)
    all_passed = passed_count == len(cases)
    callout = "TIP" if all_passed else "WARNING"
    rows = "\n".join(f"| {number} | {recorded_case.case} | {'✅ PASS' if recorded_case.passed else '❌ FAIL'} | "
                     f"Expected {recorded_case.expectation} |" for number, recorded_case in enumerate(cases, 1))
    test_cases = "\n".join(f"{number}. **{recorded_case.case}**: {recorded_case.kind} `{recorded_case.sent.splitlines()[0]}`"
                           for number, recorded_case in enumerate(cases, 1))
    environment_rows = "\n".join(f"| {name.strip()} | {value.strip()} |"
                                 for name, value in (setting.split("=", 1) for setting in environment))
    local_commands = "\n".join(f"- **Local command:** `{recorded_case.sent.splitlines()[0]}` "
                               f"in `{recorded_case.working_directory}`" for recorded_case in cases)
    data_sent = "\n\n".join(f"### {number}. {recorded_case.case}\n\n"
                            f"{fenced(recorded_case.sent, 'http' if recorded_case.kind == 'http' else 'text')}"
                            for number, recorded_case in enumerate(cases, 1))
    responses = "\n\n".join(f"### {number}. {recorded_case.case}\n\n{fenced(recorded_case.received, 'text')}"
                            for number, recorded_case in enumerate(cases, 1))
    evidence = "\n".join(f"- Case {number} started {recorded_case.started_at}, took {recorded_case.elapsed_ms} ms, "
                         f"candidate `{(recorded_case.candidate_commit or 'unknown')[:7]}`"
                         for number, recorded_case in enumerate(cases, 1))
    failures = [f"- Case {number} ({recorded_case.case}) failed: expected {recorded_case.expectation}."
                for number, recorded_case in enumerate(cases, 1) if not recorded_case.passed]
    return f"""# {title}: Test Report

## Story/Issue
{story}

## Branch
`{branch}` at candidate `{candidate}`

## Pass / Fail

> [!{callout}]
> {passed_count} of {len(cases)} cases passed on candidate `{candidate}`.

| # | Test case | Result | Why |
|---|---|---|---|
{rows}

## Test Cases
{test_cases}

## App / Environment

| Setting | Value |
|---|---|
{environment_rows or '| Environment | Local machine |'}

## Local Run Details
{local_commands}
- **Candidate identity:** `{candidate}`
- **Cleanup:** {cleanup}

## Data Sent

{data_sent}

## Response Received

{responses}

## Evidence
{evidence}

## Bugs / Follow-ups
{chr(10).join(failures) or 'None'}

## Document Status
{'complete' if all_passed else 'draft'}

## Project
{project}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modes = parser.add_subparsers(dest="mode", required=True)
    run_parser = modes.add_parser("run", help="Run and record a local command; put it after --")
    run_parser.add_argument("--cwd", type=Path, default=Path("."), help="Working directory, usually the candidate checkout")
    run_parser.add_argument("--expect-exit", type=int, default=0)
    run_parser.add_argument("command", nargs=argparse.REMAINDER)
    http_parser = modes.add_parser("http", help="Send and record one HTTP request")
    http_parser.add_argument("--url", required=True)
    http_parser.add_argument("--method", default="GET")
    http_parser.add_argument("--header", action="append", default=[], help="Name: value; repeatable")
    http_parser.add_argument("--body", help="Request body text")
    http_parser.add_argument("--expect-status", type=int)
    http_parser.add_argument("--expect-text")
    http_parser.add_argument("--checkout", type=Path, default=Path("."), help="Candidate checkout, for its commit")
    for recording_parser in (run_parser, http_parser):
        recording_parser.add_argument("--evidence", type=Path, required=True, help="JSON-lines evidence file")
        recording_parser.add_argument("--case", required=True, help="Test case name")
        recording_parser.add_argument("--timeout-seconds", type=float, default=300.0)
    render_parser = modes.add_parser("render", help="Print a report body from recorded cases")
    render_parser.add_argument("--evidence", type=Path, required=True)
    render_parser.add_argument("--title", required=True)
    render_parser.add_argument("--story", required=True)
    render_parser.add_argument("--branch", required=True)
    render_parser.add_argument("--project", required=True)
    render_parser.add_argument("--env", action="append", default=[], help="Setting=value row; repeatable")
    render_parser.add_argument("--cleanup", default="Stopped the candidate process tree; no fixtures remain.")
    args = parser.parse_args()

    if args.mode == "render":
        try:
            if any("=" not in setting for setting in args.env):
                raise ValueError("--env takes Setting=value")
            # Reports contain non-ASCII marks; a Windows console code page cannot encode them, and
            # redirected output would otherwise gain CRLF line endings.
            sys.stdout.reconfigure(encoding="utf-8", newline="\n")
            print(render_report(read_cases(args.evidence), title=args.title, story=args.story, branch=args.branch,
                                project=args.project, environment=args.env, cleanup=args.cleanup), end="")
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
            print(f"cannot render {args.evidence}: {error}", file=sys.stderr)
            return 2
        return 0
    if args.mode == "run":
        command = args.command[1:] if args.command[:1] == ["--"] else args.command
        if not command:
            print("run needs a command after --", file=sys.stderr)
            return 2
        recorded_case = record_command(args.case, command, args.cwd.resolve(), args.expect_exit, args.timeout_seconds)
    else:
        if not args.url.startswith(("http://", "https://")):
            print("--url must be an http(s) URL", file=sys.stderr)
            return 2
        if any(":" not in header for header in args.header):
            print("--header takes 'Name: value'", file=sys.stderr)
            return 2
        headers = dict((name.strip(), value.strip()) for name, value in (header.split(":", 1) for header in args.header))
        recorded_case = record_http(args.case, args.method.upper(), args.url, headers, args.body, args.expect_status,
                                    args.expect_text, args.checkout.resolve(), args.timeout_seconds)
    append_case(args.evidence, recorded_case)
    print(f"[{'pass' if recorded_case.passed else 'FAIL'}] {recorded_case.case}: expected {recorded_case.expectation}")
    return 0 if recorded_case.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
