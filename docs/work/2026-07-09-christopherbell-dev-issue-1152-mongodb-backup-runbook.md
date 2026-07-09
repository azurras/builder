# christopherbell.dev issue 1152 MongoDB backup runbook

- Status: active
- Source issue: https://github.com/azurras/christopherbell.dev/issues/1152
- Spoke repo: `christopherbell-dev` at `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1152-mongodb-backup-runbook`
- Branch: `agent/1152-mongodb-backup-runbook` from `origin/main`
- Objective: document concise production MongoDB backup, restore, verification, and restore smoke-check procedures for the Spring Boot app.
- Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments were present.
- Current state: baseline `:website:test` passed with `GRADLE_USER_HOME=C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1152` after the shared Gradle daemon registry failed before test execution.
- Next steps: save reviewed spec, save reviewed implementation plan, implement docs, run automated and local app smoke validation, save test report, open PR, wait for CI, merge, close issue, and save session memory.

## Validation

- Baseline: `.\gradlew.bat :website:test` with shared Gradle home failed before code execution due to registry write failure.
- Baseline retry: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1152'; .\gradlew.bat --no-daemon :website:test` passed.
