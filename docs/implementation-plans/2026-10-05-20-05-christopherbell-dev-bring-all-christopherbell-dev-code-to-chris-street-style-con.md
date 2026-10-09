# Bring All christopherbell.dev Code to Chris Street Style Conformance

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> Every tracked first-party code file in christopherbell.dev is reviewed against write-chris-street-style-code and either recorded as conforming or brought into conformance, one feature slice per pull request, without changing observable behavior.

## Background
The user asked on 2026-10-05 to start a project that moves all christopherbell.dev code to the Chris Street Style. The [2026-10-04 audit](2026-10-04-christopherbell-dev-chris-street-style-audit.md), merged in PR #1480, reviewed 1,421 files but by its own non-goals made only 23 targeted, evidence-backed corrections and ruled out broad rewrites. Most code therefore still predates the standard: vague names, reused variables whose meaning changes, loosely typed states and catch-all failure handling remain common. The user chose full conformance over contract-only fixes, one PR per feature, and the smallest feature first.

## Goals
- Every tracked first-party code file has a recorded verdict, conforming as-is or changed, in the slice plan that covered it (AC-1, AC-2, AC-6).
- Each slice reaches conformance with behavior preserved, proven by native checks and local runtime evidence (AC-3, AC-4).
- Each slice ships as its own reviewed, merged and deployed pull request, so any one can be reverted alone (AC-5).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing routes, JSON payloads, persisted field names, schemas or Mongo collections | Conformance is a behavior-preserving migration; contract changes need their own decision |
| New features or bug fixes found along the way | A real bug found during a slice is logged and delivered as its own small change, not folded into a style diff |
| Formatter-only or whole-file reformatting | The standard is about meaning, not whitespace; churn hides the real changes from reviewers |
| New frameworks, libraries, npm packages or build tools | Spoke AGENTS.md forbids them and the standard does not need them |
| Historical design documents, data sets, media, vendored or generated files | Not first-party code |
| Reworking draft PR #1477 or the 23 per-correction plans still marked blocked from the earlier audit | Their code shipped in #1480; tidying those records is separate housekeeping |
| Manual production operations | Production changes only through the supported CI-gated auto-deploy of each merged slice |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | This plan's slice ledger names every slice, its files and its order, and is published on Builder `origin/main` |
| AC-2 | Each slice has its own plan whose Expected Changes lists every file in the slice with a verdict (conforming or changed) and the rule it served |
| AC-3 | Each slice candidate passes `:website:check :cbell-lib:check :website:bootJar`, plus Pester for script slices, and write-chris-street-style-code review of the full diff finds no blocker |
| AC-4 | Each slice candidate runs locally on an isolated `test` MongoDB, the slice's routes or jobs are exercised, and a test report naming the candidate commit is published before its PR |
| AC-5 | Each slice PR merges after all required checks pass, and the auto-deployed production `/actuator/info` reports the merge commit |
| AC-6 | After the last slice, a recount of tracked first-party code files equals the number of files with verdicts across the slice plans, and this plan's Outcome is complete |

## Inputs
- **Request:** user on 2026-10-05: start a project to move all christopherbell.dev code to the Chris Street Style. Decisions via question: full conformance, one PR per feature, smallest feature first.
- **Standard:** Builder `.agents/skills/write-chris-street-style-code/SKILL.md` and its references; spoke `AGENTS.md` "Chris Street Style" section.
- **Prior work:** [2026-10-04 audit plan](2026-10-04-christopherbell-dev-chris-street-style-audit.md), PR #1480 (`a9d20589`); [isolated test database bootstrap](2026-10-05-07-17-christopherbell-dev-bootstrap-isolated-empty-test-database.md).
- **Inspected:** spoke `origin/main` `ef15adc0`: package tree under `website/src/main/java/dev/christopherbell`, test tree, `cbell-lib`, `static/js`, templates, PowerShell, Gradle and workflow files, with file and line counts per slice below.

## Branch
Each slice uses its own branch `claude/style-<slice>` from the then-current spoke `origin/main`; this umbrella plan has no code branch.

## Assumptions
- The isolated-`test` bootstrap from 2026-10-05 still starts a fresh candidate without production data.
- Existing tests cover enough behavior to show preservation; where a slice finds a gap, it adds characterization tests before refactoring.
- Merging a slice to `main` deploys it automatically through the CI-gated pipeline, which AGENTS.md treats as authorized deployment.

## Open Questions
None. Large slices are split at their own planning time by subpackage, recorded in this plan's log.

## Design
Work proceeds slice by slice in ascending size. A slice is a feature package with everything it owns: main Java, its tests, its page JavaScript module and template, and feature-owned CSS. Cross-cutting areas follow the features. Each slice gets its own task-contract-v2 plan, written when the slice starts and based on the code as it is then, with a per-file ledger in Expected Changes. Slices over about 8,000 lines are split into sub-slices by subpackage when planned, each with its own PR.

**Conformance** means a write-chris-street-style-code review of the file finds no blocker and no actionable warning against the ten mandatory rules. Typical changes: role-revealing names and call sites that read as sentences, new variables when meaning changes, value types or enums for loosely typed states, validation at trust boundaries, narrowed catches that keep causes, visible effects and ownership, and tests that show input and output. Renamed Java fields that are persisted or serialized keep their stored or wire names.

| Alternative | Why not |
|---|---|
| One big PR per language layer | Each PR would span the whole site; review and rollback get impractical (user decision) |
| Contract fixes only, as in the audit | The audit already did this; the user wants full conformance |
| Enforce on touched code only | Leaves most code nonconforming indefinitely (user decision) |
| Largest or riskiest slice first | The workflow and ledger format should be proven on a small slice first (user decision) |

### Slice ledger
Line counts are main plus test Java at `ef15adc0`; feature JavaScript, templates and CSS are added when each slice is planned.

| Order | Slice | Java main / test files | Java lines | Status |
|---|---|---|---|---|
| 1 | photo | 5 / 4 | 287 | done: [plan](2026-10-05-20-06-christopherbell-dev-photo-slice-conforms-to-chris-street-style.md), PR #1488 `1d6c7d0` |
| 2 | blog | 5 / 3 | 375 | done: [plan](2026-10-06-19-31-christopherbell-dev-blog-slice-conforms-to-chris-street-style.md), PR #1492 `07859a2` |
| 3 | permission | 1 / 1 | 447 | done: [plan](2026-10-06-19-43-christopherbell-dev-permission-slice-conforms-to-chris-street-style.md), PR #1493 `17e24c4` |
| 4 | location (with `zip-coordinates.js`) | 11 / 4 | 899 | done: [plan](2026-10-06-19-59-christopherbell-dev-location-slice-conforms-to-chris-street-style.md), PR #1494 `1f1287d` |
| 5 | report | 18 / 7 | 1,704 | done: [plan](2026-10-06-20-16-christopherbell-dev-report-slice-conforms-to-chris-street-style.md), PR #1495 `6dad824` |
| 6 | sitemonitor | 17 / 6 | 1,778 | done: [plan](2026-10-06-20-33-christopherbell-dev-sitemonitor-slice-conforms-to-chris-street-style.md), PR #1496 `1d1516f` |
| 7 | message | 19 / 9 | 1,786 | done: [plan](2026-10-06-20-47-christopherbell-dev-message-slice-conforms-to-chris-street-style.md), PR #1497 `38907c6` |
| 8 | view | 13 / 3 | 1,794 | done: [plan](2026-10-06-20-56-christopherbell-dev-view-slice-conforms-to-chris-street-style.md), PR #1498 `d83f96c` |
| 9 | notification | 29 / 13 | 2,323 | done: [plan](2026-10-06-21-07-christopherbell-dev-notification-slice-conforms-to-chris-street-style.md), PR #1499 `4ba1cf6` |
| 10 | canesboxtracker | 13 / 4 | 2,953 | done: [plan](2026-10-06-21-21-christopherbell-dev-canesboxtracker-slice-conforms-to-chris-street-style.md), PR #1500 `5038999` |
| 11 | federation | 40 / 23 | 5,033 | done: [plan](2026-10-09-09-45-christopherbell-dev-federation-slice-conforms-to-chris-street-style.md), PR #1501 `be88be2` |
| 12 | vehicle | 44 / 14 | 6,880 | done: [plan](2026-10-09-10-04-christopherbell-dev-vehicle-slice-conforms-to-chris-street-style.md), PR #1502 `8bd5e2f` |
| 13 | music | 81 / 25 | 7,239 | done: [plan](2026-10-09-10-18-christopherbell-dev-music-slice-conforms-to-chris-street-style.md), PR #1503 `00d898a` |
| 14 | account | 60 / 26 | 7,435 | done: [plan](2026-10-09-10-33-christopherbell-dev-account-slice-conforms-to-chris-street-style.md), PR #1504 `8d5c68f` |
| 15 | admin | 41 / 25 | 8,506 | 15a Java done: [plan](2026-10-09-10-54-christopherbell-dev-admin-java-slice-conforms-to-chris-street-style.md), PR #1505 `3f4af8b`; 15b back-office JavaScript done: [plan](2026-10-09-11-10-christopherbell-dev-back-office-javascript-slice-conforms-to-chris-street-style.md), PR #1506 `9962afd` |
| 16 | post | 68 / 35 | 8,653 | 16a Java done: [plan](2026-10-09-11-20-christopherbell-dev-post-java-slice-conforms-to-chris-street-style.md), PR #1507 `db86567`; 16b post and Void JavaScript and templates done: [plan](2026-10-09-11-26-christopherbell-dev-post-and-void-javascript-and-templates-conform-to-chris-stre.md), PR #1508 `7ec9ae1` |
| 17 | whatsforlunch | 96 / 18 | 11,800 | 17a workflow engine done: [plan](2026-10-09-11-31-christopherbell-dev-whats-for-lunch-workflow-engine-conforms-to-chris-street-sty.md), PR #1509 `c84d203`; 17b importing and configuration done: [plan](2026-10-09-11-38-christopherbell-dev-whats-for-lunch-importing-and-configuration-conform-to-chris.md), PR #1510 `7a1b097`; 17c sessions, votes, favorites, preferences and selection done: [plan](2026-10-09-14-46-christopherbell-dev-whats-for-lunch-sessions-votes-and-selection-conform-to-chri.md), PR #1511 `7d71174`; 17d models, repositories, mapper and OpenStreetMap client done: [plan](2026-10-09-14-50-christopherbell-dev-whats-for-lunch-models-repositories-and-client-conform-to-ch.md), PR #1512 `787a281`; 17e restaurant service done: [plan](2026-10-09-14-59-christopherbell-dev-whats-for-lunch-restaurant-service-conforms-to-chris-street.md), PR #1513 `67abb24`; 17g front end done: [plan](2026-10-09-15-07-christopherbell-dev-whats-for-lunch-front-end-conforms-to-chris-street-style.md), PR #1514 `06297e6`; 17f restaurant controller done: [plan](2026-10-09-15-19-christopherbell-dev-whats-for-lunch-restaurant-controller-conforms-to-chris-stre.md), PR #1515 `2e31f37` |
| 18 | configuration | 90 / 70 | 17,691 | 18a root, mail and persistence done: [plan](2026-10-09-15-25-christopherbell-dev-configuration-root-mail-and-persistence-conform-to-chris-str.md), PR #1516 `080a67e`; 18b filter in progress: [plan](2026-10-09-15-31-christopherbell-dev-configuration-filters-conform-to-chris-street-style.md); 18c root security in progress: [plan](2026-10-09-15-50-christopherbell-dev-security-configuration-conforms-to-chris-street-style.md); 18d browser sessions in progress: [plan](2026-10-09-15-54-christopherbell-dev-browser-sessions-conform-to-chris-street-style.md); 18e mongo root and runtime in progress: [plan](2026-10-09-16-01-christopherbell-dev-mongo-runtime-configuration-conforms-to-chris-street-style.md); 18f mongo migration and 18g mongo domain pending |
| 19 | sharedfolder | 101 / 35 | 26,570 | pending; split when planned |
| 20 | Application and cross-feature tests (`architecture` and other test-only packages) | remaining | counted when planned | pending |
| 21 | cbell-lib | 65 Java files | 4,386 | pending |
| 22 | Shared browser JavaScript (`lib`, `components`, `auth`, `app.js`) and JS tests not owned by a feature | part of 128 files | part of 22,935 | pending |
| 23 | Shared templates and CSS | part of 35 templates and 10 stylesheets | counted when planned | pending |
| 24 | Operational PowerShell and `prod.cmd` | 35 files | 36,268 | pending; split when planned |
| 25 | Gradle, workflows and application YAML | 4 Gradle, 12 YAML and related | counted when planned | pending |

## Expected Changes

| File or area | Change |
|---|---|
| Builder `docs/implementation-plans/` | This umbrella plan, plus one plan per slice or sub-slice |
| Builder `docs/test-reports/` | One runtime report per slice candidate |
| Spoke code in each slice | Behavior-preserving conformance edits, plus characterization tests where coverage is missing |
| Spoke feature READMEs | Updated only where a rename changes a documented name |

## Task Breakdown

### Task 1 - Publish the umbrella plan and slice ledger

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | This plan |
| **Symbols** | Slice ledger table |
| **Inspection** | Spoke `origin/main` `ef15adc0` file and line counts per package, as listed in Inputs |
| **Behavior** | Documentation only; no spoke change |
| **Invariants** | Every first-party code area belongs to exactly one slice |
| **Boundary/API** | None |
| **Effects and failures** | Builder publication only |
| **Tests and evidence** | Plan validation and review |
| **Verification** | Save helper validation; phase finalizer publishes to Builder `origin/main` |

### Task 2 - Deliver each slice in ledger order

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1; each slice starts after the previous slice merges, so it builds on current `main` |
| **Files** | The slice's files as listed in its own plan, enumerated with `git ls-files` at the slice's base commit |
| **Symbols** | Every type, method, function and configuration key in the slice's files |
| **Inspection** | Each slice plan records its own inspection of the slice's files, callers outside the slice, tests and owning README at its base commit |
| **Behavior** | Routes, status codes, response bodies, rendered pages, scheduled jobs, persisted documents and logs keep their observable behavior |
| **Invariants** | Stored field names and JSON property names stay the same; security checks and Modulith boundaries hold; no new dependencies |
| **Boundary/API** | Published module APIs used by other slices may be renamed only with every caller updated in the same PR; external HTTP and persistence contracts are fixed |
| **Effects and failures** | Narrowed catches keep causes and the same user-facing outcome; no new I/O or background work |
| **Tests and evidence** | Passing characterization before and after; failing-then-passing regression when a style fix exposes a real defect, which is logged |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar`; Pester for script slices; local runtime report; PR CI; production `/actuator/info` readback |

### Task 3 - Recount and close the migration

| Contract | Detail |
|---|---|
| **Dependencies** | Task 2 for every slice |
| **Files** | This plan's ledger and Outcome |
| **Symbols** | Slice ledger statuses |
| **Inspection** | `git ls-files` recount of first-party code files at the final `origin/main` |
| **Behavior** | Documentation only |
| **Invariants** | Recount equals the sum of slice verdicts, or each difference is explained |
| **Boundary/API** | None |
| **Effects and failures** | Builder publication only |
| **Tests and evidence** | Recount output recorded in the log |
| **Verification** | Plan validation; Outcome reports AC-1 to AC-6 |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan validation | Not applicable: documentation |
| AC-2 | Slice plan validation and review | Not applicable: documentation |
| AC-3 | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar`; Pester for script slices; full-diff style review | Covered by AC-4 |
| AC-4 | Characterization tests for the slice | verify-local-app starts the packaged candidate on isolated MongoDB `test`; requests to the slice's routes and pages, or triggers of its jobs, return the same results as the baseline |
| AC-5 | Required PR checks: build, three Analyze, dependency-review | `wait_for_github.py live` confirms production `/actuator/info` serves the merge commit |
| AC-6 | Recount script output | Not applicable: documentation |

- **Regressions:** each slice also exercises one route of a neighboring slice that calls its published API.
- **Reruns:** any runtime-affecting edit after a report reruns the affected checks and updates the report before the PR is updated.

## Rollback or Recovery
Each slice is one squash-merged PR; revert that merge commit and let auto-deploy roll forward to the revert. No data or schema changes are in scope, so no data recovery is needed. A partially delivered migration leaves earlier slices merged and later ones pending, which is a valid state.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A rename silently changes a Mongo field or JSON property | Medium | Keep `@Field` or `@JsonProperty` names; runtime reads and writes existing-shape documents |
| Large style diffs hide a behavior change | Medium | Slices stay small; characterization before and after; one purpose per PR |
| Concurrent feature work conflicts with a slice | Medium | Slice branches are short-lived and rebased on current `main` |
| Unrelated production problem appears after an auto-deploy | Low | Production Watch and diagnostics; revert the slice if it is the cause |

## Implementation Log

### 2026-10-05 - Slice 1 (photo) delivered; workflow settled

- **Change:** Photo shipped in PR #1488 (`1d6c7d0`). The settled per-slice workflow: plan with a per-file verdict table, worktree branch, baseline focused tests, edits, full check, commit, packaged candidate on a fresh isolated MongoDB `test`, JSON compared byte-for-byte with production on the previous commit, report, PR with auto-merge, and `wait_for_github.py live` readback.
- **Reason:** Proving the workflow on the smallest slice was the user's chosen order.
- **Impact:** Later slices reuse it. Gradle needs `JAVA_TOOL_OPTIONS` as well as `GRADLE_OPTS` set to the socket folder, and must run outside the command sandbox. Auto-deploy took about 20 minutes after merge.

### 2026-10-06 - Workflow adjustments from slices 2 to 4

- **Change:** PRs that fall behind `main` are updated with `gh pr update-branch` instead of a rebase and force-push. Unpushed candidates are rebased locally before verification. The watcher script stops before deploy readback when there is no merge SHA.
- **Reason:** Another session merges Survive game work to `main` concurrently. Force-pushing is an approval gate. One watcher run reported a vacuous readback on an empty SHA.
- **Impact:** Each slice's report covers its own diff; CI verifies the combined head.

### 2026-10-06 - Cross-area moves must go through published APIs

- **Change:** When a slice moves a dependency that another area uses, the new home must be that area's published `api` package, or the frozen architecture rule fails. Resolved frozen violations must be removed from the store in the same PR.
- **Reason:** Learned in the permission slice (`LoginTokens` moved to `account.api`).
- **Impact:** Later slices check `ModularMonolithArchitectureTest` early.

### 2026-10-06 - No local ADMIN for runtime checks

- **Change:** Admin-only runtime paths are proven by unit and slice tests. Runtime reports cover everything a USER or anonymous visitor can reach, and name the gap.
- **Reason:** The application has no supported way to create a local ADMIN. A temporary promotion endpoint was refused by the session's safety classifier, and direct database writes are prohibited.
- **Impact:** This affects the admin-heavy slices (admin, report moderation, the command center). A supported, reviewed local-admin bootstrap would close the gap, but it is a security decision for the user.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
