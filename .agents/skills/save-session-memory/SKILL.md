---
name: save-session-memory
description: Record work, decisions, events and outcomes in separate dated session-memory files for each project.
---

# Save Session Memory

Use docs/session-memory/YYYY-MM-DD-project.md for the actual work date. Append same-day activity; another date gets another file. Record requests, actions, discoveries, decisions and reasons, attempts/results, reviews, tests, blockers and outcomes. Preserve sufficient context to resume; link primary evidence instead of copying it. Append corrections without erasing history.

Pass complete entry Markdown on stdin:
python .agents/skills/save-session-memory/scripts/save_session_memory.py --root . --project builder --date YYYY-MM-DD --title 'Work update'

--project is required; use the established slug. --date defaults to the current local date; --title names the entry and optional --time records a known time. The helper preserves existing bytes. Serialize same-file writes. For retrospective entries distinguish known work dates/times from recording time; never invent chronology.

Read the relevant dates/sections using targeted searches. Do not load an entire project history or create a permanent project file. Closure results belong on their actual date, linked to earlier proposals when needed.

Use the [phase finalizer](../commit-push-builder-main/references/phase-finalization.md) for authorized persistence. Review/inspection-only requests do not write memory without authorization. For auditing the completed historical migration only, see [migration audit](references/migration-audit.md).
