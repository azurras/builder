# christopherbell.dev MongoDB Collection Catalog Test Report

## Document Status

complete

## Story/Issue

- Work record: [christopherbell.dev MongoDB Collection Catalog](../session-memory/2026-08-09-christopherbell-dev.md#source-docs-work-2026-08-09-christopherbell-dev-mongodb-collection-catalog-md)
- Specification: [MongoDB Collection Catalog](../session-memory/2026-08-09-christopherbell-dev.md#source-docs-specs-2026-08-09-christopherbell-dev-mongodb-collection-catalog-md)
- Implementation plan: [MongoDB Collection Catalog](../implementation-plans/2026-08-09-christopherbell-dev-mongodb-collection-catalog.md)
- Source request: reduce MongoDB operational overhead safely for the website without compromising correctness or mutating live data.

## Branch

- Repository: `azurras/christopherbell.dev`
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\mongodb-collection-catalog`
- Branch: `codex/mongodb-collection-catalog`
- Base: `2f025762e248cab5befe0fb699e0560f57006572`
- Verified feature head: `e5d900524ba42000a6c4518fdd1df9bce9f7b2e3`
- Pull request: [#1352](https://github.com/azurras/christopherbell.dev/pull/1352)
- Production merge commit: `0bcc8a9b83738df9c4adcf076e4be4443090448c`

## App / Environment

- App: packaged Spring Boot `website.jar`, Java 25, Spring Boot 4.1.
- Candidate: profile `local`, `http://127.0.0.1:8097`.
- Disposable MongoDB: MongoDB 8.3.2 at `127.0.0.1:27018`, database `christopherbell`.
- Production: website `127.0.0.1:8080`, MongoDB `127.0.0.1:27017`, public `https://www.christopherbell.dev/`.
- Deployment: SYSTEM-owned protected Windows auto-deployer; protected ProgramData ACLs remained unchanged.

## Local Run Details

Fresh final-head automated command:

```powershell
$env:GRADLE_USER_HOME = 'C:\Users\Christopher\AppData\Local\Temp\cbell-gradle-mongodb-catalog-final-root'
.\gradlew.bat :website:check --no-daemon --console=plain
```

Result: exit `0`, `BUILD SUCCESSFUL in 5m 7s`; 21 tasks, 1,679 Java tests with zero failures/errors, and production suites 83/83 under PowerShell 7 and Windows PowerShell 5.1.

Candidate package/start:

```text
.\gradlew.bat --no-daemon :website:bootJar
java.exe -jar A:\Projects\christopherbell.dev-worktrees\mongodb-collection-catalog\website\build\libs\website.jar --spring.profiles.active=local --server.port=8097 --spring.mongodb.uri=mongodb://127.0.0.1:27018/christopherbell --app.scheduling.enabled=false --app.mail.enabled=false --wfl.restaurant-import.monthly.enabled=false --command-center.enabled=false
```

Candidate PID `45400` and MongoDB PID `2824` were stopped; ports 8097/27018 were released; production ports 8080/27017 were untouched. The stopped Temp root `C:\Users\Christopher\AppData\Local\Temp\christopherbell-dev-mongo-catalog-final-runtime-e5d90052` remains because recursive cleanup was policy-blocked; no bypass was attempted.

## Test Cases

1. Catalog/source drift, malformed rows, manual/shared ownership, status vocabulary, and vehicle import-state startup enforcement.
2. PowerShell trust boundary and exact metadata-only command policy in both supported PowerShell hosts.
3. Real disposable MongoDB inventory for regular, view, capped, and time-series namespaces, BSON Long normalization, sorted indexes, and nested redaction.
4. Packaged candidate readiness, liveness, home page, and stable Mongo-backed empty-result API on 8097.
5. Required PR and post-merge CI, Dependency Review, and CodeQL.
6. Protected production rotation to the exact merge SHA and local/public health.
7. Live metadata-only inventory compared with the 51-row catalog.

## Data Sent

No application document body, mutation payload, credential, collection write, schema/index change, rename, merge, drop, compact, repair, or migration was sent.

| Method / command | Target | Input |
| --- | --- | --- |
| `GET` | `http://127.0.0.1:8097/actuator/health/liveness` | No body |
| `GET` | `http://127.0.0.1:8097/actuator/health/readiness` | No body |
| `GET` | `http://127.0.0.1:8097/` | No body |
| `GET` | `http://127.0.0.1:8097/api/location/zip/78701` | No body; empty disposable database |
| metadata script | `mongodb://127.0.0.1:27018/admin` | Fixed database and audited list/getIndexes/collStats path |
| `GET` | local production liveness, readiness, home, and public HTTPS home | No body |
| metadata script | `mongodb://127.0.0.1:27017/admin` | Exact merged generator and validator; fixed database |

## Response Received

The running candidate and production app returned explicit HTTP response status codes and bodies:

| Request | Status code | Response body / result |
| --- | ---: | --- |
| candidate liveness | 200 | `{"status":"UP"}` |
| candidate readiness | 200 | `{"status":"UP"}` |
| candidate home | 200 | `<title>CB | Home</title>` and `Drop into the Void.` |
| candidate ZIP lookup | 404 | `RESOURCE_NOT_FOUND` stable response envelope |
| production liveness | 200 | `{"status":"UP"}` |
| production readiness | 200 | `{"status":"UP"}` |
| local and public production home | 200 | HTML |

Disposable inventory returned `complete=true` for regular, view, capped, and time-series namespaces. BSON Long TTL metadata normalized exactly, indexes were sorted, sensitive scalars were `[redacted]`, view pipelines were omitted, and no document sentinel appeared. The candidate created 37 cataloged collections and 149 indexes with `actualOnly=[]`.

Mission Control reported commit `0bcc8a9b`; its server log recorded PID `62412` starting the full merge-SHA JAR at `2026-08-09T16:12:38.840-05:00`. `ChristopherBellDev`, `MongoDB`, and `Cloudflared` were Running/Automatic; port 8080 had one listener at PID `62412`; port 8081 was free.

Live inventory generated at `2026-08-09T21:14:00.599Z` returned `complete=true`, database `christopherbell`, 47 collections, 163 indexes, `actualOnly=[]`, and zero sensitive scalar leaks. Cataloged-but-uncreated names were `account_deletion_jobs`, `command_center_pending_actions`, `federation_scan_state`, and `zip_coordinate_import_state`.

## Pass / Fail

| Test case | Result | Reason |
| --- | --- | --- |
| Full repository | PASS | Gradle exit 0; 1,679 Java and both 83-test production suites green |
| Trust boundary/policy | PASS | Focused operations 69/69 in both hosts; final review clean |
| Disposable inventory | PASS | Supported namespace shapes, BSON Long, sorting, and redaction verified |
| Packaged candidate | PASS | Health/home 200, stable API 404, listeners stopped |
| PR/main CI and security | PASS | All platform, Dependency Review, and CodeQL gates succeeded |
| Production deployment | PASS | Exact merge SHA started as PID 62412; local/public health and services green |
| Live inventory | PASS | 47 collections, 163 indexes, no live-only names, no sensitive scalar leaks |

## Evidence

- Independent reviews left no open finding; both final residuals were confirmed addressed with no new breakage or scope drift.
- PR #1352 passed every required check and squash-merged as `0bcc8a9b83738df9c4adcf076e4be4443090448c`; post-merge CI Build and CodeQL passed.
- Non-elevated `prod.cmd mongo-inventory` failed closed at protected `deploy.json`. No ACL was weakened. Live evidence invoked the exact merged generator and canonical validator with the known `mongosh` executable against the same fixed production URI.
- The dirty authoritative checkout remained untouched.

## Bugs / Follow-ups

- No implementation or production defect remains.
- Four cataloged-but-uncreated names are unexercised flows, not orphan candidates or deletion authority.
- The retained stopped disposable root is approximately 212 MB; cleanup was policy-blocked.
- No collection consolidation was performed. Production already uses one native MongoDB service and one database; future physical cleanup needs separate backup-gated approval.
