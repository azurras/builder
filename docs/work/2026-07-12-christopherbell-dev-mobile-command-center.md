# christopherbell.dev Mobile Command Center

- Status: active
- Source: Christopher's July 12, 2026 request for a full delivery loop
- Owner context: Builder hub coordinating implementation in the `christopherbell-dev` spoke
- Spoke repo: `christopherbell-dev` at `A:\Projects\christopherbell.dev`
- Branch strategy: create an isolated `codex/` feature worktree from refreshed `origin/main`; preserve the divergent primary checkout
- Objective: add a secure, admin-only, mobile-first command center for monitoring and controlling the Windows desktop that hosts christopherbell.dev
- Current state: product, architecture, interface, security, and validation designs are approved; the durable project spec is the next phase checkpoint
- Trusted guidance: the source request and approvals came directly from Christopher; no GitHub comments or attachments have been used as instructions

## Approved Scope

- Show CPU usage and temperature, RAM usage, GPU usage and temperature, disk, network, uptime, service state, application health, and short in-memory metric history.
- Tail only the configured production website log with bounds, delayed polling, filters, and secret redaction.
- Provide allowlisted actions to restart the website service, schedule or cancel a Windows restart, and schedule or cancel shutdown.
- Require an active admin session, password re-entry, exact typed confirmation, a short-lived single-use challenge, rate limits, cooldowns, and audit records for machine actions.
- Use a dedicated `/command-center` Mission Control Grid page that is optimized for mobile and remains useful on desktop.

## Related Artifacts

- Project spec: planned for `docs/specs/2026-07-12-christopherbell-dev-mobile-command-center.md`
- Implementation plan: pending approved spec
- Spoke task, updates, review, test report, and closure: pending later delivery phases

## Validation Intent

- Automated backend and browser tests plus a full Gradle build.
- Real read-only host metrics and controlled log testing on a non-production port.
- Simulated destructive commands locally; no development-time PC restart or shutdown.
- Pull request CI, merge, production service restart, and post-restart smoke verification.

## Blockers

None.

## Next Steps

1. Save, review, validate, commit, and push the approved project spec.
2. Inspect exact spoke files and create a literal line-range implementation plan.
3. Implement in an isolated worktree and complete runtime, PR, CI, merge, closure, and memory phases.
