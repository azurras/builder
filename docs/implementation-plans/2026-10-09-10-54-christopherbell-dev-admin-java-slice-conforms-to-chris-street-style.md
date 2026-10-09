# Admin Java Slice Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> Every admin Java file conforms to write-chris-street-style-code, and admin activity, the command-center snapshot, logs and protected host actions behave as before.

## Background
This is slice 15a of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The ledger said to split admin when planning it. Slice 15a is the admin Java (41 main files, 3 READMEs, 25 tests). Slice 15b is the back-office JavaScript and template. Inspection at `00d898a2` found:

1. **Stringly typed outcomes.** `CommandCenterActionService.rejectionCategory` chooses the audited outcome with a `switch` on exception message text. A reworded message would silently audit the wrong category.
2. **A broad catch.** The metrics provider loop catches `Exception` where only `ExecutionException` and unchecked failures can reach it.
3. **Optional misuse:**
   - `MongoPendingActionStore.active` calls `get()`.
   - `cancel` unwraps with `orElse(null)`.
   - `ApplicationHostMetricsProvider` turns an `Optional` commit back into a nullable string.
4. **Silent catches.** Four empty `catch` blocks in `SecureNativeLibraryProvisioner` give no reason.
5. **Smaller issues:**
   - About 20 fully qualified names in main code and many in tests.
   - A locale-less `toUpperCase` in an audit action name.
   - An anonymous `OutputStream` written only to feed a digest.
   - A redundant local in `NvidiaMetricsProvider.parse`.
   - One-line Mongo adapter methods.

## Goals
- Every admin Java file has a recorded verdict and conforms (AC-1, AC-2).
- Admin endpoints stay protected and background sampling keeps working (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Back-office JavaScript and `back-office.html` | Slice 15b |
| Removing the `NullPointerException` catch in password verification | It fails closed on unverifiable stored credentials; it now says so |
| Changing host commands, ACL hardening, checksums, log redaction or cursor format | Security-sensitive behavior |
| The nullable `pendingAction` in the snapshot record | It is a JSON field that is null when nothing is pending |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every admin Java file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that readiness is UP through the database health indicator, anonymous admin reads match production, a USER is rejected from every command-center and activity endpoint, and background sampling logs no unexpected errors |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 15; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `00d898a2`:
  - All `admin` main and test sources.
  - `InvalidRequestException`, which is not final.
  - The shared `ControllerExceptionHandler`, which maps `InvalidRequestException` and its subclasses to 400.

## Branch
`claude/style-admin-20261009` from spoke `origin/main` `00d898a2`.

## Assumptions
None beyond Inputs.

## Open Questions
None.

## Design
- **Rejections:**
  - `ActionRejection` names each refusal with its unchanged message and audited outcome.
  - `ActionRejectedException extends InvalidRequestException` carries it, so callers still receive the same 400 and message.
  - `rejectionCategory` reads the rejection and keeps `invalid-challenge` as the fallback.
- **Metrics:** the provider loop catches `ExecutionException | RuntimeException`, which is everything it caught before apart from the timeout and interrupt cases handled above it.
- **Optional:**
  - `safeCommit` returns `Optional`, and the commit and service readings use `map`/`orElseGet`.
  - The pending-action store reads its reservation once.
- **Provisioner:** hashing uses `DigestInputStream` into `OutputStream.nullOutputStream()`, and each best-effort catch explains why it is safe.

| Alternative | Why not |
|---|---|
| Keep the message switch with tests | The coupling between text and audit category stays invisible to the compiler |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/admin/commandcenter/action/ActionRejection.java`, `ActionRejectedException.java` | new | Closed rejection set |
| `website/src/main/java/dev/christopherbell/admin/commandcenter/action/CommandCenterActionService.java` | changed | Typed rejections, `Optional`, locale, imports |
| `website/src/main/java/dev/christopherbell/admin/commandcenter/action/MongoPendingActionStore.java` | changed | No `get()` |
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/ApplicationHostMetricsProvider.java`, `CommandCenterMetricsService.java`, `NvidiaMetricsProvider.java` | changed | `Optional`, narrow catch, imports, redundant local |
| `website/src/main/java/dev/christopherbell/admin/commandcenter/metrics/SecureNativeLibraryProvisioner.java` | changed | Explained catches, `DigestInputStream`, imports |
| `website/src/main/java/dev/christopherbell/admin/commandcenter/action/WindowsCommandExecutor.java`, `logs/CommandCenterLogService.java` | changed | Imported names |
| `website/src/main/java/dev/christopherbell/admin/activity/MongoAdminActivityRepository.java` | changed | One statement per line |
| Remaining 32 admin main Java files and the 3 READMEs | conforming | No change |
| 14 admin test files (`AdminActivityQueryServiceTest`, `AdminActivityServiceTest`, `CommandCenterControllerTest`, `CommandCenterPropertiesTest`, `CommandCenterActionServiceTest`, `MongoPendingActionStoreTest`, `WindowsCommandExecutorTest`, `CommandCenterMetricsServiceTest`, `DatabaseHealthConfigurationTest`, `DatabaseHealthHttpSecurityIntegrationTest`, `LibreHardwareCpuTemperatureClientTest`, `NvidiaMetricsProviderTest`, `PowerShellCpuTemperatureProbeTest`, `SecureNativeLibraryProvisionerTest`) | changed | Imported names instead of fully qualified ones |
| Remaining 11 admin test files | conforming | No change |

## Task Breakdown

### Task 1 - Conform the admin Java slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `ActionRejection`, `ActionRejectedException`, `CommandCenterActionService.rejectionCategory`, `cancel`; `MongoPendingActionStore.active`; `ApplicationHostMetricsProvider.read`, `safeCommit`; `CommandCenterMetricsService.collect`; `SecureNativeLibraryProvisioner.sha256` |
| **Inspection** | All files in Inputs at `00d898a2` |
| **Behavior** | Same responses, messages, audit outcomes, commands, alerts and readings |
| **Invariants** | Endpoints, security expressions and host argument arrays unchanged |
| **Boundary/API** | None outside the package |
| **Effects and failures** | None new |
| **Tests and evidence** | Admin suites (including the audited rejection categories); runtime protection checks |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Admin suites | verify-local-app: readiness, anonymous reads compared with production, USER rejections, sampling log. Admin success paths need an ADMIN, which has no supported local path, so they rely on the controller, action and metrics tests |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A rejection is audited with a different category | Low | `CommandCenterActionServiceTest` asserts the categories; every former message maps to its former category |
| Bundled library checksums change | Very low | `DigestInputStream` hashes the same bytes; the provisioner tests verify checksums |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the account slice was in CI.
- **Reason:** I worked ahead between deploys.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome

> [!TIP]
> Shipped in PR #1505 (`3f4af8b`) and auto-deployed. Production `/actuator/info` reports the merge commit and `/back-office` returns 200. Admin success paths remain covered by tests only, because no local ADMIN exists.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every admin Java file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-10-54-christopherbell-dev-admin-java-slice-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 13 of 13 runtime cases passed on candidate `3887b55` ([report](../test-reports/2026-10-09-10-54-christopherbell-dev-admin-java-slice-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1505](https://github.com/azurras/christopherbell.dev/pull/1505) merged as `3f4af8b` after all checks passed; production `/actuator/info` reports `3f4af8b` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
