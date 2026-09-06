---
name: record-runtime-verification
description: Save or validate evidence from a running local application, including exact inputs, responses, pass/fail results, and environment details.
---

# Record Runtime Verification

Choose **report** to preserve actual local application evidence or **validate** for a read-only check of an existing report. Validation alone does not save artifacts, commit, create memory, or close work.

Runtime evidence is required for application runtime changes or an explicit runtime-verification request. For documentation, planning, static policy, or standalone tooling without runtime impact, record the reason and native checks in the plan/continuity record. Unit tests, lint, and build output alone are not a runtime report.

For report mode, consume existing or supplied verification evidence and read [report content](references/report.md). Record the candidate that was tested, representative endpoint/UI inputs and outputs, regressions, and cleanup; it need not still be running. Saving completed results does not restart verification. If proof is missing, perform further runtime work only within the authorized task; otherwise record the gap and keep the report incomplete. Use `verify-local-spring-app` when Spring execution is required and authorized. Sanitize secrets; preserve actual inputs/outputs rather than manufacturing missing proof.

Save complete Markdown on stdin with `python .agents/skills/save-test-report/scripts/save_test_report.py --root . --title 'Report title'`. The helper validates before writing under `docs/test-reports/`; it refuses duplicates unless intentional `--overwrite` is supplied after reading the existing report.

Validate with `python .agents/skills/validate-test-report/scripts/validate_test_report.py docs/test-reports/YYYY-MM-DD-title.md`. Missing runtime details, data sent, response, pass/fail, or evidence blocks completion when runtime proof is required. Structural success still requires checking that the evidence supports the claim.

The saved test report must be committed and pushed before moving to the next delivery-loop step through the [phase finalizer](../maintain-builder-hub/references/phase-finalization.md). Link this report from closure and continuity instead of repeating its raw evidence.
