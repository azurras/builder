# Target christopherbell.dev CI on Windows

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Run the website build workflow only on a Windows GitHub Actions runner so CI matches the supported Windows environment.

## Background
The `ci.yml` workflow currently runs the same Java 25 build on Ubuntu, macOS, and Windows. The user requested that website CI target Windows only.

## Goals
- Run the CI build job only on `windows-latest` while preserving its Windows setup and build steps (AC-1).
- Merge the verified workflow change through the spoke PR process (AC-2).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing CodeQL, dependency-review or other workflows | The request concerns the `ci.yml` build workflow; other workflow behavior is outside scope. |
| Changing build logic, application code, or production deployment | Only the CI runner target is requested. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | `.github/workflows/ci.yml` runs only on `windows-latest`, retains Pester and the Windows Gradle build, its configuration tests assert that contract, and local workflow validation and candidate verification pass. |
| AC-2 | The spoke PR's required checks pass and the change is merged with merge readback recorded. |

## Inputs
- **Request:** User asked to update christopherbell.dev CI so it only targets Windows.
- **Repository evidence:** `.github/workflows/ci.yml` on refreshed `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`; it uses an OS matrix of Ubuntu, macOS and Windows, with Windows-specific Pester and Gradle steps.
- **Repository instructions:** `AGENTS.md`, root README and workflow configuration.
- **Related context:** Prior site delivery guidance says to preserve the dirty authoritative checkout and use a clean worktree.

## Branch
Builder plan on primary Builder `main`; spoke implementation on `codex/windows-only-ci-20261004` from refreshed `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6c`.

## Assumptions
- `ci.yml` means the build workflow at `.github/workflows/ci.yml`; analysis and dependency-review workflows are not part of this request.
- Windows GitHub-hosted runner `windows-latest` is the intended sole target.

## Open Questions
None.

## Design
Set the job's runner directly to `windows-latest`, remove the operating-system matrix and Unix-only setup/build branches, and use the retained Windows `gradlew.bat build` step. Keep pinned setup actions, Java 25, Node 24, Gradle caching, Pester installation, and failed-test artifacts, with a stable Windows artifact name. Local checks will validate workflow syntax and run the repository's Windows Gradle build; `verify-local-app` will provide local candidate execution and document any concrete environmental blocker.

| Alternative | Why not |
|---|---|
| Keep an OS matrix containing only Windows | Leaves matrix indirection and OS conditionals for a single fixed runner. |
| Change other workflow runners too | Broader than the specifically requested build workflow. |

## Expected Changes
| File or area | Change |
|---|---|
| `.github/workflows/ci.yml` | Make `windows-latest` the sole runner; remove Unix-specific steps and obsolete matrix references while retaining Windows checks and artifacts. |
| `website/src/test/java/dev/christopherbell/configuration/GitHubAutomationConfigurationTest.java` | Update CI contract tests from multi-platform runner and condition expectations to the single Windows workflow. |

## Task Breakdown
### Task 1 - Restrict the CI build workflow to Windows
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `.github/workflows/ci.yml`; `website/src/test/java/dev/christopherbell/configuration/GitHubAutomationConfigurationTest.java`. |
| **Symbols** | `jobs.build.runs-on`, `jobs.build.strategy.matrix`, build setup/test steps, failed-test artifact naming; `ciBuildsOnlyOnWindowsWithoutGeneratedDatabaseSources`, `ciRunsPinnedWindowsPesterAndRetainsItsNunitResults`, and `ciCancelsOnlySupersededPullRequestsAndBoundsWork`. |
| **Inspection** | Read current workflow and repository `AGENTS.md`; inspected refreshed `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c`. |
| **Behavior** | The build runs once on Windows; Pester installs and `gradlew.bat build` runs; failed test output remains uploadable. |
| **Invariants** | Keep action pins, Java 25, Node 24, Gradle setup/caching, permissions, trigger/concurrency policy and artifact retention. No non-Windows runner remains in this build workflow. |
| **Boundary/API** | GitHub Actions workflow only; do not alter CodeQL or dependency-review. |
| **Effects and failures** | Workflow changes affect pull request and main build execution; CI failure artifacts remain available for 14 days. Rollback by reverting the single workflow commit. |
| **Tests and evidence** | Update and run workflow contract tests, validate workflow structure, run native Windows Gradle build and verify-local-app on the committed candidate, inspect final diff, then require spoke PR CI before merge. |
| **Verification** | Assert the effective build runner is only `windows-latest`, no Unix build branch or stale cross-platform assertion remains, workflow parser succeeds, `gradlew.bat build` succeeds locally, and required PR checks pass. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Updated `GitHubAutomationConfigurationTest`; workflow parser; `gradlew.bat build`; semantic review of triggers, runner, retained steps and artifact paths. | Use `verify-local-app` to execute the committed application candidate on the local machine with isolated test resources and exercise readiness; publish the report before PR creation. |
| AC-2 | Observe all required PR checks pass; read back merged PR and merge SHA. | Not applicable; covered by AC-1. |

Regressions: ensure setup still uses Java 25 and Node 24; Pester 5.9.0 still installs on Windows; the Gradle wrapper command uses `gradlew.bat`; failure artifacts still include build reports and test results; no Ubuntu/macOS references or multi-platform contract assertions remain for the build job.

## Rollback or Recovery
Revert the workflow change through a follow-up commit and let the usual pull request CI validate it. No production deployment or data migration is involved.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Windows-only execution loses early detection of platform-specific regressions on Linux/macOS | Medium | This is the requested scope; retain existing Windows tests and document the coverage change in the PR. |
| YAML edits accidentally remove required setup or artifacts | Low | Review semantic workflow structure, run native validation/build and require PR CI. |

## Implementation Log

### 2026-10-04 - Update outdated workflow contract tests

- **Change:** Add `GitHubAutomationConfigurationTest.java` to the implementation scope and update its expected workflow contract.
- **Reason:** The existing CI tests encode the old three-platform matrix, conditional Pester setup and Unix Gradle invocation; the new Windows-only workflow correctly made those three assertions fail.
- **Impact:** Task 1, Expected Changes, AC-1 and the Test Plan now include updating and running the workflow contract tests. No behavior beyond the requested CI target is added.

### 2026-10-04 - Block on protected cutover startup gate

- **Change:** Record local application verification as blocked and set the plan status to `blocked`.
- **Reason:** A separate authenticated MongoDB `test` database allowed the candidate to connect, but its startup migration 015 requires a verified target-active domain cutover ledger; a fresh test database lacks that protected production migration state.
- **Impact:** AC-1 remains partly met because workflow validation and the full Windows build passed but the required application runtime proof did not; AC-2 has not started because Builder policy forbids PR creation without that proof. A blocked test report records the evidence.

## Outcome
> [!WARNING]
> The Windows-only workflow is implemented, the focused configuration tests and full Windows build pass, and candidate `b0fc64b` is committed. Local application runtime proof is blocked by the protected cutover startup requirement, so no spoke PR was opened.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ⚠️ Partly met. Workflow YAML validation and all 2,164 JUnit tests passed (110 skipped), but local runtime verification stopped at migration 015 because the isolated fresh database lacks the verified `TARGET_ACTIVE` cutover ledger. | [Test report](../test-reports/2026-10-04-23-52-christopherbell-dev-windows-only-website-ci.md); candidate commit `b0fc64b`. |
| AC-2 | ❌ Not met. PR creation and merge are deferred until a cutover-ready isolated runtime fixture or authorized test-only initialization path is available. | No PR created; Builder's before-PR runtime proof requirement remains unmet. |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
