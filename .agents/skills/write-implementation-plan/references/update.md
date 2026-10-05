# Update Mode

A plan is only useful if it stays true. Update it as the work moves, not after.

## When to Update

- **Implementation starts:** set Document Status to `in-progress`.
- **Work diverges from the plan:** a different file, symbol, design choice, test, task order or risk than planned; a discovery that changes an assumption; an abandoned approach. Edit the affected sections so they describe current truth, and append a log entry that records the difference.
- **Scope changes:** a new or dropped goal, non-goal or acceptance criterion. Proceed only with existing authority; expansions beyond it need the user. Log the change and who decided it.
- **Blocked:** set `blocked` and log what blocks it and who can unblock it.
- **Closure:** write Outcome with every AC ID, its result and evidence links (test report, commits, PR), what shipped versus planned, and follow-ups; then set `complete`.

Routine progress that matches the plan needs no entry. Do not use the log as a diary; dated session memory records the day's work and links here.

## Log Entries

Each entry is a dated `###` heading with three labeled lines:

```markdown
### 2026-10-04 - Read the secret through Environment

- Change: `App.requiredSecret` reads `Environment` instead of `System.getenv`.
- Reason: Existing tests inject configuration through `Environment`.
- Impact: Task 1 Symbols updated; acceptance criteria unchanged.
```

Change says what differs from the plan, Reason says why, and Impact names the sections, tasks or acceptance criteria that changed. Add evidence links when they exist. Entries are append-only: a correction is a new entry, never an edit to an earlier one.

## Helper

Pass the entry body on stdin. `--status` optionally moves Document Status in the same write:

```powershell
@'
- Change: ...
- Reason: ...
- Impact: ...
'@ | python .agents/skills/write-implementation-plan/scripts/log_plan_change.py --plan docs/implementation-plans/YYYY-MM-DD-title.md --title 'Short title' --status in-progress
```

The helper appends at the end of Implementation Log (replacing the `No entries yet.` placeholder, or creating the section before Outcome in an older plan), preserves every other byte and line ending, validates the result and leaves the file unchanged when validation fails. Edit the other sections with ordinary file edits.

## Publication

Publish plan updates with the next phase checkpoint through the [phase finalizer](../../commit-push-builder-main/references/phase-finalization.md); an individual log entry does not need its own commit. The completed plan is published with the delivery memory before closure.
