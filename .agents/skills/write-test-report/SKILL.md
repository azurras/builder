---
name: write-test-report
description: Save supplied runtime evidence or validate an existing application test report without restarting completed verification.
---

# Write Test Report

This skill owns the runtime report: its content, its candidate identity and how it is updated. verify-local-app produces the evidence; this skill records it. Reports always live in Builder under `docs/test-reports/`, even for spoke changes.

Read [report content](references/report.md), the [template](references/template.md) and the [complete example](references/example.md) before writing one.

Consume actual candidate, environment, inputs, responses, expected and actual results, and cleanup evidence. Sanitize secrets. Missing proof stays an explicit gap; do not fabricate it or restart an application merely to save a report. Further runtime work needs task authority and goes through verify-local-app.

## Candidate Identity

The Branch section names the branch and the commit that was run: the candidate commit's short SHA, at least 7 lowercase hex characters, for example `` `codex/issue-42-require-secret` at `abc1234` ``. The candidate is a committed HEAD, never an uncommitted working tree. publish-spoke-changes' preflight refuses a report that does not name the commit it is about to push.

## Statuses

| Status | Use when |
|---|---|
| `draft` | Evidence is still being gathered |
| `complete` | Every test case ran on the named candidate and the evidence is recorded |
| `blocked` | Verification could not run or finish; Bugs / Follow-ups says what blocks it |
| `superseded` | A later dated report replaces this one; link it in Bugs / Follow-ups |

Only `complete` reports satisfy the before-PR rule and the spoke preflight.

## Updating a Report

Rerun verification after any edit that affects runtime, as verify-local-app requires. Then:

- **Same date:** read the existing report and replace it with `--overwrite`, naming the new candidate. List the superseded candidate SHAs and why they were rerun in Bugs / Follow-ups. The earlier text stays in Git history.
- **Later date:** save a new dated report for the new candidate. Set the old report's status to `superseded` with a link to the new one, and publish both.

## Save

Save complete Markdown on stdin:

```powershell
Get-Content -Raw -LiteralPath $reportDraftPath | python .agents/skills/write-test-report/scripts/save_test_report.py --root . --title 'Require explicit JWT secret'
```

`--title` names the change and becomes the filename slug, `docs/test-reports/YYYY-MM-DD-<slug>.md`. `--date` (`YYYY-MM-DD`) defaults to today's local date. The helper validates before writing and refuses an existing file unless `--overwrite` intentionally replaces a report you have read.

## Validate

```powershell
python .agents/skills/write-test-report/scripts/validate_test_report.py docs/test-reports/YYYY-MM-DD-title.md
```

Structural validity does not prove the evidence supports the claim. AGENTS.md defines when runtime proof is required. Publish report changes through the [phase finalizer](../publish-builder-changes/references/phase-finalization.md); validation alone does not write, commit or close work.
