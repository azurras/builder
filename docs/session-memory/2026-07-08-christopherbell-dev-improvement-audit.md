# 2026-07-08 - christopherbell.dev improvement audit

## 21:30 - christopherbell.dev improvement audit

### Request

The user asked from the Builder hub to inspect the `christopherbell.dev` repository, identify improvements, and create GitHub issues for each one.

### Project Context

`christopherbell.dev` is a registered Builder spoke at `C:\Users\Christopher\Developer\christopherbell.dev` with remote `https://github.com/azurras/christopherbell.dev.git`. The repo is a Java 21 Spring Boot 3.4 app with MongoDB, Thymeleaf templates, vanilla ES modules, Gradle wrapper, and no npm workflow. Builder hub artifacts should stay under `docs/` and be committed/pushed to Builder `main` after substantive updates.

### Work Completed

Created the Builder work record `docs/work/2026-07-08-christopherbell-dev-improvement-audit.md` and closure record `docs/work-closures/2026-07-08-christopherbell-dev-improvement-audit-closure.md`. Refreshed `docs/spokes/state.md`.

Created five GitHub issues in `azurras/christopherbell.dev`:

- https://github.com/azurras/christopherbell.dev/issues/1105 - Fix CI workflow matrix and Java version alignment
- https://github.com/azurras/christopherbell.dev/issues/1106 - Automate portable JavaScript test execution
- https://github.com/azurras/christopherbell.dev/issues/1107 - Update Dependabot to monitor Gradle dependencies
- https://github.com/azurras/christopherbell.dev/issues/1108 - Implement or remove incomplete workflow retry lifecycle in cbell-lib
- https://github.com/azurras/christopherbell.dev/issues/1109 - Add MongoDB indexes for feed, notification, and message query paths

### Decisions

Filed only specific improvements with clear evidence and acceptance criteria. Dropped a production JWT secret candidate after verifying `PermissionService` already has production fail-fast behavior and tests. Dropped a scheduling candidate after verifying `@EnableScheduling` is present on the application entry point.

### Validation

Searched existing open GitHub issues for the selected themes before creating new issues; no matching open issues were found. Verified issue evidence remained present on the final `main` checkout.

Java tests passed with `.\gradlew.bat --no-daemon test` from `C:\Users\Christopher\Developer\christopherbell.dev` using a temporary `GRADLE_USER_HOME`. The default Gradle cache first failed with `Could not write cache value to ...registry.bin`, so the isolated temp cache avoided local daemon/cache state.

Bundled Node was required because `node` was not on the PowerShell PATH. Running bundled Node over individual `website/src/test/js/*.test.js` files produced 93 tests, 92 passing, 1 failing. The failure is the CRLF-sensitive assertion in `website/src/test/js/a11y-markup.test.js`; issue #1106 tracks making JS tests portable and automated.

### Current State

The spoke repo was initially observed clean on branch `yep` at `4b3b9b80`. During the session, the spoke reflog showed checkout to `main` and a fast-forward pull. Final refreshed spoke state is clean on `main` at `5f361778`.

Builder has new/modified hub artifacts that should be committed and pushed after indexes and validation are refreshed.

### Follow-ups

Prioritize #1105 and #1106 first so CI accurately reports supported Java and JS test health. Then handle #1107 for dependency update coverage, #1108 for workflow library correctness, and #1109 for Mongo query performance.
