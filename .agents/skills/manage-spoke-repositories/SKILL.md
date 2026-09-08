---
name: manage-spoke-repositories
description: Inspect a repository read-only or append verified repository facts and snapshots to the corresponding project memory.
---

# Manage Spoke Repositories

Read repository context from the project's memory. Reverify the actual path, origin, branch, and relevant guardrails before acting; historical configuration may be stale. Record newly verified context through `save-session-memory` with the existing project slug. There is no separate repository registry.

Default to read-only inspection:

```powershell
python .agents/skills/manage-spoke-repositories/scripts/manage_spoke_repositories.py inspect --path 'A:\Projects\christopherbell.dev'
```

Use the path established for this task. Omitting the mode also inspects. Git failures produce explicit errors and nonzero status, never a clean result. Inspection does not fetch, modify the source repo, append memory, or authorize deployment.

For an authorized persistent snapshot, use `snapshot --path <verified-path> --root . --project <existing-project>`. It appends evidence to today's `YYYY-MM-DD-project.md`. Repeating today's most-recent snapshot leaves memory unchanged; a new day has its own record. Errors are recorded honestly and still fail the command. Use the phase finalizer for changed memory, without a separate state file or extra summary entry.
