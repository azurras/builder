# 2026-07-09 - Configure builder repo for this computer

## 19:41 - Configure builder repo for this computer

### Request
The user asked to prepare this repository for use on this Windows computer, enable multi-agent support in the Codex config, rename active repository guidance from Azurras to Builder, and make the guarded commit/push workflow support the current Windows path plus `/Users/cbell/Developer/builder` on macOS.

### Project Context
The checkout is `C:\Users\Christopher\Developer\builder` on branch `main`, tracking `https://github.com/azurras/builder.git`. The repository is a workflow hub with repo-scoped skills under `.agents/skills/`, shared helper code under `.agents/lib/`, and durable Markdown artifacts under `docs/`. Historical session-memory files from 2026-07-04 still refer to Azurras and were intentionally left as archival records.

### Work Completed
Enabled `multi_agent = true` under `[features]` in `C:\Users\Christopher\.codex\config.toml`.

Renamed active Builder hub guidance across `AGENTS.md`, `README.md`, `docs/status-model.md`, current skill `SKILL.md` files, current skill `agents/openai.yaml` metadata, and helper script descriptions. Renamed the shared helper module from `.agents/lib/azurras_hub.py` to `.agents/lib/builder_hub.py` and updated imports.

Renamed the guarded commit/push skill from `.agents/skills/commit-push-azurras-main/` to `.agents/skills/commit-push-builder-main/`, including the helper script from `commit_push_azurras_main.py` to `commit_push_builder_main.py`. The helper now allows exactly `C:/Users/Christopher/Developer/builder` and `/Users/cbell/Developer/builder`, requires branch `main`, and requires origin `https://github.com/azurras/builder.git`.

Added `.agents/tests/test_commit_push_builder_main.py` to cover the expected Builder roots, Builder remote, and rejection of the old `/Users/cbell/Developer/azurras` root.

### Decisions
Kept historical session-memory entries unchanged because they record the original Azurras naming at the time those actions occurred. Updated active operational files and generated indexes instead.

Stored expected commit-helper roots as normalized strings rather than resolved `Path` objects so Windows does not reinterpret the macOS `/Users/cbell/...` path as a Windows drive-rooted path.

### Validation
Watched the new unittest fail before implementation because `.agents/skills/commit-push-builder-main/scripts/commit_push_builder_main.py` did not exist yet. After implementation, ran `python -m unittest discover -s .agents/tests`; all 3 tests passed.

Ran helper compilation with `PYTHONPYCACHEPREFIX` pointed at a temp directory: `python -m py_compile` over all `.agents/**/*.py`; it passed. Ran `python .agents/skills/validate-hub-state/scripts/validate_hub_state.py`; it passed. Ran `python .agents/skills/update-hub-indexes/scripts/update_hub_indexes.py --check`; indexes were current before this memory entry. Ran the new commit helper with `--dry-run`; it accepted the Windows path, `main` branch, and builder remote.

### Follow-ups
Future Codex sessions may need to restart before the newly renamed `commit-push-builder-main` skill appears in the session skill list. The Codex config change is local machine state and is not part of the repository commit.
