# ChristopherBell.dev ActivityPub Discovery Foundation Test Report

## Document Status

complete

## Story/Issue

Release 3 gate 1 from [Void Public Growth Program](../session-memory/christopherbell-dev.md#source-docs-specs-2026-07-28-void-public-growth-program-md), implemented by [the approved plan](../implementation-plans/2026-07-28-christopherbell-dev-activitypub-discovery-foundation.md) and shipped in [PR #1316](https://github.com/azurras/christopherbell.dev/pull/1316).

## Branch

- Spoke branch: `codex/activitypub-federation`
- Tested head: `45b3618bdd185d3b994096b58bc25df48174830f`
- Merged main SHA: `6cd9e397e4ec2c3175ae5c31a95f633b7a7c7c95`
- Commits: `d7c11fa3`, `50cf469a`, `45b3618b`

## App / Environment

- Spring Boot website from `A:\Projects\christopherbell.dev-worktrees\activitypub-federation`
- Local profile, port 8081, base URL `http://localhost:8081`
- Isolated database `christopherbell_activitypub_discovery_test`
- Enabled pass: discovery true; inbound/outbound false; test-only 32-byte key; local public origin
- Disabled pass: all federation flags false and no encryption key
- Production: Windows service on `127.0.0.1:8080`, public URL `https://christopherbell.dev`, federation disabled

## Local Run Details

- Built with `gradlew.bat :website:bootJar --no-daemon` and isolated `GRADLE_USER_HOME=A:\Temp\gradle-activitypub`.
- Started `website\build\libs\website.jar` hidden on port 8081 with logs under `A:\Temp\activitypub-acceptance`.
- Enabled process PID 44916 was restarted as PID 46752. Disabled-default process used PID 39624.
- Stopped only the validated port-8081 processes, dropped only the isolated database, and removed the temporary scripts/logs. Port 8081 ended with zero listeners.
- The production port-8080 process was not stopped during local acceptance.

## Test Cases

1. Create an opted-in account through the real CSRF-protected signup API.
2. Resolve WebFinger, NodeInfo 2.1, actor, outbox/page, followers, and following.
3. Confirm no encrypted/private key fields appear publicly.
4. Reject foreign/malformed WebFinger and block inbox POST.
5. Restart and confirm stable actor, key, and WebFinger identity.
6. Authenticate, disable consent, confirm actor 404, re-enable, and confirm the same public key.
7. Start with discovery disabled and no key; confirm site 200, disabled signup choice, and discovery 404.
8. Verify post-merge automatic production deployment, services, disabled federation, and Mongo index/data state.

## Data Sent

- `GET http://localhost:8081/signup` to obtain `XSRF-TOKEN`.
- `POST /api/accounts/2024-12-15/create` with JSON fields `firstName=Federation`, `lastName=Acceptance`, `email=federation-acceptance@example.test`, `username=fedacceptance`, a test-only password, and `federatePublicVoidPosts=true`; sent the matching `X-XSRF-TOKEN`.
- `GET /.well-known/webfinger?resource=acct%3Afedacceptance%40localhost%3A8081`, `GET /.well-known/nodeinfo`, and `GET /nodeinfo/2.1`.
- Anonymous GETs to `/ap/users/fedacceptance`, `/outbox`, `/outbox?page=true&size=20`, `/followers`, and `/following`.
- Negative requests used foreign `acct:fedacceptance@example.test`, malformed `not-an-acct`, and `POST /ap/users/fedacceptance/inbox` with `Content-Type: application/activity+json` and body `{"type":"Follow"}`.
- Browser-cookie login used `X-CBELL-Browser-Session: cookie`; consent requests used authenticated GET and CSRF-protected PATCH bodies `{"enabled":false}` and `{"enabled":true}`.
- Production probes sent local/public GETs to `/`, `/signup`, `/.well-known/nodeinfo`, and `/ap/users/nonexistent`.

## Response Received

- Running app account-create response status code: 200. Response body identified `fedacceptance` with `federationEnabled=true`; isolated Mongo showed ACTIVE state, canonical actor/key IDs, public key, and encrypted ciphertext.
- WebFinger response status code: 200, `Content-Type: application/jrd+json`, subject `acct:fedacceptance@localhost:8081`, and canonical actor self link.
- NodeInfo response status code: 200 with the 2.1 profile media type, protocol `activitypub`, one local user, and zero posts.
- Actor response status code: 200, `Content-Type: application/activity+json`, type `Person`, public key present, and no encrypted/private key field text.
- Empty outbox/page/followers/following response status code: 200 with correct ordered-collection types and zero items.
- Federation headers were `Cache-Control: no-store`, `Access-Control-Allow-Origin: *`, and `X-Content-Type-Options: nosniff`.
- Foreign WebFinger status code: 404; malformed WebFinger status code: 400; inbox POST status code: 403 with no mutation.
- After restart, actor ID, key ID, public key, WebFinger subject, and self link were unchanged.
- Consent GET response body was `{enabled:true,enrollmentAvailable:true}`. Disable status code: 200, then actor status code: 404. Re-enable status code: 200, then actor status code: 200 with an exact public-key match.
- Disabled startup root status code: 200; NodeInfo/actor status code: 404; signup UI state showed the choice present and disabled without a key.
- Automatic production deployment rotated port 8080 from PID 34768 to PID 33352. Local/public home and signup status code: 200; new signup markup was present and disabled; public NodeInfo/actor status code: 404.
- MongoDB, ChristopherBellDev, and cloudflared UI/service state was Running and Automatic. Production retained 20 accounts, zero enabled federation accounts, zero federation identities, and gained `federation_actor_lookup` on status/federationEnabled/username.

## Pass / Fail

- PASS - all eight runtime cases produced the intended behavior.
- PASS - `:website:check` ran 1,353 Java tests with zero failures/errors and three skips; complete JavaScript and packaged/runtime checks passed.
- PASS - PR CI passed on Ubuntu, macOS, and Windows; CodeQL and dependency review passed.
- PASS - temporary acceptance data was removed and production account data remained unchanged.

## Evidence

- PR: https://github.com/azurras/christopherbell.dev/pull/1316
- Merge SHA: `6cd9e397e4ec2c3175ae5c31a95f633b7a7c7c95`
- Local full check: `BUILD SUCCESSFUL`; 1,353 tests; zero failures/errors.
- Exact runtime methods, URLs, request bodies, response status codes, headers, stable IDs, service state, and Mongo state are recorded above.

## Bugs / Follow-ups

- No defect remains in this gate.
- Production federation is intentionally unavailable until a separate protected secret is installed and discovery is explicitly enabled.
- Inbound/outbound federation remain intentionally unimplemented. The next controlled-peer delivery gate requires SSRF, redirects, replay, retry, payload bounds, kill switches, and moderation evidence before enablement.
