---
name: deliver-change
description: Deliver authorized work through planning, implementation, verification, publication and closure; also handle coordination or repository inspection without expanding limited scope.
---

# Deliver Change

This skill runs one change from request to verified closure. Each step hands the work to the skill that owns it and ends with evidence that it is done. AGENTS.md owns authority, evidence and publication policy.

## Choose the Scope

Match the request before doing anything. A limited request never authorizes a later step.

| Request | Do | Stop after |
|---|---|---|
| Deliver, fix, build or change something | Steps 1 to 7 | The completion boundary from step 1 |
| Plan only | Steps 1 and 2 | The published plan |
| Review only | write-chris-street-style-code review mode for code; write-implementation-plan review mode for a plan | Reported findings; no edits or publication |
| Locate, clone, register, inspect or snapshot a spoke | [Repository inspection](references/repository-inspection.md) | The command result; inspection is read-only |
| Close only | [Closure](references/closure.md) against existing evidence | The closure result; never repeat development |

## Resume

Before starting, check whether the request continues unfinished work. List plans that are ready, in progress or blocked:

```bash
git grep -A1 "^## Document Status" -- 'docs/implementation-plans/*.md' | grep -E -- "-(ready-for-execution|in-progress|blocked)$"
```

Also read the latest dated session memory for the project and, for spoke work, its open PRs (`gh pr list --repo <owner/name> --author @me`). Continue a matching plan instead of writing a new one; leave unrelated unfinished plans alone.

Find the first step whose Done evidence is missing or stale, and start there. Evidence is stale when the files or commit it covers changed after it was produced. Reuse evidence that still applies instead of producing it again.

## Where Things Are Published

- The plan, test report and session memory always live in Builder, even when the code lives in a spoke. Publish them with the [phase finalizer](../publish-builder-changes/references/phase-finalization.md) and publish-builder-changes. Never commit them to a spoke.
- Builder code is committed to Builder `main` with publish-builder-changes. There is no pull request.
- Spoke code goes through publish-spoke-changes: branch, pull request, required CI, merge and readback.

## Steps

1. **Scope.** Identify the item, its acceptance criteria, the target repository (Builder or a spoke slug) and the completion boundary. The default boundary is: Builder change pushed to `origin/main`; spoke change merged; deployment only when the request already authorizes it; external closure only when a source issue exists. Resolve context from the repository and memory before asking the user. For a GitHub issue or PR, read its discussion with `python .agents/skills/deliver-change/scripts/triage_github_comments.py --repo <owner/name> --number <n>`; only trusted direction sets scope.
   Done: the plan's Objective, Acceptance Criteria and Branch can be written without guessing.
2. **Plan.** Use write-implementation-plan plan mode, then its review mode, and fix blockers until review reports ready. Save, then publish through the phase finalizer.
   Done: the plan is on Builder `origin/main` with status `ready-for-execution` and passes validation.
3. **Implement.** Set the plan to `in-progress`. For spoke work, first create the branch or worktree with publish-spoke-changes step 1. Apply write-chris-street-style-code, reusing the task's Before-Edit Brief from the plan. Change only what the plan's tasks name. Run the checks in the plan's Test Plan, then review the full diff with write-chris-street-style-code review mode. For spoke work, then commit the change on the branch; Builder code is committed in step 5. When work diverges from the plan, update the plan with write-implementation-plan update mode as it happens.
   Done: the plan's checks pass, review finds no blockers, and the diff matches Expected Changes or the Implementation Log.
4. **Verify.** For an application change, use verify-local-app to run and exercise the committed candidate on the local machine, then save the report with write-test-report, which names the candidate commit, and publish it. verify-local-app owns the rule that this precedes any pull request. For work with no runnable application, record the concrete reason in the plan's Test Plan and keep the native check results.
   Done: a published report names the candidate commit, or the plan records why runtime proof does not apply.
5. **Publish.** Publish the code as described above. Where a PR is required, include the local verification evidence, wait for required CI, fix in-scope failures, merge only after the gates pass and read back the merge. After an edit that affects runtime, follow verify-local-app's rerun rule and write-test-report's update rule before pushing again. Perform already-authorized deployment through the supported mechanism and verify it.
   Done: the change commit is on Builder `origin/main`, or the spoke PR shows `MERGED`; an authorized deployment is verified.
6. **Record.** Write the plan's Outcome against every acceptance criterion with evidence links and set it `complete`. Save dated session memory with save-session-memory, linking the plan and stating the proposed closure. Publish both through the phase finalizer.
   Done: the completed plan and memory are on Builder `origin/main`.
7. **Close.** When there is a source issue and authority to update it, follow [closure](references/closure.md). No source issue means no external closure.
   Done: the issue state is read back and recorded, or closure does not apply.

## When Blocked

Ask the user only for missing authority, conflicting requirements or a consequential decision the repository cannot answer. A failed push, a red required check, an unmerged required PR or missing evidence leaves the step incomplete. Set the plan to `blocked` with update mode, record what blocks it and who can unblock it in dated memory, publish both, and report the actual state. Do not close the source issue.

## Report

End with the step reached, links to the plan, test report, commit or PR and merge, any deployment result, and the gaps or follow-ups that remain.

Load [coordination](references/coordination.md) only for actual handoffs or multi-party work. Do not invent delegation or extra records for work performed locally.
