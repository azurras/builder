# Cloudflare Analytics CSP Runtime Verification

## Document Status
draft

## Story/Issue
Builder site bug-audit implementation plan Task 64: allow the automatically injected integrity-protected Cloudflare Web Analytics beacon under the site's CSP.

## Branch
`codex/cloudflare-analytics-csp` at candidate commit `e4935aa5631e500471b116b82d87c459fde23314`, based on `origin/main` `9730446890122f72ab640a58abd9b958b706b433`. PR #1466 is open and all required CI checks have passed; deployment has not yet occurred.

## App / Environment
- App: `christopherbell.dev`, Spring Boot web application, Java 25.0.3, packaged candidate `website/build/libs/website.jar`.
- Candidate profile: `test,deploy-smoke`; scheduled jobs and mail disabled.
- Candidate URL: `http://127.0.0.1:18090`.
- Candidate MongoDB: isolated standalone MongoDB on `127.0.0.1:27028`, database `test`, data directory `build/runtime-smoke-bom-20261003/mongo-data`. Application startup logs confirm connection to `127.0.0.1:27028`; production database was not accessed.
- Production baseline before merge: fresh auto-status `UP_TO_DATE`, healthy/running, with remote, active, attempted, and successful SHA all `9730446890122f72ab640a58abd9b958b706b433`.

## Local Run Details
- Build and tests: `$env:TEMP='C:\t'; $env:TMP='C:\t'; .\gradlew.bat --no-daemon :website:check` (exit 0).
- Candidate was packaged from the candidate branch and launched on alternate port 18090 with the `test,deploy-smoke` profiles, isolated Mongo URI `mongodb://127.0.0.1:27028/test`, and scheduled work/mail disabled.
- Candidate processes: website PID 35020 and isolated MongoDB PID 8108. Both were stopped after verification; ports 18090 and 27028 were confirmed closed.
- Candidate logs and process snapshot: `build/runtime-smoke-cf-csp-20261003/website.stdout.log`, `website.stderr.log`, `mongod.log`, and `processes.txt` in the isolated site worktree.

## Test Cases
1. Observe the security-policy regression fail against the old CSP, then pass with the exact Cloudflare script origin allowed.
2. Run the focused security integration test and full website check.
3. Start packaged candidate on isolated MongoDB and alternate port; request readiness, liveness, homepage, and `/void`; inspect returned CSP.
4. Verify pull request CI across Java 25 Linux, macOS, and Windows, CodeQL analyses, and Dependency Review.

## Data Sent
- `GET http://127.0.0.1:18090/actuator/health/readiness`.
- `GET http://127.0.0.1:18090/actuator/health/liveness`.
- `GET http://127.0.0.1:18090/` and `GET http://127.0.0.1:18090/void`.
- No authentication, data mutation, or production fixture was used.

## Response Received
- Readiness and liveness returned HTTP 200; homepage and `/void` returned HTTP 200.
- Candidate CSP contained `script-src 'self' https://static.cloudflareinsights.com`; a comparison guard confirmed the other security-policy directives and headers remained unchanged.
- Startup log confirmed MongoDB connection to the isolated `127.0.0.1:27028` process and Tomcat on port 18090.
- Focused regression: failed before the CSP change because the permitted source was absent; passed after the change.
- Full `:website:check`: passed, including 1,975 Java tests (0 failures, 0 errors, 108 skipped) and native Windows checks.
- PR #1466: Dependency Review, CodeQL, Java 25 Ubuntu/macOS/Windows builds, and Java/Kotlin and JavaScript/TypeScript analyses all passed.

## Pass / Fail
- PASS: the exact Cloudflare Insights script host is allowed by `script-src`.
- PASS: all other security directives and headers remain unchanged.
- PASS: isolated candidate startup, MongoDB connection, health endpoints, homepage, and `/void`.
- PASS: full website checks and all required PR checks.
- PENDING: post-deployment browser verification of the injected script request and absence of the CSP violation; public and local production checks; final fresh deployer SHA.

## Evidence
- Candidate startup: `build/runtime-smoke-cf-csp-20261003/website.stdout.log` and `mongod.log` in the isolated worktree.
- Candidate process record: `build/runtime-smoke-cf-csp-20261003/processes.txt`.
- PR: https://github.com/azurras/christopherbell.dev/pull/1466, head `e4935aa5631e500471b116b82d87c459fde23314`.
- Deployment baseline captured 2026-10-03: `prod.cmd auto-status` showed fresh healthy `UP_TO_DATE` at base revision `9730446890122f72ab640a58abd9b958b706b433`.

## Bugs / Follow-ups
- Deploy through the supported automatic deployer after merging PR #1466, then verify a fresh matching active SHA, readiness/liveness, representative public routes, and in Chrome that Cloudflare's integrity-protected beacon loads without a CSP violation.
- Existing non-elevated poller inspection remains `UNKNOWN/ACCESS_DENIED`; deployment status itself is readable and healthy.
