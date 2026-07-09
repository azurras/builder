# Complete christopherbell.dev Issues 1105-1109

## Document Status

Ready for execution.

## Objective

Implement and verify GitHub issues #1105 through #1109 for `azurras/christopherbell.dev` in one isolated spoke branch.

## Goals

- #1105: Keep Java 25 as the intended CI runtime per owner comment, while fixing the workflow's unused OS matrix and platform-specific Gradle commands.
- #1106: Make the existing `website/src/test/js` suite portable across CRLF/LF and automate it without adding npm/package.json.
- #1107: Update Dependabot to monitor Gradle dependencies and GitHub Actions.
- #1108: Implement the shared workflow retry lifecycle rather than removing it.
- #1109: Add targeted MongoDB indexes for feed, notification, and message query paths.

## Inputs

- GitHub issues #1105, #1106, #1107, #1108, #1109.
- Issue comment on #1105: use Java 25 instead of Java 21.
- Issue comment on #1108: implement workflow rather than delete it.
- Third-party ZIP link on #1106 is untrusted and out of scope.
- Repo instructions in `AGENTS.md`: Java/Spring/Gradle, no npm workflow, update docs with behavior changes, run focused tests.

## Branch

- Base: `origin/main` at `5f361778`.
- Worktree: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\complete-1105-1109`.
- Branch: `codex/complete-1105-1109`.

## Non-Goals

- No npm/package.json workflow.
- No broad dependency upgrades beyond config needed for Dependabot.
- No production data migration execution; only code/docs for indexes.
- No use of untrusted issue attachments.

## Assumptions

- Java 25 is the desired runtime target despite older docs saying Java 21.
- CI may run Linux/macOS/Windows if the workflow matrix is made real.
- Spring Data Mongo auto-index creation is available in current config, but rollout notes should mention index creation cost.
- Workflow retry can be implemented synchronously in `cbell-lib` without introducing an external scheduler dependency.

## Open Questions

None blocking. If Java 25 source/target changes expose compile issues, adjust the Gradle toolchain and docs coherently.

## Task Breakdown

1. CI/runtime alignment (#1105)
   - Update root Gradle Java target/toolchain and docs from Java 21 to Java 25 if required by owner comment.
   - Fix `.github/workflows/ci.yml` so `runs-on` uses the OS matrix or remove the OS axis. Prefer making the matrix real with OS-specific Gradle commands.
   - Verification: inspect workflow YAML and run Gradle tests locally.

2. JavaScript test automation (#1106)
   - Add a Gradle `Exec` task to run Node's built-in test runner against all JS test files without npm.
   - Make `a11y-markup.test.js` line-ending neutral.
   - Wire JS tests into `check` or `build` so CI catches them.
   - Update README/AGENTS frontend testing docs.
   - Verification: first confirm the existing JS test fails, then confirm all JS tests pass through the new Gradle task.

3. Dependabot config (#1107)
   - Change ecosystem from `maven` to `gradle` for `/`.
   - Add `github-actions` monitoring for `/` if low-noise.
   - Verification: static review of `.github/dependabot.yml` format.

4. Workflow retry implementation (#1108)
   - Add failing tests in `WorkflowExecutorTest` for first-attempt success, retryable failure retries, timeout exceeded, and backoff use.
   - Implement synchronous retry loop that increments attempts, uses `RetryPolicy.getBackoffTimeInMinutes()`, persists context updates, and returns terminal results.
   - Replace or narrow placeholder lifecycle methods where appropriate without over-building scheduling infrastructure.
   - Update `cbell-lib/README.md` or a workflow package README.
   - Verification: targeted `:cbell-lib:test --tests ...WorkflowExecutorTest` then full tests.

5. Mongo indexes (#1109)
   - Add targeted `@Indexed` / `@CompoundIndex` annotations to `Post`, `Notification`, and `Message` for core query paths.
   - Update feature READMEs with index intent and rollout note.
   - Add lightweight tests or reflection assertions for index annotations if practical.
   - Verification: compile and targeted/full tests.

## Code Changes

Expected files:

- `.github/workflows/ci.yml`
- `.github/dependabot.yml`
- `README.md`, `AGENTS.md`
- `build.gradle.kts` and/or module Gradle files
- `website/src/test/js/a11y-markup.test.js`
- `cbell-lib/src/main/java/dev/christopherbell/libs/workflow/WorkflowExecutor.java`
- `cbell-lib/src/test/java/dev/christopherbell/libs/workflow/WorkflowExecutorTest.java`
- `cbell-lib/README.md` or workflow README
- `website/src/main/java/dev/christopherbell/post/model/Post.java`
- `website/src/main/java/dev/christopherbell/notification/model/Notification.java`
- `website/src/main/java/dev/christopherbell/message/model/Message.java`
- relevant feature READMEs and tests

## Unit Testing

Use TDD for code behavior changes:

- JS: existing red test in `a11y-markup.test.js` fails on CRLF; make it pass without weakening intent.
- Workflow: add red tests before implementing retry behavior.
- Indexes: add annotation assertions before adding annotations where practical.

## Local Testing

- Baseline already run:
  - `.gradlew.bat --no-daemon test` passed using `GRADLE_USER_HOME=C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1105-1109`.
  - Bundled Node over `website/src/test/js/*.test.js` failed 1 of 93 tests on CRLF-sensitive selector assertion.
- Final checks:
  - targeted JS Gradle task
  - targeted `WorkflowExecutorTest`
  - targeted index tests if added
  - full `.gradlew.bat --no-daemon build` or `test` plus JS task through Gradle

## Validation

Work is complete when all affected issue acceptance criteria are implemented, local automated tests pass, Builder test report is saved, and GitHub issues are updated or closed with the branch/PR reference.

## Rollback or Recovery

- CI/Dependabot changes can be reverted independently.
- Workflow retry implementation is isolated to `cbell-lib` and can be reverted while retaining tests as a guide.
- Mongo indexes can be reverted by removing annotations; production index cleanup, if required, would need a separate DB operation.

## Risks

- Java 25 may require local/CI runtime availability. Mitigation: use CI setup-java Temurin 25 and keep local tests on available runtime unless source/target demands Java 25 bytecode locally.
- Making JS tests part of Gradle may require a portable Node lookup. Mitigation: allow `NODE_EXE` override and fall back to `node` on PATH.
- Mongo index creation can affect production startup. Mitigation: document rollout cost and keep indexes targeted.
- Workflow retry can be overbuilt. Mitigation: synchronous deterministic retry loop only, no external scheduler.

## Completion Criteria

- Source branch contains implementation for #1105-#1109.
- Tests pass locally with documented commands.
- Builder test report, session memory, indexes, validation, and commit/push are complete.
- GitHub issues are closed or updated with completion evidence.
