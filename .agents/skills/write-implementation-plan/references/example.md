# Require the JWT Signing Secret

## Plan Format
task-contract-v2

## Document Status
complete

## Project
example-app

## Objective
The application refuses to start without an explicit JWT signing secret.

## Background
Example issue 42: `SecurityConfig` falls back to a hard-coded `dev-secret` when `JWT_SECRET` is unset, so a misconfigured deployment signs tokens with a public value.

## Goals
- No code path signs tokens with a built-in secret (AC-1).
- Correctly configured environments are unaffected (AC-2).

## Non-Goals
- Rotating existing production secrets: owned by operations and unaffected by this code change.
- Moving secrets to a vault: a separate infrastructure decision with its own issue.

## Acceptance Criteria
- AC-1: Starting without `JWT_SECRET` fails at startup with an error that names the variable and not its value.
- AC-2: Starting with `JWT_SECRET` set serves `/actuator/health` with 200.
- AC-3: The change is merged to `main` and issue 42 is closed with the test report linked.

## Inputs
- Story: Example issue 42.
- Repository `example-app` at `main` `abc1234`; read `SecurityConfig`, its callers and `SecurityConfigTest`.

## Branch
`codex/issue-42-require-secret` from `main`.

## Assumptions
- All configuration loads through Spring's `Environment`, so one lookup covers every entry point.

## Open Questions
None.

## Design
Replace the fallback with a required lookup that fails during context startup.

Alternatives considered:
- Log a warning and keep the fallback: rejected because the app would still run insecurely.
- Generate a random secret per start: rejected because tokens would break across restarts and instances.

## Expected Changes
- `src/main/java/example/SecurityConfig.java`: `jwtSecret()` requires `JWT_SECRET`.
- `src/test/java/example/SecurityConfigTest.java`: regression for the missing secret.
- Local run configuration documents the required variable.

## Task Breakdown

### Task 1 - Require the signing secret
Required skill: write-chris-street-style-code
Dependencies: None.
Files: `src/main/java/example/SecurityConfig.java`; `src/test/java/example/SecurityConfigTest.java`
Symbols: `SecurityConfig.jwtSecret`, `SecurityConfig.validateSecret`
Inspection: Read `SecurityConfig`, its two callers and `SecurityConfigTest` at `abc1234`.
Behavior: Missing `JWT_SECRET` fails context startup; a present value is used unchanged.
Invariants: No built-in secret remains; the secret value never appears in errors or logs.
Boundary/API: `jwtSecret()` signature unchanged; environment variable name unchanged.
Effects and failures: Startup throws `IllegalStateException` naming the variable.
Tests and evidence: Failing regression for the missing secret first, then passing; existing tests still pass.
Verification: `./gradlew test --tests SecurityConfigTest`

## Test Plan
- AC-1: `SecurityConfigTest.rejectsMissingSecret`; then start locally without `JWT_SECRET` with verify-local-app and capture the startup error.
- AC-2: Start locally with `JWT_SECRET=local-test-secret` and request `/actuator/health`; expect 200.
- AC-3: CI passes on the PR; merge and closure readback.
- Regression: full `./gradlew test`.

## Rollback or Recovery
Revert the merge commit; no data or schema changes.

## Risks
- Developers without `JWT_SECRET` cannot start the app locally: mitigated by the run configuration and a clear error.

## Implementation Log

### 2026-10-04 - Fail in the bean, not at first use

- Change: The check moved from `jwtSecret()` callers into a `@PostConstruct` validation on `SecurityConfig`.
- Reason: One caller is lazy, so a missing secret only failed on the first login instead of at startup (AC-1).
- Impact: Task 1 Symbols now include `SecurityConfig.validateSecret`; Expected Changes unchanged.

## Outcome
- AC-1: Met. Startup fails with "JWT_SECRET is required"; see test report `2026-10-04-require-jwt-secret.md`.
- AC-2: Met. Health returned 200 with the secret set; same report.
- AC-3: Met. Merged in PR 43; issue 42 closed with the report linked.
- Shipped as planned except the startup validation hook recorded in the log. No follow-ups.
