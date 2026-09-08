# christopherbell.dev Authentication Request Efficiency Test Report

## Document Status

complete

The corrected isolated candidate passed every functional, query-count, and cleanup
criterion. The one known disposable identity created by an earlier misconfigured run
was removed under explicit authority, with exact zero-match verification afterward.

## Story/Issue

[christopherbell.dev Performance, Scalability, and Library Optimization](../session-memory/2026-07-29-christopherbell-dev.md#source-docs-work-2026-07-29-christopherbell-dev-performance-scalability-library-optimization-md),
authentication request-efficiency plan.

## Branch

- Candidate branch: `codex/performance-authentication-efficiency`
- Final candidate commit tested at runtime: `df3b23e1`.
- Merged production commit: `3a8e249a45e50e53f1ddc6fa1c520dcc82adee03`
  through PR #1329.
- Final full-gate commit: `df3b23e1`; `:website:check` passed after live account
  validation was folded into one bounded Mongo aggregation.
- Baseline commit: `e3afbf3c9eeb65525f573f299f82287ef8665554`

## App / Environment

- App: `christopherbell.dev` Spring Boot website.
- Profile: `local` with mail disabled and a throwaway JWT secret.
- Baseline URL: `http://127.0.0.1:8091`.
- Candidate URL: `http://127.0.0.1:8092`.
- Corrected baseline database:
  `christopherbell_perf_auth_before_safe_20260729`.
- Corrected candidate database:
  `christopherbell_perf_auth_after_safe_20260729`.
- Final joined-lookup database:
  `christopherbell_perf_auth_join_20260729`.
- Both the Mongo URI and the higher-precedence `spring.mongodb.database`
  property named the exact disposable database.
- Port 8080 was never targeted by a test command. Its externally managed listener
  rotated from PID `60136` to PID `48420` while testing was underway.

## Local Run Details

The baseline JAR ran as PID `48412` on 8091 and the candidate JAR ran as PID
`50412` on 8092. Startup logs showed Tomcat initialized and started on the assigned
alternate port; candidate PID 50412 reported `Started Application` after 5.729
seconds. Each exact disposable database was verified empty before signup and
populated only by its matching run. Both PIDs were stopped explicitly, both ports
were confirmed free, and only the two exact corrected disposable databases were
dropped and verified empty.

After whole-branch security review restored live account validation, final candidate
`f90e6d7b` was remeasured as PID `44836` on 8092 against exact disposable database
`christopherbell_perf_auth_final_safe_20260729`. The database was proven empty before
mutation, PID 44836 was stopped, port 8092 was confirmed free, and the exact database
was dropped and verified empty. This final measurement supersedes the earlier
candidate query and latency values below wherever they differ.

The final joined-lookup candidate `df3b23e1` was measured as PID `62140` on
8092 against exact disposable database `christopherbell_perf_auth_join_20260729`.
It preserved live account validation while resolving the session and minimal current
account security state in one `browser_sessions` aggregation. PID 62140 was stopped,
port 8092 was confirmed free, and the exact database was dropped and verified empty.
Production 8080 stayed on PID 49588 throughout this candidate run.

The same temporary, property-gated Mongo command listener and request-correlation
filter was applied to both worktrees. It recorded request ID, path, collection, and
command only. Secret scans found no password, JWT secret, bearer value, or browser
authentication-cookie value. The diagnostic source was removed with `apply_patch`
and never committed.

## Test Cases

| Case | Expected | Result |
| --- | --- | --- |
| Full candidate gate | Java, JavaScript, packaging, sensor runtime, and policy pass on final rebased commit | Pass: `BUILD SUCCESSFUL in 1m 58s` |
| Static assets with credentials | Real unversioned and SHA-versioned assets return 200 with zero auth Mongo commands | Pass |
| Normal cookie authentication | One bounded `browser_sessions` aggregate, zero separate account reads, and live account validation | Pass |
| Activity coalescing | Five requests inside five minutes perform no session write | Pass |
| Baseline comparison | Baseline and candidate both validate the account; candidate removes a network round trip and repeated full session updates | Pass |
| Login/logout | Browser cookies set at login and zero-aged at logout | Pass |
| Revoked cookie | Old cookie fails closed after logout | Pass: 401 and authentication cookies cleared |
| Descriptive latency | Same endpoint, headers, host, and 30-request method on both builds | Pass; no statistical claim made |
| Corrected data cleanup | Stop exact PIDs and drop only the two exact safe databases | Pass |
| Discarded initial run cleanup | Remove only the exact production-named test identity and sessions | Pass: 1 account and 2 sessions deleted; zero remain |

## Data Sent

- `GET /login` to obtain the CSRF cookie.
- `POST /api/accounts/2024-12-15/create` with a fresh disposable USER account.
- Browser-cookie login at `POST /api/accounts/2024-12-15/login`.
- `GET /js/app.js` and the real build-versioned
  `GET /<commit-sha>/js/app.js` with a stale cookie and bearer header.
- Cookie-authenticated `GET /api/accounts/2024-12-15`. A USER is correctly denied
  by the ADMIN-only endpoint after authentication, isolating authentication reads
  from controller-level account reads.
- Five repeated copies of that protected request within five minutes.
- Thirty sequential copies of the protected request for descriptive latency.
- `POST /api/accounts/2024-12-15/logout`, then the protected request with the old
  revoked cookie.

Credentials, cookie values, bearer values, password text, and the JWT secret were
not retained in this report.

## Response Received

The running baseline and candidate each returned status code: 200 for `/login`,
browser login, both real static assets, and logout. The authenticated USER request
to the ADMIN-only account endpoint returned status code: 403 after successful
authentication. Reusing the revoked cookie after logout returned status code: 401
and cleared the authentication cookies.

| Flow | Baseline | Candidate |
| --- | --- | --- |
| Anonymous login page | 200 | 200 |
| Browser login | 200; HttpOnly auth cookie and UI-state cookie set | 200; same transition |
| Unversioned static asset | 200; auth commands 0 | 200; auth commands 0 |
| Real SHA-versioned static asset | 200; auth commands 0 | 200; auth commands 0 |
| Protected account authorization | 403; session find 1, account find 1 | 403; one `browser_sessions` aggregate, account find 0, session writes 0 |
| Five interactive requests | each 403; session find 1, account find 1, session update 1 | each 403; one aggregate, account find 0, session writes 0 |
| Logout | 200; auth cookies zero-aged | 200; auth cookies zero-aged |
| Old cookie after logout | 401; auth cookies cleared | 401; auth cookies cleared |

The actual asset paths were
`/e3afbf3c9eeb65525f573f299f82287ef8665554/js/app.js` and
`/df3b23e1/js/app.js` for the authoritative final joined-lookup rerun.

## Pass / Fail

All corrected isolated functional and performance cases passed. Security review
showed that separate account mutation and session deletion cannot guarantee durable
revocation if deletion fails. The final candidate therefore retains live account
validation but performs it inside the same bounded Mongo aggregation that loads the
session. Ordinary cookie authentication now has one database round trip, zero
separate account reads, and no activity write inside the five-minute coalescing
window. Recognized static assets perform zero authentication work. Final latency
values are descriptive local samples only.

Overall report status is complete. The discarded URI-only baseline run created one
known test account in the production-named database; explicit authority was obtained,
the exact identity was verified, and only that account and its browser sessions were
deleted.

## Evidence

### Automated verification

```text
GRADLE_USER_HOME=...performance-authentication-20260729-task5
./gradlew.bat :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest --tests dev.christopherbell.configuration.security.browser.* --tests dev.christopherbell.account.* --tests dev.christopherbell.report.moderation.*
PASS in 26.6 s

./gradlew.bat :website:check --no-daemon
PASS in 1m 58s on final rebased commit df3b23e1
1,551 Java tests, 0 failures, 0 errors, 3 skipped
289 JavaScript tests passed; packaging and sensor-runtime verification passed
```

An earlier final-gate attempt paired `--offline` with a new empty Gradle cache and
failed before compilation because the Spring Boot plugin was unavailable locally.
The warmed isolated cache rerun above is the valid result.

### Sanitized startup excerpt

```text
PID 50412: Tomcat initialized with port 8092
PID 50412: Tomcat started on port 8092 with context path '/'
PID 50412: Started Application in 5.729 seconds
```

### Sanitized correlated command excerpts

```text
baseline-safe-protected  /api/accounts/2024-12-15  browser_sessions find
baseline-safe-protected  /api/accounts/2024-12-15  accounts         find

candidate-safe-protected /api/accounts/2024-12-15  browser_sessions find
candidate-join-protected /api/accounts/2024-12-15 browser_sessions aggregate
```

For baseline interactive requests 1 through 5, each correlation contained exactly:

```text
browser_sessions find
accounts         find
browser_sessions update
```

For final `df3b23e1` interactive requests 1 through 5, each correlation contained
exactly one bounded `browser_sessions aggregate`, zero separate `accounts find`
commands, and no session write. Final candidate logout returned 200; the revoked
cookie produced one aggregate, returned 401, and cleared cookies.

No Mongo event exists for either candidate static-asset correlation. The retained
HTTP summary recorded status 200 for both actual paths. Raw HTTP headers and
individual latency samples were not written to disk; their sanitized status/cookie
transitions and aggregate values are preserved here and must not be represented as
raw captures.

### Descriptive latency

| Build | n | p50 ms | p95 ms | min ms | max ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | 30 | 4.914 | 8.735 | 3.325 | 19.313 |
| Pre-review candidate `ed87db40` (superseded) | 30 | 4.927 | 5.606 | 3.846 | 14.832 |
| Final candidate `f90e6d7b` | 30 | 6.531 | 8.391 | 5.571 | 20.436 |
| Joined-lookup candidate `df3b23e1` | 30 | 6.365 | 8.488 | 5.010 | 16.735 |

Against baseline, the joined-lookup observed p50 was 1.451 ms higher and p95 was
0.247 ms lower. The sample is descriptive; the proven scalability improvement is
the reduction from two database commands to one while retaining live validation.

### Cleanup evidence

`mongosh` verified and dropped only:

```text
christopherbell_perf_auth_before_safe_20260729  ok: 1
christopherbell_perf_auth_after_safe_20260729   ok: 1
```

Reconnects to both exact names returned zero collections. Candidate and baseline
tracked worktrees were clean after diagnostic removal; 8091 and 8092 had no listener.

The final remeasurement similarly dropped only
`christopherbell_perf_auth_final_safe_20260729` (`ok: 1`); reconnecting returned zero
collections, accounts, and sessions. PID 44836 was stopped, diagnostics were removed,
and the candidate worktree was clean.

The joined-lookup measurement dropped only
`christopherbell_perf_auth_join_20260729` (`ok: 1`); reconnecting returned zero
collections, accounts, and sessions. PID 62140 was stopped, 8092 was free,
diagnostics were removed, and the candidate worktree was clean.

Under explicit production-cleanup authority, a read-only exact match first confirmed:

```text
database: christopherbell
account id: 87bb9e7d-ed0b-4d97-acbb-8cc15ab7e77b
email: perf-auth-20260729@example.test
username: perfauthbaseline20260729
browser sessions: 2
```

The cleanup deleted the two sessions before deleting the single fully matched account.
Immediate exact verification returned:

```text
deletedBrowserSessions: 2
deletedAccounts: 1
remainingAccount: 0
remainingBrowserSessions: 0
```

No other production collection or identity was inspected or changed. These direct
deletions are recoverable only through the existing production backup process.

## Bugs / Follow-ups

1. Candidate startup initially exposed a real Spring proxy defect: a final
   `MongoBrowserSessionActivityStore` could not be subclassed for repository
   exception translation. The branch made only that adapter proxyable and added a
   real Spring class-proxy context regression.
2. The first baseline/candidate attempts supplied only the database component of
   the Mongo URI. `application-local.yml` supplied a higher-precedence explicit
   database, so those runs were invalid and discarded. Corrected runs supplied both
   properties and proved isolation before mutation.
3. Explicit authority was obtained to remove the known initial test identity:
   - account ID: `87bb9e7d-ed0b-4d97-acbb-8cc15ab7e77b`
   - email: `perf-auth-20260729@example.test`
   - username: `perfauthbaseline20260729`
   - created: `2026-07-29T17:21:02.421Z`
   - creation endpoint: `POST /api/accounts/2024-12-15/create`
   - a later candidate attempt with the same email returned `RESOURCE_EXISTS` and
     did not create a second account.
   Exact pre-delete matching found that one account and two browser sessions. The
   sessions and account were deleted in that order, and exact follow-up counts were
   zero. No further cleanup remains.
4. Whole-branch review proved that save-then-revoke cannot safely support snapshot-only
   authentication when session deletion fails. Final code validates ACTIVE account
   state and fingerprint through one bounded `$lookup` aggregation, retains explicit
   revocation as defense in depth, and adds failed-revocation/no-op-retry coverage.
5. Concurrent rotation review added a CAS-loss reload that accepts only the winner's
   strictly live previous-overlap credential and emits no losing cookie mutation.
   Revoke, expiry, invalid-token, current-token-only, account-fingerprint, and Mongo
   failure paths remain fail closed. The final exact-head gate passed 1,551 Java tests
   with zero failures/errors and 3 skips, plus JavaScript, boot JAR, and sensor runtime.
6. PR #1329 passed Windows, Linux, macOS, dependency review, and CodeQL before merge.
   Post-merge CI and CodeQL passed at `3a8e249a`. Automatic deployment rotated the
   production listener from PID 49588 to PID 61024; local and public liveness/readiness
   returned `UP`, the apex and `www` roots returned 200, and rendered asset URLs carried
   the exact merged SHA.
