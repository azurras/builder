#!/usr/bin/env python3
"""Compare a local candidate's HTTP responses with a reference, such as production.

  shape  GETs one URL and compares the JSON shape of its body (keys and value types, not values)
         with a saved JSON file. Lists compare by their first element, so an empty list matches a
         list of any element type, and null matches any type.
  same   GETs a candidate URL and a reference URL and requires both to answer the expected status
         with the same body. JSON bodies compare after dropping --ignore-field keys at the top
         level (timestamp by default); other bodies compare byte for byte. Error statuses are data.

Requests send --accept and a non-default User-Agent, because some edges refuse Python's own.
Exit codes: 0 match, 1 difference, 2 unusable input or a request that got no HTTP response.
"""
import argparse
import json
from pathlib import Path
import sys
from typing import Any
import urllib.error
import urllib.request

DEFAULT_USER_AGENT = "builder-verify-local-app"
REQUEST_TIMEOUT_SECONDS = 30


def fetch(url: str, accept: str, user_agent: str) -> tuple[int, bytes]:
    """The status and body of a GET, treating HTTP error statuses as ordinary responses."""
    request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": user_agent})
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:  # noqa: S310
            return response.status, response.read()
    except urllib.error.HTTPError as error_response:
        return error_response.code, error_response.read()


def json_shape(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: json_shape(child) for key, child in value.items()}
    if isinstance(value, list):
        return [json_shape(value[0])] if value else []
    return "null" if value is None else type(value).__name__


def shape_differences(expected: Any, actual: Any, path: str = "$") -> list[str]:
    if isinstance(expected, dict) and isinstance(actual, dict):
        differences = []
        for key in sorted(set(expected) | set(actual)):
            if key not in actual:
                differences.append(f"{path}.{key} missing")
            elif key not in expected:
                differences.append(f"{path}.{key} unexpected")
            else:
                differences.extend(shape_differences(expected[key], actual[key], f"{path}.{key}"))
        return differences
    if isinstance(expected, list) and isinstance(actual, list):
        if expected and actual:
            return shape_differences(expected[0], actual[0], path + "[0]")
        return []
    if "null" in (expected, actual) or expected == actual:
        return []
    return [f"{path} {expected} != {actual}"]


def comparable_body(raw_body: bytes, ignored_fields: list[str]) -> Any:
    """A JSON body without its ignored top-level fields, or the raw bytes of any other body."""
    try:
        decoded_body = json.loads(raw_body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return raw_body
    if isinstance(decoded_body, dict):
        for field in ignored_fields:
            decoded_body.pop(field, None)
    return decoded_body


def describe(body: Any) -> str:
    text = body.decode("utf-8", "replace") if isinstance(body, bytes) else json.dumps(body, sort_keys=True)
    return text if len(text) <= 300 else text[:300] + "..."


def compare_shape(arguments: argparse.Namespace) -> int:
    expected_shape = json_shape(json.loads(Path(arguments.expected_file).read_text(encoding="utf-8")))
    status, raw_body = fetch(arguments.url, arguments.accept, arguments.user_agent)
    try:
        actual_shape = json_shape(json.loads(raw_body))
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"{arguments.url} answered {status} with a body that is not JSON: {describe(raw_body)}")
        return 1
    differences = shape_differences(expected_shape, actual_shape)
    print(f"{arguments.url} answered {status}; " + ("shape matches" if not differences else "shape differs:"))
    for difference in differences:
        print(f"  {difference}")
    return 1 if differences else 0


def compare_same(arguments: argparse.Namespace) -> int:
    ignored_fields = arguments.ignore_field if arguments.ignore_field is not None else ["timestamp"]
    candidate_status, candidate_raw_body = fetch(arguments.candidate, arguments.accept, arguments.user_agent)
    reference_status, reference_raw_body = fetch(arguments.reference, arguments.accept, arguments.user_agent)
    candidate_body = comparable_body(candidate_raw_body, ignored_fields)
    reference_body = comparable_body(reference_raw_body, ignored_fields)
    print(f"candidate {candidate_status} {describe(candidate_body)}")
    print(f"reference {reference_status} {describe(reference_body)}")
    is_same = candidate_status == reference_status == arguments.expect_status and candidate_body == reference_body
    print("same" if is_same else "different")
    return 0 if is_same else 1


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modes = parser.add_subparsers(dest="mode", required=True)
    shape_parser = modes.add_parser("shape", help="Compare a response's JSON shape with a saved JSON file")
    shape_parser.add_argument("--url", required=True)
    shape_parser.add_argument("--expected-file", required=True, help="Saved JSON whose shape the body must have")
    same_parser = modes.add_parser("same", help="Require the same status and body from candidate and reference")
    same_parser.add_argument("--candidate", required=True, help="Candidate URL")
    same_parser.add_argument("--reference", required=True, help="Reference URL, usually production")
    same_parser.add_argument("--expect-status", type=int, required=True)
    same_parser.add_argument("--ignore-field", action="append",
                             help="Top-level JSON field to ignore; repeatable; defaults to timestamp")
    for mode_parser in (shape_parser, same_parser):
        mode_parser.add_argument("--accept", default="application/json")
        mode_parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        return compare_shape(arguments) if arguments.mode == "shape" else compare_same(arguments)
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
        print(f"Comparison could not run: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
