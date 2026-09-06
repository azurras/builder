---
name: maintain-builder-hub
description: Check Builder artifact conventions and index freshness read-only, or explicitly refresh indexes and validate before publication.
---

# Maintain Builder Hub

Use **check** by default for validation, audits, and readiness questions:

```powershell
python .agents/skills/maintain-builder-hub/scripts/maintain_builder_hub.py check --root .
```

Omitting the mode also checks. This runs index freshness checks and hub validation without rewriting artifacts. Report errors and warnings; do not silently repair, save session memory, or commit in check-only scope.

Use **refresh** after authorized artifact changes:

```powershell
python .agents/skills/maintain-builder-hub/scripts/maintain_builder_hub.py refresh --root .
```

Refresh regenerates `docs/active.md` and the artifact indexes, then validates directories, templates, filenames, canonical statuses, local links, skill frontmatter, plan contracts, and runtime reports. Review generated changes and fix errors before publication. Eight explicitly named historical pre-schema plans remain warnings; do not extend that exemption to new plans.

Maintenance does not create its own memory or commit cycle. The caller owns the [phase finalizer](references/phase-finalization.md), including selected-file publication and separate delivery checkpoints. Existing index and validation CLI paths remain supported for automation.
