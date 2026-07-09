# christopherbell.dev Issue 1120 Spring Boot 4.1 Upgrade Closure

## Final Status

Complete.

GitHub issue https://github.com/azurras/christopherbell.dev/issues/1120 was closed by merged PR https://github.com/azurras/christopherbell.dev/pull/1121 on July 9, 2026.

## Related Work Record

- `docs/work/2026-07-08-christopherbell-dev-issue-1120-spring-boot-upgrade.md`

## Spoke Repository

- Repository: `azurras/christopherbell.dev`
- Local worktree: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\issue-1120-spring-boot-4-1`
- Branch: `codex/issue-1120-spring-boot-4-1`
- Final branch commit: `4e66f305bbd3e42d5e6a1b9fe6d43edd12b6de83`
- Merge commit: `d5ac7aba5abf3a2c8e2ab9bd792273207eb6cda3`
- PR: https://github.com/azurras/christopherbell.dev/pull/1121

## Completed Scope

- Upgraded Spring Boot plugin and BOM from `3.4.4` to `4.1.0`.
- Upgraded `org.springdoc:springdoc-openapi-starter-webmvc-ui` to `3.0.3` after resolving a current-main conflict from `2.8.17`.
- Migrated Jackson imports and direct dependency usage to Jackson 3 `tools.jackson` packages.
- Updated Jackson 3 API usages in shared test utilities and the Canes box tracker JSON traversal.
- Migrated Spring Security public route matchers from removed `AntPathRequestMatcher` to `PathPatternRequestMatcher`.
- Anchored the custom JWT authentication filter before Spring Security 7 `AuthorizationFilter`.
- Added Boot 4 MVC slice test helpers without disabling CSRF, after CodeQL flagged the first helper version.
- Updated MVC test annotation imports to Boot 4 packages and added `spring-boot-starter-webmvc-test`.

## Validation

Local validation:

```powershell
$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; .\gradlew.bat --no-daemon :website:test
```

Result: `BUILD SUCCESSFUL`, 423 tests passed after the final CodeQL fix and rebase onto current `origin/main`.

Local runtime smoke:

```powershell
$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-issue-1120'; $env:SERVER_PORT='8082'; .\gradlew.bat --no-daemon :website:bootRun --args='--spring.profiles.active=local --server.port=8082'
```

- Spring Boot startup banner reported `v4.1.0`.
- `GET http://localhost:8082/` returned status `200`, title `CB | Home`, content length `3912`.
- `GET http://localhost:8082/actuator/health` returned `403`, matching current anonymous security behavior.

Saved test report: `docs/test-reports/2026-07-08-issue-1120-spring-boot-4-1-upgrade.md`.

GitHub validation:

- CodeQL `Analyze (actions)`: pass.
- CodeQL `Analyze (java-kotlin)`: pass.
- CodeQL `Analyze (javascript-typescript)`: pass.
- CodeQL aggregate check: pass after removing disabled CSRF from test helper.
- CI Build Java 25 on macOS, Ubuntu, and Windows: pass.

## Closure Text

Issue 1120 was completed by PR 1121. Spring Boot is now upgraded to 4.1.0, springdoc is on 3.0.3, Jackson/Spring Security/Boot MVC test compatibility changes are included, local tests and smoke verification passed, and GitHub CI/CodeQL checks passed before merge.

## Known Gaps / Follow-ups

- Local bootRun logged an existing external Overpass `504` during startup catch-up import. It did not block startup or the public route smoke check and was not caused by this dependency upgrade.
- The local feature worktree remains available for inspection but the remote branch was deleted by the merge command.
