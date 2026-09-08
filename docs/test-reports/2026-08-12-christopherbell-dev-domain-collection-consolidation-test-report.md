# christopherbell.dev Domain Collection Consolidation Test Report

## Document Status

complete

## Story/Issue

[Domain Collection Consolidation](../session-memory/2026-08-10-christopherbell-dev.md#source-docs-work-2026-08-10-christopherbell-dev-domain-collection-consolidation-md)

## Branch

- Production application release: `62e1c7193414ecab266a217d221141120c8ecaef`
- Final read-only inventory tooling fix: PR [#1369](https://github.com/azurras/christopherbell.dev/pull/1369), merged as `e073823d14ffed0b4c113707d16c0ad0cfe1b7fa`; it may deploy through the next ordinary release and was not required for application or schema health.

## App / Environment

- Application: `christopherbell.dev`
- Profile: protected native-Windows production
- Local URL: `http://127.0.0.1:8080`
- Public URLs: `https://www.christopherbell.dev/` and `https://christopherbell.dev/`
- Database: production `christopherbell` MongoDB on the native Windows service
- Migration contract: manifest digest `576fa007a848780ff8f1e21e4a492f3758ad92ed72d829a75819bdfaf41a9b24`

## Local Run Details

The exact merged release was built and validated against a restored candidate database, then published through the guarded `mongo-consolidate` production command under the protected deployment lock. The final elevated process ran from `A:\Projects\christopherbell.dev-worktrees\domain-complete-merged-clean`, PID `17688`, from 2026-08-12 22:16:50 through 22:40:19 America/Chicago. It wrote `C:\Users\Christopher\AppData\Local\Temp\cbell-domain-cutover-final-success.log` and exited with status `SUCCESS`.

The cutover intentionally stopped the website writer during staged migration, exact verification, publication, and legacy deletion. It restarted `ChristopherBellDev` on production port 8080 only after the target ledger and catalog were complete. The app was left running; no candidate listener remained on port 8081.

## Test Cases

1. Guarded migration preview, candidate restore/migration, target publication, exact legacy deletion, final verification, and production start.
2. Local liveness and readiness checks.
3. Local home-page response.
4. Canonical public home-page response and apex-to-`www` redirect behavior.
5. Protected production service and release status.
6. Read-only exact MongoDB catalog, kind, and index compliance.

## Data Sent

- `GET http://127.0.0.1:8080/actuator/health/liveness`
- `GET http://127.0.0.1:8080/actuator/health/readiness`
- `GET http://127.0.0.1:8080/`
- `GET https://www.christopherbell.dev/`
- `GET https://christopherbell.dev/` with normal redirect following
- Protected read-only `prod.cmd status`
- Read-only inventory evaluation against fixed database `christopherbell`, loading the checked-in immutable domain manifest; no document values, credentials, or mutation commands were requested.

## Response Received

- Liveness: HTTP 200, `{"status":"UP"}`.
- Readiness: HTTP 200, `{"status":"UP"}`.
- Local home: HTTP 200, 3,981-byte HTML document beginning with `<!DOCTYPE html>`.
- Canonical public home: HTTP 200, matching 3,981-byte HTML response.
- Apex public home: HTTP 200 after redirect to `https://www.christopherbell.dev/`.
- Protected status: `WebsiteService`, `MongoService`, and `CloudflaredService` all `Running`; current release `62e1c7193414ecab266a217d221141120c8ecaef`; production PID `20572` on port 8080.
- Mongo inventory: `complete=true`; database `christopherbell`; manifest, collection, kind, and index compliance all `true`; exactly 14 collections, 52 kinds, and 126 indexes.
- Exact physical collections: `accounts`, `admin_activity`, `application_migrations`, `application_runtime`, `canes_box_tracker`, `communications`, `content`, `federation`, `location`, `music`, `sessions`, `shared_folder`, `vehicles`, and `whatsforlunch`.

## Pass / Fail

All six production acceptance cases passed. The guarded cutover status was `SUCCESS`; production is live on the exact merged application release and the consolidated database matches the approved manifest.

## Evidence

- Guarded transcript: `C:\Users\Christopher\AppData\Local\Temp\cbell-domain-cutover-final-success.log`
- Guarded status file: `C:\Users\Christopher\AppData\Local\Temp\cbell-domain-cutover-final-success.status`
- Protected status transcript: `C:\Users\Christopher\AppData\Local\Temp\cbell-postcutover-readonly.log`
- Automated pre-production evidence included 1,881 website tests with zero failures/errors, full PowerShell 7 and Windows PowerShell 5.1 boundary suites, Node contracts, and the marker-owned Mongo matrix covering 52 kinds, 126 indexes, 14 final collections, 52 drops, and 468 interruption boundaries.
- PRs [#1366](https://github.com/azurras/christopherbell.dev/pull/1366), [#1367](https://github.com/azurras/christopherbell.dev/pull/1367), [#1368](https://github.com/azurras/christopherbell.dev/pull/1368), and [#1369](https://github.com/azurras/christopherbell.dev/pull/1369) merged with required CI and independent review.

## Bugs / Follow-ups

No application or schema follow-up blocks completion. The read-only inventory command load-order defect discovered during post-cutover verification was fixed and merged in PR #1369. Because the site and schema were already healthy and the corrected command independently proved the live catalog, that tooling-only commit is intentionally left for the next ordinary deployment rather than forcing another production restart.
