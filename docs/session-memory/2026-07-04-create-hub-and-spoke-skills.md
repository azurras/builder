# 2026-07-04 - Create hub and spoke skills

## 19:26 - Create hub and spoke skills

### Request
The user asked to write skills for the eight missing hub-and-spoke capabilities: registering spoke repos, starting hub work, dispatching spoke tasks, ingesting spoke updates, syncing spoke state, saving decision records, reviewing spoke work, and closing hub work.

### Project Context
Azurras is the AI workflow hub at `/Users/cbell/Developer/azurras`. Repo-scoped skills live under `.agents/skills`. Durable state is stored in Markdown under `docs/`. The goal is to start work from this repo, coordinate agents acting in other repos, and keep the source of truth for work state in this hub.

### Work Completed
Created eight repo-scoped Codex skills under `/Users/cbell/Developer/azurras/.agents/skills`:

- `register-spoke-repo`: maintains `docs/spokes/repos.md` with one Markdown section per external spoke repository. Helper: `scripts/register_spoke_repo.py`.
- `start-hub-work`: creates central work ledger records in `docs/work/YYYY-MM-DD-title.md`. Helper: `scripts/start_hub_work.py`.
- `dispatch-spoke-task`: saves task briefs for agents working in spoke repos under `docs/spoke-tasks/YYYY-MM-DD-title.md`. Helper: `scripts/dispatch_spoke_task.py`.
- `ingest-spoke-update`: records spoke agent progress/results under `docs/spoke-updates/YYYY-MM-DD-title.md`. Helper: `scripts/ingest_spoke_update.py`.
- `sync-spoke-state`: reads `docs/spokes/repos.md` and writes a Git state snapshot to `docs/spokes/state.md`. Helper: `scripts/sync_spoke_state.py`.
- `save-decision-record`: saves durable decisions under `docs/decisions/YYYY-MM-DD-title.md`. Helper: `scripts/save_decision_record.py`.
- `review-spoke-work`: saves findings-first review records under `docs/spoke-reviews/YYYY-MM-DD-title.md`. Helper: `scripts/review_spoke_work.py`.
- `close-hub-work`: saves final closure records under `docs/work-closures/YYYY-MM-DD-title.md`. Helper: `scripts/close_hub_work.py`.

Updated `/Users/cbell/Developer/azurras/AGENTS.md` to include the new durable artifact locations and the hub-and-spoke workflow sequence. Updated `/Users/cbell/Developer/azurras/README.md` to document the new directories, skill list, artifact conventions, and the intended eight-step hub-and-spoke workflow.

### Decisions
Implemented each capability as a separate focused skill instead of one large orchestration skill. This keeps triggers and responsibilities clear and lets future agents invoke only the workflow they need.

Used Markdown files for all durable hub artifacts. For deterministic file writes, each skill includes a small standard-library Python helper. Most helpers fail closed on duplicate dated titles unless `--overwrite` is passed. `register-spoke-repo` updates an existing spoke section by slug, and `sync-spoke-state` is read-only against spoke repos except for writing the hub snapshot.

Kept the hub as the source of truth: spoke repos hold implementation changes, while Azurras stores registry, tasks, updates, state snapshots, reviews, decisions, work ledgers, and closure records.

### Validation
Ran frontmatter validation across every `.agents/skills/*/SKILL.md`; all passed the same standard-library checks used previously for name, description, allowed keys, hyphen-case names, and description limits.

Ran `PYTHONPYCACHEPREFIX=/private/tmp/azurras-hub-spoke-pycache python3 -m py_compile .agents/skills/*/scripts/*.py`; all helper scripts compiled.

Tested helpers in `/private/tmp/azurras-hub-spoke-test`:

- `register_spoke_repo.py` created `docs/spokes/repos.md` for an `Azurras Hub` spoke entry.
- `start_hub_work.py` created `docs/work/2099-01-01-demo-hub-work.md`.
- `dispatch_spoke_task.py` created `docs/spoke-tasks/2099-01-01-demo-spoke-task.md`.
- `ingest_spoke_update.py` created `docs/spoke-updates/2099-01-01-demo-spoke-update.md`.
- `save_decision_record.py` created `docs/decisions/2099-01-01-demo-decision.md` and duplicate protection failed closed as expected on a second write without `--overwrite`.
- `review_spoke_work.py` created `docs/spoke-reviews/2099-01-01-demo-review.md`.
- `close_hub_work.py` created `docs/work-closures/2099-01-01-demo-closure.md`.
- `sync_spoke_state.py` read the registered spoke and wrote `docs/spokes/state.md` with branch, HEAD, origin, and status for `/Users/cbell/Developer/azurras`.

Attempted the official `quick_validate.py`; it still fails in this environment because `PyYAML` is not installed.

### Current State
Pending repo changes include the eight new skill directories plus updates to `AGENTS.md`, `README.md`, and this session memory file. Per repo workflow, these changes should be committed and pushed to `origin main` with `commit-push-azurras-main`.

### Follow-ups
Future hub-and-spoke work should start with `start-hub-work`, register affected repos with `register-spoke-repo`, dispatch and ingest spoke tasks through the new artifacts, periodically run `sync-spoke-state`, and close work with `close-hub-work` once spoke changes and hub state are complete.
