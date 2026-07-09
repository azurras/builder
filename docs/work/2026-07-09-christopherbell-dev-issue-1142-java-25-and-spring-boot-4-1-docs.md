# christopherbell.dev issue 1142 Java 25 and Spring Boot 4.1 docs

- Status: active
- Source issue: https://github.com/azurras/christopherbell.dev/issues/1142
- Spoke repo: `christopherbell-dev` at `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1142-docs-java25-boot41`
- Branch: `agent/1142-docs-java25-boot41` from `origin/main`
- Objective: update project documentation so the root README, website README, AGENTS.md, and Copilot instructions consistently describe the current Java 25 and Spring Boot 4.1 baseline.
- Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments were present.
- Current state: baseline `:website:test` passed with `GRADLE_USER_HOME=C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142`.
- Next steps: save reviewed spec, save reviewed implementation plan, implement docs, run automated and local app smoke validation, save test report, open PR, wait for CI, merge, close issue, and save session memory.

## Validation

- Baseline: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142'; .\gradlew.bat --no-daemon :website:test` passed.
