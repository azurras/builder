# christopherbell.dev Mobile Command Center Spec

## Document Status

ready-for-review

## Purpose

Add a secure, admin-only, mobile-first command center to christopherbell.dev so Christopher can monitor and perform a small set of controlled actions on the Windows desktop that hosts the production website, whether he is away from the computer or sitting beside it.

## Source and Trusted Guidance

- Source: Christopher's direct request on July 12, 2026 for the full design, implementation, local verification, test reporting, pull request, CI, merge, production restart, closure, and session-memory loop.
- Trusted decisions: full machine controls are in v1; destructive actions require current-password re-entry and an exact typed phrase; only the configured application log is exposed; the page is a dedicated `/command-center` route; the Mission Control Grid layout is approved; OSHI with the optional Windows LibreHardwareMonitor integration is approved.
- No GitHub comments, attachments, ZIP files, patches, or linked files have been used as instructions.

## Background

christopherbell.dev is a Java 25, Spring Boot 4.1 monolith with Thymeleaf templates, vanilla browser JavaScript, MongoDB, JWT authentication, method security, and an existing admin Back Office. The production app runs on the same Windows 11 Pro desktop as an automatic WinSW service named `ChristopherBellDev`. The service runs as `LocalSystem`, depends on MongoDB, restarts on failure, and writes rolling stdout, stderr, and wrapper logs beneath `C:\ProgramData\christopherbell.dev\logs`.

The host currently has an Intel Core i5-13600K, 32 GB RAM, and an NVIDIA GeForce RTX 4070. NVIDIA's installed `nvidia-smi` command returns GPU utilization, temperature, and memory readings. OSHI provides CPU, memory, disk, network, uptime, and sensor APIs; its optional Windows LibreHardwareMonitor integration is required for the best available CPU-temperature reading. Any unsupported sensor must remain explicitly unavailable rather than being estimated.

The authoritative spoke checkout is `A:\Projects\christopherbell.dev`. Its primary `main` checkout was clean but divergent when inspected, so implementation must use an isolated feature worktree created from refreshed `origin/main` and must not disturb the primary checkout.

## Goals

- Provide a fast, responsive command-center page optimized for a phone while remaining useful on a desktop display.
- Show current and short-history CPU, CPU temperature, RAM, GPU, GPU temperature, storage, network, uptime, application, and dependency health.
- Show a delayed, bounded, searchable, severity-filtered tail of the configured website application log.
- Allow an administrator to restart the website service, schedule a Windows restart, schedule Windows shutdown, and cancel a pending restart or shutdown.
- Require defense in depth for privileged actions: server-side admin authorization, password re-verification, a short-lived one-time challenge, exact confirmation phrases, throttling, cooldowns, idempotency, and audit records.
- Keep runtime overhead low by sampling once on the server and returning cached snapshots to all browser clients.
- Complete automated, local runtime, CI, merge, production restart, closure, and durable Builder reporting phases.

## Non-Goals

- No general terminal, remote shell, PowerShell console, command input, script runner, or arbitrary process execution.
- No arbitrary file browser, file path parameter, full-file download, file deletion, log deletion, or log mutation.
- No general Windows process manager, registry editor, service manager, package installer, desktop streaming, keyboard/mouse control, or remote file transfer.
- No exposure of Windows Event Logs in v1.
- No Prometheus, Grafana, Elasticsearch, or separate privileged sidecar service in v1.
- No durable database storage for high-frequency metric samples; short history remains in memory.
- No real PC restart or shutdown during development verification.
- No broad authentication-system rewrite or MFA enrollment feature in this change.

## User Experience

### Navigation and Access

- Add a dedicated `/command-center` page and an admin-only link from Back Office and the authenticated navigation menu.
- The server-rendered page shell contains no machine data and remains hidden until the browser confirms the current account has `ADMIN` authority.
- Every data and action API independently enforces an active, approved, authenticated administrator on the server. Loading the unauthenticated HTML shell must not reveal host data or enable any operation.
- Unauthorized or expired sessions redirect to login or Back Office with a clear, non-sensitive message.

### Mission Control Grid

- Header: overall state (`Healthy`, `Degraded`, `Action pending`, or `Offline`), production-service state, and age of the most recent sample.
- Primary cards: CPU use, CPU temperature, RAM used/total, GPU use, and GPU temperature.
- Supporting cards: GPU memory and power when available, disk used/free, network receive/transmit rate, Windows uptime, website uptime, production port, application version/commit, last application start, MongoDB connectivity, and local response time.
- In-memory sparklines cover approximately the latest 15 minutes for CPU, RAM, GPU, temperatures, disk activity, and network traffic.
- Alert strip identifies stale samples, unavailable sensors, configured high-use or high-temperature thresholds, low disk space, MongoDB failure, service failure, and pending actions.
- Thresholds are configuration properties with conservative defaults and can be changed without code edits.
- Missing values display `Unavailable`; stale last-good values display their sample time and never masquerade as current readings.

### Application Log Panel

- Poll for new application-log records every five seconds; do not use WebSockets or server-sent events for v1.
- Read only the server-configured production stdout log. The API accepts no file path or filename.
- Support pause/resume, auto-scroll, a fixed severity selector, literal case-insensitive text search, copy-visible-lines, and clear-view.
- Clear-view changes only browser state and never truncates or deletes the real file.
- Return a bounded page with an opaque cursor, maximum record count, and maximum byte count. Recover safely from file rotation, truncation, deletion, or an expired cursor.
- Redact likely authorization headers, bearer tokens, JWTs, passwords, API keys, secrets, and token-like values before returning lines.
- Render all log content with text nodes, never injected HTML.

### Danger Zone

- Keep machine actions visually separate from metrics and logs.
- Offer `Restart Website`, `Restart Computer`, `Shut Down Computer`, and `Cancel Pending Action`.
- Restart and shutdown use a 60-second Windows countdown. The page shows the deadline and enables cancellation before the operating system accepts the final transition.
- Restart Website returns an accepted response before invoking the fixed WinSW restart command. The browser enters reconnect mode, backs off polling, and reports when the site becomes healthy again.
- Prevent accidental double taps and duplicate network retries from creating multiple actions.

## Backend Architecture

Create a focused `dev.christopherbell.admin.commandcenter` feature with small ownership boundaries:

- `metrics`: scheduled host sampling, immutable current snapshot, short in-memory history, threshold evaluation, and provider health.
- `logs`: fixed-path incremental tailing, cursor handling, rotation recovery, bounding, severity filtering, literal search, and redaction.
- `action`: challenge creation/consumption, password re-verification, command eligibility, cooldowns, idempotency, execution, pending-action state, and cancellation.
- `model`: explicit response, challenge, confirmation, action, sensor-status, and health-status contracts.
- Thin controller methods under a versioned admin API delegate all rules to these services.
- Existing `AdminActivityService` records command-center action outcomes instead of creating a second audit store.
- Configuration properties own polling intervals, history duration, alert thresholds, enabled state, service name, WinSW executable path, production log path, timeouts, and maximum log page bounds.

### Sampling and Data Flow

1. One scheduled collector samples host providers every five seconds.
2. CPU, memory, filesystem, network, operating-system uptime, application uptime, and CPU sensors come from OSHI.
3. A fixed `nvidia-smi` query collects RTX 4070 utilization, temperature, memory, and power with a short process timeout.
4. Application and MongoDB health checks are bounded and cannot stall the collector.
5. Each provider publishes success, unavailable, stale, or error state independently.
6. The collector stores an immutable latest snapshot and bounded in-memory samples for sparklines.
7. Browser polling reads the cached snapshot; it never starts hardware commands per client request.
8. Browser polling pauses while the document is hidden and backs off after failures.

### Proposed API Surface

- `GET /api/admin/command-center/2026-07-12/snapshot`: current health, metrics, alert state, pending action, and bounded history.
- `GET /api/admin/command-center/2026-07-12/logs`: new redacted records after an opaque cursor, with fixed level and literal-query filters.
- `POST /api/admin/command-center/2026-07-12/action-challenges`: create a single-use challenge for one fixed action enum.
- `POST /api/admin/command-center/2026-07-12/actions`: consume the challenge with current password and the action's exact confirmation phrase.
- `POST /api/admin/command-center/2026-07-12/actions/cancel`: cancel a pending machine restart or shutdown for an authenticated administrator.

Exact request and response records will be finalized in the implementation plan after source inspection. Password fields must be write-only request data and excluded from logs, exceptions, audit details, equality output, and string representations.

## Privileged Action Security

1. The controller and service both require an active, approved `ADMIN` account.
2. Challenge creation accepts only a closed action enum; it generates a cryptographically random identifier bound to the account, action, and two-minute expiry.
3. Confirmation consumes the challenge atomically so replay, action substitution, and concurrent double submission fail closed.
4. The server re-verifies the account's current password hash and current admin state at execution time.
5. Exact phrases are `RESTART SITE`, `RESTART COMPUTER`, and `SHUTDOWN COMPUTER`.
6. Failed challenge or password attempts are rate-limited. Accepted actions have configurable cooldowns and idempotency protection.
7. Production actions are disabled by default and require explicit Windows production configuration.
8. Execution uses `ProcessBuilder` argument arrays built entirely from trusted configuration and fixed enum mappings. Requests never contribute executable paths, service names, file paths, arguments, or shell fragments.
9. Website restart invokes only the configured WinSW executable with its fixed restart operation after the HTTP response can be returned.
10. Machine restart maps only to a fixed `shutdown.exe` restart argument list with a 60-second delay. Machine shutdown maps only to a fixed shutdown argument list with the same delay. Cancellation maps only to the fixed abort operation.
11. Audit records include administrator, action, source IP, challenge result, request and completion times, accepted command type, execution result, cancellation, and a safe failure category. They exclude passwords, JWTs, authorization headers, raw request bodies, and command-line secrets.
12. Log lines are untrusted input and must not be used to construct markup, commands, paths, or queries.

## Performance and Reliability

- Default server sampling and browser polling interval: five seconds.
- Expensive hardware providers execute once per server interval, not once per connected browser.
- Each external command and health dependency has an independent timeout and failure state.
- Metric history is bounded by sample count and discarded on application restart.
- Log reads are incremental and bounded by both record count and bytes.
- The UI remains usable when individual providers are unavailable.
- A stale-data watchdog marks the dashboard degraded when the collector stops advancing.
- No command-center failure may prevent the public website from starting; unsupported providers must degrade gracefully.

## Configuration and Deployment

- Local and test profiles default to simulated actions.
- Production power actions require an explicit enable property and Windows host detection.
- Production configuration fixes the service name to `ChristopherBellDev`, the WinSW executable beneath `C:\ProgramData\christopherbell.dev\service`, and the stdout log beneath `C:\ProgramData\christopherbell.dev\logs`.
- Sensitive configuration remains in environment or deployment files and is never committed.
- The existing automatic service and restart-on-failure policy remain in place.
- Dependency additions must use current compatible OSHI and Windows sensor artifacts without adding a frontend package workflow.

## Expected Files and Modules

- `website/build.gradle.kts`: OSHI and Windows sensor dependencies.
- `website/src/main/java/dev/christopherbell/admin/commandcenter/**`: feature backend.
- `website/src/main/java/dev/christopherbell/admin/README.md`: command-center ownership and API behavior.
- `website/src/main/java/dev/christopherbell/configuration/**`: typed command-center configuration when cross-cutting ownership is required.
- `website/src/main/java/dev/christopherbell/view/**`: dedicated page route.
- `website/src/main/resources/templates/command-center.html`: page shell.
- `website/src/main/resources/static/js/command-center.js`: polling, rendering, logs, and action confirmation.
- `website/src/main/resources/static/js/lib/api.js`: versioned API paths.
- `website/src/main/resources/static/js/components/nav.js` and Back Office assets: admin-only discovery link.
- `website/src/main/resources/static/css/main.css` and CSS ownership docs: responsive Mission Control layout.
- Focused Java and browser tests mirroring the new feature boundaries.

## Validation Plan

### Automated Validation

- Develop with tests first for each service and controller boundary.
- Test CPU/RAM/disk/network sampling, OSHI unavailable values, NVIDIA success, timeout, missing executable, malformed output, and stale-last-good behavior.
- Test bounded history and threshold alerts.
- Test log cursor progression, initial tail, record and byte bounds, filtering, literal search, rotation, truncation, missing file, and secret redaction.
- Test anonymous, regular-user, inactive-admin, and valid-admin API paths.
- Test wrong password, wrong phrase, expired challenge, replay, action mismatch, concurrent consumption, rate limits, cooldowns, idempotency, disabled actions, non-Windows execution, and audit outcomes.
- Test exact fixed command argument arrays and prove request fields cannot alter executable paths or arguments.
- Test JavaScript polling, tab visibility behavior, stale/unavailable rendering, log text rendering, filters, countdown, cancellation, double-submit prevention, and restart reconnection.
- Run focused tests first, then `:website:test`, `:website:jsTest`, `node --check` for touched browser files, and `:website:build` with an isolated Windows Gradle user home if needed.

### Local Runtime Validation

- Start the implementation from an isolated worktree on a non-production port, leaving port 8080 untouched.
- Use real read-only host metrics, real NVIDIA output, OSHI CPU temperature when available, and a controlled temporary application log.
- Authenticate as a local admin and exercise the command-center page at phone and desktop viewport sizes.
- Exercise log polling with exact test lines, rotation, filtering, search, and redaction evidence.
- Run all privileged actions in simulation mode and record the exact intended command type and argument list without restarting or shutting down Windows.
- Verify anonymous and non-admin requests cannot read metrics/logs, create challenges, run actions, or cancel actions.
- Save a detailed Builder test report with exact URLs, inputs, responses, screenshots or equivalent evidence, and pass/fail state.

### Publish and Production Validation

- Push a feature branch, open a pull request, wait for all required GitHub CI gates, and merge only when they pass.
- Deploy the merged build using the existing production service workflow.
- Perform one real `Restart Website` action, confirm the WinSW service returns, and verify the public homepage, authenticated admin flow, command-center snapshot, and log stream afterward.
- Do not trigger a real PC restart or shutdown during the delivery loop. Their executor mappings and simulation evidence are the acceptance proof for v1.

## Acceptance Criteria

- Only an active, approved administrator can read command-center data or request actions.
- The dedicated mobile-first page displays all requested metrics when supported and explicit unavailable/stale states otherwise.
- CPU temperature uses the approved OSHI Windows sensor integration and never fabricates readings.
- GPU usage, temperature, memory, and power are collected through the installed NVIDIA tooling with bounded execution.
- Application log polling is delayed, incremental, bounded, redacted, fixed-path, searchable, filterable, and safe from HTML injection.
- Website restart, machine restart, shutdown, and cancellation exist as closed, allowlisted actions with the approved step-up confirmation flow.
- Accepted machine restart and shutdown requests provide a 60-second cancellation window.
- Every action attempt and outcome is auditable without recording credentials or secrets.
- Command-center failures do not block normal website startup or public behavior.
- Automated tests, safe local runtime testing, test report validation, PR CI, merge, production website restart, and post-restart smoke verification pass.
- Builder work, spec, implementation plan, spoke updates/review, test report, closure, and session memory are indexed, validated, committed, and pushed at their required phase checkpoints.

## Risks and Mitigations

- Host-control exposure increases the consequence of admin compromise. Mitigate with server-side authorization, password re-verification, one-time challenges, exact phrases, throttling, closed action enums, fixed command arrays, TLS-only production access, and audit evidence.
- The production website currently runs as `LocalSystem`. Keep v1 commands strictly allowlisted and record a future least-privilege service-account evaluation rather than adding general host capabilities.
- CPU sensors vary by motherboard and driver. Use the approved sensor integration, independent provider state, and explicit unavailable/stale UI.
- A service restart interrupts its own page. Return acceptance first, run the fixed restart asynchronously, and make the browser reconnect with bounded backoff.
- Log files can contain sensitive or attacker-controlled text. Enforce fixed paths, bounds, server redaction, literal filtering, and text-only rendering.
- Frequent polling can waste resources. Cache samples server-side, pause hidden tabs, and keep history and log responses bounded.
- The primary spoke checkout is divergent. Use an isolated worktree from current `origin/main` and preserve the existing checkout exactly.

## Rollback

- Disable command-center actions through production configuration without removing the monitoring page.
- Remove the admin navigation link and command-center API mappings if an emergency disable is required.
- Revert the merged feature commit and redeploy the prior known-good JAR through the existing WinSW deployment path.
- The feature adds no metric-history persistence or irreversible data migration.

## Open Questions

None. The product, layout, sensor dependency, log scope, privileged-action scope, confirmation method, security flow, and validation boundaries were approved before this spec was written.

## Spec Self-Review

- Placeholder scan: no incomplete placeholders or unresolved implementation decisions remain.
- Internal consistency: the dedicated page, cached polling architecture, fixed log source, closed action set, step-up security, and verification strategy agree across sections.
- Scope check: the work is substantial but cohesive around one admin command-center feature and can be executed from one detailed implementation plan with focused subfeature boundaries.
- Ambiguity check: unsupported sensors, destructive-action testing, production restart scope, command allowlisting, and the divergent primary checkout are explicit.
