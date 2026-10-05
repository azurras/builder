# Make Plans and Test Reports Pleasant to Read

## Plan Format
task-contract-v2

## Document Status
complete

## Objective
A person who opens a new implementation plan or test report on GitHub can see what it is, where it stands and how it ended at a glance, because the templates present the same content as summary callouts, tables and labeled blocks instead of runs of label lines and paragraphs.

## Background
The user asked on 2026-10-04: the implementation plan and the test report are the two documents humans read, and their templates are not in a friendly format; the amount of text is fine, the presentation is the problem. Inspection on Builder `main` at `567912a` confirms it. The plan example (`write-implementation-plan/references/example.md`) opens with `Plan Format` metadata, renders each task as ten bare `Label: value` lines that GitHub joins into one paragraph, and reports acceptance criteria, tests and outcome as three separate bullet lists the reader must cross-reference by ID. The report template (`write-test-report/references/template.md`) is a list of bare headings; real reports such as `docs/test-reports/2026-10-04-christopherbell-dev-chris-street-style-audit.md` become walls of prose with the verdict buried in the ninth section.

## Goals
- A plan reads top-down for a human: title, status, objective callout, then scope, design, work, proof and outcome, with comparable facts in tables (AC-1, AC-3).
- A report leads with its verdict: status, candidate, and a results table before environment details, with inputs and outputs in fenced blocks per test case (AC-2, AC-3).
- The prettier forms pass the existing validators and helpers, and every existing plan and report still validates (AC-4).
- Delivered on Builder main (AC-5).

## Non-Goals
- Renaming or removing required section headings. Reason: `preflight_spoke_pr.py`, `log_plan_change.py`, the deliver-change resume `grep`, the hub check and the tests key on them; renaming would force a format migration for no reader benefit that tables and order cannot give.
- Migrating existing plans and reports to the new layout. Reason: they are historical records; AGENTS.md preserves history.
- A new plan format version. Reason: the contract (sections, IDs, task fields, log fields) is unchanged; only accepted Markdown forms widen.
- HTML rendering, a site generator or Markdown linting. Reason: GitHub's Markdown rendering is where these are read; GitHub-flavored tables, alerts and `<details>` cover the need.

## Acceptance Criteria
- AC-1: `write-implementation-plan/references/example.md` and the Sections guidance in `plan.md` use the new layout: H1 title, `Document Status` directly under it, an `> [!IMPORTANT]` objective callout, tables for Non-Goals, Acceptance Criteria, alternatives in Design, Expected Changes, Test Plan, Risks and Outcome, each task contract as a two-column table, log entries with bold labels, and `Plan Format` as trailing metadata. `update.md` shows the bold-label log entry.
- AC-2: `write-test-report/references/template.md`, `report.md` and `example.md` use the new layout: H1 title, status, candidate, a `Pass / Fail` section placed before the run details with a verdict callout and a results table, App / Environment as a table, bold-labeled run details with the command in a fenced block, and Data Sent / Response Received grouped per numbered test case in fenced blocks.
- AC-3: Both example documents validate with the shared validators, and each Markdown table in them has a header and separator row with matching column counts.
- AC-4: The validator accepts acceptance criteria as table rows, task contract and log fields as bold labels or table rows, and `Local command:` style labels in bold or table form; new unit tests cover each form and the existing suite passes; `check_hub.py check` reports every existing plan and report as before.
- AC-5: The plan, change, test report and dated memory are on Builder origin/main, confirmed by `git ls-remote`.

## Inputs
- User request in chat on 2026-10-04 (quoted in Background).
- Inspected on Builder `main` at `567912a`, clean tree: `.agents/lib/artifact_quality.py` (`_acceptance_criterion_ids`, `_validate_task_contracts`, `_validate_log_entries`, `LOCAL_COMMAND_PATTERN`, `_plain_status`, `markdown_sections`), `write-implementation-plan/references/{plan,example,update,review,validation}.md`, `scripts/log_plan_change.py` (`with_document_status`, `with_log_entry`), `write-test-report/SKILL.md` and `references/{report,template,example}.md`, both `agents/openai.yaml`, `.agents/tests/test_artifact_quality.py`, `publish-spoke-changes/scripts/preflight_spoke_pr.py` status read, deliver-change resume `grep`, and the plan `2026-10-04-repair-the-historical-migration-audit.md` and report `2026-10-04-christopherbell-dev-chris-street-style-audit.md` as real samples.

## Branch
Builder primary checkout `main` at `567912a`; publish the exact task files through publish-builder-changes.

## Assumptions
- GitHub is the primary reading surface; it renders pipe tables, `> [!NOTE]`-style alerts and `<details>`. Elsewhere alerts degrade to blockquotes, which stay readable.
- `markdown_sections` splits only on `## ` headings, so `###` subsections inside Data Sent and Response Received stay within their sections.

## Open Questions
None.

## Design
Keep the machine contract, change the presentation. Required `##` headings, the status value line under `## Document Status` and the `### Task N` / `### YYYY-MM-DD - Title` headings stay exactly as they are, so every helper keeps working. Section order is free, so the templates reorder for a reader: plans keep `Document Status` directly under the title and move `Plan Format` to the end; reports put `Pass / Fail` right after the candidate.

Widen the validator to the prettier forms, narrowly:
- An acceptance criterion ID may start a table row: `| AC-1 | ... |` or `| **AC-1** | ... |`.
- A task or log field may be written `Field: value`, `**Field:** value`, or as a table row `| Field | value |` (label optionally bold). One shared helper reads a labeled field in all three forms, used for task fields and log fields.
- `LOCAL_COMMAND_PATTERN` accepts the label in bold and as a table row.
Status stays a plain value line: the resume `grep` matches `-in-progress$` and `log_plan_change.py` rewrites that line.

Alternatives considered:

| Option | Why not |
|---|---|
| New `task-contract-v3` with friendlier headings | Same contract, new name; touches every helper, preflight and test for headings a reader barely notices |
| YAML front matter for status and format | GitHub renders front matter as a table but `grep`, `_plain_status` and the log helper would all need a second parser |
| Emoji in the status line (`ðŸŸ¢ complete`) | Breaks status parsing and the resume `grep`; emoji belongs in result cells instead |
| Collapse whole sections in `<details>` | Hides content from search and skimming; reserve it for long raw output only |

## Expected Changes

| File | Change |
|---|---|
| `.agents/lib/artifact_quality.py` | Labeled-field reader shared by task and log checks; table-row AC IDs; bold/table local command label |
| `.agents/tests/test_artifact_quality.py` | A pretty-form living plan and report that validate, plus a check of the reference examples |
| `write-implementation-plan/references/plan.md` | Sections table gains layout guidance; new Presentation section |
| `write-implementation-plan/references/example.md` | Rewritten in the new layout |
| `write-implementation-plan/references/update.md` | Bold-label log entry |
| `write-test-report/references/template.md`, `report.md`, `example.md` | New order, layout rules and example |
| `write-implementation-plan/references/review.md` | Warn on plans that ignore the presentation conventions |
| `.agents/lib/builder_hub.py` and the six stdin-reading helper scripts | Read stdin as UTF-8 so result markers survive saving |

## Task Breakdown

### Task 1 - Accept the prettier Markdown forms
Required skill: write-chris-street-style-code before code edits.
Dependencies: None.
Files: `.agents/lib/artifact_quality.py`; `.agents/tests/test_artifact_quality.py`
Symbols: `_acceptance_criterion_ids`, `_validate_task_contracts`, `_validate_log_entries`, `LOCAL_COMMAND_PATTERN`, new `_labeled_field_value`
Inspection: Read all of `artifact_quality.py` and the living-plan and report tests at `567912a`.
Behavior: Table-row AC IDs, bold-label and table-row task and log fields, and bold or table-row local command labels validate exactly as their plain forms do.
Invariants: Every currently valid plan and report stays valid; missing or empty fields still fail; a test runner named as the local command still does not prove a run.
Boundary/API: Public functions `validate_implementation_plan_text` and `validate_test_report_text` keep their signatures and error messages.
Effects and failures: Pure text checks; no I/O.
Tests and evidence: New tests fail against the old validator, then pass; the full suite passes; `check_hub.py check` finds no new errors.
Verification: `python -m unittest discover -s .agents/tests`

### Task 2 - Rewrite the plan guidance and example
Dependencies: Task 1, so the example validates.
Files: `write-implementation-plan/references/plan.md`, `example.md`, `update.md`
Symbols: Headings `Sections`, `Presentation`, `Log Entries`; the example document
Inspection: Read all three files at `567912a`.
Behavior: A writer following `plan.md` produces the AC-1 layout; the example shows every section in it.
Invariants: Section list, statuses and task fields unchanged; v1 and legacy guidance unchanged.
Boundary/API: Documentation only; helper commands unchanged.
Effects and failures: None.
Tests and evidence: Example validates (Task 1 test); hub link check passes.
Verification: `python .agents/skills/write-implementation-plan/scripts/validate_implementation_plan.py .agents/skills/write-implementation-plan/references/example.md`

### Task 3 - Rewrite the report guidance, template and example
Dependencies: Task 1, so the example validates.
Files: `write-test-report/references/report.md`, `template.md`, `example.md`; `write-test-report/SKILL.md`
Symbols: Headings `Report Content`, `Presentation`; the template and example documents
Inspection: Read all four files at `567912a`.
Behavior: A writer following the template produces the AC-2 layout, verdict first.
Invariants: Eleven required headings, statuses and candidate identity rule unchanged.
Boundary/API: Documentation only; helper commands unchanged.
Effects and failures: None.
Tests and evidence: Example validates as `complete` (Task 1 test); hub link check passes.
Verification: `python .agents/skills/write-test-report/scripts/validate_test_report.py .agents/skills/write-test-report/references/example.md`

## Test Plan
- AC-1: Review the rendered example on GitHub after publication; the Task 1 test validates it.
- AC-2: Same for the report example and template.
- AC-3: A unit test validates both examples and checks every table's column counts.
- AC-4: New unit tests for each widened form; full `python -m unittest discover -s .agents/tests`; `check_hub.py check` before and after shows the same result for existing documents.
- AC-5: `git ls-remote origin main` matches the pushed commit.
- Runtime: Builder has no runnable application; this changes validators and documentation. A test report records the actual validator runs against the new examples and a real existing plan and report as the runtime evidence for the helpers.

## Rollback or Recovery
Revert the change commit. Documents written in the new layout would then fail only where they use table or bold forms; rewrite those fields as plain labels.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Widened field regex accepts a field inside an unrelated table | Low | Only exact field names in the first cell match, and only within the task or log entry |
| A reader on a non-GitHub viewer sees raw `[!IMPORTANT]` | Medium | It degrades to a readable blockquote |
| Agents keep writing the old layout from habit | Medium | Templates and examples are what agents copy; plan review notes layout |

## Implementation Log

### 2026-10-04 - Wait for the project registry change

- Change: Implementation paused before Task 1.
- Reason: The concurrent in-progress plan [Builder Hub Model and Project Registry](2026-10-04-builder-hub-model-and-project-registry.md) has uncommitted edits to `artifact_quality.py` and plans to change every file in this plan's Expected Changes, adding a `Project` section to plans and reports. The user chose to wait and build on it.
- Impact: Status blocked until that plan's change is on origin/main; the new templates and examples will then include its Project section. Tasks unchanged.

### 2026-10-04 - Resume on the project registry change

- Change: Implementation resumed on `79f7f77`, after the project registry change landed (`4da4e7b`, `79f7f77`).
- Reason: The blocking plan is complete on origin/main and the shared files are clean; the user said continue.
- Impact: New templates and examples keep that change's plain `## Project` slug section directly under Document Status, because `project_of` reads the whole section as the slug. Inspection baseline for every task is now `79f7f77`.

### 2026-10-04 - Put machine values last

- **Change:** Machine-value sections moved to the end: reports close with Document Status and Project, plans with Project and Plan Format; plans keep Document Status under the title. The validator also accepts `| Port | 8081 |` as a local-run port, and the table column test checks fenced skeleton tables too. Review mode now warns, without blocking, on plans that ignore the presentation conventions.
- **Reason:** GitHub renderings of the first draft (via the GitHub Markdown API, viewed in the browser pane) opened the report with four headings holding one bare value each before the verdict. The App / Environment table would otherwise not count as naming a port. The report template is a fenced skeleton whose tables would go unchecked.
- **Impact:** AC-1 and AC-2 layouts updated as described; Expected Changes gain `write-implementation-plan/references/review.md`; `write-test-report/SKILL.md` needed no change. Acceptance criteria otherwise unchanged.

### 2026-10-04 - Read helper stdin as UTF-8

- **Change:** Added `builder_hub.read_stdin_text`, which decodes stdin as UTF-8, and used it in the six helpers that read a document body from stdin: both save helpers, both validators, `log_plan_change.py` and `save_session_memory.py`. A regression test pipes ✅, an em dash and an accented letter through four of them.
- **Reason:** Gathering evidence after `e9385e6` showed Python's stdin is cp1252 on this machine, so `save_test_report.py` stored the example's ✅ as `âœ…`. The new templates put result markers in every completed plan and report, so AC-1 and AC-2 are unusable without this fix. The memory helper has the same defect and shares the reader. The scope addition was decided in-session under the existing authority to deliver this change.
- **Impact:** Expected Changes gain `.agents/lib/builder_hub.py` and the six scripts. AC-4 now also covers UTF-8 stdin. Windows PowerShell 5.1 still sends ASCII to native programs; PowerShell 7, the documented shell, sends UTF-8.

## Outcome

> [!TIP]
> Shipped in `e9385e6` (layout, validator) and `d769e30` (UTF-8 stdin). Deviations are in the log: machine values moved to the end, a review-mode warning, and the stdin fix. No source issue; external closure does not apply.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Plan `example.md`, `plan.md` (Sections layout column, Presentation) and `update.md` in `e9385e6`; rendered through GitHub's Markdown API and viewed |
| AC-2 | ✅ Met | Report `template.md`, `report.md` and `example.md` in `e9385e6`, verdict first, per-case fenced blocks; rendered and viewed |
| AC-3 | ✅ Met | `test_reference_examples_validate` and `test_reference_tables_have_matching_column_counts` pass |
| AC-4 | ✅ Met | Widened-form and UTF-8 tests pass (113 tests); hub check passes over all 206 plans and reports; [test report](../test-reports/2026-10-04-builder-make-plans-and-test-reports-pleasant-to-read.md) |
| AC-5 | ✅ Met | Plan, change, report and memory pushed to origin/main; `git ls-remote` readback recorded in session memory |

Follow-up: none required. Windows PowerShell 5.1 would still send `?` for markers; PowerShell 7 is the documented shell.
