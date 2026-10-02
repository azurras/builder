## Document Status

draft

## Story/Issue

Task 52 of the ongoing christopherbell.dev site bug audit: prevent malformed VIN values from reaching the public decode API.

## Branch

Site worktree: `A:\Projects\christopherbell.dev-worktrees\site-bug-audit-20261001`, branch `codex/site-bug-audit-20261002`, base SHA `71aceeefad5bebf908acdeab82a3a12d4b19c32a`. Candidate JAR SHA-256: `75E7B3FCD22B9B892243FA095FD59B40F723DB26840D633049F54F432DCAC7C8`.

## App / Environment

Spring Boot 4.1, Java 25.0.3. Candidate URL `http://127.0.0.1:18081`, profiles `test,deploy-smoke`. Candidate MongoDB 8.3.2 was bound to `127.0.0.1:27019` and used database `test`. The database directory was copied from the previously verified restored test fixture at `C:\Users\Christopher\AppData\Local\Temp\codex-mongodb-only-restored-20260924T193158Z`. Source and copy tree digests both equaled `D60F589980C76F3402C55F21326EB343DEE1048E068903F5A3E2A25F5ECEECFC`. Application scheduling and mail were disabled. No production database connection was configured.

## Local Run Details

Built with `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp .\gradlew.bat --no-daemon :website:bootJar`. Started `website/build/libs/website.jar` with `SPRING_PROFILES_ACTIVE=test,deploy-smoke`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, `APP_SCHEDULING_ENABLED=false`, `APP_MAIL_ENABLED=false`, and `SERVER_PORT=18081`. Candidate app PID 25520 and MongoDB PID 6032 both stopped after verification. Candidate ports 18081 and 27019 were closed afterward; production listeners 8080 and 27017 remained present. The copied fixture and MongoDB log remain under the isolated worktree's ignored `website/build/verification` directory.

## Test Cases

1. Run the new VIN decoder JS regression before the fix and confirm it fails because an invalid short VIN causes one `fetch`.
2. Run the regression after the fix and verify invalid submission shows local validation without `fetch`.
3. Run all browser-side JS tests and JavaScript syntax check.
4. Build the packaged candidate.
5. Check candidate readiness, homepage, VIN page, and VIN script on the alternate port.
6. In a browser, enter a 16-character VIN and submit; verify browser-native validation blocks submission and the page stays in place.
7. Read production deployer status and verify candidate cleanup/listener isolation.

## Data Sent

Candidate unauthenticated GET requests:
- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`
- `GET http://127.0.0.1:18081/vin-decoder`
- `GET http://127.0.0.1:18081/js/vin-decoder.js`

The local candidate browser field received `1HGCM82633A00435` and the Decode button was clicked. Native form validity prevented submission. The automated regression directly dispatched an invalid submit event to the production page module and observed zero fetch calls after the fix. No VIN was sent to NHTSA or the production site.

## Response Received

- Regression before fix: failed as expected; observed 1 fetch instead of 0.
- Regression after fix: passed; fetch count was 0 and the local message was `VIN must be exactly 17 valid characters.`.
- `:website:jsTest`: 345 passed, 0 failed.
- `node --check website/src/main/resources/static/js/vin-decoder.js`: passed.
- `git diff --check`: passed; Git printed only working-tree LF-to-CRLF notices.
- `:website:bootJar`: succeeded.
- Candidate readiness: HTTP 200, body `{"status":"UP"}`.
- Candidate homepage, VIN page, and VIN script: HTTP 200. Rendered template included `minlength="17"` and the 17-character VIN pattern; delivered script included the client validation guard.
- Browser submission: accessibility tree showed `Please match the requested format.`; the form remained on `/vin-decoder`.
- Production read-only `prod.cmd auto-status`: `FRESH`, `UP_TO_DATE`, `RUNNING`, `HEALTHY`, matching active/remote/attempted/successful SHA `71aceeefad5bebf908acdeab82a3a12d4b19c32a`. Non-elevated poller lookup remained `UNKNOWN` / `ACCESS_DENIED`.

## Pass / Fail

Candidate and local verification passed. PR review, required CI, deployment, and deployed acceptance remain pending; this report is therefore a draft.

## Evidence

The focused regression was observed failing before implementation and passing afterward. The full JS suite output ended with `tests 345, pass 345, fail 0`. Gradle required the process-only JDK 25 socket-path override above; no system configuration was changed. Candidate browser interaction used the hidden Codex in-app browser tab. After shutdown, only production listeners on 8080 and 27017 were present.

## Bugs / Follow-ups

The confirmed defect was that short VIN input passed the client-side empty check and reached the API. The fix adds a 17-character VIN pattern guard and native HTML form constraints. No backend/API behavior changed. Complete diff review, full CI, supported production deployment, and deployed page/asset acceptance before marking this report complete.
