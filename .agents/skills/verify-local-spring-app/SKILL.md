---
name: verify-local-spring-app
description: Verify a local Spring Boot application on an isolated non-production port. Use for desktop runtime checks and, when deployment is already authorized, routing the validated candidate through the repository's production deployment mechanism.
---

# Verify Local Spring App

The development host may also serve production. Choose verification-only or verification-plus-deployment from the user's request and existing authorization. Local testing alone does not authorize deployment. Do not request approval again when the session already authorizes the deployment.

## Preflight Before Tests or Startup

1. Read repository `AGENTS.md`, README, and relevant run/deployment instructions. Inspect Git state and preserve unrelated dirty work. Identify the production port, service or process supervisor, and the documented local test profile.
2. Before any database-backed automated test or candidate startup, verify the effective database target from the actual profile, environment overrides, credentials/role, and connection configuration. In Builder-coordinated MongoDB/PostgreSQL work, use database `test` only. PostgreSQL tests use a role isolated from production. Never rely on port isolation to imply data isolation; never use local-development, staging, or production databases for tests.
3. If the effective database target or permissions cannot be verified, stop database-dependent execution and resolve the configuration. A test may be database-free only when inspected configuration/code proves no database connection is used. Record sanitized target evidence without credentials.
4. Check background jobs, external integrations, and storage paths that the test profile enables; isolate effects that could mutate live state. Choose a free alternate port and explicit profile/port settings. Keep production running.

## Verify the Candidate

1. Run focused automated checks and repository-required broader validation with the verified test configuration.
2. Start the candidate on the alternate port with explicit configuration. Keep its process/session handle, command, artifact/commit identity, and log location. Start background helpers hidden on Windows unless the user requested a visible window.
3. Poll with a bounded startup deadline and check the application's expected readiness response. An arbitrary HTTP response, redirect to login, or error page is not proof of health.
4. Exercise changed endpoints/UI flows with representative inputs and relevant regressions. Record URL/port, method or UI action, sanitized input, expected/actual status and output, and pass/fail results.
5. Stop only the candidate process owned by this verification session, including on failure. Save runtime evidence with `record-runtime-verification` when working through Builder.
6. For verification-only scope, finish here. Do not restart production.

## Authorized Deployment

Proceed only when deployment is within the existing request and candidate verification passed.

1. Identify the repository's supported deployment script/pipeline/service manager and its protected operating procedure. Confirm the merged revision/artifact to deploy and required CI gates. Do not substitute an ad hoc `bootRun` or PID kill for a managed service deployment.
2. Before mutation, record the currently deployed artifact/configuration, rollback command or procedure, backup prerequisites for data/schema changes, and bounded success/failure criteria. Keep secrets redacted and preserve protected ACLs. If the deployment mechanism or recovery path is unknown, resolve that prerequisite before proceeding.
3. Use the supported deployment mechanism. Let its service/supervisor own process rotation. For an explicitly documented unmanaged process, follow that repository's exact stop/start/rollback procedure; identifying a port owner alone is insufficient authority or recovery planning.
4. Verify service state, expected listener, application readiness, deployed revision when exposed, and the changed production behavior through authorized non-destructive checks. Confirm required dependencies without writing test fixtures into production.
5. If deployment fails, follow the pre-established rollback procedure and verify the restored service. Stop repeated restart attempts; report failure evidence and whether recovery succeeded. If rollback fails, leave the service state explicit and request only the missing decision or access.

## Read-Only Windows Inspection

```powershell
Get-NetTCPConnection -LocalPort 8080 -State Listen | Select-Object LocalAddress,LocalPort,OwningProcess
```

Replace 8080 with the verified production port. Match the owner to the documented Windows service/supervisor; this command does not authorize stopping it.

## Completion Evidence

Record automated results, sanitized database isolation, candidate commit/artifact, exact runtime inputs and outputs, and candidate cleanup. For deployment scope also record the deployment mechanism/result, service and application health, deployed identity, and rollback outcome if used. A verification-only result should state that production deployment was outside that request.
