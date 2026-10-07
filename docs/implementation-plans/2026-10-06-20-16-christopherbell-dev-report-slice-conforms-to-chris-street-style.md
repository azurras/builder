# Report Slice Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> Every file in the report slice conforms to write-chris-street-style-code, and report submission, the admin queue and moderation behave exactly as before.

## Background
This is slice 5 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `07859a2f` found these problems in `ReportModerationService`:

1. It fills repeat-report counts, which are database reads that mutate each report, inside a stream `peek`.
2. It stamps `resolvedOn` with `Instant.now()` instead of the application `Clock`.
3. It signals "no suspension" with a `null` username.
4. It picks an audit summary by comparing the action string.
5. It names values `nullSafe` and `stateValue`, and uses a fully qualified enum.

`ReportQueryService` builds criteria inline, carries the counts in a `long[]` pair, and uses fully qualified `java.util` and `Pageable` names. `MongoReportRepository` packs methods onto one line, with `value` and `key` parameters. The controller names its query port `reportQueryService` and has `createReportVersioned`. The facade has `getReports`. `report.js` uses `form`, `e`, `err` and `getPostId`, and `back-office-reports.js` uses `toInstant(value)`.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- Submission, dedupe, admin-only access and moderation behave as before (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing `PostReport` to a record | Persisted Mongo document with audit fields and indexes |
| Renaming routes, request records or `ReportQueryPort.query` | Public or cross-file contracts that already read clearly |
| Changing `ReportType.fromReason` mapping unknown reasons to `OTHER` | Documented behavior that stored data relies on |
| Exercising ADMIN moderation at runtime | No supported local ADMIN; see the umbrella log |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the packaged candidate: lets a USER report another user's post through the 2026-07-26 API (it returns the report); returns the same report for a duplicate submission; accepts the 2025-09-03 submission with no payload; denies that USER the admin queue and resolve (403); and rejects an anonymous submission. All recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 5; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `07859a2f`:
  - All `report` Java and READMEs.
  - The tests `ReportServiceTest`, `ReportModerationLifecycleTest`, `ReportQueryServiceTest`, `ReportSubmissionServiceTest`, `ReportControllerTest`, `MongoReportContractTest` and `ReportParityContract`.
  - `static/js/report.js`, `static/js/lib/back-office-reports.js` and `templates/report.html`, plus the caller `back-office.js` and `back-office-reports.test.js`.
  - The post creation API (`PostController`, `PostCreateRequest`) for the runtime fixture.

## Branch
`claude/style-report-20261006` from spoke `origin/main` `07859a2f`, rebased onto `17e24c43` (permission merged) before verification.

## Assumptions
- The `Clock` bean (`ApplicationClockConfiguration`, system UTC) gives the same `resolvedOn` values as `Instant.now()`.

## Open Questions
None.

## Design
The behavior and the order of effects stay exactly the same. The changes are:

- **Review queue:** `listReportsForReview` loops over the newest 100 reports to add counts and returns an unmodifiable list.
- **Audit summaries:** `reportAuditCommand` takes its summary template as a parameter.
- **Suspension:** `suspendUserIfRequested` returns `Optional<String>`.
- **Post deletion:** a constant set names the resolutions that delete the post.
- **Query service:** `criteriaFor(reportQuery)` builds the filter, and `RepeatReportCounts` holds the open and resolved counts per account.
- **Naming:** the controller, facade, submission service, Mongo adapter and scripts name values by role.

| Alternative | Why not |
|---|---|
| Keep `peek` with a comment | `peek` is for debugging; the counts are real effects |
| Rename `ReportQueryPort.query` | Reads clearly as `reportQueries.query(reportQuery)`; the rename would touch the parity contract tests for no gain |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/report/moderation/ReportModerationService.java` | changed | Loop instead of `peek`, injected `Clock`, `Optional` suspension, summary parameter, named constants (rules 1, 7, 8, 9) |
| `website/src/main/java/dev/christopherbell/report/query/ReportQueryService.java` | changed | `criteriaFor`, `RepeatReportCounts`, imports (rules 2, 4, 9) |
| `website/src/main/java/dev/christopherbell/report/submission/ReportSubmissionService.java` | changed | Role names, documented dedupe (rule 2) |
| `website/src/main/java/dev/christopherbell/report/ReportController.java` | changed | `submitReport`, `submitReportReturningIt`, `listReportsForReview`, `reportQueries`, `ResponseEntity.ok` (rule 1) |
| `website/src/main/java/dev/christopherbell/report/ReportService.java` | changed | `listReportsForReview` (rule 1) |
| `website/src/main/java/dev/christopherbell/report/MongoReportRepository.java` | changed | Formatting, parameter names, `newestFirst` (rule 2) |
| `website/src/main/java/dev/christopherbell/report/ReportOpenDedupeKey.java`, `ReportRepository.java` | conforming | No change |
| `website/src/main/java/dev/christopherbell/report/model/*.java` (7 files) | conforming | Records, enums and the persisted document |
| `website/src/main/java/dev/christopherbell/report/query/ReportPage.java`, `ReportQuery.java`, `ReportQueryPort.java` | conforming | Records and port |
| `website/src/main/java/dev/christopherbell/report/**/README.md` (4 files) | conforming | No renamed names documented |
| `website/src/main/resources/static/js/report.js` | changed | Role names for elements, events, failures and helpers (rules 1, 2) |
| `website/src/main/resources/static/js/lib/back-office-reports.js` | changed | Role names; `isoInstantFromLocalDateTime` (rules 1, 2) |
| `website/src/main/resources/templates/report.html` | conforming | No change |
| `website/src/test/java/dev/christopherbell/report/ReportServiceTest.java`, `moderation/ReportModerationLifecycleTest.java` | changed | Pass the clock; renamed list method |
| Other report tests (5 files) and `back-office-reports.test.js` | conforming | No change |

## Task Breakdown

### Task 1 - Conform the report slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Permission slice merged (rebase base) |
| **Files** | As listed in Expected Changes |
| **Symbols** | `ReportModerationService.listReportsForReview`, `resolveReport`, `reopenReport`, `suspendUserIfRequested`, `reportAuditCommand`; `ReportQueryService.query`, `criteriaFor`, `RepeatReportCounts`; `ReportSubmissionService.submitReport`; `ReportController` handlers; `ReportService.listReportsForReview`; Mongo adapter methods; `report.js`, `back-office-reports.js` internals |
| **Inspection** | All files in Inputs at `07859a2f` |
| **Behavior** | Same submission dedupe, same moderation effects in the same order (audit, delete post, suspend and revoke, save, activity records), same queue order and counts, same query validation |
| **Invariants** | Routes, payloads, stored fields, unique open-dedupe index use and audit record contents unchanged |
| **Boundary/API** | `ReportService.getReports` renamed; its only caller is the controller |
| **Effects and failures** | Duplicate-key races still resolve to the winning report; validation messages unchanged |
| **Tests and evidence** | Existing report tests pass with the clock; runtime submission flows |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | `ReportServiceTest`, `ReportModerationLifecycleTest`, `ReportQueryServiceTest`, `ReportSubmissionServiceTest`, `ReportControllerTest`, JS tests | verify-local-app on isolated MongoDB `test`: two disposable USERs are created through the API, the author posts, and the reporter submits through both APIs and repeats a submission (same id); the reporter gets 403 on the admin queue and resolve; an anonymous submission is rejected |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data or schema change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Moderation effect order changes | Low | Lifecycle tests assert audit, deletion, suspension and activity records |
| Unmodifiable review list breaks a caller that mutates it | Low | Only the controller serializes it |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while earlier slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-06 - PR branch updated with main before merge

- **Change:** `gh pr update-branch` merged `main` `1f1287d2` (location slice) into the PR branch, and CI passed on the merged head.
- **Reason:** The ruleset requires up-to-date branches, and force-pushing is a gate.
- **Impact:** None to the report diff.

## Outcome

> [!TIP]
> Shipped in PR #1495 (`6dad824`) and auto-deployed. ADMIN moderation was not exercised at runtime; the lifecycle tests cover it.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every slice file |
| AC-2 | ✅ Met | Full check on `873fb78`: 2,256 Java tests with 0 failures, 390 JS tests ([report](../test-reports/2026-10-06-20-21-christopherbell-dev-report-slice-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 8 of 8 runtime cases: submit, dedupe, 2025-09-03 submit, USER 403 on queue and resolve, anonymous rejected ([report](../test-reports/2026-10-06-20-21-christopherbell-dev-report-slice-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1495](https://github.com/azurras/christopherbell.dev/pull/1495) merged as `6dad824` after all six checks passed; production `/actuator/info` reports `6dad824` |


## Project
christopherbell-dev

## Plan Format
task-contract-v2
