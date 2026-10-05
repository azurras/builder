# Harden CI/CD Robustness and Observability: Test Report

## Story/Issue
User request on 2026-10-05 to fix all ten CI/CD robustness and observability findings for christopherbell.dev. [Implementation plan](../implementation-plans/2026-10-05-08-52-christopherbell-dev-harden-ci-cd-robustness-and-observability.md).

## Branch
`claude/cicd-hardening-20261005` at `b5f7f5c`

## Pass / Fail

> [!TIP]
> **9 of 9 passed** on candidate `b5f7f5c`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Isolated startup and readiness | ✅ PASS | Candidate reached readiness against disposable MongoDB database `test` only |
| 2 | Public build info | ✅ PASS | Anonymous `/actuator/info` returns 200 with `build.version` `0.0.0-dev.b5f7f5c…` and no other sections |
| 3 | Protected actuator routes | ✅ PASS | `/actuator/env` and `/actuator/health` stay 403 anonymously |
| 4 | Generated request ID | ✅ PASS | `GET /` without a header returns a UUID `X-Request-Id` |
| 5 | Echoed request ID | ✅ PASS | A well-formed inbound `X-Request-Id` is echoed on `/blog` and on a rejected API request |
| 6 | Unsafe request ID replaced | ✅ PASS | `bad id <script>` is replaced by a UUID |
| 7 | ECS JSON file log with request IDs | ✅ PASS | All 44 file lines parse as ECS 8.11 JSON; request lines carry `requestId` |
| 8 | Console correlation | ✅ PASS | Console lines show `[verify-cicd-0001]` through `logging.pattern.correlation` |
| 9 | Production Watch read-only verdict | ✅ PASS | Script against live production probes routes and GitHub correctly; only `/actuator/info` fails, as expected before this deploys |

## Test Cases
1. **Isolated startup and readiness:** boot JAR started with profile `test` against a fresh loopback MongoDB, polled `GET /actuator/health/readiness`.
2. **Public build info:** anonymous `GET /actuator/info`.
3. **Protected actuator routes:** anonymous `GET /actuator/env` and `GET /actuator/health`.
4. **Generated request ID:** `GET /` without `X-Request-Id`.
5. **Echoed request ID:** `GET /blog` and `GET /api/does-not-exist` with well-formed IDs.
6. **Unsafe request ID replaced:** `GET /blog` with `X-Request-Id: bad id <script>`.
7. **ECS JSON file log with request IDs:** the production file-logging settings applied at a scratch path, then the file parsed.
8. **Console correlation:** captured candidate stdout for the request lines.
9. **Production Watch read-only verdict:** `Get-ProductionWatchVerdict` and `Format-WatchReport` run against https://www.christopherbell.dev and the GitHub API, without the issue-writing step.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev website boot JAR `website/build/libs/website.jar`, sha256 `e59290f04bdb092d745f1b644ce2b8aa115b9b5733fe19eaf972bbd811c3ff09` |
| Runtime | Java 25 (Temurin 25.0.3), Spring profile `test`, Windows 11 |
| Database | Disposable `mongod` 8.3, PID 48660, `127.0.0.1:57295`, fresh data directory under `%TEMP%\christopherbell-test-mongo-93fc1f3b…`; `SPRING_MONGODB_URI=mongodb://127.0.0.1:57295/test` |
| Isolation proof | Before start: only `SPRING_PROFILES_ACTIVE=test` and that URI were set. After start: the driver log shows `hosts=[127.0.0.1:57295]`, and `listDatabases` returned `["admin","config","local","test"]` |
| Base URL | `http://127.0.0.1:57296` (OS-selected free port; not 8080/8081/27017) |
| Logging overrides | `--logging.file.name=<scratch>\application.json.log --logging.structured.format.file=ecs --logging.logback.rollingpolicy.max-file-size=10MB --logging.level.org.springframework.web.servlet.DispatcherServlet=DEBUG` (mirrors `application-prod.yml`; DEBUG makes each request write a line) |
| Secrets | Random 32-byte `APP_JWT_SECRET` generated per run, not recorded |

## Local Run Details
- **Local command:** `java -jar website\build\libs\website.jar --server.address=127.0.0.1 --server.port=57296 --logging.file.name=<scratch>\application.json.log --logging.structured.format.file=ecs --logging.logback.rollingpolicy.max-file-size=10MB --logging.level.org.springframework.web.servlet.DispatcherServlet=DEBUG`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\cicd-hardening-20261005`
- **Candidate identity:** commit `b5f7f5c072f1f3414220d551b86e6a82d2d581cb`, clean tree; JAR rebuilt with `gradlew.bat :website:bootJar` after the commit.
- **Process details:** candidate PID 47192 and mongod PID 48660, both started hidden with `Start-Process -PassThru`.
- **Logs:** session scratchpad `runtime-evidence\candidate.out.log`, `candidate.err.log`, `application.json.log`, `evidence.json` (outside the repository).
- **Cleanup:** stopped both process trees with `taskkill /T /F`; confirmed neither port still listens; removed the generated MongoDB root and Java socket directory after validating their names and parents; cleared the four process environment variables.
- **Native checks:** At `b5f7f5c`, `gradlew.bat --write-verification-metadata sha256 --continue build` ran the full build, which passed 3,198 tests: 0 failed and 112 opt-in skips, including the 121-test `automationPester` run. It left `gradle/verification-metadata.xml` unchanged, so the Dependabot regeneration command is a no-op on current dependencies. Running every production Pester suite directly passed 851 tests with 28 skips.

## Data Sent

### 1. Isolated startup and readiness

```http
GET http://127.0.0.1:57296/actuator/health/readiness
```

### 2. Public build info

```http
GET http://127.0.0.1:57296/actuator/info
```

### 3. Protected actuator routes

```http
GET http://127.0.0.1:57296/actuator/env
GET http://127.0.0.1:57296/actuator/health
```

### 4. Generated request ID

```http
GET http://127.0.0.1:57296/
```

### 5. Echoed request ID

```http
GET http://127.0.0.1:57296/blog
X-Request-Id: verify-cicd-0001

GET http://127.0.0.1:57296/api/does-not-exist
X-Request-Id: verify-cicd-0002
```

### 6. Unsafe request ID replaced

```http
GET http://127.0.0.1:57296/blog
X-Request-Id: bad id <script>
```

### 7. ECS JSON file log with request IDs

```text
Get-Content <scratch>\application.json.log | ConvertFrom-Json   # every line
Select lines matching 'verify-cicd-000' and the generated home-page ID
```

### 8. Console correlation

Log excerpt from candidate stdout:

```text
Select-String candidate.out.log -Pattern '\[verify-cicd-000'
```

### 9. Production Watch read-only verdict

```powershell
. ./.github/scripts/Test-ProductionSite.ps1
Get-ProductionWatchVerdict -Repository azurras/christopherbell.dev -SiteUrl https://www.christopherbell.dev `
  -Token <gh auth token> -DeployLagThresholdMinutes 45 -ProbeAttempts 1 -ProbeRetryDelaySeconds 0 | Format-WatchReport
```

## Response Received

### 1. Isolated startup and readiness

```text
Started Application in about 5 seconds
HTTP/1.1 200 OK
{"status":"UP"}
```

### 2. Public build info

HTTP/1.1 200 OK response body:

```json
{"build":{"artifact":"website","name":"website","time":"2026-10-05T14:38:45.626Z","version":"0.0.0-dev.b5f7f5c072f1f3414220d551b86e6a82d2d581cb","group":"christopherbell.dev"}}
```

### 3. Protected actuator routes

```text
GET /actuator/env (anonymous): HTTP/1.1 403 Forbidden
GET /actuator/health (anonymous): HTTP/1.1 403 Forbidden
```

### 4. Generated request ID

```text
HTTP/1.1 200 OK, X-Request-Id: a4842a60-9ea7-4b08-a710-5d5225843395
```

### 5. Echoed request ID

```text
GET /blog: HTTP/1.1 200 OK, X-Request-Id: verify-cicd-0001
GET /api/does-not-exist: HTTP/1.1 403 Forbidden, X-Request-Id: verify-cicd-0002
```

### 6. Unsafe request ID replaced

```text
HTTP/1.1 200 OK, X-Request-Id: 0675a23a-49d8-43bf-b531-481f11dbb991
```

### 7. ECS JSON file log with request IDs

Log excerpt from application.json.log:

```json
{"@timestamp":"2026-10-05T14:38:58.801684700Z","log":{"level":"DEBUG","logger":"org.springframework.web.servlet.DispatcherServlet"},"process":{"pid":47192,"thread":{"name":"http-nio-127.0.0.1-57296-exec-1"}},"service":{"node":{}},"message":"GET \"/blog\", parameters={}","requestId":"verify-cicd-0001","tags":["COMMONS-LOGGING"],"ecs":{"version":"8.11"}}
```

```text
44 lines, all parsed as JSON; ecs.version=8.11
2 lines carry verify-cicd-000x; 2 lines carry the generated home-page id
```

### 8. Console correlation

Log excerpt from candidate stdout:

```text
2026-10-05T09:38:58.801-05:00 DEBUG 47192 --- [.1-57296-exec-1] [verify-cicd-0001] o.s.web.servlet.DispatcherServlet        : GET "/blog", parameters={}
```

### 9. Production Watch read-only verdict

```text
| GET /actuator/health/readiness | Passed | HTTP 200 |
| GET / | Passed | HTTP 200 |
| GET /blog | Passed | HTTP 200 |
| GET /actuator/info | **Failed** | GET https://www.christopherbell.dev/actuator/info failed after 1 attempts: HTTP 403 |
| Latest Production deployment | Passed | Deployment of 7a2e011 is success. |
| Deployment lag | Passed | main a9d2058 passed CI 20 minutes ago; an unknown commit is live while it deploys. |
```

## Evidence
- Runtime run at 2026-10-05 09:38 CDT on `b5f7f5c`; evidence captured in `runtime-evidence\evidence.json` and the candidate logs.
- Earlier runs on `64cd652` and `1a00621` found two defects that this candidate fixes; see Bugs / Follow-ups.
- Production Watch run at 2026-10-05 about 09:15 CDT. The first run exposed a timestamp defect, fixed and covered by a regression, and the rerun shows correct lag.
- A live `Invoke-WebRequest` to production readiness returned `Content` as `System.Byte[]` for `application/vnd.spring-boot.actuator.v3+json`.

## Bugs / Follow-ups
- Found and fixed during verification: `/actuator/info` reported `build.version: "unspecified"` on `64cd652` and `1a00621`, fixed in `b5f7f5c`. Production Watch would have read actuator JSON bytes as text, fixed in `1a00621`. Production Watch lag was computed from a zone-stripped timestamp, fixed before `64cd652`.
- Superseded candidates: `64cd652` (readiness probe parse failure in the verification harness, then the version gap) and `1a00621` (version gap).
- `/actuator/info` returns 403 in production until this change deploys, so a scheduled Production Watch run between merge and deploy can open one alert issue that the next healthy run closes.
- GitHub deployment records (AC-6) cannot be exercised live until the user installs a token; covered by Pester tests only.

## Document Status
complete

## Project
christopherbell-dev
