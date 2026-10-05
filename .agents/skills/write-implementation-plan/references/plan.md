# Plan Mode

Save Markdown under `docs/implementation-plans/YYYY-MM-DD-HH-MM-project-title.md` at the active Builder root; `HH-MM` is the local time the plan is first saved, so several plans on one day sort in creation order. The helper takes the project from the plan's Project section and adds it to the filename unless the title already starts with it. Use the user's local date and time, a concise lowercase slug, and `--overwrite` only after reading an existing file and intentionally replacing its complete contents. `--overwrite` replaces the plan with the same date and title whatever time its name carries, including older names without one.

## What a Plan Is

A plan is the single living record of one change. A separate spec is not a prerequisite: requirements, acceptance criteria and design live here. A reader who opens the plan at any point should learn why the change exists, what is in and out of scope, what will change, how it will be proven, what happened along the way and how it ended. Link relevant historical memory entries when useful.

New plans use `## Plan Format` with value `task-contract-v2`; the save helper refuses any other format for a new file. Existing `task-contract-v1`, unversioned and legacy plans remain valid historical records; do not migrate them. When an in-flight v1 plan needs a log, [update mode](update.md) adds one.

## Sections

Start with a `# Title` that names the outcome, then write the sections in this order. Keep each short; a small change gets a small plan, and a change AGENTS.md defines as small needs none: log it in the plan whose goals it serves, or in dated session memory. When a section genuinely does not apply, say so and why rather than leaving it empty. The Layout column is how a human reader sees it; [Presentation](#presentation) explains the conventions.

| Section | What good content looks like | Layout |
|---|---|---|
| Document Status | `draft`, `ready-for-review`, `ready-for-execution`, `in-progress`, `blocked` or `complete` | The bare value on the line under the heading |
| Objective | One or two sentences: the outcome, not the activity | `> [!IMPORTANT]` callout |
| Background | Why now: the problem, its evidence and who asked | Prose; a numbered list for several causes |
| Goals | Outcomes we commit to, each with how we will know (point to acceptance criteria) | Bullets ending in `(AC-N)` |
| Non-Goals | Tempting adjacent work we will not do, each with the reason; this is the scope fence reviewers enforce | Table: Not doing, Why |
| Acceptance Criteria | Numbered `AC-1`, `AC-2`, ... observable, testable statements of done, including the delivery boundary (merged, deployed, closed) | Table: ID, Done when |
| Inputs | Request, issue, user decisions and the files read, with the inspected commit | Bullets with bold labels |
| Branch | Branch and base, or the Builder checkout and commit | One line |
| Assumptions | Facts relied on but not proven; each is a risk if wrong | Bullets |
| Open Questions | Unresolved decisions and who owns them, or None | Bullets, or `None.` |
| Design | The chosen approach, alternatives considered and why they lost, and key decisions with reasons | Prose, then a table: Alternative, Why not |
| Expected Changes | By file or area: what will change and why; the reviewer's map of the diff | Table: File or area, Change |
| Task Breakdown | Ordered task contracts (below) | One `###` heading and contract table per task |
| Test Plan | For every AC ID: the native tests and the local runtime check that prove it; regressions and edge cases; reruns after runtime-affecting edits | Table: AC, Native check, Local runtime check; regressions as bullets below |
| Rollback or Recovery | How to undo safely, including data and partial publication | Prose or numbered steps |
| Risks | What could go wrong, its likelihood and the mitigation | Table: Risk, Likelihood, Mitigation |
| Implementation Log | `No entries yet.` until work diverges; then dated entries (see [update mode](update.md)) | Dated `###` entries with bold labels |
| Outcome | `Pending.` until closure; then each AC with its result and evidence links, what shipped versus planned and any follow-ups | `> [!TIP]` summary (`> [!WARNING]` when an AC is not met), then a table: AC, Result, Evidence |
| Project | One slug: `builder` for hub work, the spoke's slug for spoke work, or an active entry under `projects` in spokes.json. The save helper refuses a new plan without it or with an unknown or retired slug. Plans written before this section existed keep their names; do not add it to them | The bare slug, near the end as metadata |
| Plan Format | `task-contract-v2` | Last, as metadata |

The validator requires every section to be nonempty, `AC-N` IDs to be sequential, every ID to appear in Test Plan, log entries to be well formed, and a complete plan's Outcome to report every ID. Section order is not validated.

## Presentation

People read plans on GitHub. Present the same content so a reader can scan it:

- **Tables for comparable facts.** Anything with the same shape on every row (criteria, changes, risks, results, alternatives) is a table. Keep cells to one sentence. Escape a literal pipe as `\|`; put long commands in a fenced block below the table.
- **Callouts for what a reader must not miss.** The Objective is an `> [!IMPORTANT]` callout and the Outcome opens with `> [!TIP]` or `> [!WARNING]`. Use at most one callout per section; GitHub renders them as colored boxes and other viewers as quotes.
- **Bold labels, not bare ones.** Write `- **Change:** ...` rather than `Change: ...`; GitHub joins consecutive bare label lines into one paragraph.
- **Result markers.** In Outcome and other result columns, use ✅ Met, ⚠️ Partly met or ❌ Not met, followed by the evidence.
- **Plain machine values.** Document Status, Project and Plan Format stay bare values on their own line: helpers and the resume search read them. Never add emoji, bold or extra text there. Status opens the plan because readers ask where it stands; Project and Plan Format close it as metadata.
- **Collapse only raw output.** `<details>` is for long logs or pasted output, never for sections a reviewer must read.

The validator also accepts the older bullet and bare-label forms, so existing plans need no rewrite.

## Task Contracts

Use sequential `### Task N - Title` headings. Every code-changing task must state `Required skill: write-chris-street-style-code` before code changes and include its task-specific Before-Edit Brief. Put the `Required skill` line under the task heading, then give these fields as a two-column table (`| Contract | Detail |`) with each label bold in the first column, as the [example](example.md) does. The validator also accepts each field as a `Label: value` line. Every field needs a nonempty value:

- Dependencies: preceding tasks and why, or None.
- Files: inspected repository-relative paths; for new files name the intended path and inspected neighboring pattern.
- Symbols: functions, types, configuration keys, or document headings to change or add.
- Inspection: what was read and the relevant branch/commit or current checkout context. Planned targets alone are not inspection evidence.
- Behavior: observable outcome or behavior to preserve.
- Invariants: constraints that must remain true.
- Boundary/API: affected interfaces and compatibility requirements.
- Effects and failures: mutations, I/O, ownership, and expected failure handling.
- Tests and evidence: risk-appropriate starting and final evidence.
- Verification: concrete commands or observable acceptance checks for this task.

Behavior through Tests and evidence form the five-field Before-Edit Brief. Documentation-only tasks can name headings and documentation checks. Exact line ranges and prewritten replacement code are optional; prefer inspected files and stable symbols, and use a legacy `#### Code Edit N.N` block (File, Lines, Action, Current for replace/delete/move, Proposed, fenced code, Verification) only when a literal patch clarifies a fragile edit. `TBD`, `TODO` and pending inspection cannot appear in a ready, in-progress or complete plan. Reinspect targets before editing if the checkout has changed.

For any change in an application repository, the Test Plan must use verify-local-app to run the candidate locally, verify its behavior and publish runtime evidence before creating a PR, including a draft PR, regardless of language. Work with no runnable application records the concrete reason runtime execution does not apply and the appropriate native checks.

## Workflow

1. Inspect repository instructions, relevant files, callers, and tests. Resolve material scope questions using existing authorization and context.
2. Draft the plan. Use draft or blocked when inspection or execution prerequisites remain unresolved.
3. Run review mode and correct blockers. Mechanical validation checks structure; it cannot prove that a symbol was inspected or that a proposed change is correct.
4. Save with the helper, which validates before writing. Do not mark ready-for-execution until validation and review pass.
5. Use the [phase finalizer](../../publish-builder-changes/references/phase-finalization.md) with the exact saved plan and intended indexes at the AGENTS.md publication checkpoint.
6. From here on, keep the plan current with [update mode](update.md).

See the [complete example](example.md).

## PowerShell Helper

Pass complete Markdown through stdin. For an existing draft file:

```powershell
Get-Content -Raw -LiteralPath $draftPath | python .agents/skills/write-implementation-plan/scripts/save_implementation_plan.py --root . --title 'Implementation title'
```

Set `$draftPath` to the reviewed draft. The helper refuses accidental overwrite, refuses new plans in an older format and exits nonzero on invalid plan structure. It retains `--date`, `--time` (`HH:MM`), `--plan-dir`, and `--overwrite` for explicit requests.
