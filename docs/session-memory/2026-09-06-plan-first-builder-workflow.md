# 2026-09-06 - Plan-first Builder Workflow

## 23:53 - Plan-first Builder Workflow

### Request and Decisions

The user approved starting delivery directly with an implementation plan and cleaning unnecessary document folders from old skills. This supersedes the earlier mandatory spec checkpoint. Plans now include requirements, acceptance criteria, and relevant design decisions. Separate specs are optional for substantial requirements exploration, multiple implementation plans, or an explicit user request; they may share the plan checkpoint. Spec-only requests publish the requested artifact without starting implementation. The reviewed-plan, applicable runtime-report, continuity, publication, and closure requirements remain.

### Changes and Folder Audit

Updated AGENTS.md, README, delivery/planning/closure/finalizer instructions, companion metadata, and checkpoint tests. Shared optional-folder policy keeps index generation and validation aligned for specs and decisions. Maintenance does not create or require empty optional folders; saving records enables their indexes.

The folder inventory found zero decision records, 47 existing specs, 53 runtime reports, 35 spoke reviews, 4 task briefs, 25 updates, 32 work records, and 29 closures. Removed only docs/decisions and its generated index. Kept every historical record and the optional decision template/helper. No source repository or live service changes occurred.

### Validation and Publication

Plan checkpoint c0ad2e5 was published before implementation; no separate spec was created. Implementation d5bd048 is pushed to Builder main. All 56 tests passed, including absent/populated optional-folder behavior and plan-first checkpoint rules. All 11 skill entrypoints and YAML metadata validated. Hub refresh/check and git diff --check passed; the eight historical pre-schema plan warnings remain unchanged. Independent review found no blockers across ordinary bug delivery, spec-only work, plan review without a spec, and empty optional-folder maintenance.

Runtime Evidence Required: false, because the change affects standalone workflow tooling and instructions; temporary-root CLI tests provide native evidence. No external issue was supplied, so issue closure is not applicable. This completion record and completed plan form the final publication checkpoint.

### Follow-ups

None required. Historical session records describe the policy in effect when written; current AGENTS.md and skills define plan-first delivery. Revert d5bd048 to restore the prior behavior if recovery is needed.
