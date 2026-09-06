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

Retired directories retain Python commands so existing automation and historical instructions keep working. They no longer contain `SKILL.md` or UI metadata. No compatibility stub is discoverable as a duplicate skill. The decision-record template and command remain available through planning; a standalone decision skill is unnecessary for the observed workflow.

`sync_spoke_state.py` still writes snapshots by default for compatibility; add `--inspect` for no writes. The new `manage_spoke_repositories.py` defaults to inspect and requires `snapshot` for persistence. Unchanged snapshots preserve contents and modification time; Git failures now produce explicit errors and nonzero status. The legacy index/validation and artifact save commands keep their paths and arguments.

Use the [phase finalizer](../.agents/skills/maintain-builder-hub/references/phase-finalization.md) once per artifact-writing phase. Required spec, plan, runtime-report, and continuity checkpoints remain separate. Internal maintenance and review do not generate additional memory/commit cycles. Link primary evidence rather than copying it into every record.
