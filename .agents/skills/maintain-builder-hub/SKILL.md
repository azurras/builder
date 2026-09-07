---
name: maintain-builder-hub
description: Check or refresh navigation and validate implementation plans, runtime test reports, and project session-memory documents.
---

# Maintain Builder Hub

Use read-only **check** by default:

```powershell
python .agents/skills/maintain-builder-hub/scripts/maintain_builder_hub.py check --root .
```

Use explicit **refresh** after authorized document changes. It generates only `index.md` in `docs/implementation-plans/`, `docs/test-reports/`, and `docs/session-memory/`, then validates filenames, local links, skill metadata and plan/report quality. There is no `active.md` or inferred status dashboard. Project progress belongs in dated memory entries.

Only those three folders belong under `docs/`. Plans/reports use dated filenames; project memory uses stable lowercase project slugs. Historical imported source bodies are evidence, not new execution instructions. Eight explicitly grandfathered pre-schema plans remain warnings; no new exemptions.

Check-only requests do not rewrite, append memory, or commit. Refresh does not add a continuity entry about itself. The calling phase owns the [phase finalizer](references/phase-finalization.md) and selected-file publication.
