# Issue 1142 Java 25 Spring Boot 4.1 Docs Test Report

## Document Status

complete

## Story/Issue

- GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1142
- Pull request: https://github.com/azurras/christopherbell.dev/pull/1183
- Trusted guidance: issue body authored by `azurras`; no issue comments or attachments were present.

## Branch

- Spoke branch under test: `agent/1142-docs-java25-boot41`
- Spoke commit under test: `bc2f6571` (`Update docs for Java 25 and Spring Boot 4.1`)
- PR merge commit after CI: `123785da4855971ced0600338ff4d7c766970542`

## App / Environment

- App: `christopherbell.dev` Spring Boot website.
- Local worktree: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1142-docs-java25-boot41`
- Java: Eclipse Adoptium JDK 25.0.3 from local app logs.
- Gradle user home: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142`
- Spring profile: default `local`.
- MongoDB: local `localhost:27017`; app logs show the Mongo monitor connected successfully.
- Base URL under test: `http://localhost:8083`

## Local Run Details

- Documentation stale-reference check:
  - `rg -n "Spring Boot 3|Spring Boot 3.4|Java 21|CI builds with Java 21" README.md website\README.md AGENTS.md .github\copilot-instructions.md`
  - Result: no stale references; command returned no matches and the wrapper printed `NO_STALE_REFS`.
- Documentation current-reference check:
  - `rg -n "Spring Boot 4\.1|Java 25" README.md website\README.md AGENTS.md .github\copilot-instructions.md`
  - Result: current Java 25 and Spring Boot 4.1 references found in all issue-scoped docs.
- Automated regression command:
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142'; .\gradlew.bat --no-daemon :website:test`
- Automated regression result: `BUILD SUCCESSFUL in 18s`; 8 Gradle tasks, 3 executed and 5 up-to-date.
- Runtime start command:
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142'; $env:SERVER_PORT='8083'; .\gradlew.bat --no-daemon :website:bootRun`
- Runtime process: Java PID `31024`, Tomcat listening on port `8083`.
- Runtime logs: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1142-docs-java25-boot41\.codex-run\bootrun-1142.out.log` and `.codex-run\bootrun-1142.err.log`.
- App started at `2026-07-09T14:57:41.201-05:00` and was stopped after the smoke request with `Stop-Process -Id 31024 -Force`.
- The Gradle `bootRun` task reported a non-zero exit only after the test process was intentionally stopped.

## Test Cases

1. Documentation stale-reference check: verify issue-scoped docs no longer mention Java 21 or Spring Boot 3/3.4 baselines.
2. Documentation current-reference check: verify issue-scoped docs mention Java 25 and Spring Boot 4.1 where appropriate.
3. Automated regression: run `:website:test` to confirm unchanged application behavior remains healthy.
4. Local runtime smoke: start the app on port `8083` and request the public home page.
5. PR CI: verify GitHub checks pass before merge.

## Data Sent

- Runtime HTTP request:
  - Method: `GET`
  - URL: `http://localhost:8083/`
  - Command: `curl.exe -i http://localhost:8083/`
- No request body, form data, or authentication headers were sent.
- CI data reviewed:
  - PR: `https://github.com/azurras/christopherbell.dev/pull/1183`
  - Head branch: `agent/1142-docs-java25-boot41`

## Response Received

- Local runtime response excerpt:

```http
HTTP/1.1 200
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Type: text/html;charset=UTF-8
Date: Thu, 09 Jul 2026 19:57:51 GMT
```

- Response body evidence:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
```

- Title check: the response body matched `<title>CB | Home</title>`.
- Runtime log evidence:
  - `Spring Boot :: (v4.1.0)`
  - `Starting Application using Java 25.0.3`
  - `Tomcat started on port 8083 (http) with context path '/'`
  - `Monitor thread successfully connected to server` for `localhost:27017`
- GitHub CI response:
  - `build (25, ubuntu-latest)`: success
  - `build (25, macos-latest)`: success
  - `build (25, windows-latest)`: success
  - `Analyze (actions)`: success
  - `Analyze (java-kotlin)`: success
  - `Analyze (javascript-typescript)`: success
  - `CodeQL`: success

## Pass / Fail

- Documentation stale-reference check: pass. No issue-scoped stale references remained.
- Documentation current-reference check: pass. Java 25 and Spring Boot 4.1 are present in the issue-scoped docs.
- Automated regression: pass. `:website:test` completed successfully.
- Local runtime smoke: pass. `GET /` returned `HTTP/1.1 200` and the expected home page title.
- PR CI: pass. All GitHub checks completed successfully before merge.

## Evidence

- Spoke commit: `bc2f6571`.
- PR: https://github.com/azurras/christopherbell.dev/pull/1183.
- Merge commit: `123785da4855971ced0600338ff4d7c766970542`.
- Issue closure: https://github.com/azurras/christopherbell.dev/issues/1142 closed at `2026-07-09T20:02:02Z`.
- Local app request command: `curl.exe -i http://localhost:8083/`.
- Local response status: `HTTP/1.1 200`.
- Local response title match: `True` for `<title>CB | Home</title>`.
- CI checks: seven successful checks on PR #1183.

## Bugs / Follow-ups

None found. The worktree remains available locally for inspection; the remote feature branch was deleted by the merge command.
