# christopherbell.dev PostgreSQL Shadow Rehearsal Test Report

## Document Status

complete

## Story/Issue

[christopherbell.dev PostgreSQL Migration](../session-memory/christopherbell-dev.md#source-docs-work-2026-08-13-christopherbell-dev-postgresql-migration-md), Task 8 shadow rehearsal and PostgreSQL-only candidate acceptance.

## Branch

- Spoke branch: `codex/postgresql-migration`
- Reviewed commit: `09cd454b1d84c6e83a36514a004c94a326e5f9de`
- Task 8 range: `9c48adfa..09cd454b`

## App / Environment

- Application: `christopherbell.dev` website candidate
- Candidate URL: `http://127.0.0.1:18087`
- Database: isolated PostgreSQL 18.4 at `127.0.0.1:55434/christopherbell`
- Runtime database role: `christopherbell_app`; bridge credentials were not used by the application
- Schema: forward migrations V1 through V27
- Source rehearsals: read-only live Mongo source and a production archive restored only into disposable Mongo database `test`
- Production listeners remained unchanged at ports 8080, 5432, and 27017

## Local Run Details

The reviewed boot JAR, SHA-256 `4E92E5EB878510BFB261F77DA9883C09DE78BEA65D48D295180974C9FB7138B1`, was started with the sanitized command `pwsh -NoProfile -File .superpowers/sdd/2026-08-13-christopherbell-dev-postgresql-migration/round-3-evidence/start-candidate.ps1`. Candidate PID 43612 started at 2026-08-21T14:43:16Z, became ready at 14:43:23Z, and listened only on `127.0.0.1:18087`.

The matrix ran with `pwsh -NoProfile -File .superpowers/sdd/2026-08-13-christopherbell-dev-postgresql-migration/round-3-evidence/candidate-matrix.ps1` from 14:46:29Z through 14:46:30Z. Cleanup stopped the exact candidate and PostgreSQL processes, removed the isolated database and roles, deleted the protected disposable secret, and verified ports 18087 and 55434 were closed. The app was not left running.

## Test Cases

1. Repeated all-52-kind SHADOW and RECONCILE runs against the read-only live Mongo source.
2. Repeated migration of a restored production archive containing 63,230 documents into isolated PostgreSQL schemas.
3. PostgreSQL-only candidate authentication and account creation for admin and non-admin users.
4. Account, posts, messages, notifications, music, shared-folder, vehicle, lunch, administration, location, and Canes API requests.
5. Public, non-admin, and admin health visibility and PostgreSQL identity reporting.
6. Home, login, blog, messages, notifications, music, shared-folder, VIN decoder, lunch, back-office, and command-center UI responses.
7. Scheduler activity with the Canes effect disabled, datasource-role separation, connection capacity, and eleven representative query plans.
8. Full repository verification and exact cleanup/secret scans.

## Data Sent

- Cookie-bound CSRF flows followed by `POST /api/accounts/2024-12-15/create` and `POST /api/accounts/2024-12-15/login` for disposable admin and user accounts; passwords and cookies were redacted.
- Authenticated `GET` requests covered account self/admin lists, post feed, conversations, notifications, music access/catalog, shared-folder entries, vehicles, lunch selections/sessions, admin activity, command-center snapshot, ZIP lookup, and Canes history.
- Public and authenticated `GET` requests covered liveness, readiness, aggregate health, and eleven HTML routes.
- Every matrix row retained the method, URL, sanitized input, UTC timestamps, expected status, complete response SHA-256, safe structural summary, latency, and a 2,000 ms budget.

## Response Received

- Candidate matrix: 39 of 39 exact expected HTTP statuses; 39 of 39 requests below 2,000 ms; maximum latency 75.298 ms.
- Representative HTTP response bodies: account creation returned status code 201 and login returned status code 200 with JSON keys `messages,payload,requestId,success`. Public liveness/readiness returned status code 200 with body `{"status":"UP"}`. Unauthenticated aggregate health returned status code 403; non-admin and admin health returned status code 200 with the intended disclosure levels.
- Admin health reported backend `postgresql`, database `christopherbell`, and schema version 27.
- UI responses returned HTTP 200 with the expected titles. Deliberately disabled or empty features returned their contract statuses, including music catalog 503, shared-folder entries 404, ZIP lookup 404, and empty Canes history 200.
- PostgreSQL activity showed 10 app-role sessions, zero bridge-role sessions, and zero sessions idle in transaction.
- Four scheduler threads were live; two independent readbacks found zero Canes leases and zero collector runs while the feature was disabled.
- Eleven representative plans passed; the slowest measured execution was 0.077 ms.
- The live source produced identical SHADOW replay and two identical RECONCILE digests. The restored archive completed all 52 kinds and 63,230 documents repeatedly.

## Pass / Fail

All Task 8 candidate, rehearsal, database-role, scheduler, plan, latency, capacity, and cleanup cases passed. Independent review found no remaining Critical, Important, Blocker, or Warning finding in the scoped Task 8 result.

## Evidence

- Definitive source gate: `:website:jooqCodegen :cbell-lib:check :website:check --no-daemon --max-workers=2`, BUILD SUCCESSFUL in 354.419 seconds; 2,386 combined Java tests, 2,311 passed, 75 expected skips, zero failures/errors.
- Operations verification: PowerShell/Pester variants passed 182/1 expected skip, 182/1 expected skip, and 75/0; JavaScript and deployment verifiers passed.
- Candidate HTTP evidence: 39 complete uppercase 64-hex response SHA-256 values with safe structural summaries.
- Credential scan: 20 evidence targets checked against 10 disposable secrets and credential/token patterns; zero literal or pattern findings.
- Cleanup readback: candidate/database/roles/owned PostgreSQL PID/listeners absent; protected secret absent; production PIDs unchanged at 8080/19812, 5432/7808, and 27017/5712.
- V1 through V14 remained byte-identical; no FINALIZE, cutover, production database, service, or configuration action occurred.

## Bugs / Follow-ups

No Task 8 blocker remains. Task 9 is intentionally not authorized by this report: production authority transfer still requires the separately approved maintenance window and its own final backup, frozen-source, and rollback-readiness gates.
