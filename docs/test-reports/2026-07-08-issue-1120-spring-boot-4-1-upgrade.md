## Document Status

complete

## Story/Issue

GitHub issue: https://github.com/azurras/christopherbell.dev/issues/1120

Objective tested: Spring Boot upgrade for `christopherbell.dev` from 3.4.4 to 4.1.0 with Spring Security 7, Jackson 3, springdoc 3.0.3, and Boot 4 MVC test compatibility changes.

## Branch

Spoke repository: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-1120-spring-boot-4-1`

Branch: `codex/issue-1120-spring-boot-4-1`

Base: `origin/main` at `ab42e4cc`

## App / Environment

Windows local worktree using Java 25.0.3 and Gradle wrapper.

Local app runtime: `./gradlew.bat --no-daemon :website:bootRun --args='--spring.profiles.active=local --server.port=8082'`

Base URL under test: `http://localhost:8082`

Spring Boot startup banner reported `v4.1.0`; Tomcat started on port 8082.

## Local Run Details

Automated regression command:

```powershell
$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test
```

Local runtime command:

```powershell
$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; $env:SERVER_PORT='8082'; .\gradlew.bat --no-daemon :website:bootRun --args='--spring.profiles.active=local --server.port=8082'
```

The app stayed running after startup. Startup attempted the existing OpenStreetMap monthly catch-up and logged an external Overpass `504`, but this did not prevent the app from serving requests.

## Test Cases

1. Full automated website test suite after Spring Boot 4.1.0 upgrade.
2. Local bootRun startup on alternate port 8082 using the `local` profile.
3. Anonymous request to protected actuator health endpoint to confirm current security behavior.
4. Anonymous request to public home route for runtime smoke verification.

## Data Sent

Automated tests: Gradle executed `:website:test` with the upgrade branch code and isolated `GRADLE_USER_HOME`.

Runtime request 1:

```http
GET /actuator/health HTTP/1.1
Host: localhost:8082
```

Runtime request 2:

```http
GET / HTTP/1.1
Host: localhost:8082
```

## Response Received

Automated tests: Gradle reported `BUILD SUCCESSFUL` for `:website:test` with 423 tests passing.

Runtime response 1: `status code 403` for `GET http://localhost:8082/actuator/health`, because actuator health is protected by the app's current security rules for anonymous requests.

Runtime response 2: `status code 200`; response title extracted from the HTML was `CB | Home`, with content length 3912.

## Pass / Fail

Pass.

The Spring Boot 4.1.0 upgrade passed the full automated suite and the local app served a public route successfully on port 8082. The actuator health endpoint returning 403 is recorded as expected current security behavior, not a regression from this upgrade.

## Evidence

- `:website:test`: `BUILD SUCCESSFUL` after 423 tests.
- Local startup log: `:: Spring Boot :: (v4.1.0)` and `Tomcat started on port 8082 (http)`.
- Protected endpoint smoke: `GET http://localhost:8082/actuator/health` returned `403`.
- Public endpoint smoke: `GET http://localhost:8082/` returned `200`, title `CB | Home`, content length `3912`.
- Local bootRun session was stopped after verification.

## Bugs / Follow-ups

- Existing startup catch-up import can log an external Overpass `504`; it did not block startup or request serving and is not caused by this upgrade.
- No upgrade-blocking bugs found in local verification.
