---
name: complete-builder-work
description: Deliver authorized work through planning, implementation, verification, publication and closure; also handle coordination or repository inspection without expanding limited scope.
---

# Complete Builder Work

AGENTS.md owns shared authority, evidence and publication policy. Resume at the first incomplete gate supported by current evidence.

1. Identify the item, acceptance criteria, repository, branch strategy and completion boundary. Resolve context locally before asking the user.
2. Use plan-builder-work for a reviewed, validated plan; improve it until no blockers remain. Publish it before implementation.
3. Apply write-chris-street-style-code, implement within scope, run the appropriate checks, and review the diff.
4. For any application change, use verify-local-app to run and exercise the candidate on the local machine, regardless of language, and write-test-report for the report. Complete and publish required runtime proof before creating a PR, including a draft PR. For work with no runnable application, record the concrete reason and native results.
5. Publish by target policy after required local verification passes. Where a PR is required, include local verification evidence, wait for required CI gates, resolve in-scope failures, merge only after gates pass, and confirm the merge. Rerun affected local checks after runtime-affecting edits before updating the PR. Perform already-authorized deployment through the supported mechanism and verify it.
6. Save dated session memory with delivery evidence and proposed closure; publish it. Use [closure](references/closure.md) for external closure and readback. No source issue means no external closure.

Load [coordination](references/coordination.md) only for actual handoffs or multi-party work. Do not invent delegation or extra records for work performed locally.
Load [repository inspection](references/repository-inspection.md) to locate, clone or inspect a registered spoke from spokes.json, or for an explicitly requested snapshot.
For review-only requests, use write-chris-street-style-code review mode. For closure-only requests, inspect existing evidence using the closure reference without restarting delivery.
