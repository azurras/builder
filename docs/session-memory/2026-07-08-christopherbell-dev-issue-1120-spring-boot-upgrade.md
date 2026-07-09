# 2026-07-08 - christopherbell-dev-issue-1120-spring-boot-upgrade

## 22:51 - christopherbell dev issue 1120 spring boot upgrade

### Request

User asked Codex to take care of GitHub issue https://github.com/azurras/christopherbell.dev/issues/1120 from the Builder hub. The issue requested upgrading `azurras/christopherbell.dev` to the latest Spring Boot version.

### Project Context

Builder hub instructions required the story/issue delivery loop with durable artifacts under `docs/`, local app testing, a test report, closure, session memory, hub index updates, validation, and committing/pushing Builder main. The primary `C:\Users\Christopher\Developer\christopherbell.dev` checkout was dirty on another branch, so work was done in isolated worktree `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-1120-spring-boot-4-1` on branch `codex/issue-1120-spring-boot-4-1`.

### Work Completed

Created Builder artifacts:

- Work record: `docs/work/2026-07-08-christopherbell-dev-issue-1120-spring-boot-upgrade.md`
- Implementation plan: `docs/implementation-plans/2026-07-08-issue-1120-spring-boot-4-1-upgrade.md`
- Test report: `docs/test-reports/2026-07-08-issue-1120-spring-boot-4-1-upgrade.md`
- Closure record: `docs/work-closures/2026-07-08-christopherbell-dev-issue-1120-spring-boot-upgrade.md`

Spoke changes were implemented, committed, pushed, reviewed by CI, and merged through PR https://github.com/azurras/christopherbell.dev/pull/1121. Issue https://github.com/azurras/christopherbell.dev/issues/1120 was closed by the merge.

Spoke implementation details:

- Upgraded Spring Boot Gradle plugin and `cbell-lib` BOM from `3.4.4` to `4.1.0`.
- Upgraded `org.springdoc:springdoc-openapi-starter-webmvc-ui` to `3.0.3` after resolving a rebase conflict against current main's `2.8.17`.
- Migrated Jackson 3 package imports to `tools.jackson`, changed `cbell-lib` from an explicit Jackson 2 dependency to managed `tools.jackson.core:jackson-databind`, removed obsolete `findAndRegisterModules()` usage in `TestUtil`, and replaced `JsonNode.elements()` traversal with `values().iterator()`.
- Migrated Spring Security public route matching from removed `AntPathRequestMatcher` to `PathPatternRequestMatcher`.
- Anchored the custom JWT filter before Spring Security 7 `AuthorizationFilter`.
- Added Boot 4 MVC test dependency `spring-boot-starter-webmvc-test` and updated MVC test annotation imports to `org.springframework.boot.webmvc.test.autoconfigure`.
- Added MVC-slice test security helpers in `website/src/test/java/dev/christopherbell/configuration/security/`. The first version disabled CSRF and CodeQL flagged it, so the helper was revised to keep CSRF enabled while relying on existing `csrf()` request processors.

Final spoke commit before merge: `4e66f305bbd3e42d5e6a1b9fe6d43edd12b6de83`. Merge commit: `d5ac7aba5abf3a2c8e2ab9bd792273207eb6cda3`.

### Decisions

Spring Boot `4.1.0` was used because official/current release lookup showed it as the latest release on July 9, 2026. Springdoc was moved to 3.0.3 because the 2.x line targets the older Spring Boot generation. The test helper exposes production public matchers via `SecurityConfig.publicMatchersList()` and `publicMatchers()` to avoid duplicating route rules in tests.

When GitHub reported a merge conflict after the first PR push, the branch was rebased onto current `origin/main` and the springdoc conflict was resolved to keep the Boot 4-compatible `3.0.3` instead of main's `2.8.17`.

### Validation

Baseline before edits: `:website:test` passed in the isolated worktree.

Final local validation after rebase and CodeQL fix:

```powershell
$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test
```

Result: `BUILD SUCCESSFUL`, 423 tests passed.

Local app smoke:

```powershell
$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; $env:SERVER_PORT='8082'; .\gradlew.bat --no-daemon :website:bootRun --args='--spring.profiles.active=local --server.port=8082'
```

Spring Boot banner reported `v4.1.0`; `GET http://localhost:8082/` returned `200`, title `CB | Home`, content length `3912`. `GET /actuator/health` returned `403` because anonymous actuator access is protected. The bootRun process was stopped after verification.

GitHub checks on PR 1121 passed before merge: CodeQL actions/java-kotlin/javascript-typescript plus aggregate CodeQL, and CI Build Java 25 on macOS, Ubuntu, and Windows.

### Current State

Issue 1120 is closed. PR 1121 is merged. Remote feature branch was deleted by `gh pr merge --delete-branch`; the local worktree/branch still exists for inspection. No local app server remains running.

### Follow-ups

Local bootRun logged an existing external Overpass `504` during startup catch-up import; it did not block startup or serving `GET /` and was not caused by this upgrade. No remaining follow-up is required for issue 1120.
