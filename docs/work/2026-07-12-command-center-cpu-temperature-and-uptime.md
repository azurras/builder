# christopherbell.dev Command Center CPU Temperature and Uptime

- Status: active
- Source: Christopher's July 12, 2026 follow-up to fix the production CPU-temperature timeout and display uptime in human units
- Owner context: Builder hub coordinating a focused bug fix in the `christopherbell-dev` spoke
- Spoke repo: `christopherbell-dev` at `A:\Projects\christopherbell.dev`
- Branch strategy: isolated `codex/` worktree from refreshed `origin/main`; preserve the divergent primary checkout
- Objective: produce a real CPU temperature without blocking five-second telemetry or leaking PowerShell processes, and render uptime as minutes, hours, and days
- Current state: implementation and safe port-8090 runtime verification passed; test report checkpoint is complete and publication is next
- Trusted guidance: direct user request; no GitHub comments or attachments used as instructions

## Root-Cause Evidence

- Production config gives every provider two seconds.
- The CPU-temperature client starts a reusable jPowerShell session but recreates and opens a LibreHardwareMonitor `Computer` for every read.
- On timeout, jPowerShell abandons its response reader and attempts asynchronous process cleanup; the production host retained the PowerShell children.
- Two live snapshots 15 seconds apart showed Java-descendant PowerShell processes increase from 14 to 16, with a new process approximately every seven seconds.
- The official jPowerShell default is ten seconds and its documentation recommends longer deadlines for scripts.
- A checksum-verified direct jLibreHardwareMonitor scan found the i5-13600K but returned zero CPU temperatures without elevation, confirming that privileged access is required for the CPU sensor on this host.

## Related Artifacts

- Parent closure: [Mobile Command Center Closure](../work-closures/2026-07-12-christopherbell-dev-mobile-command-center.md)
- Spec: [Command Center CPU Temperature and Uptime Spec](../specs/2026-07-12-command-center-cpu-temperature-and-uptime.md)
- Implementation plan: [Command Center CPU Temperature and Uptime Implementation Plan](../implementation-plans/2026-07-12-command-center-cpu-temperature-and-uptime.md)
- Test report: [Command Center CPU Temperature and Uptime Test Report](../test-reports/2026-07-12-command-center-cpu-temperature-and-uptime-test-report.md)
- Spoke update/review and closure: pending later delivery phases

## Validation Intent

- Failing tests first for timeout process-tree termination, non-blocking cached refresh, last-good retention, and human uptime formatting.
- Full Java/JavaScript build and security-focused diff review.
- Candidate runtime on a non-production port with no changes to live port 8080.
- CI, merge, native Windows deployment, live CPU-temperature result, stable PowerShell process count, and uptime visual verification.

## Blockers

None. A valid CPU temperature remains hardware/driver dependent; safe unavailable behavior is still required if SYSTEM cannot obtain a non-zero value.

## Next Steps

1. Save and validate the implementation plan.
2. Implement in an isolated spoke worktree using TDD.
3. Complete safe runtime, CI, merge, deploy, production verification, and Builder closure.
