"""Quality validators for Builder Markdown artifacts."""

from __future__ import annotations

from pathlib import Path
import re


PLAN_STATUSES = {
    "draft",
    "ready-for-review",
    "ready-for-execution",
    "in-progress",
    "blocked",
    "complete",
}

REPORT_STATUSES = {
    "draft",
    "complete",
    "blocked",
    "superseded",
}

PLAN_REQUIRED_SECTIONS = (
    "Document Status",
    "Objective",
    "Goals",
    "Inputs",
    "Branch",
    "Non-Goals",
    "Assumptions",
    "Open Questions",
    "Task Breakdown",
    "Code Changes",
    "Files and Modules",
    "Unit Testing",
    "Local Testing",
    "Validation",
    "Rollback or Recovery",
    "Risks",
    "Completion Criteria",
)

REPORT_REQUIRED_SECTIONS = (
    "Document Status",
    "Story/Issue",
    "Branch",
    "App / Environment",
    "Local Run Details",
    "Test Cases",
    "Data Sent",
    "Response Received",
    "Pass / Fail",
    "Evidence",
    "Bugs / Follow-ups",
)

UNIT_TEST_ONLY_PATTERNS = (
    r"\bunit tests?\b",
    r"\bgradlew\s+test\b",
    r"\bmvn\s+test\b",
    r"\bnpm\s+(run\s+)?test\b",
    r"\bpnpm\s+(run\s+)?test\b",
    r"\byarn\s+test\b",
    r"\bpytest\b",
    r"\bpython\s+-m\s+unittest\b",
    r"\bgo\s+test\b",
    r"\bcargo\s+test\b",
    r"\bjest\b",
    r"\bvitest\b",
)

LOCAL_APP_RUN_PATTERNS = (
    r"\blocalhost\b",
    r"\b127\.0\.0\.1\b",
    r"\b0\.0\.0\.0\b",
    r"\bserver\.port\b",
    r"\bbase url\b",
    r"\bport\s*[:=]\s*\d+",
    r"\bbootrun\b",
    r"\bnpm\s+run\s+dev\b",
    r"\byarn\s+dev\b",
    r"\bpnpm\s+dev\b",
    r"\buvicorn\b",
    r"\bflask\s+run\b",
    r"\brails\s+server\b",
    r"\bdotnet\s+run\b",
)

RUNTIME_DATA_PATTERNS = (
    r"\b(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+/",
    r"\bcurl\b",
    r"\bhttps?://",
    r"\bquery params?\b",
    r"\brequest body\b",
    r"\bpayload\b",
    r"\bform data\b",
    r"\bui input\b",
    r"\bclicked?\b",
    r"\btyped?\b",
    r"\bbrowser\b",
)

RUNTIME_RESPONSE_PATTERNS = (
    r"\bHTTP/1\.[01]\s+\d{3}\b",
    r"\bstatus\s*(code)?\s*[:=]?\s*\d{3}\b",
    r"\b\d{3}\s+(OK|Created|Accepted|No Content|Bad Request|Unauthorized|Forbidden|Not Found|Conflict|Internal Server Error)\b",
    r"\bresponse body\b",
    r"\bredirect\b",
    r"\bscreenshot\b",
    r"\bui (result|state|message)\b",
    r"\blog excerpt\b",
)


def _label(path: Path | None) -> str:
    return f"{path}: " if path else ""


def markdown_sections(markdown: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", markdown))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections[match.group(1).strip()] = markdown[start:end].strip()
    return sections


def _plain_status(value: str) -> str:
    first = value.strip().splitlines()[0].strip() if value.strip() else ""
    first = re.sub(r"^[-*]\s*", "", first).strip()
    return first.strip("`").lower()


def _require_sections(
    sections: dict[str, str],
    required: tuple[str, ...],
    errors: list[str],
    path: Path | None,
) -> None:
    for section in required:
        if section not in sections:
            errors.append(f"{_label(path)}missing required section: {section}")


def _matches_any(value: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, value, re.IGNORECASE) for pattern in patterns)


def validate_implementation_plan_text(markdown: str, path: Path | None = None) -> list[str]:
    errors: list[str] = []
    sections = markdown_sections(markdown)
    _require_sections(sections, PLAN_REQUIRED_SECTIONS, errors, path)

    status = _plain_status(sections.get("Document Status", ""))
    if status and status not in PLAN_STATUSES:
        errors.append(f"{_label(path)}invalid plan status {status!r}")

    task_breakdown = sections.get("Task Breakdown", "")
    if not re.search(r"(?m)^###\s+Task\s+\d+\b", task_breakdown):
        errors.append(f"{_label(path)}Task Breakdown must include ordered task headings")
    if "#### Code Edit" not in task_breakdown:
        errors.append(f"{_label(path)}Task Breakdown must include task-level Code Edit blocks")

    code_edit_blocks = re.split(r"(?m)^####\s+Code Edit\s+", task_breakdown)[1:]
    for ordinal, block in enumerate(code_edit_blocks, start=1):
        if not re.search(r"(?m)^-\s*File:\s*`?[^`\n]+`?\s*$", block):
            errors.append(f"{_label(path)}Code Edit {ordinal} missing File")
        line_match = re.search(r"(?m)^-\s*Lines:\s*(.+?)\s*$", block)
        if not line_match:
            errors.append(f"{_label(path)}Code Edit {ordinal} missing Lines")
        else:
            lines = line_match.group(1).strip().lower()
            concrete_line = re.match(r"(before|after)\s+\d+$", lines) or re.match(r"\d+(-\d+)?$", lines)
            pending = lines == "line range pending file inspection"
            if not concrete_line and not pending:
                errors.append(f"{_label(path)}Code Edit {ordinal} has invalid Lines value {lines!r}")
            if pending and status in {"ready-for-execution", "complete"}:
                errors.append(f"{_label(path)}Code Edit {ordinal} has line range pending in {status} plan")
        action = ""
        action_match = re.search(r"(?m)^-\s*Action:\s*(.+?)\s*$", block)
        if not action_match:
            errors.append(f"{_label(path)}Code Edit {ordinal} missing Action")
        else:
            action = action_match.group(1).strip().lower()
            if action not in {"add", "replace", "delete", "move"}:
                errors.append(f"{_label(path)}Code Edit {ordinal} has invalid Action")
        if "Current:" not in block and action != "add":
            errors.append(f"{_label(path)}Code Edit {ordinal} missing Current")
        if "Proposed:" not in block:
            errors.append(f"{_label(path)}Code Edit {ordinal} missing Proposed")
        if "Verification:" not in block:
            errors.append(f"{_label(path)}Code Edit {ordinal} missing Verification")
        if block.count("```") < 2:
            errors.append(f"{_label(path)}Code Edit {ordinal} must include fenced code")

    return errors


def validate_test_report_text(markdown: str, path: Path | None = None) -> list[str]:
    errors: list[str] = []
    sections = markdown_sections(markdown)
    _require_sections(sections, REPORT_REQUIRED_SECTIONS, errors, path)

    status = _plain_status(sections.get("Document Status", ""))
    if status and status not in REPORT_STATUSES:
        errors.append(f"{_label(path)}invalid test report status {status!r}")

    for section in ("Data Sent", "Response Received", "Pass / Fail", "Evidence"):
        if section in sections and not sections[section].strip():
            errors.append(f"{_label(path)}{section} must not be empty")

    app_context = "\n".join(
        sections.get(section, "")
        for section in ("App / Environment", "Local Run Details", "Evidence")
    )
    data_sent = sections.get("Data Sent", "")
    response_received = sections.get("Response Received", "")
    report_body = "\n".join(sections.values())

    has_local_app_run = _matches_any(app_context, LOCAL_APP_RUN_PATTERNS)
    has_runtime_data = _matches_any(data_sent, RUNTIME_DATA_PATTERNS)
    has_runtime_response = _matches_any(response_received, RUNTIME_RESPONSE_PATTERNS)
    mentions_unit_tests = _matches_any(report_body, UNIT_TEST_ONLY_PATTERNS)

    if status == "complete":
        if not has_local_app_run:
            errors.append(
                f"{_label(path)}complete test report must identify the local app runtime, port, or base URL under test"
            )
        if not has_runtime_data:
            errors.append(
                f"{_label(path)}complete test report Data Sent must describe an endpoint request, UI input, or other local app interaction"
            )
        if not has_runtime_response:
            errors.append(
                f"{_label(path)}complete test report Response Received must describe an HTTP response, UI result, screenshot, redirect, or log output from the running app"
            )
    if status == "complete" and mentions_unit_tests and not (
        has_local_app_run and has_runtime_data and has_runtime_response
    ):
        errors.append(
            f"{_label(path)}test reports are for local app verification; unit test output alone is not sufficient evidence"
        )

    return errors
