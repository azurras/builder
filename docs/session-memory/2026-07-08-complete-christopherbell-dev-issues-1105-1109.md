# 2026-07-08 - Complete christopherbell.dev issues 1105-1109

## 21:47 - Complete christopherbell.dev issues 1105-1109

### Request

The user asked to complete the `christopherbell.dev` stories they had created, noting that some issues had comments with more details. The relevant GitHub issues were #1105 through #1109.

### Project Context

Builder is the hub repository for durable workflow artifacts. The spoke repository is `azurras/christopherbell.dev`, worked in the isolated worktree `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\complete-1105-1109` on branch `codex/complete-1105-1109`. Owner comments clarified that #1105 should use Java 25 rather than Java 21, and that #1108 should implement the workflow retry lifecycle rather than delete it. A third-party ZIP link on #1106 was ignored as untrusted.

### Work Completed

Created and merged PR https://github.com/azurras/christopherbell.dev/pull/1110 from spoke commit `12ec8769 Complete maintenance stories 1105-1109`; GitHub created merge commit `e7da615a`.

Implemented #1105 by aligning root Gradle Java source/target/toolchain and docs to Java 25, making the GitHub Actions OS matrix real, adding platform-aware Gradle commands, and setting up Node 24 for CI.

Implemented #1106 by adding `:website:jsTest` as a Gradle `Exec` verification task, wiring it into `check`, supporting a `NODE_EXE` override, documenting the canonical command, and making the CRLF-sensitive JS assertion portable.

Implemented #1107 by changing Dependabot from Maven to Gradle monitoring at `/` and adding GitHub Actions monitoring.

Implemented #1108 by adding deterministic synchronous retry behavior to `WorkflowExecutor.executeWorkflowWithRetry`, using `RetryPolicy.getBackoffTimeInMinutes()`, incrementing attempts, returning terminal results, marking expired retry windows stopped, and adding focused retry lifecycle tests. The repo has only a `RetryPolicy` interface and no external workflow scheduler/persistence implementation, so `saveContext` remains the persistence hook.

Implemented #1109 by adding targeted MongoDB `@CompoundIndexes` to `Post`, `Notification`, and `Message`, documenting index intent/rollout notes in feature READMEs, and adding `MongoIndexAnnotationTest` to lock the expected index definitions.

### Decisions

Used Java 25 everywhere because the owner comment superseded the issue body's Java 21 wording. Kept the JS test workflow npm-free per issue scope and repo conventions. Did not consume or inspect the third-party ZIP attachment on #1106. Opened the PR with `Closes #1105` through `Closes #1109` so issues close on merge rather than closing them before review.

### Validation

Local verification passed in the spoke worktree with isolated Gradle cache and bundled Node:

- `:website:jsTest`: 93 tests passed.
- `:cbell-lib:test --tests dev.christopherbell.libs.workflow.WorkflowExecutorTest --info`: passed.
- `:website:test --tests dev.christopherbell.configuration.MongoIndexAnnotationTest`: 3 tests passed.
- root `.\gradlew.bat --no-daemon build`: build successful, including Java and JS tests.
- `node.exe --check website\src\test\js\a11y-markup.test.js`: passed with no output.

Saved Builder test report at `docs/test-reports/2026-07-08-christopherbell-dev-issues-1105-1109-test-report.md`. PR checks later passed for CodeQL, analysis jobs, and Java 25 builds on Ubuntu, macOS, and Windows. PR #1110 was merged on July 9, 2026 and closed issues #1105 through #1109.

### Current State

PR #1110 is merged and the remote branch `codex/complete-1105-1109` was deleted. The local worktree `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\complete-1105-1109` remains on the now-merged local branch. Builder had unrelated modified `.agents/skills/save-implementation-plan/scripts/save_implementation_plan.py`, `.agents/skills/save-project-spec/scripts/save_project_spec.py`, `.agents/skills/save-test-report/scripts/save_test_report.py`, `.agents/tests/test_test_report_workflow.py` plus untracked `.agents/lib/artifact_io.py`, `.agents/lib/artifact_quality.py`, `.agents/skills/close-story-issue/`, `.agents/skills/review-implementation-plan/`, `.agents/skills/validate-implementation-plan/`, `.agents/skills/validate-test-report/`, `.agents/tests/test_artifact_io.py`, and `.agents/tests/test_artifact_quality.py` files outside this story batch; leave them untouched unless the user asks.

### Follow-ups

No follow-up required for this story batch. PR #1110 is merged and issues #1105 through #1109 are closed.
