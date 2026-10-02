# Infinite feed error feedback runtime verification

## Document Status

complete

## Story/Issue

Task 58 in the christopherbell.dev bug-audit plan. Verify error reporting and retry behavior for the Void and public-profile infinite feeds, including loading-skeleton cleanup, alert ownership, malformed/repeated cursor handling, and stale request suppression.

## Branch

Branch `codex/infinite-feed-error-feedback-20261002`, updated to deployed Boot 4.1.1 base commit `4b665913be7356b6d8f6a437899beda0b22cfff6`. Task 58 source changes were uncommitted during candidate verification. Candidate JAR SHA-256: `CC41B2F93A47DC99435076A66562161745BD5CC432925A5DB0557CACD9C6E588`.

## App / Environment

Spring Boot 4.1.1, Java 25.0.3, MongoDB Java driver 5.8.1. Candidate app URL `http://127.0.0.1:18082`; production remained on port 8080. Candidate URI explicitly selected `mongodb://127.0.0.1:27020/test`, served by isolated MongoDB 8.3 bound to loopback and backed by a separate copy of the verified disposable test fixture at `website/build/verification/task58-mongodb-seeded`. Test and deploy-smoke profiles disabled scheduled collectors; mail was disabled. Production MongoDB on 27017 was not a candidate target.

## Local Run Details

Ran `.\gradlew.bat :website:check --no-daemon --console=plain --max-workers=1` with process-only `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:/Windows/Temp` and a private `GRADLE_USER_HOME` under LocalAppData. All 21 Gradle tasks passed in 7m26s. The Java suite reported 1,975 passed, 0 failures/errors, and 108 skipped; Windows operations suites passed. The full JavaScript task passed with the added feed regressions. Focused Task 58 tests passed 16/16; `node --check` passed for all four changed modules.

An initial start against a newly empty database failed at migration `015-require-domain-collection-schema`; that database was an invalid fixture setup. The app and candidate MongoDB were stopped, and a separate copy of the verified disposable `test` fixture was started on port 27020. No production port or database was used.

Started candidate MongoDB PID 18312 with `mongod.exe --dbpath website/build/verification/task58-mongodb-seeded --bind_ip 127.0.0.1 --port 27020 --logpath website/build/verification/task58-mongod-seeded.log --logappend`. `mongosh` against database `test` returned `ping=1`. Started packaged JAR PID 72444 with profiles `test,deploy-smoke`, URI `mongodb://127.0.0.1:27020/test`, port 18082, scheduling disabled, and mail disabled. Startup identified Java 25.0.3, Boot 4.1.1, and Mongo driver 5.8.1.

## Test Cases

1. Run full repository checks and focused feed regressions.
2. Verify candidate readiness on the alternate port.
3. Load the Void feed page and its hashed `home-feed.js` asset.
4. Load a public profile page from an existing disposable test account and its hashed `user-feed.js` asset.
5. Stop candidate processes and confirm only candidate ports close.

## Data Sent

- MongoDB ping to `mongodb://127.0.0.1:27020/test`.
- `GET http://127.0.0.1:18082/actuator/health/readiness`.
- `GET http://127.0.0.1:18082/void` and its returned hashed home-feed script.
- `GET http://127.0.0.1:18082/u/Chris` and its returned hashed user-feed script. This was an existing fixture account; no account or post was created or changed.

## Response Received

- MongoDB reported database `test`, ping `1`.
- Readiness returned HTTP response status code 200 with JSON `status=UP`.
- `/void` returned HTTP response status code 200, title `CB | Void`; hashed `home-feed.js` returned HTTP response status code 200 (8,753 bytes).
- `/u/Chris` returned HTTP response status code 200, title `CB | @Chris in the Void`; hashed `user-feed.js` returned HTTP response status code 200 (7,933 bytes).
- Full `:website:check` passed 21/21 Gradle tasks; Java results were 1,975 passed, 0 failures/errors, 108 skipped. Focused Task 58 tests passed 16/16.
- Candidate PIDs 72444 and 18312 were stopped through their owned sessions. Ports 18082 and 27020 closed. Production listener PIDs 72856 (8080) and 5016 (27017) remained. No production data, service, or listener was changed.

## Pass / Fail

Candidate verification passed against the verified disposable fixture. The first attempt against a newly empty database failed at the required migration precondition and was discarded without production effects. Full native checks, candidate readiness, both feed-page shells, both changed script assets, and exact candidate cleanup passed.

## Evidence

Observed on 2026-10-02. Test output, sanitized readiness JSON, route responses, process ownership, and listener cleanup were inspected directly. The fixture copy, MongoDB log, and generated JAR are under ignored worktree build output. Required PR CI, merge, and supported production deployment remain pending.

## Bugs / Follow-ups

The change reports initial and scroll-load errors on `/void` and `/u/{username}`, clears empty-feed skeletons after failure, preserves unrelated alerts, keeps failed pages retryable, rejects malformed/repeated cursors, and ignores superseded results. PR CI and supported production acceptance are the remaining delivery gates.

## Supplemental browser attempt - 2026-10-02 16:24 CDT

The isolated in-app browser showed the candidate `/void` page and its empty-feed state. It had no feed items to trigger a scroll retry. To make the first feed request fail deterministically, a one-shot local proxy was planned, but the candidate application could not be restarted against the reused `task58-mongodb-seeded` fixture: migration `015-require-domain-collection-schema` reported an incomplete durable record. The candidate MongoDB process was stopped; ports 18082, 27020, and 18083 were closed, while production listeners 8080 and 27017 remained present. No browser-level failure/retry was exercised; the existing regression suite remains the evidence for those behaviors. Do not treat browser retry acceptance as verified.
