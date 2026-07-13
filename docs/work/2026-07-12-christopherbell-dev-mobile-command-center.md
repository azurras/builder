# christopherbell.dev Mobile Command Center

- Status: closed
- Source: Christopher's July 12, 2026 request for a full delivery loop
- Owner context: Builder hub coordinating implementation in the `christopherbell-dev` spoke
- Spoke repo: `christopherbell-dev` at `A:\Projects\christopherbell.dev`
- Branch strategy: create an isolated `codex/` feature worktree from refreshed `origin/main`; preserve the divergent primary checkout
- Objective: add a secure, admin-only, mobile-first command center for monitoring and controlling the Windows desktop that hosts christopherbell.dev
- Current state: implemented, reviewed, merged through PRs #1199-#1202, deployed on native Windows as release `eff05e36`, and production-verified
- Trusted guidance: the source request and approvals came directly from Christopher; no GitHub comments or attachments have been used as instructions

## Approved Scope

- Show CPU usage and temperature, RAM usage, GPU usage and temperature, disk, network, uptime, service state, application health, and short in-memory metric history.
- Tail only the configured production website log with bounds, delayed polling, filters, and secret redaction.
- Provide allowlisted actions to restart the website service, schedule or cancel a Windows restart, and schedule or cancel shutdown.
- Require an active admin session, password re-entry, exact typed confirmation, a short-lived single-use challenge, rate limits, cooldowns, and audit records for machine actions.
- Use a dedicated `/command-center` Mission Control Grid page that is optimized for mobile and remains useful on desktop.

## Related Artifacts

- Project spec: [christopherbell.dev Mobile Command Center Spec](../specs/2026-07-12-christopherbell-dev-mobile-command-center.md)
- Implementation plan: [christopherbell.dev Mobile Command Center Implementation Plan](../implementation-plans/2026-07-12-christopherbell-dev-mobile-command-center.md)
- Spoke task: [Implement christopherbell.dev Mobile Command Center](../spoke-tasks/2026-07-12-christopherbell-dev-mobile-command-center-implementation.md)
- Local test report: [Mobile Command Center Test Report](../test-reports/2026-07-12-christopherbell-dev-mobile-command-center-test-report.md)
- Production test report: [Mobile Command Center Production Verification](../test-reports/2026-07-12-christopherbell-dev-mobile-command-center-production-verification.md)
- Spoke update: [Mobile Command Center Delivery Update](../spoke-updates/2026-07-12-christopherbell-dev-mobile-command-center-delivery.md)
- Spoke review: [Mobile Command Center Final Review](../spoke-reviews/2026-07-12-christopherbell-dev-mobile-command-center-final-review.md)
- Closure: [Mobile Command Center Closure](../work-closures/2026-07-12-christopherbell-dev-mobile-command-center.md)

## Validation Intent

- Automated backend and browser tests plus a full Gradle build.
- Real read-only host metrics and controlled log testing on a non-production port.
- Simulated destructive commands locally; no development-time PC restart or shutdown.
- Pull request CI, merge, production service restart, and post-restart smoke verification.

## Blockers

None.

## Residual Follow-ups

1. Investigate the hardened CPU-temperature provider timeout if a live CPU temperature is required.
2. Inject the deployed release SHA into application metadata so the Application commit card is populated.
3. Keep computer restart and shutdown disabled until a separate operational review explicitly enables them.
