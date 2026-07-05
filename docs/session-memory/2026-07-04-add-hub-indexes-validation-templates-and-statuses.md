# 2026-07-04 - Add hub indexes validation templates and statuses

## 19:35 - Add hub indexes validation templates and statuses

### Request
The user asked to implement improvements 2 through 6 from the prior recommendation list: hub index files, a validation skill/script, a shared helper library, artifact templates, and a canonical status model.

### Project Context
Azurras is the AI workflow hub at `/Users/cbell/Developer/azurras`. Repo-scoped skills live under `.agents/skills`, shared skill support code now lives under `.agents/lib`, and durable hub artifacts live under `docs/`. Existing hub-and-spoke skills already covered registry, work records, task dispatch, updates, state sync, decisions, reviews, and closures.

### Work Completed
Added shared Python helper library `/Users/cbell/Developer/azurras/.agents/lib/azurras_hub.py` with common functions for slugging, dated Markdown paths, local timestamps, Markdown listing, first-heading extraction, link parsing, status extraction, and Git command execution.

Created new repo-scoped skill `update-hub-indexes` under `/Users/cbell/Developer/azurras/.agents/skills/update-hub-indexes`. Its helper script generates hub index files: `docs/active.md`, `docs/work/index.md`, `docs/spokes/index.md`, `docs/decisions/index.md`, `docs/specs/index.md`, `docs/implementation-plans/index.md`, `docs/spoke-tasks/index.md`, `docs/spoke-updates/index.md`, `docs/spoke-reviews/index.md`, `docs/work-closures/index.md`, and `docs/session-memory/index.md`. The script supports `--check` and uses deterministic generated text rather than volatile timestamps so checks do not go stale just because time passes.

Created new repo-scoped skill `validate-hub-state` under `/Users/cbell/Developer/azurras/.agents/skills/validate-hub-state`. Its helper script checks required templates, required indexes, dated Markdown filename conventions, canonical work statuses, local Markdown links, and repo-scoped skill frontmatter.

Added canonical status reference `/Users/cbell/Developer/azurras/docs/status-model.md` with statuses: `proposed`, `active`, `blocked`, `in-review`, `ready-to-close`, and `closed`.

Added reusable Markdown templates under `/Users/cbell/Developer/azurras/docs/templates`: `work-record.md`, `spoke-task.md`, `spoke-update.md`, `spoke-review.md`, `decision-record.md`, and `work-closure.md`.

Generated hub index files across the docs tree. Migrated the historical session memory file from `docs/session-memory/2026-07-04.md` to `docs/session-memory/2026-07-04-create-save-session-memory-skill.md` and updated its heading so the stricter filename validation can remain meaningful.

Updated `/Users/cbell/Developer/azurras/AGENTS.md` and `/Users/cbell/Developer/azurras/README.md` to document `.agents/lib`, the new index and validation workflow, templates, and the canonical status model.

### Decisions
Kept indexes generated but checked in, so future agents can quickly inspect active state without running scripts first. Made generated index content deterministic by avoiding live timestamps. Treated the old date-only session memory file as historical data that should be migrated to the current convention rather than adding a validator exception.

Added shared helper code first and used it in the new index and validation scripts. Existing helper scripts can be refactored onto the shared library over time without changing their behavior in this pass.

### Validation
Ran `python3 .agents/skills/update-hub-indexes/scripts/update_hub_indexes.py`, which generated all configured index files. Ran `python3 .agents/skills/update-hub-indexes/scripts/update_hub_indexes.py --check`, which passed after deterministic generation was added.

Ran `python3 .agents/skills/validate-hub-state/scripts/validate_hub_state.py`, which passed after migrating the historical date-only session memory file.

Ran `PYTHONPYCACHEPREFIX=/private/tmp/azurras-status-pycache python3 -m py_compile .agents/lib/azurras_hub.py .agents/skills/update-hub-indexes/scripts/update_hub_indexes.py .agents/skills/validate-hub-state/scripts/validate_hub_state.py`, which passed.

Attempted the official `quick_validate.py` against `update-hub-indexes`, but it still fails in this environment because `PyYAML` is not installed.

### Current State
Pending changes include the new shared helper library, two new repo-scoped skills, templates, status model, generated indexes, README/AGENTS updates, the migrated historical session memory filename, and this new session memory file. Indexes should be regenerated after this memory save so `docs/session-memory/index.md` includes it before commit.

### Follow-ups
A future cleanup can refactor older save/helper scripts to import `.agents/lib/azurras_hub.py` directly. Another useful future enhancement is stable `WORK-YYYY-NNNN` ID generation and validation across all hub artifacts.
