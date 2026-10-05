#!/usr/bin/env python3
"""Print a GitHub issue or pull request discussion split into trusted direction and untrusted input.

Reads through `gh api` GET requests only; never posts, edits or downloads attachments.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))
from github_trust import discussion_from_payload, render_triage

REPOSITORY_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/[A-Za-z0-9._-]+")


def read_github_api(api_path: str, *, all_pages: bool) -> object:
    command = ["gh", "api", "-H", "Accept: application/vnd.github+json", api_path]
    if all_pages:
        command += ["--paginate", "--slurp"]
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=120, check=False)
    if completed.returncode:
        raise ValueError(f"gh api {api_path} failed ({completed.returncode}): {completed.stderr.strip()}")
    try:
        response = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ValueError(f"gh api {api_path} returned invalid JSON: {error}") from error
    if all_pages:
        return [record for page in response for record in page]
    return response


def fetch_discussion_payload(repository: str, number: int) -> dict:
    issue_path = f"repos/{repository}/issues/{number}"
    opening_post = read_github_api(issue_path, all_pages=False)
    payload = {"item": opening_post, "comments": read_github_api(f"{issue_path}/comments", all_pages=True)}
    if isinstance(opening_post, dict) and "pull_request" in opening_post:
        pull_path = f"repos/{repository}/pulls/{number}"
        payload["reviews"] = read_github_api(f"{pull_path}/reviews", all_pages=True)
        payload["reviewComments"] = read_github_api(f"{pull_path}/comments", all_pages=True)
    return payload


def positive_number(raw_number: str) -> int:
    number = int(raw_number)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive issue or pull request number")
    return number


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="owner/name, for example azurras/christopherbell.dev")
    parser.add_argument("--number", required=True, type=positive_number, help="Issue or pull request number")
    parser.add_argument("--from-json", type=Path,
                        help="Read a saved {item, comments, reviews, reviewComments} payload instead of calling gh")
    args = parser.parse_args()
    if not REPOSITORY_RE.fullmatch(args.repo):
        parser.error("--repo must be owner/name")
    try:
        if args.from_json:
            payload = json.loads(args.from_json.read_text(encoding="utf-8"))
        else:
            payload = fetch_discussion_payload(args.repo, args.number)
        discussion = discussion_from_payload(payload)
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    print(render_triage(args.repo, args.number, discussion), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
