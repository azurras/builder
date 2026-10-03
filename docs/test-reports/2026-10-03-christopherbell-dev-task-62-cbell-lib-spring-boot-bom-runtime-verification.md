# christopherbell.dev Task 62 cbell-lib Spring Boot BOM Runtime Verification

## Document Status

complete

## Story/Issue

Builder implementation plan Task 62: align the standalone `cbell-lib` Spring Boot dependency BOM with the repository's latest stable Spring Boot release, 4.1.1.

## Branch

`codex/cbell-lib-spring-boot-bom-411-20261003`, based on `origin/main` SHA `df3a1e0143e2f909c7c9ced389fbea4a3ea73fbf`. The only source change is `cbell-lib/build.gradle.kts`, changing its BOM from 4.1.0 to 4.1.1. No dependency verification metadata changes were needed. Packaged candidate JAR: `website/build/libs/website.jar`; SHA-256 `0AA2FB4AF1F885CB57062754563039BA84E0FD8191CA0CC429F7E2DA5C43A13D`.

## App / Environment

Windows 11; Java 25.0.3; Spring Boot 4.1.1; MongoDB 8.3.2. Candidate profile `test,deploy-smoke`, bound only to `127.0.0.1:18088`. Candidate database URI was `mongodb://127.0.0.1:27028/test`, backed by a fresh temporary MongoDB process (PID 27756) with data under the isolated worktree's ignored `build/runtime-smoke-bom-20261003/mongo-data` directory. The test database contained one deterministic synthetic `TARGET_ACTIVE` cutover ledger matching `DomainCollectionManifest.DIGEST`; application startup completed with 16 migration records and no failed migration records. `application-test.yml` disables Cane's and WFL monthly imports; `application-deploy-smoke.yml` disables scheduling. No production data was copied or accessed.

## Local Run Details

Built with `:website:bootJar`; build exit code 0. Candidate launch command:

```powershell
$env:JAVA_TOOL_OPTIONS='-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp'
java -jar website/build/libs/website.jar `
  --spring.profiles.active=test,deploy-smoke `
  --spring.mongodb.uri=mongodb://127.0.0.1:27028/test `
  --app.scheduling.enabled=false `
  --server.address=127.0.0.1 `
  --server.port=18088
```

The first candidate launch (PID 17524) exited before binding because Java could not establish its Windows loopback channel. Retrying with the process-only `JAVA_TOOL_OPTIONS` above succeeded (PID 15624). Startup logs show connection to MongoDB at `127.0.0.1:27028`, Tomcat on port 18088, and `Started Application`. The candidate was stopped by PID after verification. The temporary MongoDB process was stopped; candidate ports 18088 and 27028 are closed. Production listeners remained on 8080 and 27017, with `ChristopherBellDev`, `MongoDB`, and `cloudflared` Running/Automatic.

## Test Cases

1. Verify `cbell-lib` compile, runtime, and test-runtime Spring Boot dependency management.
2. Run `:cbell-lib:check` and full `:website:check`.
3. Package and run the candidate against the isolated MongoDB `test` database.
4. Request readiness, liveness, and homepage from the candidate.
5. Confirm candidate cleanup and unchanged production listeners/services.

## Data Sent

- `GET http://127.0.0.1:18088/actuator/health/readiness`, no body or special headers.
- `GET http://127.0.0.1:18088/actuator/health/liveness`, no body or special headers.
- `GET http://127.0.0.1:18088/`, no body or special headers.
- Candidate application used only `mongodb://127.0.0.1:27028/test`; the database was isolated and named `test`.

## Response Received

- Readiness HTTP response: `HTTP/1.1 200 OK`, body `{"status":"UP"}`.
- Liveness HTTP response: `HTTP/1.1 200 OK`, body `{"status":"UP"}`.
- Homepage HTTP response: `HTTP/1.1 200 OK`, 3,981 bytes, title `CB | Home`.
- Candidate MongoDB contained 16 migration records and zero with `payload.status=FAILED`; the active domain ledger reported `TARGET_ACTIVE`.
- After the BOM change, `:cbell-lib:dependencyInsight` resolved Spring Boot Mongo starter 4.1.1 on compile, runtime, and test runtime, and Spring Data MongoDB 5.1.1 on runtime. Before the change, the library runtime graph resolved 4.1.0 and 5.1.0 while the website graph already resolved 4.1.1 and 5.1.1.
- `:cbell-lib:check` passed. `:website:check` exited 0; its Java reports recorded 1,975 tests, 0 failures, 0 errors, and 108 skips. The check also ran the repository JavaScript and Windows operations tasks successfully.
- `:website:bootJar` exited 0; `git diff --check` passed. The diff changes one BOM version and no other dependency metadata.

## Pass / Fail

All dependency resolution, library checks, site checks, packaged-candidate, HTTP, database-isolation, and cleanup cases passed. The initial candidate start failed before binding due the known Windows JDK Unix-domain socket issue; the process-scoped temp-directory setting resolved it without changing project configuration. No production process, listener, or database was touched during candidate testing.

## Production Deployment

- PR #1463 passed Dependency Review, CodeQL, and Java 25 Ubuntu/macOS/Windows CI, then squash-merged as `dd87087f4d9c6f43cb6730408a315cd640820e69`.
- The readable automatic-deployment status record at `C:\ProgramData\christopherbell.dev-status\auto-deploy.json` reported `UP_TO_DATE`; `remoteSha`, `activeSha`, `attemptedSha`, and `successfulSha` all matched the merge SHA. `toolRefreshStatus` was `SUCCEEDED`, `failureCategory` was `NONE`, and the record was fresh at read time. This status store grants Users read-only access; no elevated access or protected configuration access was used.
- After deployment, local readiness and liveness each returned HTTP 200 with `{"status":"UP"}`. Local and public homepage requests returned HTTP 200 with title `CB | Home`. `ChristopherBellDev`, `MongoDB`, and `cloudflared` remained Running/Automatic, and listeners remained on 8080 and 127.0.0.1:27017.
- The first `prod.cmd auto-status` invocation came from the dirty production checkout, which was 87 commits behind `origin/main`; that stale script tried to read protected `C:\ProgramData\christopherbell.dev\config\deploy.json` and failed without elevation. Running the current `origin/main` command read-only succeeded: `available=True`, `freshness=FRESH`, `status=UP_TO_DATE`, active/successful SHA matched the merge SHA, service was `RUNNING`, and site health was `HEALTHY`. Its only unavailable field was scheduled-task registration (`pollerState=UNKNOWN`, `pollerReason=ACCESS_DENIED`), which is the documented non-elevated task-query limitation. No elevation was used.

## Evidence

- Gradle dependency-insight output captured the pre-change mismatch and post-change 4.1.1/5.1.1 resolutions.
- Java test XML reports are under `website/build/test-results/test` in the isolated worktree.
- Candidate logs and HTTP response bodies are under ignored `build/runtime-smoke-bom-20261003` in the isolated worktree.
- Read-only final listener/service inspection confirmed ports 8080 and 27017 and all production services remained running after candidate cleanup.

## Bugs / Follow-ups

Task 62 is complete. The only product source change aligns the `cbell-lib` BOM to Spring Boot 4.1.1; the merged SHA is deployed and production health checks passed.
