# 2026-07-09 - Require runtime evidence in test reports

## 21:59 - Require runtime evidence in test reports

### Request
The user pointed out that a generated Builder test report only documented unit tests, which is exactly what test reports should not do. They clarified that test reports are for running the app locally and exercising an endpoint, UI flow, or similar real-world behavior with data sent and response observed.

### Project Context
Builder test report skills had been recently added under `.agents/skills/save-test-report` and `.agents/skills/validate-test-report`, with shared validation in `.agents/lib/artifact_quality.py`. The previous validator required non-empty Data Sent, Response Received, Pass / Fail, and Evidence sections, but did not reject unit-test-only content.

### Work Completed
Added regression coverage in `.agents/tests/test_artifact_quality.py` proving that a `complete` report containing only `./gradlew test` style evidence is invalid. Added a companion test proving that a `blocked` report can honestly document that local app testing did not happen.

Updated `.agents/lib/artifact_quality.py` so complete test reports must identify local runtime details and include runtime interaction data plus runtime response evidence. The validator now recognizes local app run indicators, endpoint/UI input indicators, runtime response indicators, and common unit-test-only command patterns.

Updated `.agents/skills/save-test-report/SKILL.md`, `.agents/skills/validate-test-report/SKILL.md`, and their `agents/openai.yaml` prompts to state that unit test, lint, or build output alone is not a test report. The workflow now requires starting or identifying a local app runtime and exercising an endpoint, browser/UI flow, webhook, CLI-to-app path, or equivalent runtime behavior before saving a complete report.

Updated `.agents/skills/complete-story-issue/SKILL.md` to separate automated implementation validation from real-world local app testing, and to forbid treating unit tests as a substitute for a test report.

Migrated `docs/test-reports/2026-07-08-christopherbell-dev-issues-1105-1109-test-report.md` from `complete` to `superseded` and added notes explaining it is retained as automated validation evidence only, not a complete local app test report under the current Builder standard.

### Decisions
The validator only applies the runtime-evidence gate to `complete` reports. `blocked`, `draft`, or `superseded` reports may document that local app testing was not performed, which lets agents preserve honest evidence without letting it pass as closure-grade real-world testing.

### Validation
Confirmed the new regression test failed before the validator change. After the change, ran `python -m unittest discover -s .agents\tests`; 14 tests passed. Ran `python .agents\skills\validate-test-report\scripts\validate_test_report.py docs\templates\examples\test-report-example.md` and the migrated historical report; both passed. Ran `python .agents\skills\validate-hub-state\scripts\validate_hub_state.py`; hub validation passed with existing legacy implementation-plan warnings only. Ran `python -m py_compile` for the touched validator and report scripts; it exited successfully.

### Current State
The work is on `main` in `C:\Users\Christopher\Developer\builder`. Hub indexes were checked and were already current. No app server was started because this change is to Builder workflow validation and skill instructions.

### Follow-ups
Future generated test reports should be rejected if they claim completion from unit tests alone. If older automated-validation artifacts are encountered, mark them blocked or superseded rather than weakening the complete-report gate.
