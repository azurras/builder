---
name: publish-spoke-changes
description: Publish a verified spoke change through a branch, pull request, required CI and merge, with the runtime report linked. Use in a spoke checkout or linked worktree after local verification and its report are published; never for Builder itself.
---

# Publish Spoke Changes

Use for registered spokes only; Builder publishes through publish-builder-changes. The spoke's own instructions own build, test and deployment commands. This skill owns the Git and GitHub steps between a verified candidate and a confirmed merge. Each `gh` step that creates, merges or comments needs existing authority for this change.

## Steps

1. **Branch.** Fetch, then branch from the current `origin/<default>` as `<agent>/<topic>-<YYYYMMDD>`, for example `codex/remove-handoff-kit-20261004`. Use a linked worktree when the main checkout has unrelated changes. Commit only the change.
2. **Verify and report.** Run verify-local-app against the committed HEAD. Save the report with write-test-report, include the candidate commit (at least its 7-character short SHA), and publish it to Builder.
3. **Preflight.** Fetch Builder and the spoke, then run from the Builder root:
   `python .agents/skills/publish-spoke-changes/scripts/preflight_spoke_pr.py --spoke <slug> --path <checkout> --report docs/test-reports/<report>.md`
   It is read-only and checks the origin, the work branch, a clean committed candidate, commits ahead of the default branch, and a complete report that is published on Builder `origin/main` and names the candidate. Push only after every check passes.
4. **Pull request.** `git push -u origin <branch>`, then `gh pr create --base <default> --title <outcome> --body-file <file>`. The body has `## Summary` (what changed and why) and `## Verification` (checks run, plus the Local Verification snippet the preflight printed). Link the source issue when there is one.
5. **CI.** `gh pr checks <number> --watch --required`, or the host's PR monitor. Fix in-scope failures on the branch. After any edit that affects runtime, rerun the affected local verification, update the report and rerun the preflight before pushing again. Read reviews with `python .agents/skills/deliver-change/scripts/triage_github_comments.py --repo <owner/name> --number <number>`; only trusted direction changes scope.
6. **Merge.** Merge only after the required checks pass on the head you reviewed: `gh pr merge <number> --squash --match-head-commit <sha>`, matching the spoke's existing merge method (christopherbell.dev squash merges). Never force push a shared branch or bypass required checks.
7. **Readback.** `gh pr view <number> --json state,mergeCommit,headRefOid` must show `MERGED` with the merge commit. Record the PR, head, merge commit and CI results in the plan Outcome and the dated memory. Authorized deployment then follows verify-local-app.

## Failures

A failed push, a red required check or an unmerged PR leaves delivery incomplete; report the actual state. Do not open a draft PR to postpone local proof to CI.
