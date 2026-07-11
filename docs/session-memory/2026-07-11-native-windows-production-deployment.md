# 2026-07-11 Native Windows Production Deployment

## 13:10 - Implementation merged; host cutover requires elevation

### Request

Replace the WSL-dependent `christopherbell.dev` production runtime with native Windows MongoDB and Java services, start them at computer boot without login, make app upgrades easy, and automatically deploy new `origin/main` commits with a cheap one-minute poller. Continue implementation through PR merge while documenting the complete workflow and preserving all production data.

### Project Context

The development computer is also the production host. Existing production remains on WSL/port 8080, while native candidates must be proven on port 8081. The WSL MongoDB data and BSON/JSON archives are rollback evidence and must not be deleted during initial migration or soak.

### Work Completed

- Approved native Windows design committed in `A:\Projects\christopherbell.dev-worktrees\boot-persistent-deploy-20260711`.
- Added mutation-free `deploy-smoke` profile with property-controlled scheduling.
- Added `prod.cmd`, Make aliases, PowerShell modules for configuration, deployment, WinSW installation, migration, operations, and automatic polling.
- Added versioned clean-worktree builds, candidate checks, release junction switching, rollback, backups, inventory equality, protected secrets, Automatic MongoDB/website startup, and `ChristopherBellAutoDeploy` Scheduled Task design.
- Added Windows production and MongoDB recovery runbooks.
- Opened PR #1185; all seven required CI/CodeQL checks passed; squash-merged as `c4cb9814f636321d073c135294887a46790fc8e7`.

### Decisions

- Automatic deployment uses outbound `git ls-remote` every 60 seconds, not a self-hosted runner or inbound webhook.
- Unchanged SHAs cause no fetch/build/restart; failed SHAs back off for 15 minutes; newer SHAs remain immediately eligible.
- WinSW v2.12.0 is pinned by independently verified SHA-256.
- Migration backup and source inventory invoke WSL tools explicitly, then stop WSL website/MongoDB only after backup verification so native MongoDB can bind 27017.
- Candidate validation runs against both `christopherbell_restore_check` and final native `christopherbell` before service cutover.

### Validation

- 25 Pester tests passed with zero parser errors.
- `:website:build` passed with 93 JavaScript tests and the complete Java suite.
- Native Windows candidate on 8081 returned home 200 and 401 `INVALID_TOKEN` for a stored account with wrong password; it did not return `RESOURCE_NOT_FOUND` and showed no mutation-start patterns.
- Candidate PID 31092 was stopped and port 8081 confirmed free.
- GitHub Windows/macOS/Ubuntu builds plus Actions, Java/Kotlin, and JavaScript CodeQL passed.

### Current State

- PR #1185 is merged.
- Native Windows production is not yet installed: current Codex process reports `IS_ADMIN=False`; `MongoDB` remains Stopped/Disabled; ProgramData deploy configuration is absent.
- Existing production port 8080 was not modified.
- Main checkout at `A:\Projects\christopherbell.dev` has local commits divergent from the squash merge; do not reset or overwrite it. Continue host work from the merged source/worktree without discarding user state.

### Follow-ups

1. Open Administrator PowerShell in the merged checkout and run the documented install bootstrap.
2. Configure protected `deploy.json` and `app.env` with actual native paths and smoke account.
3. Run deploy/migrate WhatIf gates, fresh WSL backup and inventory, validation restore, controlled cutover, and rollback rehearsal.
4. Install the auto-deploy task, reboot without login, verify services/8080/task state, then retain WSL for the seven-day soak.
