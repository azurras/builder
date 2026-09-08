# 2026-07-11 - christopherbell-dev Session Memory

Website development and production-delivery history. Repository paths, guardrails, reviews, and snapshots are dated evidence; verify current configuration before execution.

## Reading and Updating This Record

This file records work and events for this project on this date. Append same-day progress, decisions, reviews, blockers, publication and closure here; use a separate file for each other date. Sources with no date in their filename are grouped by their last recorded Git change date in the original corpus; that is archival provenance, not a claim that every described event occurred that day. Plans and runtime reports remain separate evidence documents. Imported instructions and statuses are historical evidence, not current operating policy; current AGENTS.md and skills take precedence. Use the source navigation or search for an issue, date, or topic rather than loading the entire history.

## Imported Source Navigation

- [docs/session-memory/2026-07-11-native-windows-production-deployment.md](#source-docs-session-memory-2026-07-11-native-windows-production-deployment-md)
- [docs/spoke-reviews/2026-07-11-native-windows-production-deployment-review.md](#source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md)

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md"></a>
## 2026-07-11 | session-memory | 2026-07-11 Native Windows Production Deployment

Original source: `docs/session-memory/2026-07-11-native-windows-production-deployment.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `21862393a9e68474d6958a5bc2d4c5f4eb32febbfde8850335ee8738304c5ca5`.

<!-- migrated-source: docs/session-memory/2026-07-11-native-windows-production-deployment.md -->
<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--2026-07-11-native-windows-production-deployment"></a>
### 2026-07-11 Native Windows Production Deployment

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--1310---implementation-merged-host-cutover-requires-elevation"></a>
#### 13:10 - Implementation merged; host cutover requires elevation

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--request"></a>
##### Request

Replace the WSL-dependent `christopherbell.dev` production runtime with native Windows MongoDB and Java services, start them at computer boot without login, make app upgrades easy, and automatically deploy new `origin/main` commits with a cheap one-minute poller. Continue implementation through PR merge while documenting the complete workflow and preserving all production data.

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--project-context"></a>
##### Project Context

The development computer is also the production host. Existing production remains on WSL/port 8080, while native candidates must be proven on port 8081. The WSL MongoDB data and BSON/JSON archives are rollback evidence and must not be deleted during initial migration or soak.

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--work-completed"></a>
##### Work Completed

- Approved native Windows design committed in `A:\Projects\christopherbell.dev-worktrees\boot-persistent-deploy-20260711`.
- Added mutation-free `deploy-smoke` profile with property-controlled scheduling.
- Added `prod.cmd`, Make aliases, PowerShell modules for configuration, deployment, WinSW installation, migration, operations, and automatic polling.
- Added versioned clean-worktree builds, candidate checks, release junction switching, rollback, backups, inventory equality, protected secrets, Automatic MongoDB/website startup, and `ChristopherBellAutoDeploy` Scheduled Task design.
- Added Windows production and MongoDB recovery runbooks.
- Opened PR #1185; all seven required CI/CodeQL checks passed; squash-merged as `c4cb9814f636321d073c135294887a46790fc8e7`.

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--decisions"></a>
##### Decisions

- Automatic deployment uses outbound `git ls-remote` every 60 seconds, not a self-hosted runner or inbound webhook.
- Unchanged SHAs cause no fetch/build/restart; failed SHAs back off for 15 minutes; newer SHAs remain immediately eligible.
- WinSW v2.12.0 is pinned by independently verified SHA-256.
- Migration backup and source inventory invoke WSL tools explicitly, then stop WSL website/MongoDB only after backup verification so native MongoDB can bind 27017.
- Candidate validation runs against both `christopherbell_restore_check` and final native `christopherbell` before service cutover.

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--validation"></a>
##### Validation

- 25 Pester tests passed with zero parser errors.
- `:website:build` passed with 93 JavaScript tests and the complete Java suite.
- Native Windows candidate on 8081 returned home 200 and 401 `INVALID_TOKEN` for a stored account with wrong password; it did not return `RESOURCE_NOT_FOUND` and showed no mutation-start patterns.
- Candidate PID 31092 was stopped and port 8081 confirmed free.
- GitHub Windows/macOS/Ubuntu builds plus Actions, Java/Kotlin, and JavaScript CodeQL passed.

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--current-state"></a>
##### Current State

- PR #1185 is merged.
- Native Windows production is not yet installed: current Codex process reports `IS_ADMIN=False`; `MongoDB` remains Stopped/Disabled; ProgramData deploy configuration is absent.
- Existing production port 8080 was not modified.
- Main checkout at `A:\Projects\christopherbell.dev` has local commits divergent from the squash merge; do not reset or overwrite it. Continue host work from the merged source/worktree without discarding user state.

<a id="source-docs-session-memory-2026-07-11-native-windows-production-deployment-md--follow-ups"></a>
##### Follow-ups

1. Open Administrator PowerShell in the merged checkout and run the documented install bootstrap.
2. Configure protected `deploy.json` and `app.env` with actual native paths and smoke account.
3. Run deploy/migrate WhatIf gates, fresh WSL backup and inventory, validation restore, controlled cutover, and rollback rehearsal.
4. Install the auto-deploy task, reboot without login, verify services/8080/task state, then retain WSL for the seven-day soak.

<!-- /migrated-source: docs/session-memory/2026-07-11-native-windows-production-deployment.md -->

<a id="source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md"></a>
## 2026-07-11 | spoke-reviews | Native Windows Production Deployment Review

Original source: `docs/spoke-reviews/2026-07-11-native-windows-production-deployment-review.md` at `78f01833d1c348b4ac87c90e9832bb41481f93db`. SHA-256 (normalized text): `73ac9be971ad41208df4e14dc30e80267559e15ac8d648d62b9f4e544b191ff0`.

<!-- migrated-source: docs/spoke-reviews/2026-07-11-native-windows-production-deployment-review.md -->
<a id="source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md--native-windows-production-deployment-review"></a>
### Native Windows Production Deployment Review

<a id="source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md--findings"></a>
#### Findings

No critical or important code findings remained at merge. Direct review corrected process-output deadlock risk, secret-safe child failure messages, explicit WSL MongoDB source backup/inventory, native MongoDB Automatic startup, WSL/native listener cutover ordering, validation-database candidate testing, and automatic-deploy SHA race handling before publication.

<a id="source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md--reviewed-work"></a>
#### Reviewed Work

- Repository: `A:\Projects\christopherbell.dev` / `https://github.com/azurras/christopherbell.dev.git`.
- Branch: `codex/boot-persistent-deploy`.
- Implementation commit: `8c68fe82`.
- Pull request: [#1185](https://github.com/azurras/christopherbell.dev/pull/1185).
- Merge: `c4cb9814f636321d073c135294887a46790fc8e7`.
- Scope: native Windows service installation, clean-release deployment, MongoDB migration, operations, one-minute automatic deployment, mutation-free candidate profile, tests, and runbooks.

<a id="source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md--validation-checked"></a>
#### Validation Checked

- 25 Pester tests and zero PowerShell parser errors.
- Full `:website:build`, including 93 JavaScript tests and the complete Java suite.
- Port-8081 runtime smoke against live data: home 200; stored account with invalid password 401 `INVALID_TOKEN`, not `RESOURCE_NOT_FOUND`; zero mutation-start log matches.
- Candidate stopped and port 8081 released.
- WinSW pinned SHA-256 independently verified.
- GitHub Windows/macOS/Ubuntu builds and all CodeQL analyses successful.

<a id="source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md--residual-risks"></a>
#### Residual Risks

- Host migration and reboot behavior remain operational acceptance work, not code-review evidence.
- The current Codex process is not elevated, so services and ProgramData configuration were deliberately left unchanged.
- WSL source data and backups must remain intact through soak closure.

<a id="source-docs-spoke-reviews-2026-07-11-native-windows-production-deployment-review-md--merge-readiness"></a>
#### Merge Readiness

Ready and merged. Host cutover remains gated on Administrator PowerShell, real protected configuration, verified backup/inventory equality, alternate-port checks, rollback rehearsal, and reboot acceptance.

<!-- /migrated-source: docs/spoke-reviews/2026-07-11-native-windows-production-deployment-review.md -->

