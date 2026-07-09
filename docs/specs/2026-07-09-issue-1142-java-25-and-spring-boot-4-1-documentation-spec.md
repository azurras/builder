# Issue 1142 Java 25 and Spring Boot 4.1 Documentation Spec

## Document Status

ready-for-execution

## Purpose

Resolve `azurras/christopherbell.dev` issue #1142 by updating repository documentation so setup, build, and architecture docs consistently describe the current Java 25 and Spring Boot 4.1 baseline.

## Background

The current code uses Spring Boot `4.1.0` in `build.gradle.kts` and runs under Java 25. Several docs still mention older baselines:

- Root `README.md` says Spring Boot 3.4.
- `AGENTS.md` says Spring Boot 3.4.
- `website/README.md` says Java 21 target, Spring Boot 3, and Java 21 CI.
- `.github/copilot-instructions.md` already says Java 25 Spring Boot but should be checked for consistency.

Source issue: https://github.com/azurras/christopherbell.dev/issues/1142
Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments are present.

## Goals

- Update the root README tech stack to state Spring Boot 4.1.
- Update `AGENTS.md` project facts to state Spring Boot 4.1.
- Update `website/README.md` backend and prerequisites to state Java 25 and Spring Boot 4.1.
- Confirm Copilot instructions remain consistent with Java 25 and the current Spring Boot baseline.
- Keep the change documentation-only and avoid code/config changes.

## Non-Goals

- Do not upgrade dependencies or modify Gradle build files.
- Do not change Java source compatibility, toolchains, application code, runtime config, or CI behavior.
- Do not rewrite unrelated documentation beyond the issue scope.

## Requirements

- Documentation must consistently present Java 25 as the required baseline.
- Documentation must consistently present Spring Boot 4.1 as the current framework baseline.
- The website README must no longer imply Java 21 target or Java 21 CI.
- The change must preserve repo conventions: no npm workflow, Gradle commands from repo root, MongoDB local default.
- Validation must include documentation grep checks, automated tests, local app runtime smoke, PR CI, and issue closure.

## Proposed Approach

Make focused Markdown edits in the four issue-named docs:

- `README.md`: change Spring Boot 3.4 to Spring Boot 4.1.
- `AGENTS.md`: change Project Facts from Spring Boot 3.4 to Spring Boot 4.1.
- `website/README.md`: update backend and prerequisites lines from Java 21/Spring Boot 3 to Java 25/Spring Boot 4.1.
- `.github/copilot-instructions.md`: add Spring Boot 4.1 to the existing Java 25 reminder if it does not already name the baseline.

## Files or Modules Involved

- `README.md`
- `website/README.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

## Validation Plan

- Run `rg -n "Spring Boot 3|Spring Boot 3.4|Java 21|CI builds with Java 21|Spring Boot 4.1|Java 25" README.md website/README.md AGENTS.md .github/copilot-instructions.md` and verify only current Java 25 / Spring Boot 4.1 references remain in the issue-scoped docs.
- Run `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142'; .\gradlew.bat --no-daemon :website:test` after edits.
- Start the app locally on a non-production port and request `/` to verify unchanged runtime behavior.
- Save a Builder test report with the exact request and response evidence.
- Open a PR with `Closes #1142`, wait for required GitHub CI gates, merge only after they pass, and verify the issue closes.

## Spec Review

No blockers remain.

- The issue is documentation-only and names the exact documents to update.
- The current source of truth is the checked-in Gradle build: Spring Boot `4.1.0`, Java 25.
- Local verification can be complete because the app can be tested with existing local MongoDB and a non-production port.

## Open Questions

None.
