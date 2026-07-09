from __future__ import annotations

import sys
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
