# Builder Skill Migration

The September 2026 consolidation reduces discovery from 22 skills to 11. Historical artifacts retain the names used when they were written. For current work, route those names through this table.

| Retired skill | Current entry point and mode |
| --- | --- |
| `complete-story-issue` | `complete-builder-work`: delivery |
| `close-story-issue` | `complete-builder-work`: closure |
| `save-project-spec` | `plan-builder-work`: spec |
| `save-implementation-plan` | `plan-builder-work`: plan |
| `review-implementation-plan` | `plan-builder-work`: review |
| `validate-implementation-plan` | `plan-builder-work`: validate |
| `save-decision-record` | `plan-builder-work`: optional decision |
| `start-hub-work` | `coordinate-builder-work`: start |
| `dispatch-spoke-task` | `coordinate-builder-work`: dispatch |
| `ingest-spoke-update` | `coordinate-builder-work`: update |
| `close-hub-work` | `coordinate-builder-work`: close |
| `save-test-report` | `record-runtime-verification`: report |
| `validate-test-report` | `record-runtime-verification`: validate |
| `register-spoke-repo` | `manage-spoke-repositories`: register |
| `sync-spoke-state` | `manage-spoke-repositories`: inspect/snapshot |
| `update-hub-indexes` | `maintain-builder-hub`: refresh |
| `validate-hub-state` | `maintain-builder-hub`: check |

The five other entry points remain: `commit-push-builder-main`, `verify-local-spring-app`, `write-jane-street-style-code`, `review-spoke-work`, and `save-session-memory`. Independent code review, production safeguards, selected-file publication, and durable continuity remain separate responsibilities.

The user subsequently requested complete removal of the old skill folders. All 17 retired folders are now deleted, including compatibility locations. Needed helpers were moved into the consolidated skills below, retaining their script filenames and arguments. Historical artifacts retain the paths that existed when written; use these new locations for current commands. The decision-record template remains available.

| Helper group | Current scripts directory |
| --- | --- |
| Work start, dispatch, returned update, hub closure | `.agents/skills/coordinate-builder-work/scripts/` |
| Spec, plan save/validate, optional decision | `.agents/skills/plan-builder-work/scripts/` |
| Runtime report save/validate | `.agents/skills/record-runtime-verification/scripts/` |
| Register and state snapshot | `.agents/skills/manage-spoke-repositories/scripts/` |
| Index generation and hub validation | `.agents/skills/maintain-builder-hub/scripts/` |

`manage_spoke_repositories.py` defaults to inspect and requires `snapshot` for persistence. Its relocated `sync_spoke_state.py` helper writes snapshots by default; add `--inspect` for no writes. Unchanged snapshots preserve contents and modification time; Git failures produce explicit errors and nonzero status.

Use the [phase finalizer](../.agents/skills/maintain-builder-hub/references/phase-finalization.md) once per artifact-writing phase. The default workflow now starts with an implementation plan containing requirements, acceptance criteria, and design decisions. Separate specs are optional for substantial requirements exploration, multiple implementation plans, or an explicit request, and may share the plan checkpoint. Required plan, runtime-report, and continuity checkpoints remain separate. Empty optional decisions/specs folders are created only when records are saved; historical records remain. Internal maintenance and review do not generate additional memory/commit cycles. Link primary evidence rather than copying it into every record.
