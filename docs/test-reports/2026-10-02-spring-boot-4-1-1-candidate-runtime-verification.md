# Spring Boot 4.1.1 candidate runtime verification

## Document Status

complete

## Story/Issue

Task 59 in the christopherbell.dev bug-audit plan. Verify the Spring Boot 4.1.1 dependency upgrade with strict Gradle verification and an isolated packaged-app runtime.

## Branch

Branch `codex/spring-boot-4-1-1-20261002`, based on deployed `bd1ede060d6135562230f14baf08d37df3457dcd`. Candidate source was uncommitted during verification. JAR SHA-256: `2FAB52A81E337E07C7B190F6C131B0DD35A7B27BDC45BFD214942C38B58003E1`.

## App / Environment

Spring Boot 4.1.1, Java 25.0.3, Spring Data MongoDB 5.1.1, MongoDB Java driver 5.8.1, MongoDB server 8.3.2. Candidate URL `http://127.0.0.1:18081`; production remained on port 8080. Candidate MongoDB listened only on `127.0.0.1:27019`; the application URI explicitly selected database `test`. MongoDB used a separate copy of the previously verified disposable test fixture under the isolated worktree's ignored `website/build/verification/spring-boot-mongodb` directory. The test and deploy-smoke profiles disabled the Cane's and WFL collectors and application scheduling; mail was disabled. Production MongoDB on port 27017 was not configured as a candidate target.

## Local Run Details

Used process-only `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp`. The first `:website:check --write-verification-metadata sha256` resolved the 4.1.1 managed graph and revealed one expected version-pinned test failure: the Mongo boundary snapshot expected Spring Data MongoDB 5.1.0 and Mongo driver 5.8.0. Updated only the three JAR filename expectations; their class counts and hashes stayed identical, and the access-candidate inventory and boundary assertions passed unchanged. Focused `MongoPersistenceBoundaryRulesTest` passed 4/4.

The final strict-verification command was `\.gradlew.bat :website:check --no-daemon --console=plain --max-workers=1`; it passed all 21 Gradle tasks in 6m01s. Across 299 Java test-result files, 1,975 tests passed with 0 failures/errors and 108 skipped. The Windows Pester suite passed 75/75; the project JavaScript test task passed (up-to-date after the earlier successful 363/363 run on this same source base). The 164 new verification components are additive; no existing component records were removed.

Started MongoDB PID 50416 with `mongod.exe --dbpath website/build/verification/spring-boot-mongodb --bind_ip 127.0.0.1 --port 27019 --logpath website/build/verification/spring-boot-4-1-1-mongod.log --logappend`. Started the packaged JAR in a foreground task session as Java PID 51236 with profiles `test,deploy-smoke`, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27019/test`, `SERVER_PORT=18081`, `APP_SCHEDULING_ENABLED=false`, and `APP_MAIL_ENABLED=false`. Candidate application output was captured in the task terminal; MongoDB output is in the ignored worktree log. The JAR listing and startup log identified Spring Boot 4.1.1, Spring Data MongoDB 5.1.1, and driver 5.8.1.

## Test Cases

1. Resolve and package the Boot 4.1.1 graph with normal strict checksum verification after recording new checksums.
2. Ping the disposable MongoDB copy through `mongodb://127.0.0.1:27019/test`.
3. Check candidate readiness and request the public home and Void pages.
4. Stop the candidate application and isolated MongoDB; confirm only candidate ports close and production listeners remain.

## Data Sent

- Mongo shell ping against database `test`: `db.getName()` and `db.adminCommand({ping: 1})`.
- `GET http://127.0.0.1:18081/actuator/health/readiness`
- `GET http://127.0.0.1:18081/`
- `GET http://127.0.0.1:18081/void`

## Response Received

- Mongo shell reported `database=test` and `ping=1`.
- Readiness returned JSON `status=UP`.
- Home returned status code 200, 3,981 bytes, title `CB | Home`.
- Void returned status code 200, 6,812 bytes.
- Startup log reported the Mongo driver version 5.8.1 connected to `127.0.0.1:27019`.
- Candidate Java PID 51236 was stopped with Ctrl+C; MongoDB PID 50416 was stopped after confirming ownership of candidate port 27019. Ports 18081 and 27019 closed. Production listeners 8080 and 27017 remained present. No production data or listener was changed.

## Pass / Fail

All focused architecture tests, strict full build checks, isolated database ping, readiness, and public-page checks passed. Production deployment and post-deployment acceptance were not part of this candidate runtime report.

## Evidence

Commands and results were observed on 2026-10-02. `:website:check` used strict dependency verification on the final run. Candidate artifact and disposable database copy remain in the isolated worktree's ignored build directory; no process uses either after verification.

## Bugs / Follow-ups

The upgrade requires updating the dependency-version assertions in `MongoPersistenceBoundaryRulesTest`. The Spring Data MongoDB and Mongo driver class counts and hashes, audited access-candidate hash, inert-class allowlist, and architecture classifications did not change. Required PR CI and supported production deployment remain pending.
