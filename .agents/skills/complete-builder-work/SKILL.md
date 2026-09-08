---
name: complete-builder-work
description: Deliver authorized work through planning, implementation, verification, publication and closure; also handle coordination or repository inspection without expanding limited scope.
---

# Complete Builder Work

AGENTS.md owns shared authority, evidence and publication policy. Resume at the first incomplete gate supported by current evidence.

1. Identify the item, acceptance criteria, repository, branch strategy and completion boundary. Resolve context locally before asking the user.
2. Use plan-builder-work for a reviewed, validated plan; improve it until no blockers remain. Publish it before implementation.
3. Apply write-jane-street-style-code, implement within scope, run the appropriate checks, and review the diff.
4. For required runtime proof, use verify-local-spring-app for Spring execution and record-runtime-verification for the report. For other work record the reason and native results.
5. Publish by target policy. Where a PR is required, create it, wait for required CI gates, resolve in-scope failures, merge only after gates pass, and confirm the merge. Perform already-authorized deployment through the supported mechanism and verify it.
6. Save dated session memory with delivery evidence and proposed closure; publish it. Use [closure](references/closure.md) for external closure and readback. No source issue means no external closure.

Load [coordination](references/coordination.md) only for actual handoffs or multi-party work. Do not invent delegation or extra records for work performed locally.
Load [repository inspection](references/repository-inspection.md) only for repository discovery or an explicitly requested snapshot.
For review-only requests, use write-jane-street-style-code review mode. For closure-only requests, inspect existing evidence using the closure reference without restarting delivery.
