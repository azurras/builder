# Historical Migration Audit

This is a read-only audit of the already completed document consolidation, not the daily memory workflow.

python .agents/skills/save-session-memory/scripts/consolidate_project_memory.py --root . --source-commit 78f0183 --verify

It checks the 267 full transformed source bodies against the original Git corpus. Later appended dated entries are allowed. Original source paths, hashes and dates remain in the imported sections; sources lacking filename dates use explicitly labeled historical Git dates.

Do not rerun --apply on the current repository. Exact originals remain in Git; recovery requires a scoped, reviewed change.
