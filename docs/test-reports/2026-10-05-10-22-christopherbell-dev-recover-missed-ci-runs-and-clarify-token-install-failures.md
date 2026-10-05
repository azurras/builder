# Recover Missed CI Runs and Clarify Token Install Failures: Test Report

## Story/Issue
Follow-up to #1481 after GitHub dropped the push event for `06c3718` and the user hit null-method errors in `github-token-install`. [Implementation plan](../implementation-plans/2026-10-05-10-11-christopherbell-dev-recover-missed-ci-runs-and-clarify-token-install-failures.md).

## Branch
`claude/cicd-followup-20261005` at `7fbc553`

## Pass / Fail

> [!TIP]
> **5 of 5 passed** on candidate `7fbc553`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Gate verdicts against GitHub | ✅ PASS | `a9d2058` returns SUCCESS; `06c3718`, which has no run, returns PENDING |
| 2 | Production Watch stall detection | ✅ PASS | The live run flags `06c3718` with no passing CI run past the threshold and names the recovery step |
| 3 | Non-elevated token install | ✅ PASS | `prod.cmd github-token-install` prints the elevation message and exits 1 instead of a null-method error |
| 4 | Website candidate regression | ✅ PASS | Readiness, build info, actuator protection, request IDs and ECS logs unchanged on `7fbc553` |
| 5 | Native gate | ✅ PASS | Full build: 3,208 tests, 0 failed, 112 opt-in skips; Pester follow-up suites 148/148 |

## Test Cases
1. **Gate verdicts against GitHub:** `Get-AutoDeployCiConclusion` against the live Actions API for a green commit and for the commit whose push event was dropped.
2. **Production Watch stall detection:** `Get-ProductionWatchVerdict` against https://www.christopherbell.dev and GitHub, read-only, with a 15-minute threshold so the 20-minute-old stall is visible now.
3. **Non-elevated token install:** the real `prod.cmd` entry point run from a non-elevated PowerShell with an empty token file.
4. **Website candidate regression:** the boot JAR started against a disposable MongoDB `test` database, exercising readiness, `/actuator/info`, protected actuator routes and request IDs.
5. **Native gate:** `gradlew.bat build` plus the focused Pester suites.

## App / Environment

| Setting | Value |
|---|---|
| App | christopherbell.dev production tooling (`prod.cmd`, `Production.AutoDeploy.psm1`, `.github/scripts/Test-ProductionSite.ps1`) and website boot JAR (sha256 `e73a6c2c9d0d56ecae0330bd15c8c432aea6e08a3b5c77af6e390c882dbba23e`) |
| Runtime | PowerShell 7 on Windows 11, non-elevated; Java 25 with Spring profile `test` |
| Database | Disposable `mongod` 8.3, PID 45912, `127.0.0.1:56985`, database `test`; after start, `listDatabases` returned `["admin","config","local","test"]` |
| Base URL | `http://127.0.0.1:56986` |
| External reads | GitHub REST API (read-only, the gate anonymous and the watch with the operator's `gh` token held in a process variable only), production public routes (read-only GET) |

## Local Run Details
- **Local command:** `.\prod.cmd github-token-install -GitHubTokenPath <scratch>\empty-token.txt`, plus `java -jar website\build\libs\website.jar --server.address=127.0.0.1 --server.port=56986 --logging.file.name=<scratch>\application.json.log --logging.structured.format.file=ecs --logging.level.org.springframework.web.servlet.DispatcherServlet=DEBUG`
- **Working directory:** `A:\Projects\christopherbell.dev-worktrees\cicd-followup-20261005`
- **Candidate identity:** `7fbc55389d82c09b9ce84376fa723b5bbd52a473`, clean tree. Cases 1 to 3 ran minutes before the commit on byte-identical content; the first commit attempt failed, and `git status` showed exactly the files later committed.
- **Process details:** candidate PID 45952 and mongod PID 45912, hidden.
- **Logs:** session scratchpad `runtime-evidence-followup2\` (outside the repository).
- **Cleanup:** both process trees stopped; ports confirmed free; the generated MongoDB root and Java socket directory removed; the `GITHUB_TOKEN` process variable cleared.

## Data Sent

### 1. Gate verdicts against GitHub

```text
Get-AutoDeployCiConclusion -Sha a9d20589363ed0ed139ef3c709877cca98d2d602
Get-AutoDeployCiConclusion -Sha 06c3718cdb5d8f2e727d95a8914b14776ca37749
GET https://api.github.com/repos/azurras/christopherbell.dev/actions/workflows/ci.yml/runs?head_sha=<sha>&branch=main&per_page=10
```

### 2. Production Watch stall detection

```text
Get-ProductionWatchVerdict -Repository azurras/christopherbell.dev -SiteUrl https://www.christopherbell.dev -DeployLagThresholdMinutes 15 -ProbeAttempts 1
```

### 3. Non-elevated token install

```text
.\prod.cmd github-token-install -GitHubTokenPath <scratch>\empty-token.txt   (0-byte file, non-elevated)
```

### 4. Website candidate regression

```http
GET http://127.0.0.1:56986/actuator/health/readiness
GET http://127.0.0.1:56986/actuator/info
GET http://127.0.0.1:56986/blog
X-Request-Id: verify-cicd-0001
```

### 5. Native gate

```text
gradlew.bat build
Invoke-Pester .github/scripts/tests, Production.AutoDeploy.Tests.ps1, Production.Command.Tests.ps1
```

## Response Received

### 1. Gate verdicts against GitHub

```text
gate verdict for a9d2058: SUCCESS
gate verdict for 06c3718: PENDING
```

### 2. Production Watch stall detection

```text
| GET /actuator/health/readiness | Passed | HTTP 200 |
| GET / | Passed | HTTP 200 |
| GET /blog | Passed | HTTP 200 |
| GET /actuator/info | **Failed** | ... HTTP 403 |   (pre-deploy production, expected)
| Latest Production deployment | Passed | Deployment of 7a2e011 is success. |
| Deployment lag | **Failed** | main 06c3718 has had no passing CI run for 20 minutes; auto-deploy is waiting for one. Run CI Build on main from the Actions tab. |
```

### 3. Non-elevated token install

```text
exit status: 1
Exception: github-token-install requires elevated PowerShell. Open PowerShell 7 with Run as administrator and retry.
```

### 4. Website candidate regression

```text
readiness: HTTP/1.1 200 OK {"status":"UP"}
info: HTTP/1.1 200 OK {"build":{"artifact":"website","name":"website","time":"2026-10-05T15:21:47.107Z","version":"0.0.0-dev.7fbc55389d82c09b9ce84376fa723b5bbd52a473","group":"christopherbell.dev"}}
/actuator/env and /actuator/health: HTTP/1.1 403 Forbidden
GET /blog: HTTP/1.1 200 OK, X-Request-Id: verify-cicd-0001
Log excerpt: 2026-10-05T10:22:00.093-05:00 DEBUG 45952 --- [.1-56986-exec-1] [verify-cicd-0001] o.s.web.servlet.DispatcherServlet : GET "/blog", parameters={}
```

### 5. Native gate

```text
BUILD SUCCESSFUL in 5m 10s; 3,208 tests, 3,096 passed, 0 failed, 112 skipped
Pester: Passed=148 Failed=0
```

## Evidence
- Red-before-green: 16 new or updated Pester tests failed before the implementation (event filter, stall, elevation and empty-file cases) and passed after.
- GitHub `events` and `activity` APIs show no push for `06c3718`, and its workflow-run list is empty, while `refs/heads/main` is `06c3718`.
- Live checks ran at about 10:16 CDT; the candidate run at 10:22 CDT.

## Bugs / Follow-ups
- Production still serves `a9d2058` until a CI run exists for `main`. Merging this PR creates a new `main` commit; if its push event is also dropped, run CI Build on `main` by hand.
- The user installed the deployment token from `06c3718` tooling before this fix; this change only improves the error messages.

## Document Status
complete

## Project
christopherbell-dev
