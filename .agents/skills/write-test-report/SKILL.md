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

## Record While You Run

Capture evidence as you exercise the candidate instead of transcribing it afterwards. Each call runs one case and appends it to a JSON-lines evidence file in your scratch folder, masking secret headers and common token shapes:

```powershell
python .agents/skills/write-test-report/scripts/record_run.py http --evidence $evidence --case 'Health is UP' --checkout <candidate checkout> --url http://127.0.0.1:<port>/actuator/health --expect-text '"UP"'
python .agents/skills/write-test-report/scripts/record_run.py run --evidence $evidence --case 'CLI prints version' --cwd <candidate checkout> -- <command> <arguments>
python .agents/skills/write-test-report/scripts/record_run.py render --evidence $evidence --title '<Change>' --story '<issue or request>' --branch <branch> --project <slug> --env 'Database=test' > $reportDraftPath
```

`http` passes on a status below 400 unless `--expect-status` is given, plus `--expect-text` when set; `run` passes on exit code 0 unless `--expect-exit` is given. Each prints `[pass]` or `[FAIL]` and exits 0 or 1. `render` writes every report section with fenced Data Sent and Response Received blocks, sets `complete` only when every case passed (otherwise `draft`, listing the failures), and names the candidate commit of the checkout. Review and add judgement (test case descriptions, cleanup, follow-ups) before saving.

## Save

Save complete Markdown with `--body-file` (no shell quoting) or on stdin:

```powershell
python .agents/skills/write-test-report/scripts/save_test_report.py --root . --title 'Require explicit JWT secret' --body-file $reportDraftPath
```

Or on stdin:

```powershell
Get-Content -Raw -LiteralPath $reportDraftPath | python .agents/skills/write-test-report/scripts/save_test_report.py --root . --title 'Require explicit JWT secret'
```

`--title` names the change and becomes the filename slug, `docs/test-reports/YYYY-MM-DD-HH-MM-<project>-<slug>.md`, where `HH-MM` is the local time the report is first saved; the project comes from the report's Project section and is not repeated when the title already starts with it. A new report must name `builder`, a registered spoke or an active project from spokes.json; the helper refuses anything else. `--date` (`YYYY-MM-DD`) defaults to today's local date and `--time` (`HH:MM`) to the current local time. The helper validates before writing and refuses an existing file unless `--overwrite` intentionally replaces a report you have read; it finds the report with the same date and title whatever time its name carries.

## Validate

```powershell
python .agents/skills/write-test-report/scripts/validate_test_report.py docs/test-reports/YYYY-MM-DD-HH-MM-project-title.md
```

Structural validity does not prove the evidence supports the claim. AGENTS.md defines when runtime proof is required. Publish report changes through the [phase finalizer](../publish-builder-changes/references/phase-finalization.md); validation alone does not write, commit or close work.
