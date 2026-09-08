---
name: maintain-builder-hub
description: Check document conventions and navigation, or explicitly refresh the three Builder indexes.
---

# Maintain Builder Hub

Default read-only check:
python .agents/skills/maintain-builder-hub/scripts/maintain_builder_hub.py check --root .

After authorized document changes, use refresh instead of check. It generates only index.md in implementation-plans, test-reports and session-memory, then validates document paths, links, skill frontmatter and plan/report schemas. Eight historical pre-schema plans remain explicit warnings; no new exemptions.

Maintenance creates no memory entry or commit and never infers an active-status dashboard. The writing phase uses the [phase finalizer](../commit-push-builder-main/references/phase-finalization.md).
