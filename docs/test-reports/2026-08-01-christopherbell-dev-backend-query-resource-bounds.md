# christopherbell.dev Backend Query and Resource Bounds Test Report

## Document Status

complete

## Story/Issue

[christopherbell.dev Performance, Scalability, and Library Optimization](../session-memory/christopherbell-dev.md#source-docs-work-2026-07-29-christopherbell-dev-performance-scalability-library-optimization-md),
backend query and resource-bounds plan.

## Branch

- Candidate branch: `codex/backend-query-resource-bounds`.
- Runtime-tested commit: `2bb1844fce68db913094b1abb9e4628a8726d502`.
- Final rebased and automated-tested commit:
  `52f3a61b9210599e9d76c51193b58ef4be07c51c`.
- Final base commit: `27bcaaf8e100278173acedd3fad178c3ec8da647`.
- The post-runtime rebase added only mainline build-identity configuration and its
  test. It did not change candidate application behavior. Fresh full automated
  verification passed after that rebase.

## App / Environment

- App: `christopherbell.dev` Spring Boot website.
- Candidate URL: `http://127.0.0.1:8092`.
- Profiles: `local,deploy-smoke`.
- Disposable Mongo database:
  `christopherbell_backend_verify_20260801_2bb1844f`.
- Scheduling: `APP_SCHEDULING_ENABLED=false`.
- Mail: `APP_MAIL_ENABLED=false`.
- JWT secret: temporary verification-only value, not retained.
- Production URL/listener: port 8080, PID `13080`; never targeted or changed.

## Local Run Details

The candidate JAR ran as PID `37728` from
`A:\Projects\christopherbell.dev-worktrees\performance-backend-20260729`.
The sanitized start form was:

```powershell
$env:SPRING_PROFILES_ACTIVE = 'local,deploy-smoke'
$env:SERVER_PORT = '8092'
$env:SPRING_MONGODB_URI = 'mongodb://127.0.0.1:27017'
$env:SPRING_MONGODB_DATABASE = 'christopherbell_backend_verify_20260801_2bb1844f'
$env:APP_SCHEDULING_ENABLED = 'false'
$env:APP_MAIL_ENABLED = 'false'
$env:APP_JWT_SECRET = '<redacted-verification-only-secret>'

Start-Process -WindowStyle Hidden `
  -FilePath 'java.exe' `
  -ArgumentList @('-jar', 'website\build\libs\website.jar') `
  -RedirectStandardOutput '<temporary-stdout-log>' `
  -RedirectStandardError '<temporary-stderr-log>' `
  -PassThru
```

The candidate returned HTTP 200 from `/`, liveness, and readiness; both health
groups reported `UP`. PID 37728 was stopped after verification, port 8092 was
confirmed free, the exact disposable database was dropped and verified absent,
and temporary runtime logs were removed. Production port 8080 remained PID 13080
throughout. MongoDB, ChristopherBellDev, and cloudflared remained
Running/Automatic.

## Test Cases

| Case | Expected | Result |
| --- | --- | --- |
| One versus fifty conversations | Same Mongo query-group count | Pass: five total groups for each request |
| Conversation peer hydration | One batch lookup, not one query per peer | Pass: one lookup returned 1 versus 50 rows |
| Invalid VIN | Safe client error without upstream call | Pass: HTTP 400 `REQUEST_ERROR` |
| Cached valid VIN | Successful decode without upstream call | Pass: HTTP 200 |
| VIN rate capacity | Twenty allowed requests, next request rejected | Pass: next request HTTP 429 `VIN_DECODE_RATE_LIMITED` |
| Oversized VIN batch | More than 20 entries rejected | Pass: HTTP 400 `INVALID_REQUEST` |
| Scheduled work in smoke profile | No scheduled feature writes | Pass: zero collector runs, WFL picks, and music writes |
| Full candidate gate | Java, browser, package, sensor, and deployment-context checks pass | Pass at final rebased commit |
| Cleanup and production isolation | Candidate stopped, disposable data removed, 8080 unchanged | Pass |

## Data Sent

Message fixtures used bearer authentication and the browser CSRF cookie/header
flow.

- `POST /api/messages/2025-09-14`
- One-conversation payload shape:

```json
{
  "recipientUsername": "verify_peer01",
  "text": "one conversation verification"
}
```

- Fifty-conversation fixtures used `verify_peer01` through `verify_peer50` with
  text shaped as `fifty conversation verification NN`.
- `GET /api/messages/2025-09-14/conversations?limit=1`.
- `GET /api/messages/2025-09-14/conversations?limit=50`.

VIN requests used the browser CSRF cookie and `X-XSRF-TOKEN` header.

- `POST /api/vehicles/2026-05-09/vin/decode` with invalid payload
  `{"vin":"INVALID"}`.
- The same endpoint with cached valid payload
  `{"vin":"1HGCM82633A004352"}`.
- `POST /api/vehicles/2026-07-26/vin/decode/batch` with 21 entries, exceeding
  the maximum batch size of 20.

No credentials, bearer token, CSRF value, password, JWT secret, or raw response
body from an upstream service is retained in this report.

## Response Received

- The running app returned `status code: 200` for the conversation GET requests;
  the remaining HTTP response status codes and sanitized bodies are described
  below.
- All 51 message fixture writes returned HTTP 201.
- The one-conversation request returned HTTP 200 with one summary.
- The fifty-conversation request returned HTTP 200 with fifty summaries.
- Both conversation requests used the same five Mongo query groups:
  1. bearer-authentication account lookup;
  2. conversation-owner account lookup;
  3. conversation-summary aggregation;
  4. one batched peer-account lookup; and
  5. one unread-count aggregation.
- The peer-account query returned one row for the first request and fifty rows
  for the second. Query count did not grow with cardinality.
- Invalid VIN returned HTTP 400, code `REQUEST_ERROR`, description
  `The request is invalid.`
- Cached VIN returned HTTP 200 with VIN `1HGCM82633A004352`, make `HONDA`, model
  `ACCORD`, and year `2003`.
- The initial cached request plus 19 further cached requests returned HTTP 200.
  The next request returned HTTP 429, code `VIN_DECODE_RATE_LIMITED`, description
  `Too many VIN decode requests. Please try again later.`
- The 21-entry batch returned HTTP 400, code `INVALID_REQUEST`, description
  `The request is invalid.`

All successful VIN requests were served from the disposable Mongo cache. No
external NHTSA request was made.

## Pass / Fail

All runtime and automated acceptance cases passed. Conversation query groups are
constant from one through fifty summaries. VIN request state is bounded and the
documented validation/rate-limit envelopes are preserved. Scheduled feature work
remained disabled in the smoke profile. The candidate was fully removed after
testing. Pull request 1336 was merged after every required check passed, and the
automatic production rollout was verified successfully.

## Publication and Production Verification

- Pull request: `https://github.com/azurras/christopherbell.dev/pull/1336`.
- Merged commit: `c4d60ce0c92281c201d063cfd6a07563f4a7b230`.
- Pull-request gates: dependency review, CodeQL for Actions, Java/Kotlin, and
  JavaScript/TypeScript, and the Windows, Linux, and macOS build matrix all
  passed.
- Post-merge gates: CI Build and CodeQL both completed successfully for the
  exact merged commit.
- The production listener rotated automatically from PID `13080` to PID
  `31728`; no manual production restart was performed.
- Local production root, liveness, readiness, `robots.txt`, and `sitemap.xml`
  returned HTTP 200; both health groups reported `UP`.
- Public root, `robots.txt`, and `sitemap.xml` returned HTTP 200.
- The production HTML referenced asset namespace
  `/c4d60ce0c92281c201d063cfd6a07563f4a7b230/`, exactly matching the merged
  commit.
- MongoDB, ChristopherBellDev, and cloudflared remained Running/Automatic.

## Evidence

### Final post-rebase automated gate

```text
Exact HEAD: 52f3a61b9210599e9d76c51193b58ef4be07c51c
Base:       27bcaaf8e100278173acedd3fad178c3ec8da647

:cbell-lib:test --rerun-tasks
BUILD SUCCESSFUL in 21s
113 tests, 0 failures, 0 errors, 0 skipped

:website:check --rerun-tasks
BUILD SUCCESSFUL in 4m06s; all 18 actions executed
1,617 Java tests, 0 failures, 0 errors, 3 skipped
289 browser tests, 0 failures, 0 errors, 0 skipped
Deployment-context, sensor archive, and sensor runtime checks passed
```

### Pre-rebase focused and runtime gate

```text
Exact runtime HEAD: 2bb1844fce68db913094b1abb9e4628a8726d502
Focused backend suite: 389 tests, 0 failures/errors/skips
cbell-lib: 113 tests, 0 failures/errors/skips
website check: 1,617 Java tests and 289 browser tests, all passing
```

Controlled tests additionally proved:

- limiter cardinality, expiry, atomic same-key consumption, and token charging;
- exact-limit and limit-plus-one response handling, total response deadlines,
  interruption, cancellation, and stream closure;
- eight VIN permits, ninth-call rejection, and permit recovery;
- safe status/malformed/oversized behavior for NHTSA, RandomVIN, robots,
  OpenStreetMap, and Canes clients;
- lease contention, equality-boundary takeover, renewal, stale-owner failure,
  and ownership checks before shared mutations.

Machine-readable test results remain under:

- `A:\Projects\christopherbell.dev-worktrees\performance-backend-20260729\website\build\test-results\test`
- `A:\Projects\christopherbell.dev-worktrees\performance-backend-20260729\cbell-lib\build\test-results\test`
- `A:\Projects\christopherbell.dev-worktrees\performance-backend-20260729\website\build\test-results\jsTest\results.xml`

## Bugs / Follow-ups

No backend optimization defect remains open from this verification. Live
ninth-concurrent-call and upstream exact-body-boundary tests were intentionally
not sent to public services. Those cases are covered by deterministic local tests;
runtime used cached VIN success, invalid input, rate saturation, and oversized
batch flows without uncontrolled upstream traffic.

The Mongo lease arbitration test uses a deterministic stateful Mongo query/update
boundary rather than a live second Mongo process. Alternate-port runtime confirmed
the app's disposable Mongo integration, and the test directly evaluates the
production `MongoLeaseService` query and update documents.
