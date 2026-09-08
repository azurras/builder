# ActivityPub Production Discovery Activation Test Report

## Document Status

complete

## Story/Issue

[ChristopherBell.dev ActivityPub Production Discovery Activation](../session-memory/2026-07-29-christopherbell-dev.md#source-docs-work-2026-07-29-christopherbell-dev-activitypub-production-discovery-activation-md)

## Branch

- Spoke branch: `codex/activitypub-production-activation`
- Spoke commit: `1244dd31`
- Pull request: [azurras/christopherbell.dev#1318](https://github.com/azurras/christopherbell.dev/pull/1318)
- Merged `origin/main`: `8405cd77d0f1743fe33d70cc80b47e37048090a0`

## App / Environment

- App: `christopherbell.dev`
- Local profiles: `prod,deploy-smoke`
- Local address: `http://127.0.0.1:8091`
- Local database: `christopherbell_federation_activation_20260729`
- Local key path: `A:\Projects\christopherbell.dev-worktrees\activitypub-production-activation\build\federation-activation-runtime\protected-config\federation-key-encryption-secret.bin`
- Shared-folder and music integrations: disabled for the isolated run because the non-elevated test process does not have production access to `A:\Shared-System`
- Production address: `https://www.christopherbell.dev`
- Production listener: port `8080`; process rotated automatically from PID `16956` to PID `39760`

## Local Run Details

The executable Spring Boot jar was started from the isolated worktree with Java, profiles `prod,deploy-smoke`, port `8091`, the isolated MongoDB database, the alternate test-only secret path, and shared-folder/music disabled. The app was restarted once with the same database and secret path to prove reuse. Runtime output is retained under `A:\Projects\christopherbell.dev-worktrees\activitypub-production-activation\build\federation-activation-runtime\stdout-final.log` and `stderr-final.log`. Exact local PIDs `29716`, `41608`, and `46196` were stopped during the successive startup attempts and restart proof; port `8091` was confirmed closed afterward. The isolated MongoDB database was dropped after testing.

The first startup created the key but stopped on the unrelated production shared-folder ACL. The final runs disabled those integrations and exercised the ActivityPub surface successfully. No production ACL was weakened and no production listener was touched by local testing.

## Test Cases

| Case | Result | Reason |
| --- | --- | --- |
| Local root on port 8091 | Pass | Returned HTTP 200. |
| Local `/.well-known/nodeinfo` | Pass | Returned HTTP 200 with the canonical NodeInfo 2.1 link. |
| Local `/nodeinfo/2.1` | Pass | Returned HTTP 200 and advertised ActivityPub. |
| Foreign WebFinger lookup | Pass | Returned HTTP 404; no foreign or unconsented actor was disclosed. |
| Local inbox POST | Pass | Returned HTTP 403; inbound mutation remained disabled. |
| Stable local encryption key | Pass | File length was 32 bytes and its SHA-256 remained unchanged across restart. |
| Local outbound inactivity | Pass | Isolated database had zero jobs, accounts, and posts. |
| Automatic production rollout | Pass | Listener rotated without an interactive prompt; the new process serves the added routes. |
| Public canonical and apex roots | Pass | Both returned HTTP 200; apex redirected to canonical. |
| Public NodeInfo discovery and document | Pass | Canonical and apex discovery returned HTTP 200; canonical NodeInfo 2.1 returned HTTP 200. |
| Production inbound/outbound boundaries | Pass | Foreign WebFinger returned 404, inbox POST returned 403, and production had no jobs, identities, or eligible posts. |
| Production services | Pass | MongoDB, website, media worker, and cloudflared were Running with Automatic startup. |

## Data Sent

- `GET http://127.0.0.1:8091/`
- `GET http://127.0.0.1:8091/.well-known/nodeinfo`
- `GET http://127.0.0.1:8091/nodeinfo/2.1`
- `GET http://127.0.0.1:8091/.well-known/webfinger?resource=acct%3Anobody%40example.com`
- `POST http://127.0.0.1:8091/ap/inbox` with `Content-Type: application/activity+json` and body `{}`
- Equivalent public GET requests against `https://www.christopherbell.dev` and `https://christopherbell.dev`
- `POST https://www.christopherbell.dev/ap/inbox` with `Content-Type: application/activity+json` and body `{}`
- Read-only MongoDB counts for `federation_delivery_jobs`, opted-in accounts, accounts with identities, outbound-eligible posts, and federation scan state

No authentication token, encryption key value, private key, or account data was printed or stored in this report.

## Response Received

- Local root: HTTP 200.
- Local NodeInfo discovery: HTTP 200 with `href` equal to `https://www.christopherbell.dev/nodeinfo/2.1`.
- Public canonical root, discovery, and NodeInfo 2.1: HTTP 200.
- Public apex root: HTTP 200 after redirect to `https://www.christopherbell.dev/`.
- Public apex discovery: HTTP 200 after redirect to the canonical host.
- NodeInfo 2.1 advertised software `christopherbell.dev`, protocol `activitypub`, empty inbound/outbound services, 19 total users, and 1 local post.
- Foreign WebFinger: HTTP 404.
- Inbox POST: HTTP 403.
- Local secret: 32 bytes; stable restart fingerprint `FE9456D6C155AA535A6E1F6ED730DB1A008D103596028FE5312266D234367553`.
- Production MongoDB: 0 delivery jobs, 0 consented accounts, 0 accounts with a federation identity, 0 outbound-eligible posts, and 0 scan-state documents.
- The protected production release and federation-secret paths denied the non-elevated shell, as intended.

## Pass / Fail

Pass. Read-only ActivityPub discovery is live locally and publicly. Inbound and outbound behavior remain inactive. Automatic deployment completed without weakening protected filesystem access.

## Evidence

- Fresh `gradlew.bat :website:check --no-daemon`: `BUILD SUCCESSFUL` in 2m 54s; 1,390 Java tests, 0 failures, 0 errors, 3 skipped; JavaScript test task included.
- Fresh Pester 5.9.0 `Production.Deploy.Tests.ps1`: 37 passed, 0 failed, 0 skipped.
- Pull request #1318 merged at `2026-07-29T12:09:17Z`; Ubuntu, macOS, Windows, dependency review, and all CodeQL checks concluded successfully.
- Production listener changed from PID `16956` to `39760`; local port 8080 root and NodeInfo discovery returned HTTP 200.
- `MongoDB`, `ChristopherBellDev`, `ChristopherBellMediaWorker`, and `cloudflared` reported Running and Automatic.
- Isolated worktree is clean apart from its expected deleted remote tracking branch; Builder was clean before this report.

## Bugs / Follow-ups

- No functional blocker remains for read-only discovery.
- NodeInfo currently reports software version `unknown`; this is cosmetic deployment metadata and does not affect discovery or the security gates.
- Outbound ActivityPub remains intentionally disabled until a real operator-controlled peer inbox is available for the controlled activation test. Inbound remains intentionally disabled.
