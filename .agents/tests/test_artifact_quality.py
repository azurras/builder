from __future__ import annotations

import sys
import importlib.util
import subprocess
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents" / "lib"))

from artifact_quality import validate_implementation_plan_text, validate_test_report_text


VALID_PLAN = """# Sample Plan

## Document Status
ready-for-execution

## Objective
Ship the change.

## Goals
- Goal one.

## Inputs
- Issue 42.

## Branch
`codex/sample-plan`

## Non-Goals
- None.

## Assumptions
- Tests exist.

## Open Questions
None.

## Task Breakdown

### Task 1 - Replace config fallback

Sequence / dependencies:
- First task.

Implementation notes:
- Replace the fallback.

#### Code Edit 1.1
- File: `src/main/java/App.java`
- Lines: 42-58
- Action: replace

Current:
```java
String secret = "fallback";
```

Proposed:
```java
String secret = requiredSecret();
```

Verification:
- `./gradlew test`

## Code Changes
- Task 1.1 replaces `src/main/java/App.java`.

## Files and Modules
- `src/main/java/App.java`

## Unit Testing
- `./gradlew test`

## Local Testing
- Start the app and hit `/health`.

## Validation
- Tests and local check pass.

## Rollback or Recovery
- Revert the commit.

## Risks
- Low.

## Completion Criteria
- PR merged.
"""


class ArtifactQualityTests(unittest.TestCase):
    def contract_plan(self) -> str:
        start = VALID_PLAN.index("### Task 1")
        end = VALID_PLAN.index("## Code Changes")
        return VALID_PLAN[:start].replace("## Document Status", "## Plan Format\ntask-contract-v1\n\n## Document Status") + """### Task 1 - Reject missing configuration
Dependencies: None; first task.
Files: `src/main/java/App.java`
Symbols: `App.requiredSecret`
Inspection: Read implementation and caller at baseline commit abc1234.
Required skill: write-chris-street-style-code before code edits.
Behavior: Reject missing configuration at startup.
Invariants: No fallback secret is accepted.
Boundary/API: Keep existing startup configuration interface.
Effects and failures: Missing input fails startup with a redacted error.
Tests and evidence: Regression for absent secret; valid configuration remains accepted.
Verification: `./gradlew test --tests AppTest`

""" + VALID_PLAN[end:]

    def test_save_cli_accepts_contract_and_refuses_incomplete_task_before_write(self) -> None:
        script = ROOT / ".agents/skills/write-implementation-plan/scripts/save_implementation_plan.py"
        with tempfile.TemporaryDirectory() as directory:
            for title, content, expected in (("Valid", self.contract_plan(), 0), ("Invalid", self.contract_plan().replace("Symbols: `App.requiredSecret`", "Symbols:"), 1)):
                result = subprocess.run([sys.executable, str(script), "--root", directory, "--date", "2099-04-05", "--title", title], input=content, text=True, capture_output=True)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                artifact = Path(directory) / "docs/implementation-plans" / f"2099-04-05-{title.lower()}.md"
                self.assertEqual(artifact.exists(), expected == 0)

    def test_hub_validates_new_plans_without_literal_code_edits(self) -> None:
        script = ROOT / ".agents/skills/maintain-builder-hub/scripts/validate_hub_state.py"
        spec = importlib.util.spec_from_file_location("hub_validation", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in module.ARTIFACT_DIRS:
                (root / name).mkdir(parents=True, exist_ok=True)
            for name in module.INDEX_FILES:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("# Fixture\n", encoding="utf-8")
            plan = root / "docs/implementation-plans/2099-04-05-new-plan.md"
            for content, expected in ((self.contract_plan(), 0), ("# Vague new plan\nDo something.\n", 1)):
                plan.write_text(content, encoding="utf-8")
                result = subprocess.run([sys.executable, str(script), "--root", str(root)], text=True, capture_output=True)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_inspected_symbol_contract_does_not_require_literal_patch(self) -> None:
        self.assertEqual(validate_implementation_plan_text(self.contract_plan()), [])

    def test_contract_requires_each_actionable_field(self) -> None:
        import re
        for field in ("Dependencies", "Files", "Symbols", "Inspection", "Behavior", "Invariants", "Boundary/API", "Effects and failures", "Tests and evidence", "Verification"):
            with self.subTest(field=field):
                invalid = re.sub(rf"(?m)^{re.escape(field)}:.*$", f"{field}:", self.contract_plan())
                self.assertTrue(any(field in error for error in validate_implementation_plan_text(invalid)))

    def test_each_task_needs_its_own_contract_or_patch(self) -> None:
        invalid = self.contract_plan().replace("## Code Changes", "### Task 2 - Unspecified work\nDo something later.\n\n## Code Changes")
        self.assertTrue(any("Task 2" in error for error in validate_implementation_plan_text(invalid)))

    def test_legacy_plan_retains_non_edit_delivery_tasks(self) -> None:
        historical = VALID_PLAN.replace("## Code Changes", "### Task 2 - Publish verified result\nRun the existing delivery workflow after Task 1.\n\n## Code Changes")
        self.assertEqual(validate_implementation_plan_text(historical), [])

    def test_versioned_literal_plan_requires_nonempty_document_sections(self) -> None:
        import re
        versioned = VALID_PLAN.replace("## Document Status", "## Plan Format\ntask-contract-v1\n\n## Document Status")
        for section in ("Risks", "Branch", "Rollback or Recovery"):
            with self.subTest(section=section):
                invalid = re.sub(rf"(?ms)(^## {re.escape(section)}\n).*?(?=^## |\Z)", r"\1\n", versioned)
                self.assertTrue(any(section in error for error in validate_implementation_plan_text(invalid)))

    def test_ready_contract_rejects_unresolved_inspection(self) -> None:
        invalid = self.contract_plan().replace("Read implementation and caller at baseline commit abc1234.", "pending file inspection")
        self.assertTrue(any("Inspection" in error for error in validate_implementation_plan_text(invalid)))

    def test_status_must_be_present_and_nonempty(self) -> None:
        invalid = self.contract_plan().replace("ready-for-execution", "")
        self.assertTrue(any("status" in error.lower() for error in validate_implementation_plan_text(invalid)))

    def test_valid_implementation_plan_passes(self) -> None:
        self.assertEqual(validate_implementation_plan_text(VALID_PLAN), [])

    def test_ready_plan_rejects_pending_line_ranges(self) -> None:
        invalid = VALID_PLAN.replace("- Lines: 42-58", "- Lines: line range pending file inspection")

        errors = validate_implementation_plan_text(invalid)

        self.assertTrue(any("line range pending" in error for error in errors), errors)

    def test_plan_rejects_task_without_code_edit(self) -> None:
        invalid = VALID_PLAN.replace("#### Code Edit 1.1", "#### Edit 1.1")

        errors = validate_implementation_plan_text(invalid)

        self.assertTrue(any("Code Edit" in error for error in errors), errors)

    def local_execution_report(self, run_details: str, inputs: str, results: str) -> str:
        return f"""# Local Application Report

## Document Status
complete

## Story/Issue
Generic application verification

## Branch
Candidate commit abc1234

## App / Environment
Candidate checkout with isolated fixture directory.

## Local Run Details
{run_details}

## Test Cases
Representative changed application behavior.

## Data Sent
{inputs}

## Response Received
{results}

## Pass / Fail
PASS: expected fixture result observed.

## Evidence
Captured command, candidate identity, result and owned fixture cleanup.

## Bugs / Follow-ups
None.
"""

    def test_complete_reports_accept_non_http_application_execution(self) -> None:
        scenarios = (
            ("Local command: `python -m export_tool source.csv result.json`.",
             "Command arguments: source.csv and result.json; input file contains two rows.",
             "Exit code: 0; output file result.json contains the two expected records."),
            ("Local worker launch: `./queue-worker --queue fixture-jobs --once`.",
             "Queue message: job-42 with isolated destination fixture-output.",
             "Worker result: job-42 completed; output artifact has the expected contents."),
            ("Local desktop launch: `./editor fixture.txt`.",
             "UI input: changed text, clicked Save.",
             "UI result: saved; output file fixture.txt contains the changed text."),
            ("Local consumer run: `./examples/library-consumer fixture.json`.",
             "Consumer input: fixture.json with two representative records.",
             "Exit status: 0; stdout contains the expected transformed records."),
        )
        for run_details, inputs, results in scenarios:
            with self.subTest(run=run_details):
                self.assertEqual(validate_test_report_text(
                    self.local_execution_report(run_details, inputs, results)), [])

    def test_non_http_report_still_requires_execution_input_and_result(self) -> None:
        complete_fields = (
            "Local command: `./exporter source.csv result.json`.",
            "Command arguments: source.csv and result.json.",
            "Exit code: 0; output file result.json contains expected records.",
        )
        for index, replacement in enumerate(("No application was run.", "No input recorded.", "No result recorded.")):
            with self.subTest(missing=index):
                incomplete_fields = list(complete_fields)
                incomplete_fields[index] = replacement
                self.assertTrue(validate_test_report_text(self.local_execution_report(*incomplete_fields)))

    def test_local_command_labels_do_not_turn_unit_tests_into_application_execution(self) -> None:
        for command in ("pytest -q", "python -m unittest discover", "python -B -m unittest discover",
                        "python3 -m unittest discover", "cargo test --lib", "dotnet test"):
            with self.subTest(command=command):
                report = self.local_execution_report(
                    f"Local command: `{command}`.",
                    "Command arguments: native test options; ran unit tests only.",
                    "Exit code: 0; stdout: all unit tests passed.",
                )
                self.assertTrue(validate_test_report_text(report))

    def test_report_accepts_application_execution_alongside_unit_tests(self) -> None:
        report = self.local_execution_report(
            "Local command: `pytest -q`.\nLocal command: `./exporter source.csv result.json`.",
            "Command arguments: source.csv and result.json.",
            "Exit code: 0; output file result.json contains expected records.",
        )
        self.assertEqual(validate_test_report_text(report), [])

    def test_application_arguments_can_contain_test_runner_names(self) -> None:
        report = self.local_execution_report(
            "Local command: `./exporter pytest-results.csv result.json`.",
            "Command arguments: pytest-results.csv and result.json.",
            "Exit code: 0; output file result.json contains expected records.",
        )
        self.assertEqual(validate_test_report_text(report), [])

    def test_test_report_requires_request_response_evidence(self) -> None:
        report = """# Report

## Document Status
complete

## Story/Issue
Issue 42

## Branch
`codex/issue-42`

## App / Environment
localhost:8080

## Local Run Details
`./gradlew bootRun`

## Test Cases
- Login works.

## Data Sent

## Response Received

## Pass / Fail
- PASS

## Evidence

## Bugs / Follow-ups
None.
"""

        errors = validate_test_report_text(report)

        self.assertTrue(any("Data Sent" in error for error in errors), errors)
        self.assertTrue(any("Response Received" in error for error in errors), errors)
        self.assertTrue(any("Evidence" in error for error in errors), errors)

    def test_test_report_rejects_unit_test_only_evidence(self) -> None:
        report = """# Report

## Document Status
complete

## Story/Issue
Issue 42

## Branch
`codex/issue-42`

## App / Environment
Local checkout.

## Local Run Details
No app was started.

## Test Cases
- Ran unit tests.

## Data Sent
```bash
./gradlew test
```

## Response Received
```text
BUILD SUCCESSFUL
```

## Pass / Fail
- PASS: unit tests passed.

## Evidence
- `./gradlew test`

## Bugs / Follow-ups
None.
"""

        errors = validate_test_report_text(report)

        self.assertTrue(any("local app" in error.lower() for error in errors), errors)

    def test_blocked_test_report_can_record_missing_local_app_testing(self) -> None:
        report = """# Report

## Document Status
blocked

## Story/Issue
Issue 42

## Branch
`codex/issue-42`

## App / Environment
Local checkout only.

## Local Run Details
No app was started because configuration was missing.

## Test Cases
- Unit tests were run, but local app testing is blocked.

## Data Sent
No endpoint request or UI input was sent.

## Response Received
No runtime response was received.

## Pass / Fail
- BLOCKED: local app testing was not performed.

## Evidence
- `./gradlew test` passed before the runtime blocker was found.

## Bugs / Follow-ups
Start the app locally and hit an endpoint before closure.
"""

        self.assertEqual(validate_test_report_text(report), [])


if __name__ == "__main__":
    unittest.main()
