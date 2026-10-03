# Cloudflare Analytics CSP Runtime Verification

## Document Status
complete

## Story/Issue
Builder site bug-audit implementation plan Task 64: allow the automatically injected integrity-protected Cloudflare Web Analytics beacon under the site's CSP.

## Branch
`codex/cloudflare-analytics-csp` at candidate commit `e4935aa5631e500471b116b82d87c459fde23314`, based on `origin/main` `9730446890122f72ab640a58abd9b958b706b433`. PR #1466 passed all required CI checks and squash-merged as `979d7f3b10e89b9749870f679797daf88c0495bd`.

## App / Environment
- App: `christopherbell.dev`, Spring Boot web application, Java 25.0.3, packaged candidate `website/build/libs/website.jar`.
- Candidate profile: `test,deploy-smoke`; scheduled jobs and mail disabled.
- Candidate URL: `http://127.0.0.1:18090`.
- Candidate MongoDB: isolated standalone MongoDB on `127.0.0.1:27028`, database `test`, data directory `build/runtime-smoke-bom-20261003/mongo-data`. Application startup logs confirm connection to `127.0.0.1:27028`; production database was not accessed.
- Production baseline before merge: fresh auto-status `UP_TO_DATE`, healthy/running, with remote, active, attempted, and successful SHA all `9730446890122f72ab640a58abd9b958b706b433`.
- Production deployment completed through the supported automatic deployer. Final status was fresh `UP_TO_DATE`, healthy/running, with remote, active, attempted, and successful SHA all `979d7f3b10e89b9749870f679797daf88c0495bd`.

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
5. After automatic deployment, request local readiness/liveness, local and public homepage and `/void`, inspect the CSP, and open the public homepage in Chrome to inspect the Cloudflare beacon and console.

## Data Sent
- `GET http://127.0.0.1:18090/actuator/health/readiness`.
- `GET http://127.0.0.1:18090/actuator/health/liveness`.
- `GET http://127.0.0.1:18090/` and `GET http://127.0.0.1:18090/void`.
- No authentication, data mutation, or production fixture was used.
- Production browser verification loaded `https://www.christopherbell.dev/` in Chrome; no form or application action was submitted.

## Response Received
- Candidate readiness/liveness: `HTTP 200 OK`, body `{"status":"UP"}`. Candidate `/` and `/void`: `HTTP 200 OK`.
- Candidate CSP contained `script-src 'self' https://static.cloudflareinsights.com`; a comparison guard confirmed the other security-policy directives and headers remained unchanged.
- After deployment, local readiness and liveness each returned `HTTP 200 OK` with body `{"status":"UP"}`; local and public `/` and `/void` each returned `HTTP 200 OK`.
- Local and public CSP response headers contained `script-src 'self' https://static.cloudflareinsights.com` and retained the existing `connect-src 'self'` plus existing app-specific connection sources.
- Chrome rendered the public homepage with its integrity-protected Cloudflare beacon script. Browser asset inventory recorded the beacon URL as a loaded resource; no warning or error console entries were present.
- Startup log confirmed MongoDB connection to the isolated `127.0.0.1:27028` process and Tomcat on port 18090.
- Focused regression: failed before the CSP change because the permitted source was absent; passed after the change.
- Full `:website:check`: passed, including 1,975 Java tests (0 failures, 0 errors, 108 skipped) and native Windows checks.
- PR #1466: Dependency Review, CodeQL, Java 25 Ubuntu/macOS/Windows builds, and Java/Kotlin and JavaScript/TypeScript analyses all passed.
- After merge, the supported deployer reached fresh `SUCCEEDED` with remote, active, attempted, and successful SHA all `979d7f3b10e89b9749870f679797daf88c0495bd`; a subsequent fresh status was `UP_TO_DATE`, site healthy, service running.
- Post-deployment local readiness/liveness, local `/`, local `/void`, public `/`, and public `/void` all returned HTTP 200. Local and public response CSPs both contained `script-src 'self' https://static.cloudflareinsights.com` and retained the existing `connect-src 'self'` plus its pre-existing application API sources.
- Chrome public-page verification found exactly one `https://static.cloudflareinsights.com/beacon.min.js` script element with an integrity attribute. The browser asset inventory observed the script as a resource, and the page console contained no warning or error entries, including no CSP violation.

## Pass / Fail
- PASS: the exact Cloudflare Insights script host is allowed by `script-src`.
- PASS: all other security directives and headers remain unchanged.
- PASS: isolated candidate startup, MongoDB connection, health endpoints, homepage, and `/void`.
- PASS: full website checks and all required PR checks.
- PASS: post-deployment browser verification of the injected integrity-protected beacon resource with no CSP console violation.
- PASS: public and local health/page checks and final fresh deployer SHA.

## Evidence
- Candidate startup: `build/runtime-smoke-cf-csp-20261003/website.stdout.log` and `mongod.log` in the isolated worktree.
- Candidate process record: `build/runtime-smoke-cf-csp-20261003/processes.txt`.
- PR: https://github.com/azurras/christopherbell.dev/pull/1466, head `e4935aa5631e500471b116b82d87c459fde23314`.
- Deployment baseline captured 2026-10-03: `prod.cmd auto-status` showed fresh healthy `UP_TO_DATE` at base revision `9730446890122f72ab640a58abd9b958b706b433`.
- Deployment result captured 2026-10-03 18:40 UTC: `prod.cmd auto-status` reported fresh healthy `UP_TO_DATE` with active and successful revision `979d7f3b10e89b9749870f679797daf88c0495bd`.
- Production Chrome verification at `https://www.christopherbell.dev/`: one integrity-protected beacon script, asset inventory source `resource`, and zero warning/error console records.

## Bugs / Follow-ups
No Task 64 follow-up remains. The existing non-elevated poller inspection remains `UNKNOWN/ACCESS_DENIED`; deployment status itself is readable and healthy.
