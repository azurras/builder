from __future__ import annotations

import re
import sys
import importlib.util
import subprocess
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents" / "lib"))

from artifact_quality import project_of, validate_implementation_plan_text, validate_test_report_text
from builder_hub import markdown_links
from project_registry_fixture import write_project_registry


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

    def test_hub_validates_new_plans_without_literal_code_edits(self) -> None:
        script = ROOT / ".agents/skills/publish-builder-changes/scripts/validate_hub_state.py"
        spec = importlib.util.spec_from_file_location("hub_validation", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_project_registry(root)
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

    def test_markdown_links_ignore_code_spans_and_fences(self) -> None:
        markdown = (
            "See the [plan](plan.md) and `[this](std::stop_token token)`.\n"
            "```cpp\nauto worker = [this](std::stop_token token) {};\n```\n"
            "Then the [report](report.md).\n"
        )
        self.assertEqual(markdown_links(markdown), ["plan.md", "report.md"])

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


LIVING_PLAN = """# Sample Living Plan

## Plan Format
task-contract-v2

## Document Status
ready-for-execution

## Project
builder

## Objective
Reject startup when the signing secret is missing.

## Background
The app silently falls back to a shared development secret.

## Goals
- Startup fails fast without `JWT_SECRET`, measured by AC-1.

## Non-Goals
- Rotating existing secrets: operations owns rotation.

## Acceptance Criteria
- AC-1: Starting without `JWT_SECRET` exits with a redacted error.
- AC-2: Starting with `JWT_SECRET` serves `/health` with 200.

## Inputs
Issue 42.

## Branch
`codex/issue-42-require-secret` from `main`.

## Assumptions
Configuration loads through `App.requiredSecret`.

## Open Questions
None.

## Design
Replace the fallback with a required lookup. Rejected: logging a warning, because the app would still run insecurely.

## Expected Changes
- `src/main/java/App.java`: required secret lookup.

## Task Breakdown

### Task 1 - Reject missing configuration
Dependencies: None; first task.
Files: `src/main/java/App.java`
Symbols: `App.requiredSecret`
Inspection: Read implementation and caller at baseline commit abc1234.
Behavior: Reject missing configuration at startup.
Invariants: No fallback secret is accepted.
Boundary/API: Keep existing startup configuration interface.
Effects and failures: Missing input fails startup with a redacted error.
Tests and evidence: Regression for absent secret; valid configuration remains accepted.
Verification: `./gradlew test --tests AppTest`

## Test Plan
- AC-1: `AppTest.rejectsMissingSecret`, then start locally without the variable.
- AC-2: Start locally with the variable and request `/health`.

## Rollback or Recovery
Revert the commit.

## Risks
Developers without `JWT_SECRET` must set one.

## Implementation Log
No entries yet.

## Outcome
Pending.
"""

LOG_ENTRY = """- Change: Read the secret through `Environment` instead of `System.getenv`.
- Reason: Tests inject configuration through `Environment`.
- Impact: Task 1 Symbols updated; no acceptance change.
"""


class LivingPlanTests(unittest.TestCase):
    save_script = ROOT / ".agents/skills/write-implementation-plan/scripts/save_implementation_plan.py"
    log_script = ROOT / ".agents/skills/write-implementation-plan/scripts/log_plan_change.py"

    def errors_for(self, plan: str) -> list[str]:
        return validate_implementation_plan_text(plan)

    def without_section(self, section: str) -> str:
        return re.sub(rf"(?ms)^## {re.escape(section)}\n.*?(?=^## |\Z)", "", LIVING_PLAN)

    def completed_plan(self, outcome: str) -> str:
        return LIVING_PLAN.replace("ready-for-execution", "complete").replace("## Outcome\nPending.", f"## Outcome\n{outcome}")

    def run_script(self, script: Path, *arguments: str, stdin: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *arguments], input=stdin, text=True, capture_output=True)

    def test_living_plan_passes(self) -> None:
        self.assertEqual(self.errors_for(LIVING_PLAN), [])

    def test_living_plan_requires_each_section(self) -> None:
        for section in ("Background", "Non-Goals", "Acceptance Criteria", "Design", "Expected Changes",
                        "Test Plan", "Implementation Log", "Outcome"):
            with self.subTest(section=section):
                errors = self.errors_for(self.without_section(section))
                self.assertIn(f"missing required section: {section}", errors)

    def test_acceptance_criteria_must_be_sequential(self) -> None:
        criteria_lines = ("- AC-1: Starting without `JWT_SECRET` exits with a redacted error.\n"
                          "- AC-2: Starting with `JWT_SECRET` serves `/health` with 200.")
        for criteria in ("- Starting fails without a secret.", "- AC-1: Fails.\n- AC-3: Serves health."):
            with self.subTest(criteria=criteria):
                invalid = LIVING_PLAN.replace(criteria_lines, criteria)
                self.assertTrue(any("Acceptance Criteria" in error for error in self.errors_for(invalid)))

    def test_test_plan_must_cover_every_criterion(self) -> None:
        invalid = LIVING_PLAN.replace("- AC-2: Start locally", "- Start locally")
        self.assertEqual(self.errors_for(invalid), ["Test Plan does not cover AC-2"])

    def test_log_entries_need_date_and_change_reason_impact(self) -> None:
        without_reason = LOG_ENTRY.replace("- Reason: Tests inject configuration through `Environment`.\n", "")
        cases = (
            ("### Switched config source\n" + LOG_ENTRY, "must be titled 'YYYY-MM-DD - Title'"),
            ("### 2026-10-04 - Switched config source\n" + without_reason, "missing Reason"),
        )
        for log, expected in cases:
            with self.subTest(expected=expected):
                invalid = LIVING_PLAN.replace("## Implementation Log\nNo entries yet.", f"## Implementation Log\n{log}")
                errors = self.errors_for(invalid)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_complete_plan_reports_every_criterion(self) -> None:
        self.assertEqual(self.errors_for(self.completed_plan("- AC-1: Met.\n- AC-2: Met.")), [])
        self.assertIn("complete plan Outcome must not be pending", self.errors_for(self.completed_plan("Pending.")))
        self.assertEqual(self.errors_for(self.completed_plan("- AC-1: Met.")),
                         ["complete plan Outcome does not report AC-2"])

    def test_unknown_plan_format_is_still_rejected(self) -> None:
        unknown = LIVING_PLAN.replace("task-contract-v2", "task-contract-v9")
        self.assertTrue(any("unsupported Plan Format" in error for error in self.errors_for(unknown)))

    def test_save_cli_requires_current_format_for_new_plans(self) -> None:
        v1_plan = ArtifactQualityTests().contract_plan()
        with tempfile.TemporaryDirectory() as directory:
            write_project_registry(Path(directory))
            plans = Path(directory) / "docs/implementation-plans"
            cases = (
                ("Living", LIVING_PLAN, 0),
                ("Incomplete", LIVING_PLAN.replace("Symbols: `App.requiredSecret`", "Symbols:"), 1),
                ("Contract", v1_plan, 1),
            )
            for title, content, expected in cases:
                with self.subTest(title=title):
                    result = self.run_script(self.save_script, "--root", directory, "--date", "2099-04-05",
                                             "--title", title, stdin=content)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    saved_names = {path.name for path in plans.glob("*.md")} if plans.exists() else set()
                    self.assertEqual(f"2099-04-05-builder-{title.lower()}.md" in saved_names, expected == 0)
                    self.assertNotIn(f"2099-04-05-{title.lower()}.md", saved_names)

            existing_v1_plan = plans / "2099-04-05-existing.md"
            existing_v1_plan.write_text(v1_plan, encoding="utf-8")
            replaced = self.run_script(self.save_script, "--root", directory, "--date", "2099-04-05",
                                       "--title", "Existing", "--overwrite",
                                       stdin=v1_plan.replace("Ship the change.", "Ship it."))
            self.assertEqual(replaced.returncode, 0, replaced.stdout + replaced.stderr)
            self.assertIn("Ship it.", existing_v1_plan.read_text(encoding="utf-8"))

    def test_save_cli_names_the_project_in_new_plans(self) -> None:
        unlabeled_plan = LIVING_PLAN.replace("## Project\nbuilder\n\n", "")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_project_registry(root, active=("home-lab",), retired=("old-shop",))
            plans = root / "docs/implementation-plans"
            refusals = (
                ("Unlabeled", unlabeled_plan, "need a Project section"),
                ("Unknown", LIVING_PLAN.replace("## Project\nbuilder", "## Project\nstranger"), "Unknown project"),
                ("Retired", LIVING_PLAN.replace("## Project\nbuilder", "## Project\nold-shop"), "retired"),
            )
            for title, content, expected_message in refusals:
                with self.subTest(title=title):
                    result = self.run_script(self.save_script, "--root", directory, "--date", "2099-04-05",
                                             "--title", title, stdin=content)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(expected_message, result.stderr)
            self.assertFalse(plans.exists())

            standalone_plan = LIVING_PLAN.replace("## Project\nbuilder", "## Project\n`home-lab`")
            # The second title already starts with the project, so it names the same file instead of doubling it.
            for title in ("Router upgrade", "Home lab router upgrade"):
                with self.subTest(title=title):
                    result = self.run_script(self.save_script, "--root", directory, "--date", "2099-04-05",
                                             "--title", title, "--overwrite", stdin=standalone_plan)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual([path.name for path in plans.glob("*.md")], ["2099-04-05-home-lab-router-upgrade.md"])

            historical_plan = plans / "2099-04-05-historical.md"
            historical_plan.write_text(unlabeled_plan, encoding="utf-8")
            replaced = self.run_script(self.save_script, "--root", directory, "--date", "2099-04-05",
                                       "--title", "Historical", "--overwrite",
                                       stdin=unlabeled_plan.replace("Pending.", "Still pending."))
            self.assertEqual(replaced.returncode, 0, replaced.stdout + replaced.stderr)
            self.assertIn("Still pending.", historical_plan.read_text(encoding="utf-8"))

    def test_project_section_holds_one_slug(self) -> None:
        self.assertEqual(project_of(LIVING_PLAN), "builder")
        self.assertIsNone(project_of(LIVING_PLAN.replace("## Project\nbuilder\n\n", "")))
        invalid = LIVING_PLAN.replace("## Project\nbuilder", "## Project\nBuilder hub")
        self.assertEqual(self.errors_for(invalid),
                         ["Project must be one lowercase hyphenated project slug, not 'Builder hub'"])

    def test_log_helper_appends_entries_in_order_and_sets_status(self) -> None:
        crlf_entry = LOG_ENTRY.strip().replace("\n", "\r\n")
        with tempfile.TemporaryDirectory() as directory:
            plan_file = Path(directory) / "plan.md"
            plan_file.write_bytes(LIVING_PLAN.replace("\n", "\r\n").encode("utf-8"))
            for title, status in (("Switched config source", "in-progress"), ("Added health retry", None)):
                status_arguments = ["--status", status] if status else []
                result = self.run_script(self.log_script, "--plan", str(plan_file), "--date", "2026-10-04",
                                         "--title", title, *status_arguments, stdin=LOG_ENTRY)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            updated_plan = plan_file.read_bytes().decode("utf-8")
            expected_ending = ("## Implementation Log\r\n\r\n"
                               "### 2026-10-04 - Switched config source\r\n\r\n" + crlf_entry + "\r\n\r\n"
                               "### 2026-10-04 - Added health retry\r\n\r\n" + crlf_entry + "\r\n\r\n"
                               "## Outcome\r\nPending.\r\n")
            self.assertTrue(updated_plan.endswith(expected_ending), updated_plan[-700:])
            untouched_prefix = LIVING_PLAN[:LIVING_PLAN.index("## Implementation Log")]
            expected_prefix = untouched_prefix.replace("ready-for-execution", "in-progress").replace("\n", "\r\n")
            self.assertTrue(updated_plan.startswith(expected_prefix))
            self.assertEqual(validate_implementation_plan_text(updated_plan), [])

    def test_log_helper_creates_missing_section_before_outcome(self) -> None:
        v1_plan = ArtifactQualityTests().contract_plan() + "\n## Outcome\nPending.\n"
        with tempfile.TemporaryDirectory() as directory:
            plan_file = Path(directory) / "plan.md"
            plan_file.write_text(v1_plan, encoding="utf-8", newline="\n")
            result = self.run_script(self.log_script, "--plan", str(plan_file), "--date", "2026-10-04",
                                     "--title", "Closed out", stdin=LOG_ENTRY)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            updated_plan = plan_file.read_text(encoding="utf-8")
            self.assertIn("## Implementation Log\n\n### 2026-10-04 - Closed out\n\n- Change:", updated_plan)
            self.assertLess(updated_plan.index("## Implementation Log"), updated_plan.index("## Outcome"))

    def test_log_helper_leaves_plan_unchanged_when_result_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plan_file = Path(directory) / "plan.md"
            plan_file.write_text(LIVING_PLAN, encoding="utf-8", newline="\n")
            original_bytes = plan_file.read_bytes()
            cases = (
                (["--status", "finished"], LOG_ENTRY, 2),
                ([], "- Change: Something without a reason.", 1),
                (["--status", "complete"], LOG_ENTRY, 1),
            )
            for extra_arguments, entry, expected in cases:
                with self.subTest(arguments=extra_arguments, entry=entry):
                    result = self.run_script(self.log_script, "--plan", str(plan_file), "--title", "Attempt",
                                             *extra_arguments, stdin=entry)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    self.assertEqual(plan_file.read_bytes(), original_bytes)


PLAIN_CRITERIA = ("- AC-1: Starting without `JWT_SECRET` exits with a redacted error.\n"
                  "- AC-2: Starting with `JWT_SECRET` serves `/health` with 200.")

TABLE_CRITERIA = ("| ID | Done when |\n"
                  "|---|---|\n"
                  "| **AC-1** | Starting without `JWT_SECRET` exits with a redacted error. |\n"
                  "| AC-2 | Starting with `JWT_SECRET` serves `/health` with 200. |")

PLAIN_TASK_CONTRACT = LIVING_PLAN[LIVING_PLAN.index("Dependencies:"):LIVING_PLAN.index("\n\n## Test Plan")]

TABLE_TASK_CONTRACT = """| Contract | Detail |
|---|---|
| **Dependencies** | None; first task. |
| **Files** | `src/main/java/App.java` |
| **Symbols** | `App.requiredSecret` |
| **Inspection** | Read implementation and caller at baseline commit abc1234. |
| Behavior | Reject missing configuration at startup. |
| Invariants | No fallback secret is accepted. |
| Boundary/API | Keep existing startup configuration interface. |
| Effects and failures | Missing input fails startup with a redacted error. |
| Tests and evidence | Regression for absent secret; valid configuration remains accepted. |
| Verification | `./gradlew test --tests AppTest` |"""

BOLD_LOG_ENTRY = """### 2026-10-04 - Read the secret through Environment

- **Change:** Read the secret through `Environment` instead of `System.getenv`.
- **Reason:** Tests inject configuration through `Environment`.
- **Impact:** Task 1 Symbols updated; no acceptance change.
"""


def pretty_living_plan() -> str:
    return (LIVING_PLAN.replace(PLAIN_CRITERIA, TABLE_CRITERIA)
            .replace(PLAIN_TASK_CONTRACT, TABLE_TASK_CONTRACT)
            .replace("## Implementation Log\nNo entries yet.", f"## Implementation Log\n{BOLD_LOG_ENTRY}"))


def markdown_tables(markdown: str) -> list[list[str]]:
    """Each run of consecutive table rows, including rows inside a fenced skeleton, as a list of rows."""
    tables: list[list[str]] = []
    rows: list[str] = []
    for line in markdown.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            rows.append(line.strip())
            continue
        if rows:
            tables.append(rows)
            rows = []
    return tables


def table_cell_count(row: str) -> int:
    return len(re.split(r"(?<!\\)\|", row.strip().strip("|")))


class PresentationFormTests(unittest.TestCase):
    """Readable Markdown forms validate exactly as their plain equivalents do."""

    plan_example = ROOT / ".agents/skills/write-implementation-plan/references/example.md"
    report_example = ROOT / ".agents/skills/write-test-report/references/example.md"
    report_template = ROOT / ".agents/skills/write-test-report/references/template.md"

    def test_table_and_bold_plan_forms_validate(self) -> None:
        pretty_plan = pretty_living_plan()

        self.assertNotIn("Dependencies:", pretty_plan)
        self.assertEqual(validate_implementation_plan_text(pretty_plan), [])

    def test_table_and_bold_plan_forms_still_require_values(self) -> None:
        pretty_plan = pretty_living_plan()
        cases = (
            (pretty_plan.replace("| Behavior | Reject missing configuration at startup. |", "| Behavior | |"),
             "Task 1 missing Behavior"),
            (pretty_plan.replace("| AC-2 | Starting", "| AC-3 | Starting"), "Acceptance Criteria IDs must be sequential"),
            (pretty_plan.replace("- **Reason:** Tests inject configuration through `Environment`.\n", ""),
             "missing Reason"),
        )
        for invalid_plan, expected_error in cases:
            with self.subTest(expected_error=expected_error):
                errors = validate_implementation_plan_text(invalid_plan)
                self.assertTrue(any(expected_error in error for error in errors), errors)

    def report_run_by(self, run_details: str) -> str:
        return ArtifactQualityTests().local_execution_report(
            run_details,
            "Command arguments: source.csv and result.json.",
            "Exit code: 0; output file result.json contains the two expected records.",
        )

    def test_bold_and_table_local_command_labels_prove_a_run(self) -> None:
        for run_details in ("- **Local command:** `python -m export_tool source.csv result.json`",
                            "- **Local command**: `python -m export_tool source.csv result.json`",
                            "| Setting | Value |\n|---|---|\n| **Local command** | `./queue-worker --once` |"):
            with self.subTest(run_details=run_details):
                self.assertEqual(validate_test_report_text(self.report_run_by(run_details)), [])

    def test_bold_and_table_test_runner_labels_do_not_prove_a_run(self) -> None:
        for run_details in ("- **Local command:** `pytest tests`",
                            "| **Local command** | `./gradlew test` |"):
            with self.subTest(run_details=run_details):
                errors = validate_test_report_text(self.report_run_by(run_details))
                self.assertTrue(any("local application command" in error for error in errors), errors)

    def test_environment_table_port_identifies_a_local_run(self) -> None:
        report = self.report_run_by("Started from the candidate checkout.").replace(
            "Candidate checkout with isolated fixture directory.",
            "| Setting | Value |\n|---|---|\n| Port | 8081 |")

        self.assertEqual(validate_test_report_text(report), [])

    def test_reference_examples_validate(self) -> None:
        self.assertEqual(validate_implementation_plan_text(self.plan_example.read_text(encoding="utf-8")), [])
        self.assertEqual(validate_test_report_text(self.report_example.read_text(encoding="utf-8")), [])

    def test_helpers_store_utf8_stdin_unchanged(self) -> None:
        marked_text = "✅ Met — café"
        plan = pretty_living_plan().replace("shared development secret.", f"shared development secret. {marked_text}")
        report = self.report_run_by("- **Local command:** `./export-tool in.csv`").replace("PASS:", f"{marked_text} PASS:")
        scripts = ROOT / ".agents/skills"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_project_registry(root)
            report_with_project = report.replace("## Story/Issue", "## Project\nbuilder\n\n## Story/Issue")
            saved_plan = root / "docs/implementation-plans/2099-04-05-builder-encoding.md"
            runs = (
                ("save plan", [scripts / "write-implementation-plan/scripts/save_implementation_plan.py",
                               "--root", directory, "--date", "2099-04-05", "--title", "Encoding"], plan,
                 saved_plan),
                ("log plan change", [scripts / "write-implementation-plan/scripts/log_plan_change.py",
                                     "--plan", str(saved_plan), "--date", "2099-04-06", "--title", "Logged"],
                 f"- **Change:** {marked_text}\n- **Reason:** Probe.\n- **Impact:** None.", saved_plan),
                ("save report", [scripts / "write-test-report/scripts/save_test_report.py",
                                 "--root", directory, "--date", "2099-04-05", "--title", "Encoding"],
                 report_with_project, root / "docs/test-reports/2099-04-05-builder-encoding.md"),
                ("save memory", [scripts / "save-session-memory/scripts/save_session_memory.py",
                                 "--root", directory, "--project", "builder", "--title", "Probe",
                                 "--date", "2099-04-05", "--time", "09:00"],
                 f"- {marked_text}", root / "docs/session-memory/2099-04-05.md"),
            )
            for name, arguments, stdin_text, stored_file in runs:
                with self.subTest(helper=name):
                    result = subprocess.run([sys.executable, *map(str, arguments)],
                                            input=stdin_text.encode("utf-8"), capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", "replace"))
                    self.assertIn(marked_text, stored_file.read_text(encoding="utf-8"))

    def test_reference_tables_have_matching_column_counts(self) -> None:
        for document in (self.plan_example, self.report_example, self.report_template):
            for table in markdown_tables(document.read_text(encoding="utf-8")):
                with self.subTest(document=document.name, header=table[0]):
                    self.assertGreaterEqual(len(table), 2)
                    self.assertRegex(table[1], r"^\|(\s*:?-+:?\s*\|)+$")
                    self.assertEqual({table_cell_count(row) for row in table}, {table_cell_count(table[0])})


if __name__ == "__main__":
    unittest.main()
