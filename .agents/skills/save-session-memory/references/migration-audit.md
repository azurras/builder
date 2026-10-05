# Historical Migration Audit

This is a read-only audit of the already completed document consolidation, not the daily memory workflow.

python .agents/skills/save-session-memory/scripts/consolidate_project_memory.py --root . --source-commit 78f0183 --verify

It checks the 267 full transformed source bodies against the original Git corpus. Whether a link target exists is judged against the source commit's tree, so later moves do not change what the audit expects. Later appended dated entries are allowed. Original source paths, hashes and dates remain in the imported sections; sources lacking filename dates use explicitly labeled historical Git dates. `test_real_repository_passes_migration_audit` runs this audit with the test suite.

## Renames That Touch Imported Links

Imported sections are otherwise unchanged, but a skill or file rename may retarget a link inside one so the hub link check still passes. Record each such edit in `LATER_LINK_RETARGETS` in `consolidate_project_memory.py`, in the same change, as (memory file, link as migrated, current link). The audit applies only those entries; any other edit, or an entry that no longer matches, fails.

## Merged Dated Files

In October 2026 each date's per-project memory files were merged, verbatim, into one `YYYY-MM-DD.md`. The audit reads each migrated file's sections from that dated file and applies one recorded rename to the expected text: links to a former `YYYY-MM-DD-project.md` memory file point at `YYYY-MM-DD.md`, with the same anchor (`retarget_merged_memory_links` in `.agents/lib/project_memory.py`).

Do not rerun --apply on the current repository. Exact originals remain in Git; recovery requires a scoped, reviewed change.
