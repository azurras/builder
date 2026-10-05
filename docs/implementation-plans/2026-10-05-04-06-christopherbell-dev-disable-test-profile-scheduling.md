# Disable scheduled work in the test profile

## Document Status
blocked

## Objective
> [!IMPORTANT]
> Prevent the `test` profile from registering scheduled jobs that can mutate test fixtures or make external requests during local verification.

## Background
The source review of `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6` found that `SchedulingConfiguration` enables scheduling when `app.scheduling.enabled` is missing. `application-test.yml` disables only selected jobs, leaving other scheduled cleanup and NHTSA work eligible to run in a test-profile session.

## Goals
- Set the test profile's shared scheduling switch to false and prove the real profile resource disables the scheduler bean (AC-1).
- Preserve dedicated tests that explicitly enable scheduling and leave non-test profiles unchanged (AC-1).
- Run the native checks and attempt the committed app locally with the test profile before any PR (AC-2, AC-3).

## Non-Goals
| Not doing | Why |
|---|---|
| Changing production or default scheduling behavior | The finding concerns only the `test` profile. |
| Disabling or changing individual scheduled jobs in other profiles | The profile-wide switch already owns this boundary. |
| Creating or updating PR #1477 | The user said not to trust that draft; it is excluded from the audit. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | Loading `application-test.yml` sets `app.scheduling.enabled=false`, and the property-controlled scheduling configuration registers no scheduler bean for that profile; dedicated scheduler tests can still enable it explicitly. |
| AC-2 | The focused configuration test and full required native checks pass on the committed candidate. |
| AC-3 | The committed candidate starts with isolated test resources and the test profile does not register scheduled jobs; if migration 015 blocks app readiness, record the exact candidate and blocker and do not create a PR. |

## Inputs
- **Request:** User requested a codebase-wide style rewrite in small changes, each with its own implementation plan and test report, and rejected trust in PR #1477.
- **Reviewed source:** `website/src/main/resources/application-test.yml`, `website/src/main/java/dev/christopherbell/configuration/SchedulingConfiguration.java`, and `website/src/test/java/dev/christopherbell/configuration/SchedulingConfigurationTest.java` at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`.
- **Repository guidance:** Root `AGENTS.md`, README test-database policy, and website agent guide.
- **Style guidance:** `write-chris-street-style-code` configuration/template, Java, naming/readability, and testing/review references.

## Branch
`codex/disable-test-profile-scheduling-20261005` from `origin/main` at `695a3ed8617f9b4ab07abb7413baf369c58acf6`.

## Assumptions
- Scheduled tasks must be disabled by default when the application runs with the `test` profile.
- Tests whose contract is scheduling behavior can set `app.scheduling.enabled=true` explicitly.
- The only approved database target for this verification is isolated MongoDB database `test`; do not write fixtures directly or bypass migrations.

## Open Questions
None.

## Design
Set `app.scheduling.enabled: false` under the test profile's existing `app` mapping. Extend the existing scheduling configuration test to load the actual YAML resource through Spring Boot's YAML property-source loader and assert the property disables the scheduler registration. This keeps the test tied to the deployed profile file rather than copying its value into test-only configuration.

| Alternative | Why not |
|---|---|
| Add false to each scheduled job separately | Leaves future jobs enabled by default and duplicates a profile-wide invariant. |
| Disable scheduling globally | Would alter local/production behavior outside the reported risk. |

## Expected Changes
| File or area | Change |
|---|---|
| `website/src/main/resources/application-test.yml` | Set the shared scheduling switch to false. |
| `website/src/test/java/dev/christopherbell/configuration/SchedulingConfigurationTest.java` | Load the test profile resource and prove scheduled-task registration is disabled by its value. |

## Task Breakdown
### Task 1 - Disable the scheduler in the test profile
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | `website/src/main/resources/application-test.yml`; `website/src/test/java/dev/christopherbell/configuration/SchedulingConfigurationTest.java`. |
| **Symbols** | Test profile property `app.scheduling.enabled`; scheduling configuration test context. |
| **Inspection** | Read the test profile, `SchedulingConfiguration`, scheduler test, README isolation requirements, and adjacent YAML/test patterns at `origin/main` `695a3ed8617f9b4ab07abb7413baf369c58acf6`. |
| **Behavior** | The test profile registers no scheduled-task processor unless a test explicitly opts in. |
| **Invariants** | Other profiles and explicit scheduling tests retain current behavior; no external jobs or database changes occur during this config test. |
| **Boundary/API** | Internal Spring configuration only; no public endpoint or persisted data contract changes. |
| **Effects and failures** | Test-profile background effects are disabled at the profile boundary; explicit opt-in tests remain isolated. |
| **Tests and evidence** | Witness the new profile-based context test fail before the YAML change and pass after; run `:website:test`, full website/library checks, PowerShell suite, packaging, and committed local startup under `verify-local-app`. |
| **Verification** | Run focused `SchedulingConfigurationTest`, full `.\gradlew.bat --no-parallel --max-workers=4 :website:check :cbell-lib:check :website:bootJar`, then launch the committed JAR with test profile and isolated MongoDB `test` without overriding the scheduling switch. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | New test loads `application-test.yml` and confirms it disables scheduler registration; existing explicit opt-in test remains green. | The actual app profile loads `test`; startup logs/configuration establish the profile before the known migration blocker. |
| AC-2 | Focused scheduling test, all required module checks, browser suite, PowerShell checks, and `bootJar`. | Run the committed packaged candidate with isolated MongoDB `test` and test-profile storage. |
| AC-3 | Artifact identifies the committed candidate and includes the test profile resource. | Confirm profile readiness and disabled task registration, or record migration 015 as the startup blocker and skip app interaction. |

Regressions and edge cases:
- An unset scheduling property remains enabled in the isolated default-context test.
- An explicit false property disables scheduling.
- The real test-profile YAML supplies false without a command-line override.

## Rollback or Recovery
The change only modifies test-profile configuration and its context test. Revert the single candidate commit to restore prior test-profile behavior. If application startup fails at migration 015, stop only the candidate, confirm port/process cleanup and retain the test database unchanged.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A future scheduled integration test implicitly depends on test-profile background work | Low | Dedicated tests must opt in with an explicit scheduling property. |
| Test-profile disabled switch is not proven from the resource actually loaded | Low | Use Spring's YAML loader on `application-test.yml` in the regression test. |
| App runtime remains unavailable due incomplete migration 015 | High based on audit evidence | Preserve test DB state and report the runtime gap; no PR. |

## Implementation Log

### 2026-10-05 - Disable test profile background jobs

- **Change:** Set `app.scheduling.enabled=false` in `application-test.yml` and added a context regression that loads that exact profile resource through Spring's YAML loader.
- **Reason:** Missing the shared gate caused unrelated scheduled work and external requests to remain eligible during test-profile sessions.
- **Impact:** AC-1 and AC-2 pass on candidate `2a24d6c`; AC-3 is blocked because isolated MongoDB `test` stops startup at incomplete migration 015. See the dedicated [test report](../test-reports/2026-10-05-04-13-christopherbell-dev-disable-test-profile-scheduling.md). No PR was created.

## Outcome
> [!WARNING]
> The test profile now disables scheduled work and native checks pass. Local application readiness and the required PR boundary remain blocked by incomplete migration 015 in isolated database `test`.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | The regression loads actual `application-test.yml` and verifies no scheduler bean is registered; it failed before the YAML change and passes after. Dedicated context test confirms explicit opt-in remains available. |
| AC-2 | ✅ Met | Focused configuration tests 5/5; full gate passes with 2,042 Java tests, 110 skipped, zero failures/errors, browser suite 382/382, PowerShell suites, and JAR packaging. |
| AC-3 | ⚠️ Partly met | Committed candidate used profile `test` without a scheduling override, connected to isolated MongoDB `test`, then stopped at incomplete migration 015 before readiness; process/port cleanup passed. No PR was created. [Test report](../test-reports/2026-10-05-04-13-christopherbell-dev-disable-test-profile-scheduling.md). |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
