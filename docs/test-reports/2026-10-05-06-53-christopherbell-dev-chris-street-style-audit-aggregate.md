# Chris Street Style Audit Aggregate: Test Report

## Story/Issue
Final combined verification for the repository-wide Chris Street Style audit and the isolated test database bootstrap that removed the local runtime blocker. See the [living implementation plan](../implementation-plans/2026-10-04-christopherbell-dev-chris-street-style-audit.md), [bootstrap plan](../implementation-plans/2026-10-05-07-17-christopherbell-dev-bootstrap-isolated-empty-test-database.md), and [PR #1480](https://github.com/azurras/christopherbell.dev/pull/1480). PR #1477 was not used.

## Branch
`codex/chris-street-style-audit-20261005` at `dd206c0ef2498e0d400eccce519990e8050bd021`

## Pass / Fail

> [!TIP]
> **3 of 3 verification cases passed** on candidate `dd206c0e`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Full native checks and packaged build | ✅ PASS | `:website:check :cbell-lib:check :website:bootJar` succeeded; JavaScript, PowerShell and worker checks passed; the candidate JAR was built. |
| 2 | Fresh isolated MongoDB test-profile application | ✅ PASS | Migrations 001–015 applied without a cutover ledger; readiness and `/` returned 200; domain namespaces remained empty. |
| 3 | Merged pull request CI | ✅ PASS | Windows build, all Analyze jobs, CodeQL, and Dependency Review passed; PR #1480 merged with the tested head SHA. |

## Test Cases
1. **Full native checks and packaged build:** Run the website and shared-library native gates, including Java, JavaScript, PowerShell, and worker checks, and package the website JAR.
2. **Fresh isolated MongoDB test-profile application:** Start a disposable loopback MongoDB instance and the committed candidate, then exercise readiness and the home page and inspect migration/domain state read-only.
3. **Merged pull request CI:** Confirm the checks on the exact tested PR head and read back merge state and merge commit.

## App / Environment

| Setting | Value |
|---|---|
| App | `christopherbell.dev` Spring Boot website |
| Candidate | `dd206c0ef2498e0d400eccce519990e8050bd021` |
| Runtime | Java 25; Gradle Wrapper 9.6.1; Windows PowerShell |
| Profile | `test` |
| Database | Disposable MongoDB database `test`, bound to `127.0.0.1:49354`; app on `127.0.0.1:49355` |
| Artifact | `website/build/libs/website.jar`; SHA-256 `1EB9BDB48E33B2AD705318D3C146F3520731E2ACF422CA7869A9C4E20B325799` |

## Local Run Details
- **Local command:** `.\gradlew.bat :website:check :cbell-lib:check :website:bootJar --no-daemon`
- **Application command:** `java -jar website\build\libs\website.jar --server.address=127.0.0.1 --server.port=49355`
- **Application environment:** `SPRING_PROFILES_ACTIVE=test`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:49354/test`; transient random `APP_JWT_SECRET` (value omitted); generated short `jdk.net.unixdomain.tmpdir` path.
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\chris-street-style-audit-20261005`.
- **Candidate identity:** committed HEAD `dd206c0ef2498e0d400eccce519990e8050bd021` on `codex/chris-street-style-audit-20261005`.
- **Process details:** MongoDB PID 3872 on port 49354 and website PID 22520 on port 49355; each bound to loopback only.
- **Logs:** `C:\Users\Christopher\AppData\Local\Temp\christopherbell-test-mongo-de81b8651c314dcfbf423aa8d0c2bbf2\`.
- **Cleanup:** Both processes stopped; PIDs and ports 49354/49355 confirmed gone/closed. Production MongoDB on port 27017 remained untouched. Generated temporary directories remain because recursive cleanup was rejected by command safety review. The remote and local task branches were deleted; `git worktree remove` unregistered the worktree but Windows returned `Filename too long`, leaving the residual `website` directory in the task worktree folder.

## Data Sent

### 1. Full native checks and packaged build

```text
.\gradlew.bat :website:check :cbell-lib:check :website:bootJar --no-daemon
```

### 2. Fresh isolated MongoDB test-profile application

```http
GET http://127.0.0.1:49355/actuator/health/readiness
GET http://127.0.0.1:49355/
```

### 3. Merged pull request CI

```text
gh pr view 1480 --repo azurras/christopherbell.dev --json state,headRefOid,mergeCommit
```

## Response Received

### 1. Full native checks and packaged build

```text
BUILD SUCCESSFUL in 4m 11s
24 actionable tasks
Focused migration tests: 19 passed
PowerShell suites: 203 passed, 0 failed, 1 existing skip; worker suite: 76 passed, 0 failed, 0 skipped
Artifact: website/build/libs/website.jar
```

### 2. Fresh isolated MongoDB test-profile application

```http
HTTP/1.1 200 OK
{"status":"UP"}

HTTP/1.1 200 OK
Content-Length: 3981
<title>CB | Home</title>

MongoDB test database: migration versions 001-015 APPLIED; 15 migration rows; one released lease in application_runtime; application_leases count 0; all source and target domain collections empty; no cutover ledger.
```

### 3. Merged pull request CI

```text
PR #1480: MERGED
Head: dd206c0ef2498e0d400eccce519990e8050bd021
Merge commit: a9d20589363ed0ed139ef3c709877cca98d2d602
Windows build: passed
Analyze (actions): passed
Analyze (java-kotlin): passed
Analyze (javascript-typescript): passed
CodeQL: passed
Dependency Review: passed
```

## Evidence
- Full native verification completed on the named committed candidate before PR creation; local runtime proof and all observed responses are recorded in the [bootstrap runtime report](2026-10-05-08-15-christopherbell-dev-bootstrap-empty-isolated-website-test-databases.md).
- PR readback reports `MERGED`, exact head `dd206c0ef2498e0d400eccce519990e8050bd021`, and merge commit `a9d20589363ed0ed139ef3c709877cca98d2d602`.
- Candidate changes include 23 focused style corrections and repository-local style guidance. Each correction has its own linked Builder plan and candidate report in the plan's implementation log.
- Candidate `dc928832d39c1e019483c9aca668e63ba333463d` from the former blocked report is superseded: the isolated MongoDB test bootstrap and JDK 25 socket-temp instructions were added and then verified on `dd206c0e`.

## Bugs / Follow-ups
No application defect remains from this audit. Production deployment was not requested or performed. Runtime processes and ports are closed. Generated scratch directories remain because recursive removal was rejected by command safety review. Worktree registration and branches are removed, but a residual worktree `website` directory remains after Windows returned `Filename too long`; no alternate recursive deletion method was used. See the bootstrap runtime report for the runtime scratch paths.

## Document Status
complete

## Project
christopherbell-dev
