# 2026-09-08 - christopherbell-dev

## PostgreSQL cutover recovery resumed

User requested continued delivery, then explicitly requested no new regression tests and reloading updated skills. Reloaded current Builder AGENTS.md, delivery, coding, plan, runtime-report, Spring, memory and publication skills. Existing cutover authorization persists; preserve production ACLs and secrets.

Actual production audit corrects the September 5 checkpoint: merged release 39867e9e was built and attempted, but rolled back after MONGO_ARCHIVED with Java exit 2. On September 8, journal checksum validates, authority marker is absent, source snapshot passes, all three services run, and readiness is UP. The automatic deploy task had been paused before the attempt.

Root cause proven by read-only Java probe: New-ProtectedProductionAcl creates Administrators-owned files while FinalizeEvidenceLoader.protectedAttributes rejected that owner, despite already trusting Administrators write ACL entries. Branch codex/fix-postgresql-authority-owner reuses trustedProductionWritePrincipal for ownership. No production ACL or evidence was changed. Existing eight evidence-loader tests pass; actual protected nodes and historical signed evidence now validate. No new tests added, per user request.

Plan published in Builder bd19ff6. [Runtime evidence](../test-reports/2026-09-08-postgresql-authority-owner.md). Spoke fix is locally verified, pending publication/CI/merge and another guarded cutover. Preserve prior attempts; do not bypass journal/signature/lease checks. The historical-clock probe is read-only diagnostic, never authorization to write.

Worktree: A:\Projects\christopherbell.dev-worktrees\postgresql-cutover. Private .gradle-agent cache is untracked and must stay excluded. Authoritative checkout remains untouched. Use process-local JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\cbell-no-unix-sockets-20260905 only while that path is absent for this host's JDK socket workaround. Further work: CI/merge, supported cutover, PostgreSQL-aware ordinary deploy before reenabling automation, fourteen-day soak, then evidence-gated retirement; final Mongo archive retained ninety days.
