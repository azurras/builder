# christopherbell.dev issue 1152 MongoDB backup runbook

- Status: closed
- Source issue: https://github.com/azurras/christopherbell.dev/issues/1152
- Spoke repo: `christopherbell-dev` at `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1152-mongodb-backup-runbook`
- Branch: `agent/1152-mongodb-backup-runbook` from `origin/main`
- Objective: document concise production MongoDB backup, restore, verification, and restore smoke-check procedures for the Spring Boot app.
- Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments were present.
- Current state: PR https://github.com/azurras/christopherbell.dev/pull/1182 was squash-merged as `8a4d5c6f2d97d355c134506f17bf59fe239dd391` on July 9, 2026, after local validation and GitHub CI passed. Issue https://github.com/azurras/christopherbell.dev/issues/1152 is closed.
- Next steps: none required.

## Validation

- Baseline: `.\gradlew.bat :website:test` with shared Gradle home failed before code execution due to registry write failure.
- Baseline retry: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1152'; .\gradlew.bat --no-daemon :website:test` passed.
- Final local validation: `:website:test` passed; `GET http://localhost:8082/` returned `HTTP/1.1 200` and matched `<title>CB | Home</title>`.
- PR CI: Java 25 builds on Ubuntu, macOS, and Windows plus CodeQL analyses passed before merge.
