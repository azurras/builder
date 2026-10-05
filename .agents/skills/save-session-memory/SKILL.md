---
name: save-session-memory
description: Record work, decisions, events and outcomes for every project in one session-memory file per date.
---

# Save Session Memory

Use docs/session-memory/YYYY-MM-DD.md for the actual work date. Every entry for that date goes in that one file, whatever its project; a later correction is a new entry appended to the same file. Another date gets another file. Record requests, actions, discoveries, decisions and reasons, attempts/results, reviews, tests, blockers and outcomes. Preserve sufficient context to resume; link primary evidence instead of copying it. Change-specific deviations and decisions belong in the implementation plan's log; record a short entry that links the plan. Append corrections without erasing history.

## When to Write

Write only with persistence authority. Review-only and inspection-only requests do not write memory.

- **Delivery recorded** (deliver-change step 6): one entry per change, written after the plan's Outcome.
- **Blocked:** what blocks the work, who can unblock it and the next action.
- **Proposed closure** (before any external issue update): the issue link, the exact text you will post, the evidence links, and the state you will set. Without a source issue, write "No source issue; external closure does not apply" in the delivery entry instead.
- **Closure result:** the actual issue state read back, on the date it happened, linking the proposal when it was on an earlier date.
- **Handoffs and other authorized events** that a later session needs to resume.

Routine substeps need no separate entry.

## Entry Shape

The helper writes the heading `## YYYY-MM-DD HH:MM <zone> - <title>` followed by a `**Project:** <slug>` line. Pass only the body: three to six short bullets.

1. The request: who asked, what, and a link to the plan.
2. What was done and the decisions that matter, each with its reason.
3. Discoveries, concurrent activity or deviations, linking the plan's log instead of repeating it.
4. Verification actually observed: test counts, checks, readback, or why runtime proof does not apply.
5. Blockers, follow-ups or the proposed closure, when there are any.

```markdown
- User asked to fix the helper after it refused the old side of a `git mv`. [Plan](../implementation-plans/2026-10-04-accept-staged-deletions-in-publish-builder-changes.md).
- Cause: a missing file counted as a deletion only while still in the index. The helper now also accepts a file in HEAD but not the index.
- The existing deleted-directory test caught a gap in the first version; fixed and logged in the plan.
- Verification: no runnable application. 72 tests pass and the hub check passes.
```

Name the title for the outcome, such as "Clarified deliver-change", not the activity.

## Helper

Pass the entry body on stdin:

```powershell
@'
- ...
'@ | python .agents/skills/save-session-memory/scripts/save_session_memory.py --root . --project builder --title 'Clarified deliver-change'
```

- `--project` (required): the project the entry is tagged with, not part of the filename. `builder` for hub work; the spoke's `slug` from spokes.json for spoke work; for work with no repository, an active entry under `projects` in spokes.json (add one there first when the work is new). The helper refuses unknown and retired slugs.
- `--title` (required): the entry title; the file is named for the date alone.
- `--date`: `YYYY-MM-DD`, defaulting to today's local date. Pass it only for retrospective entries.
- `--time`: 24-hour `HH:MM` local time, passed only when the work happened at a known time other than now. Without it the helper stamps the current time and time zone. For retrospective entries, distinguish the known work date and time from the recording time; never invent chronology.

The helper creates the file with its header on the first write of a date and otherwise appends, preserving existing bytes.

## Concurrent Writers

The helper appends without locking. Other sessions can write to the same day's file. Run one write at a time. Before publishing, read `git diff -- <memory file>`: it must contain only your entries on top of the published file. When another session's unpublished entry is in the diff, leave it alone and coordinate before selecting the file. When origin/main gained entries, update with publish-builder-changes' divergence procedure first.

## Reading Memory

Read the relevant dates and entries using targeted searches; `docs/session-memory/index.md` names the projects each date holds, and `**Project:** <slug>` finds one project's entries. Do not load an entire history or create a permanent project file. Dates before October 2026 were merged from per-project files: each former file is a block whose entries or `## Merged record - <slug>` heading carry its Project line.

## Publication

Publish through the [phase finalizer](../publish-builder-changes/references/phase-finalization.md). Its refresh regenerates `docs/session-memory/index.md`; select that index with a new dated file. The migration tooling (`consolidate_project_memory.py` and its [migration audit](references/migration-audit.md)) is archival: it only audits the completed July 2026 consolidation and is never used to write memory.
