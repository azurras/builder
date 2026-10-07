# Sitemonitor Slice Conforms to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every file in the sitemonitor slice conforms to write-chris-street-style-code. The website monitor pilot (adding sites, baselines, checks, reports and scheduled checks) behaves exactly as before, including its SSRF protections.

## Background
This is slice 6 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `1f1287d2` found:

1. **Dense code.** Several statements per line, one-line methods and fully qualified type names, worst in `SiteMonitorService`, `MongoMonitorWorkspaceRepository` and `MonitorScanner`.
2. **Boolean mode parameters.** `run(siteId, true)` means "capture baseline" and `run(siteId, false)` means "compare"; `addSite(label, origin, paths, demo)` takes a boolean too.
3. **Stringly typed results.** Report statuses (`HEALTHY`, `CHANGES`, `FAILURES`, `INCOMPLETE`, `BASELINE`) and finding severities are raw strings compared with `equals`.
4. **Unnamed limits.** Five sites, ten workspaces, 15-minute and one-day intervals, 45-second runs, ten assets, 400-character text, ten reports.
5. **Overgrown page capture.** `MonitorScanner.capturePage` mixes page fetch, status confirmation and asset checks in one 60-line method.
6. **Misleading destination check.** `SiteMonitorDestinationPolicy` accepts `http` in one condition and then requires exact `https`. Its error message says "HTTP(S)" and it keeps a dead port-80 branch.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- The pilot behaves as before for a signed-in user, including stored data and the published JSON strings (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing pilot limits, intervals, the proof path, allowed content types or redirect rules | Product and security behavior |
| Changing `MonitorFetchException` categories or `Page.problem` strings to enums | They are open-ended diagnostic codes stored per page; a closed enum would reject future categories |
| Changing the IP block lists or the transport's TLS and size handling | Security-critical and already conforming |
| Moving `MonitorProblem` out of `api` or the persistence layer's use of it | A package move with no behavior gain |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass, including all sitemonitor suites and `MonitorPolicyTest` (27 cases), and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, a disposable USER can: add the demo site; capture a baseline that is stored and returned with status `BASELINE`; get 429 with `Retry-After: 900` for an immediate re-check; download the plain-text report; remove the site. Anonymous access gets 401 and an invalid origin gets 400. All recorded in a published test report |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 6; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `1f1287d2`:
  - All `sitemonitor` Java and the README.
  - The tests `SiteMonitorServiceTest`, `MonitorScannerTest`, `SiteMonitorControllerTest`, `MonitorPolicyTest`, `PublicMonitorGatewayTest` and `MonitorHttpTransportTest`, plus `configuration/mongo/domain/SiteMonitorMongoIntegrationTest`.
  - `static/js/site-monitor.js`, `templates/site-monitor.html` and `site-monitor.test.js`.
  - `account.api.MonitorAccountAccess`.

## Branch
`claude/style-sitemonitor-20261006` from spoke `origin/main` `1f1287d2`.

## Assumptions
- Spring Data stores enums by name and reads stored names back into enums. Every stored status and severity is one of the enum constants, because only this code writes them.
- Jackson serializes the enums by name, so the page sees the same strings.

## Open Questions
None.

## Design
- **Typed results:** `MonitorWorkspace` gains `ReportStatus` and `FindingSeverity` enums whose names equal the existing strings, plus `Site.hasBaseline()` and `MonitorWorkspace.emptyFor(accountId)`.
- **Service:** `SiteMonitorService` exposes `captureBaseline` and `checkAgainstBaseline` over a private `runCheck` with a `CheckMode` enum. `addSite(CreateMonitorSite)` validates in `validatedNewSite`. Baseline acceptance is an explicit `withAcceptedBaseline` step, and every limit and interval is a named constant.
- **Scanner:** `MonitorScanner` splits `pageAfterConfirmingStatus` and `checkSameOriginAssets`, with an `AssetCheck` record, and names its budgets.
- **Comparison:** `MonitorComparison` uses `addChangeIfDifferent` and `overallStatusOf`.
- **Repository:** `MonitorWorkspaceRepository` names `findByAccountId` and `listAll`. The Mongo adapter names the slots and the schedule spacing.
- **Fetch layer:** fully qualified names are replaced with imports. The destination check requires `https` once and defaults the port to 443.

| Alternative | Why not |
|---|---|
| Keep `run(siteId, boolean)` and document the flag | A boolean at the call site hides which operation runs; the controller already has two routes |
| `Optional<List<Page>>` parameter for the accepted baseline | `Optional` parameters are a smell; an explicit `withAcceptedBaseline` step reads better |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/sitemonitor/model/MonitorWorkspace.java` | changed | `ReportStatus`, `FindingSeverity`, `hasBaseline`, `emptyFor`, formatting (rules 4, 9) |
| `website/src/main/java/dev/christopherbell/sitemonitor/monitor/SiteMonitorService.java` | changed | Named operations, request record, constants, explicit steps (rules 1, 4, 9) |
| `website/src/main/java/dev/christopherbell/sitemonitor/monitor/MonitorScanner.java` | changed | Split capture, `AssetCheck`, constants, `isOwnershipVerified`, `capturePages`, `boundedText`, `newRunDeadlineNanos` (rules 1, 2, 9) |
| `website/src/main/java/dev/christopherbell/sitemonitor/monitor/MonitorComparison.java` | changed | Enums and named helpers (rules 1, 4) |
| `website/src/main/java/dev/christopherbell/sitemonitor/api/SiteMonitorController.java` | changed | Handler names, `siteId` path names, constants (rule 1) |
| `website/src/main/java/dev/christopherbell/sitemonitor/persistence/MonitorWorkspaceRepository.java`, `MongoMonitorWorkspaceRepository.java` | changed | `findByAccountId`, `listAll`, slots and spacing named, imports (rules 1, 2) |
| `website/src/main/java/dev/christopherbell/sitemonitor/fetch/SiteMonitorDestinationPolicy.java` | changed | Single `https` requirement and port default; message says HTTPS (rule 1) |
| `website/src/main/java/dev/christopherbell/sitemonitor/fetch/PublicMonitorGateway.java`, `MonitorUrls.java`, `MonitorHttpTransport.java` | changed | Imports instead of fully qualified names |
| `website/src/main/java/dev/christopherbell/sitemonitor/fetch/MonitorGateway.java`, `MonitorFetchException.java`, `api/MonitorProblem.java`, `model/CreateMonitorSite.java`, `model/MonitorSchedule.java`, `monitor/SiteMonitorScheduler.java`, `README.md` | conforming | No change |
| `website/src/main/resources/static/js/site-monitor.js` | changed | Role names; `runWorkspaceRequest`, `renderSites` (rules 1, 2) |
| `website/src/main/resources/templates/site-monitor.html` | conforming | No change |
| `website/src/test/java/dev/christopherbell/sitemonitor/monitor/*Test.java`, `api/SiteMonitorControllerTest.java`, `configuration/mongo/domain/SiteMonitorMongoIntegrationTest.java` | changed | Renamed operations and enums |
| `website/src/test/java/dev/christopherbell/sitemonitor/fetch/*Test.java`, `website/src/test/js/site-monitor.test.js` | conforming | No change |

## Task Breakdown

### Task 1 - Conform the sitemonitor slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `SiteMonitorService` public operations and `runCheck`; `MonitorScanner` public methods; `MonitorComparison.compare`; `ReportStatus`; `FindingSeverity`; repository methods; controller handlers; `SiteMonitorDestinationPolicy.validateAndResolve` |
| **Inspection** | All files in Inputs at `1f1287d2` |
| **Behavior** | Same validation order and messages, cooldown and baseline rules, attempt reservation before fetch, lease checks before each fetch and save, report retention, scheduled selection, export text and HTTP headers |
| **Invariants** | Same accepted destinations (exact `https`, port 443, public addresses); same stored document shape and enum names; routes and JSON unchanged |
| **Boundary/API** | `SiteMonitorService` and scanner method renames have callers only in this slice and its tests |
| **Effects and failures** | Lease, optimistic-lock and 409 handling unchanged; fetch failures keep their categories |
| **Tests and evidence** | All sitemonitor suites and the Mongo integration test (skipped without its database, as in CI); runtime pilot flow |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | `SiteMonitorServiceTest` (8), `MonitorScannerTest` (5), `SiteMonitorControllerTest` (4), `MonitorPolicyTest` (27), transport and gateway tests | verify-local-app on isolated MongoDB `test` with a disposable USER: add the demo site, capture a baseline (read-only requests to the public demo pages), re-check immediately (429), download the report, remove the site; check anonymous access (401) and an invalid origin (400) |
| AC-4 | Required PR checks | `wait_for_github.py live` on production `/actuator/info` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. Stored workspaces keep the same strings, so either version reads them.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Enum mapping fails for stored workspaces | Low | Runtime stores and reloads a baseline report; production has at most ten pilot workspaces written by this code |
| A refactor changes the order of lease checks and fetches | Low | `leaseLossAfterOwnershipStopsBeforePageFetch` and the capacity tests |

## Implementation Log

### 2026-10-06 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while earlier slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
