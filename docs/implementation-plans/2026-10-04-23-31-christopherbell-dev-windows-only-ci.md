# Target christopherbell.dev CI on Windows

## Document Status
complete

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

### 2026-10-05 - Complete isolated local runtime verification

- **Change:** Resume the implementation after completing local runtime verification using a disposable `ci-verification` Spring profile, then remove that local-only annotation and rebuild the committed tree.
- **Reason:** Startup on a fresh authenticated MongoDB `test` database is intentionally stopped by migration 015 until protected production cutover state exists; the required local application check can still verify normal website readiness and rendering when only that gate is excluded for the isolated local run.
- **Impact:** Runtime proof records the test-only gate exclusion, isolated authenticated database, readiness/homepage results, and startup catch-up's external Overpass 504. The temporary source edit was removed before the final full build; no test profile or migration change is included in commit `b0fc64b`.

### 2026-10-05 - Merge Windows-only website CI

- **Change:** Complete the plan after PR #1479 merged; the branch's Windows build, Dependency Review and all CodeQL checks passed, and GitHub readback shows merge commit `b126b64241737995d9127d0849dcf62c68f987c0` for head `b0fc64bb4a3a0ae8cc0c128fccb12f0955a58534`.
- **Reason:** The Windows-only workflow and its updated contract test passed local build/runtime verification and all remote CI gates.
- **Impact:** AC-1 and AC-2 are complete. The local runtime report documents that migration 015 was excluded only for the isolated verification startup; the final committed tree was rebuilt after removing that test-only profile edit. No production deployment is part of this CI configuration change.

## Outcome
> [!TIP]
> The Windows-only website CI change is merged. Pull request [#1479](https://github.com/azurras/christopherbell.dev/pull/1479) merged as `b126b64241737995d9127d0849dcf62c68f987c0` from verified head `b0fc64bb4a3a0ae8cc0c128fccb12f0955a58534`.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | Met. The website build has one `windows-latest` runner, no OS matrix or Unix Gradle steps, and retains Windows Java 25, Node, Pester, the Gradle wrapper and failure artifacts. The focused workflow contract test passed 10/10; final Windows `gradlew.bat build` passed with 2,164 tests, 0 failures, 0 errors and 110 skipped. Local readiness and homepage returned 200 in an isolated authenticated `test` database; the runtime report discloses that migration 015 was excluded only by a temporary local profile, removed before the final build. | [Runtime report](../test-reports/2026-10-05-06-49-christopherbell-dev-windows-only-website-ci.md); commit `b0fc64b`. |
| AC-2 | Met. PR #1479 merged after the Windows CI build, Dependency Review and all CodeQL scans passed; GitHub readback confirms the merged state and merge SHA. | [PR #1479](https://github.com/azurras/christopherbell.dev/pull/1479); merge `b126b64241737995d9127d0849dcf62c68f987c0`. |
## Project
christopherbell-dev

## Plan Format
task-contract-v2
