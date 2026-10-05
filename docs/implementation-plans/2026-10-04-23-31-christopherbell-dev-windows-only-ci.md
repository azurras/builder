# Target christopherbell.dev CI on Windows

## Document Status
ready-for-execution

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
| AC-1 | `.github/workflows/ci.yml` runs only on `windows-latest`, retains Pester and the Windows Gradle build, and passes local workflow validation and candidate verification. |
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

## Task Breakdown
### Task 1 - Restrict the CI build workflow to Windows
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `.github/workflows/ci.yml`. |
| **Symbols** | `jobs.build.runs-on`, `jobs.build.strategy.matrix`, build setup/test steps, failed-test artifact naming. |
| **Inspection** | Read current workflow and repository `AGENTS.md`; inspected refreshed `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6c`. |
| **Behavior** | The build runs once on Windows; Pester installs and `gradlew.bat build` runs; failed test output remains uploadable. |
| **Invariants** | Keep action pins, Java 25, Node 24, Gradle setup/caching, permissions, trigger/concurrency policy and artifact retention. No non-Windows runner remains in this build workflow. |
| **Boundary/API** | GitHub Actions workflow only; do not alter CodeQL or dependency-review. |
| **Effects and failures** | Workflow changes affect pull request and main build execution; CI failure artifacts remain available for 14 days. Rollback by reverting the single workflow commit. |
| **Tests and evidence** | Validate workflow structure, run native Windows Gradle build and verify-local-app on the committed candidate, inspect final diff, then require spoke PR CI before merge. |
| **Verification** | Assert the effective build runner is only `windows-latest`, no Unix build branch remains, workflow parser/linter succeeds, `gradlew.bat build` succeeds locally, and required PR checks pass. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Workflow parser/linter; `gradlew.bat build`; semantic review of triggers, runner, retained steps and artifact paths. | Use `verify-local-app` to execute the committed application candidate on the local machine with isolated test resources and exercise readiness; publish the report before PR creation. |
| AC-2 | Observe all required PR checks pass; read back merged PR and merge SHA. | Not applicable; covered by AC-1. |

Regressions: ensure setup still uses Java 25 and Node 24; Pester 5.9.0 still installs on Windows; the Gradle wrapper command uses `gradlew.bat`; failure artifacts still include build reports and test results; no Ubuntu/macOS references remain in the build job.

## Rollback or Recovery
Revert the workflow change through a follow-up commit and let the usual pull request CI validate it. No production deployment or data migration is involved.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| Windows-only execution loses early detection of platform-specific regressions on Linux/macOS | Medium | This is the requested scope; retain existing Windows tests and document the coverage change in the PR. |
| YAML edits accidentally remove required setup or artifacts | Low | Review semantic workflow structure, run native validation/build and require PR CI. |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
