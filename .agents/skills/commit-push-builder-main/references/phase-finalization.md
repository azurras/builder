# Finish an Authorized Writing Phase

1. Finish intended artifacts and status, preserving prior content unless replacement is authorized.
2. Run maintain-builder-hub refresh once, inspect validation and the resulting diff, and resolve errors. This includes the check; do not immediately repeat it without changes.
3. Use commit-push-builder-main with the exact reviewed file selection. Follow its dry-run, staged-state and outgoing-commit checks.
4. Verify publication before the next required phase. A failed push retains its commit and remains incomplete until recovered with push-only.

AGENTS.md owns checkpoint timing and dated-memory policy. A phase can include its relevant session entry and indexes. Routine maintenance, review and coordination substeps do not each require another summary or commit cycle. Read-only work does not enter this finalizer without persistence authority.
