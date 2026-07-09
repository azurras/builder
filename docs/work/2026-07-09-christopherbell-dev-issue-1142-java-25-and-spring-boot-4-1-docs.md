# christopherbell.dev issue 1142 Java 25 and Spring Boot 4.1 docs

- Status: closed
- Source issue: https://github.com/azurras/christopherbell.dev/issues/1142
- Spoke repo: `christopherbell-dev` at `C:\Users\Christopher\Developer\christopherbell.dev-worktrees\1142-docs-java25-boot41`
- Branch: `agent/1142-docs-java25-boot41` from `origin/main`
- Objective: update project documentation so the root README, website README, AGENTS.md, and Copilot instructions consistently describe the current Java 25 and Spring Boot 4.1 baseline.
- Trusted guidance: issue body and metadata authored by `azurras`; no comments or attachments were present.
- Current state: PR https://github.com/azurras/christopherbell.dev/pull/1183 was squash-merged as `123785da4855971ced0600338ff4d7c766970542` on July 9, 2026, after local validation and GitHub CI passed. Issue https://github.com/azurras/christopherbell.dev/issues/1142 is closed.
- Next steps: none required.

## Validation

- Baseline: `$env:GRADLE_USER_HOME='C:\Users\Christopher\Developer\christopherbell.dev-worktrees\.gradle-1142'; .\gradlew.bat --no-daemon :website:test` passed.
- Final local validation: stale-reference grep passed, `:website:test` passed, and `GET http://localhost:8083/` returned `HTTP/1.1 200` with `<title>CB | Home</title>`.
- PR CI: Java 25 builds on Ubuntu, macOS, and Windows plus CodeQL analyses passed before merge.
