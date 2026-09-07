# christopherbell.dev Modular Monolith Foundation Test Report

## Document Status

complete

## Story/Issue

- Work record: [christopherbell.dev Modular Monolith Foundation](../session-memory/christopherbell-dev.md#source-docs-work-2026-08-04-christopherbell-dev-modular-monolith-foundation-md)
- Implementation plan: [Modular Monolith Foundation](../implementation-plans/2026-08-04-christopherbell-dev-modular-monolith-foundation.md)
- Scope: foundation delivery for test-only Spring Modulith discovery, normalized ArchUnit dependency enforcement, a frozen legacy baseline, generated architecture documentation, and contributor workflow.

## Branch

- Repository: `azurras/christopherbell.dev`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\modular-monolith-foundation`
- Branch: `codex/modular-monolith-foundation`
- Base: `9c587103cb7f7df2ab52ed3e232f1ca67660fd6e`
- Verified head: `f184f14125da232abf97ff0763505c23160cb1c9`

## App / Environment

- App: packaged Spring Boot `website.jar`
- Profiles: `local,deploy-smoke`
- Candidate port/base URL: `8097`, `http://localhost:8097`
- Production listener: port `8080`, PID `12896`, unchanged before and after both controller-owned candidate runs
- MongoDB: local listener; disposable database `christopherbell_modular_monolith_final_json_20260808180659`
- Private Gradle home: `%TEMP%\christopherbell-dev-modular-monolith-foundation-final-gradle`

## Local Run Details

Fresh automated verification command:

```powershell
$env:GRADLE_USER_HOME = Join-Path $env:TEMP 'christopherbell-dev-modular-monolith-foundation-final-gradle'
.\gradlew.bat :website:check --stacktrace --console=plain
```

Result: exit `0`, `BUILD SUCCESSFUL in 6m 21s`; 21 actionable tasks (13 executed, 8 up-to-date). Java, JavaScript, Pester, packaging, sensor, static-asset serialization, and production-deployment-context gates completed.

Fresh candidate start command:

```text
java.exe -jar A:\Projects\christopherbell.dev-worktrees\modular-monolith-foundation\website\build\libs\website.jar --spring.profiles.active=local,deploy-smoke --server.port=8097 --spring.mongodb.database=christopherbell_modular_monolith_final_json_20260808180659
```

- Candidate PID: `16852`
- Standard output: `website/build/modular-monolith-final-json-20260808180659.stdout.log`
- Standard error: `website/build/modular-monolith-final-json-20260808180659.stderr.log`
- The candidate was stopped after requests completed. Post-test port 8097 listener count was zero.
- `mongosh` dropped only the disposable database and a readback returned `false` for its existence.

## Test Cases

1. Full repository verification on the final branch head.
2. Packaged artifact inventory and test-only Modulith boundary.
3. Candidate readiness on port 8097.
4. Candidate liveness on port 8097.
5. Candidate home-page rendering on port 8097.
6. Candidate process, listener, database, and production-listener cleanup/isolation.

## Data Sent

No request body, form data, authentication credential, or mutation payload was sent.

| Method | URL | Relevant input |
| --- | --- | --- |
| `GET` | `http://localhost:8097/actuator/health/readiness` | No body; candidate profiles `local,deploy-smoke`; disposable MongoDB database |
| `GET` | `http://localhost:8097/actuator/health/liveness` | No body |
| `GET` | `http://localhost:8097/` | No body |

## Response Received

The readiness HTTP response had status code 200 and response body `{"status":"UP"}`. The liveness HTTP response had status code 200 and response body `{"status":"UP"}`. The home HTTP response had status code 200 and rendered the HTML title `CB | Home`.

| Request | Status | Response evidence |
| --- | ---: | --- |
| `GET /actuator/health/readiness` | 200 | `{"status":"UP"}` |
| `GET /actuator/health/liveness` | 200 | `{"status":"UP"}` |
| `GET /` | 200 | HTML title `CB | Home` |

Packaged artifact evidence:

- Exactly one JAR: `website/build/libs/website.jar`.
- Size after the fresh full check: `128,471,497` bytes.
- JAR entry count: `1,531`.
- Case-insensitive `spring-modulith` JAR-entry matches: `0`.
- Architecture baseline diff: empty.
- Generated, ignored documentation: `website/build/spring-modulith-docs/components.puml`.

## Pass / Fail

| Test case | Result | Reason |
| --- | --- | --- |
| Full `:website:check` | PASS | Gradle exit 0 and `BUILD SUCCESSFUL` |
| One-JAR/test-only boundary | PASS | One JAR, 1,531 entries, zero Modulith runtime entries |
| Readiness | PASS | HTTP 200 with exact body `{"status":"UP"}` |
| Liveness | PASS | HTTP 200 with exact body `{"status":"UP"}` |
| Home page | PASS | HTTP 200 with title `CB | Home` |
| Cleanup/isolation | PASS | PID stopped, port 8097 free, database absent, production remained PID 12896 |

## Evidence

- Controller-owned final verification ran on 2026-08-08 against commit `f184f14125da232abf97ff0763505c23160cb1c9`.
- `git status --short --branch` was clean except for the expected branch-ahead relationship.
- `git diff --check` returned exit 0.
- `git diff --exit-code -- website/src/test/resources/architecture-baseline` returned exit 0.
- MongoDB cleanup returned `{"ok":1,"dropped":"christopherbell_modular_monolith_final_json_20260808180659"}` and existence readback `false`.
- Production port 8080 reported PID `12896` before and after the candidate.

## Bugs / Follow-ups

- No local defect was found.
- Existing Gradle 9.6 deprecation warnings at unrelated `website/build.gradle.kts:692` remain outside this foundation.
- PR CI, Dependency Review, CodeQL, merge, protected deployment, and production verification remain required integration/delivery gates.
