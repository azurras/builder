# christopherbell.dev Task 66 Photography Usage Heading Runtime Verification

## Document Status

complete

## Story/Issue

Builder implementation plan Task 66: add a visible page heading to photography usage terms.

## Branch

Branch codex/photos-usage-heading-20261003, based on origin/main 02cc854e0642efd3dbd8bc9091edc01b57b09a88. Candidate source changes add the heading and its MVC regression. PR #1468 was merged with squash as `bde35ffae5d23e7754bd49ee00fc940f19123c2`; required CI passed. Candidate JAR SHA-256: 49E2968CFE585271BDF9EB51650EF1A3AD6CD1F459A5D59B5F7EAFF10624E130.

## App / Environment

Windows 11; Java 25.0.3; Spring Boot 4.1.1; MongoDB 8.3.2. Candidate profile test,deploy-smoke; app URL http://127.0.0.1:18092; isolated MongoDB URL mongodb://127.0.0.1:27029/test. The database lived under build/runtime-smoke-photos-usage-20261003/mongodb-valid and contained only the synthetic active schema ledger before application startup. The fixture used the checked-in manifest digest 576fa007a848780ff8f1e21e4a492f3758ad92ed72d829a75819bdfaf41a9b24, 52 kind metrics and 50 sorted legacy source names. No production database was used. Scheduled collectors and mail were disabled.

## Local Run Details

- Regression-first check: added an exact h1 assertion to getPhotographyUsagePage_rendersUsageContract, then ran :website:test --tests dev.christopherbell.view.ViewControllerTest. It failed at the new assertion as expected; the other 42 tests passed.
- After adding the template h1, the same focused command passed all 43 ViewControllerTest cases.
- Full check command: set process-local JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp and private GRADLE_USER_HOME=C:\Users\Christopher\AppData\Local\Temp\gradle-cbell-photos-usage-heading, then ran .\gradlew.bat :website:check --no-daemon. Exit code 0 after 5m25s. Java XML reported 1,975 tests, 0 failures, 0 errors, 108 skipped; JavaScript XML reported 374 tests.
- An initial candidate launch against a newly empty disposable database stopped at the required migration 015 schema guard. No candidate app listener remained. This was an invalid fixture, not a template failure.
- Successful candidate command: java -Djdk.net.unixdomain.tmpdir=C:/Windows/Temp -jar website/build/libs/website.jar --spring.profiles.active=test,deploy-smoke --spring.mongodb.uri=mongodb://127.0.0.1:27029/test --app.scheduling.enabled=false --app.mail.enabled=false --server.address=127.0.0.1 --server.port=18092.
- Candidate app PID 36192 connected to MongoDB PID 8812 on 127.0.0.1:27029. Startup logs identify the exact isolated server. The database then contained 16 migration records, zero with FAILED status, and the TARGET_ACTIVE cutover ledger.
- An initial polling script did not recognize the PowerShell WebRequest byte-array response body and timed out even though the app had started. Independent HttpClient requests below decoded the actual responses and verified readiness/liveness.
- Candidate app and both task-owned MongoDB processes (PIDs 3912 and 8812) were stopped. Ports 18091, 18092, 27028, and 27029 were confirmed closed; production listeners on 8080 and 27017 remained present.

## Test Cases

1. Confirm the focused MVC assertion fails before the template change and passes after.
2. Run the complete native website check.
3. Start the packaged candidate with isolated MongoDB test data and confirm readiness/liveness.
4. Request the public usage page anonymously and verify heading, terms, title and main landmark.
5. Inspect the candidate page's browser accessibility tree.

## Data Sent

- GET http://127.0.0.1:18092/actuator/health/readiness with no authentication.
- GET http://127.0.0.1:18092/actuator/health/liveness with no authentication.
- GET http://127.0.0.1:18092/photos/usage with no authentication.
- The application connected only to mongodb://127.0.0.1:27029/test. Its startup migration changes were confined to the disposable candidate database.

## Response Received

- Readiness: HTTP 200, body {"status":"UP"}.
- Liveness: HTTP 200, body {"status":"UP"}.
- Usage page: HTTP 200; one h1 inside main, exact visible text "Photography Usage"; the existing restriction paragraph and CB | Photography Usage title remained present.
- Chrome accessibility tree exposed "Photography Usage" as a level-one heading, followed by the unchanged usage restriction paragraph.
- After deployment, local readiness returned status code 200 with `{"status":"UP"}`; public `GET https://www.christopherbell.dev/photos/usage` returned status code 200 with title `CB | Photography Usage`. Its `<main>` text was `Photography Usage Usage of the images on this site is forbidden without written consent from the owner.` and contained exactly one h1. The production browser accessibility tree exposed that h1 as a level-one heading.
- MongoDB inspection confirmed database test, 16 migration records, zero failed migrations, and TARGET_ACTIVE cutover state.
- Candidate TCP inspection showed connections owned by app PID 36192 to isolated MongoDB port 27029.

## Pass / Fail

- PASS: The new regression failed against the old template at the expected h1 assertion.
- PASS: Focused ViewControllerTest passed 43/43.
- PASS: :website:check exited 0; 1,975 Java tests had 0 failures/errors and 108 skipped; JavaScript tests passed 374/374; native Windows check tasks completed.
- PASS: Candidate readiness, liveness and anonymous usage route returned HTTP 200.
- PASS: The rendered page contains one main h1 and preserves the terms and title.
- PASS: Candidate cleanup closed its app and MongoDB listeners; production listeners remained present.
- NOTE: The first candidate attempt used a blank database and was correctly rejected by migration 015; the second used the verified synthetic ledger fixture and started successfully.
- PASS: PR #1468 required checks passed: Java 25 builds on Ubuntu, macOS, and Windows; CodeQL Java, JavaScript/TypeScript, and Actions analyses; and Dependency Review. The PR merged as `bde35ffae5d23e7754bd49ee00fc940f19123c2` at 2026-10-03 20:22 UTC.
- PASS: Fresh `prod.cmd auto-status` reported `FRESH`, `UP_TO_DATE`, reason `NONE`, service `RUNNING`, site `HEALTHY`; remote, active, attempted, and successful SHA all matched `bde35ffae5d23e7754bd49ee00fc940f19123c2`; trusted deploy-tool refresh succeeded. Poller registration remains `UNKNOWN` / `ACCESS_DENIED` for the standard user.
- PASS: Post-deployment local readiness returned HTTP 200 with `{"status":"UP"}`. Public `GET https://www.christopherbell.dev/photos/usage` returned HTTP 200; the main landmark contains exactly one h1, `Photography Usage`, followed by the existing text, `Usage of the images on this site is forbidden without written consent from the owner.`; document title remains `CB | Photography Usage`. The production Chrome accessibility tree also exposed the level-one heading.
- PASS: The production Java service and MongoDB listeners remained running; no manual restart, elevated access, or production data write was used.

## Evidence

- Source/test diff: website/src/main/resources/templates/photo/usage.html and website/src/test/java/dev/christopherbell/view/ViewControllerTest.java in the candidate worktree.
- Full native check output and test XML: website/build/test-results/test/ and website/build/test-results/jsTest/results.xml in the candidate worktree.
- Candidate logs and fixture scripts: build/runtime-smoke-photos-usage-20261003/ under the candidate worktree, including mongod logs, application logs, the synthetic ledger seeding and verification scripts, and process IDs.
- Candidate worktree: A:\Projects\christopherbell.dev-worktrees\photos-usage-heading-20261003.

## Bugs / Follow-ups

The verified accessibility defect is fixed, merged, deployed, and verified on the public route. No GitHub issue was open for this item. The non-elevated scheduled-poller registration query remains `UNKNOWN` / `ACCESS_DENIED`, while deployment status itself is fresh and successful.
