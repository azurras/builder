---
name: record-runtime-verification
description: Save supplied runtime evidence or validate an existing application test report without restarting completed verification.
---

# Record Runtime Verification

For saving evidence, read [report content](references/report.md) and the [template](references/template.md).
Consume actual candidate/environment, inputs, responses, expected/actual results and cleanup evidence. Sanitize secrets. Missing proof stays an explicit gap; do not fabricate it or restart an application merely to save a report. Further runtime work requires task authority; Spring execution uses verify-local-spring-app.

Save complete Markdown on stdin:
python .agents/skills/record-runtime-verification/scripts/save_test_report.py --root . --title 'Report title'

The helper validates before writing and refuses duplicates unless --overwrite intentionally replaces a previously read report.

For read-only validation:
python .agents/skills/record-runtime-verification/scripts/validate_test_report.py docs/test-reports/YYYY-MM-DD-title.md

Structural validity does not prove the evidence supports the claim. AGENTS.md defines when runtime proof is required. Publish report-mode changes through the [phase finalizer](../commit-push-builder-main/references/phase-finalization.md); validation alone does not write, commit or close work.
