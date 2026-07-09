# Issue 1142 Java 25 and Spring Boot 4.1 Documentation Implementation Plan

## Document Status

ready-for-execution

## Objective

Update issue-scoped project documentation so it consistently describes Java 25 and Spring Boot 4.1.

## Goals

- Replace stale Spring Boot 3.4 references in root project docs with Spring Boot 4.1.
- Replace stale Java 21 / Spring Boot 3 references in `website/README.md` with Java 25 / Spring Boot 4.1.
- Make Copilot instructions explicitly name Spring Boot 4.1 alongside Java 25.
- Keep the change documentation-only.

## Inputs

- Spec: `docs/specs/2026-07-09-issue-1142-java-25-and-spring-boot-4-1-documentation-spec.md`.
- Source issue: https://github.com/azurras/christopherbell.dev/issues/1142.
- Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments are present.
- Spoke checkout: `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1142-docs-java25-boot41`.
- Baseline validation: `:website:test` passed with worktree-local `GRADLE_USER_HOME`.

## Branch

- Repository: `azurras/christopherbell.dev`.
- Base: `origin/main` at `8a4d5c6f`.
- Work branch: `agent/1142-docs-java25-boot41`.

## Non-Goals

- Do not change Gradle build files, source compatibility, toolchains, dependencies, application code, runtime config, or CI workflows.
- Do not rewrite unrelated documentation.
- Do not add or remove npm-related guidance beyond preserving existing no-npm statements.

## Assumptions

- The checked-in Gradle build is the source of truth for Spring Boot `4.1.0`.
- Java 25 is the active project baseline because root docs, AGENTS, current local runtime, and CI checks use Java 25.
- Documentation-only edits still need automated and local runtime smoke verification per Builder loop.

## Open Questions

None.

## Task Breakdown

### Task 1 - Update root README tech stack

Sequence / dependencies:
- Runs first because the root README is the primary onboarding document.

Implementation notes:
- Change only the stale Spring Boot version line.

#### Code Edit 1.1
- File: `README.md`
- Lines: 14
- Action: replace

Current:
```markdown
- Spring Boot 3.4
```

Proposed:
```markdown
- Spring Boot 4.1
```

Verification:
- `rg -n "Spring Boot 3\.4|Spring Boot 4\.1" README.md`

### Task 2 - Update website README tech stack and prerequisite

Sequence / dependencies:
- Runs after Task 1; both edits are in the website-specific onboarding doc.

Implementation notes:
- Keep the concise existing format.
- Replace Java 21 CI wording with Java 25 baseline wording.

#### Code Edit 2.1
- File: `website/README.md`
- Lines: 6
- Action: replace

Current:
```markdown
- **Backend:** Java 21 target, Spring Boot 3, Gradle
```

Proposed:
```markdown
- **Backend:** Java 25, Spring Boot 4.1, Gradle
```

Verification:
- `rg -n "Java 21 target|Spring Boot 3|Java 25|Spring Boot 4\.1" website/README.md`

#### Code Edit 2.2
- File: `website/README.md`
- Lines: 14
- Action: replace

Current:
```markdown
- Java 21+ (CI builds with Java 21; newer local JDKs such as Java 25 are supported by the wrapper)
```

Proposed:
```markdown
- Java 25 JDK
```

Verification:
- `rg -n "Java 21|Java 25 JDK" website/README.md`

### Task 3 - Update agent-facing docs

Sequence / dependencies:
- Runs after onboarding docs so assistant-facing summaries match user-facing docs.

Implementation notes:
- Update the exact stale project facts line in `AGENTS.md`.
- Make `.github/copilot-instructions.md` explicitly mention Spring Boot 4.1.

#### Code Edit 3.1
- File: `AGENTS.md`
- Lines: 28
- Action: replace

Current:
```markdown
- Java 25, Spring Boot 3.4, Gradle Wrapper.
```

Proposed:
```markdown
- Java 25, Spring Boot 4.1, Gradle Wrapper.
```

Verification:
- `rg -n "Spring Boot 3\.4|Spring Boot 4\.1" AGENTS.md`

#### Code Edit 3.2
- File: `.github/copilot-instructions.md`
- Lines: 8
- Action: replace

Current:
```markdown
- This is a Java 25 Spring Boot app with vanilla JavaScript static assets.
```

Proposed:
```markdown
- This is a Java 25 Spring Boot 4.1 app with vanilla JavaScript static assets.
```

Verification:
- `rg -n "Java 25 Spring Boot" .github/copilot-instructions.md`

## Code Changes

- `README.md`: replace line 14.
- `website/README.md`: replace lines 6 and 14.
- `AGENTS.md`: replace line 28.
- `.github/copilot-instructions.md`: replace line 8.

## Files and Modules

- `README.md`
- `website/README.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`

## Unit Testing

- No unit tests are required for documentation-only edits.
- Run automated regression coverage for unchanged app behavior:
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142'; .\gradlew.bat --no-daemon :website:test`

## Local Testing

- Start the app locally on a non-production port:
  - `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142'; $env:SERVER_PORT='8083'; .\gradlew.bat --no-daemon :website:bootRun`
- Send a public-page smoke request:
  - `curl.exe -i http://localhost:8083/`
- Expected response: `HTTP/1.1 200` and home-page HTML containing the page title.
- Stop the local process after verification.

## Validation

- Documentation grep confirms no issue-scoped stale references remain:
  - `rg -n "Spring Boot 3|Spring Boot 3\.4|Java 21|CI builds with Java 21" README.md website/README.md AGENTS.md .github/copilot-instructions.md`
- Documentation grep confirms current references exist:
  - `rg -n "Spring Boot 4\.1|Java 25" README.md website/README.md AGENTS.md .github/copilot-instructions.md`
- `:website:test` passes after the documentation change.
- Local app smoke test passes on port `8083` without touching any existing production process.
- Builder test report records data sent, response received, and pass/fail evidence.
- PR includes `Closes #1142`, required CI checks pass, PR merges, and issue closes.

## Rollback or Recovery

- Revert the documentation commit if the baseline wording is incorrect.
- Because this is documentation-only, rollback does not require database, application, or configuration changes.

## Risks

- Documentation could drift again if future dependency upgrades do not update docs. Mitigation: keep the changed docs scoped to current Gradle source of truth.
- Broad grep may find historical planning docs outside the issue scope. Mitigation: validate only the issue-named docs.

## Completion Criteria

- Reviewed spec and reviewed implementation plan are saved and pushed in Builder.
- Spoke docs are implemented, committed, pushed, and opened as a PR.
- Automated tests and local app smoke verification pass.
- Builder test report is saved, validated, committed, and pushed.
- GitHub PR CI gates pass, PR merges, and issue #1142 closes.
- Builder closure and session memory are saved, indexed, validated, committed, and pushed.
