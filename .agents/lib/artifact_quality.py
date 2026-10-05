"""Quality validators for Builder Markdown artifacts."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import re
import shlex


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

# task-contract-v2 plans are living records of one change.
CURRENT_PLAN_FORMAT = "task-contract-v2"

PLAN_V2_REQUIRED_SECTIONS = (
    "Plan Format",
    "Document Status",
    "Objective",
    "Background",
    "Goals",
    "Non-Goals",
    "Acceptance Criteria",
    "Inputs",
    "Branch",
    "Assumptions",
    "Open Questions",
    "Design",
    "Expected Changes",
    "Task Breakdown",
    "Test Plan",
    "Rollback or Recovery",
    "Risks",
    "Implementation Log",
    "Outcome",
)

PLAN_LOG_ENTRY_FIELDS = ("Change", "Reason", "Impact")

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
    r"\bdotnet\s+test\b",
    r"\bjest\b",
    r"\bvitest\b",
)

LOCAL_COMMAND_PATTERN = (
    r"(?im)^\s*(?:[-*]\s+)?local\s+"
    r"(?:(?:app(?:lication)?|cli|worker|desktop|consumer)\s+)?"
    r"(?:command|invocation|launch|run)\s*:\s*(?P<command>\S[^\n]*)$"
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
    r"\bcommand arguments?\b",
    r"\bstdin\b",
    r"\binput file\b",
    r"\bqueue message\b",
    r"\bconsumer input\b",
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
    r"\bexit\s+(code|status)\s*[:=]?\s*-?\d+\b",
    r"\b(stdout|stderr)\b",
    r"\boutput (file|artifact)\b",
    r"\bworker result\b",
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


PLAN_TASK_FIELDS = (
    "Dependencies", "Files", "Symbols", "Inspection", "Behavior", "Invariants",
    "Boundary/API", "Effects and failures", "Tests and evidence", "Verification",
)


def _validate_legacy_code_edits(
    task: str, status: str, path: Path | None, errors: list[str]
) -> None:
    code_edit_blocks = re.split(r"(?m)^####\s+Code Edit\s+", task)[1:]
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


def _validate_task_contracts(
    breakdown: str, status: str, path: Path | None, errors: list[str]
) -> bool:
    """Validate each ordered task; return whether any task uses a contract."""
    headings = list(re.finditer(r"(?m)^###[ \t]+Task[ \t]+(\d+)\b[^\n]*", breakdown))
    if not headings:
        errors.append(f"{_label(path)}Task Breakdown must include ordered task headings")
    numbers = [int(heading.group(1)) for heading in headings]
    if numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"{_label(path)}Task headings must be sequential starting at Task 1")

    has_contract = False
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(breakdown)
        task = breakdown[heading.end():end]
        label = f"{_label(path)}Task {heading.group(1)}"
        if re.search(r"(?m)^####[ \t]+Code Edit[ \t]+", task):
            _validate_legacy_code_edits(task, status, path, errors)
            continue
        has_contract = True
        for field in PLAN_TASK_FIELDS:
            match = re.search(rf"(?mi)^[ \t]*(?:-[ \t]*)?{re.escape(field)}:[ \t]*(.*)$", task)
            value = match.group(1).strip() if match else ""
            if not value:
                errors.append(f"{label} missing {field}: supply a task contract or legacy Code Edit block")
            elif status in {"ready-for-execution", "in-progress", "complete"} and re.search(
                r"(?i)\b(TBD|TODO)\b|pending file inspection|line range pending", value
            ):
                errors.append(f"{label} unresolved {field} in {status} plan")
    return has_contract


def plan_format_of(markdown: str) -> str:
    return markdown_sections(markdown).get("Plan Format", "").strip()


def validate_implementation_plan_text(markdown: str, path: Path | None = None) -> list[str]:
    sections = markdown_sections(markdown)
    if sections.get("Plan Format", "").strip() == CURRENT_PLAN_FORMAT:
        return _validate_living_plan(sections, path)
    return _validate_task_contract_v1_plan(sections, path)


def _validate_living_plan(sections: dict[str, str], path: Path | None) -> list[str]:
    errors: list[str] = []
    _require_sections(sections, PLAN_V2_REQUIRED_SECTIONS, errors, path)
    for section in PLAN_V2_REQUIRED_SECTIONS:
        if section in sections and not sections[section].strip():
            errors.append(f"{_label(path)}{section} must not be empty")
    status = _plain_status(sections.get("Document Status", ""))
    if status not in PLAN_STATUSES:
        errors.append(f"{_label(path)}invalid or empty plan status {status!r}")

    _validate_task_contracts(sections.get("Task Breakdown", ""), status, path, errors)
    criterion_ids = _acceptance_criterion_ids(sections.get("Acceptance Criteria", ""), path, errors)
    test_plan = sections.get("Test Plan", "")
    for criterion_id in criterion_ids:
        if not re.search(rf"\b{criterion_id}\b", test_plan):
            errors.append(f"{_label(path)}Test Plan does not cover {criterion_id}")
    _validate_log_entries(sections.get("Implementation Log", ""), path, errors)

    outcome = sections.get("Outcome", "")
    if status == "complete":
        if re.match(r"(?i)\s*pending\b", outcome):
            errors.append(f"{_label(path)}complete plan Outcome must not be pending")
        for criterion_id in criterion_ids:
            if not re.search(rf"\b{criterion_id}\b", outcome):
                errors.append(f"{_label(path)}complete plan Outcome does not report {criterion_id}")
    return errors


def _acceptance_criterion_ids(criteria: str, path: Path | None, errors: list[str]) -> list[str]:
    numbers = [int(number) for number in re.findall(r"(?m)^[ \t]*(?:[-*][ \t]*)?\**AC-(\d+)\b", criteria)]
    if not numbers:
        errors.append(f"{_label(path)}Acceptance Criteria must define AC-1 and onward")
    elif numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"{_label(path)}Acceptance Criteria IDs must be sequential starting at AC-1")
    return [f"AC-{number}" for number in numbers]


def _validate_log_entries(log: str, path: Path | None, errors: list[str]) -> None:
    headings = list(re.finditer(r"(?m)^###[ \t]+(.*)$", log))
    for index, heading in enumerate(headings):
        title = heading.group(1).strip()
        label = f"{_label(path)}Implementation Log entry {title!r}"
        date_match = re.match(r"(\d{4}-\d{2}-\d{2}) - \S", title)
        try:
            dt.date.fromisoformat(date_match.group(1) if date_match else "")
        except ValueError:
            errors.append(f"{label} must be titled 'YYYY-MM-DD - Title'")
        end = headings[index + 1].start() if index + 1 < len(headings) else len(log)
        entry = log[heading.end():end]
        for field in PLAN_LOG_ENTRY_FIELDS:
            match = re.search(rf"(?mi)^[ \t]*(?:-[ \t]*)?{field}:[ \t]*(.*)$", entry)
            if not match or not match.group(1).strip():
                errors.append(f"{label} missing {field}")


def _validate_task_contract_v1_plan(sections: dict[str, str], path: Path | None) -> list[str]:
    errors: list[str] = []
    _require_sections(sections, PLAN_REQUIRED_SECTIONS, errors, path)
    status = _plain_status(sections.get("Document Status", ""))
    if status not in PLAN_STATUSES:
        errors.append(f"{_label(path)}invalid or empty plan status {status!r}")

    breakdown = sections.get("Task Breakdown", "")
    plan_format = sections.get("Plan Format", "").strip()
    if plan_format and plan_format != "task-contract-v1":
        errors.append(f"{_label(path)}unsupported Plan Format {plan_format!r}")
    # Unversioned literal-patch plans keep their original whole-plan checks.
    # Their non-edit delivery tasks predate the per-task contract format.
    if not plan_format and "#### Code Edit" in breakdown:
        if not re.search(r"(?m)^###\s+Task\s+\d+\b", breakdown):
            errors.append(f"{_label(path)}Task Breakdown must include ordered task headings")
        _validate_legacy_code_edits(breakdown, status, path, errors)
        return errors

    has_contract = _validate_task_contracts(breakdown, status, path, errors)

    if has_contract or plan_format == "task-contract-v1":
        for section in PLAN_REQUIRED_SECTIONS:
            if section in sections and not sections[section].strip():
                errors.append(f"{_label(path)}{section} must not be empty")
    return errors


def _is_test_command(command: str) -> bool:
    invocation = command.strip().lstrip("`").split("`", 1)[0]
    try:
        tokens = shlex.split(invocation, posix=False)
    except ValueError:
        return True  # An unparseable invocation cannot establish application execution.
    if not tokens:
        return True
    executable = re.split(r"[/\\]", tokens[0].strip("\"'"))[-1].lower().removesuffix(".exe")
    arguments = [token.strip("\"'") for token in tokens[1:]]
    if executable in {"pytest", "jest", "vitest"}:
        return True
    if re.fullmatch(r"python(?:\d+(?:\.\d+)*)?|py", executable):
        return any(argument == "-m" and arguments[index + 1] in {"unittest", "pytest"}
                   for index, argument in enumerate(arguments[:-1]))
    if executable in {"gradle", "gradlew", "gradlew.bat", "mvn", "mvnw", "mvnw.cmd"}:
        return any(argument.rsplit(":", 1)[-1] == "test" for argument in arguments)
    if executable in {"cargo", "go", "dotnet", "npm", "pnpm", "yarn", "npx"}:
        subcommands = [argument for argument in arguments if not argument.startswith("-")]
        return bool(subcommands) and (
            subcommands[0] in {"test", "jest", "vitest"}
            or subcommands[:2] in (["run", "test"], ["exec", "jest"], ["exec", "vitest"])
        )
    return False


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

    local_commands = re.finditer(LOCAL_COMMAND_PATTERN, app_context)
    has_application_command = any(
        not _is_test_command(command.group("command"))
        for command in local_commands
    )
    has_local_app_run = has_application_command or _matches_any(app_context, LOCAL_APP_RUN_PATTERNS)
    has_runtime_data = _matches_any(data_sent, RUNTIME_DATA_PATTERNS)
    has_runtime_response = _matches_any(response_received, RUNTIME_RESPONSE_PATTERNS)
    mentions_unit_tests = _matches_any(report_body, UNIT_TEST_ONLY_PATTERNS)

    if status == "complete":
        if not has_local_app_run:
            errors.append(
                f"{_label(path)}complete test report must identify the local application command, runtime, port, or base URL under test"
            )
        if not has_runtime_data:
            errors.append(
                f"{_label(path)}complete test report Data Sent must describe a request, UI input, command arguments, fixture input, or queue message"
            )
        if not has_runtime_response:
            errors.append(
                f"{_label(path)}complete test report Response Received must describe an application response, UI result, exit status, output artifact, worker result, or log output"
            )
    if status == "complete" and mentions_unit_tests and not (
        has_local_app_run and has_runtime_data and has_runtime_response
    ):
        errors.append(
            f"{_label(path)}test reports are for local app verification; unit test output alone is not sufficient evidence"
        )

    return errors
