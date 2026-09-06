---
name: manage-spoke-repositories
description: Inspect registered repositories read-only, explicitly persist a Git-state snapshot, or register verified repository facts in Builder.
---

# Manage Spoke Repositories

Default to **inspect** for questions about repository state. Use **snapshot** only when persisting state is requested or needed by authorized coordination; use **register** to change the registry. None of these modes authorizes source edits, fetch/push, cleanup, or deployment.

Run from the verified Builder root:

```powershell
python .agents/skills/manage-spoke-repositories/scripts/manage_spoke_repositories.py inspect --root .
```

Omitting the mode also inspects. Inspection reads `docs/spokes/repos.md` and prints local branch, HEAD, origin, and dirty state without writing. It does not infer current remote synchronization from local state. Missing/inaccessible repositories and Git failures produce explicit errors and a nonzero result, never a clean result.

**Snapshot:** replace `inspect` with `snapshot` to save `docs/spokes/state.md`. Unchanged semantic state preserves existing bytes and modification time; a timestamp advances only when state changes. Error states are saved honestly and still fail the command. Review changes, then use the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md) if changed; no extra memory artifact is needed for routine refresh.

**Register:** read [registration](references/registration.md) for verified path/remote/branch, purpose, guardrails, and the command. Review only the intended registry section, then finalize the phase. Existing local Git data can be stale; record gaps rather than inventing facts.
