---
name: save-test-report
description: Save local app test reports as Markdown files under docs/test-reports with dated filenames. Use when Codex runs an app locally, exercises endpoints or UI flows, captures request data and responses, records manual verification evidence, or preserves pass/fail testing results in the builder workflow hub.
---

# Save Test Report

## Overview

Save test reports in a predictable place and filename format so local app verification evidence is durable and easy to review. Test reports must be Markdown files under `docs/test-reports/`.

Test reports are for real local runtime checks. A unit test command, lint command, or build output is not a test report by itself. Record unit test results in implementation validation or session memory; include them in a test report only as supporting evidence after the app was started locally and exercised through an endpoint, browser/UI flow, CLI command against the running app, webhook, or comparable runtime interaction.

## Storage Rules

- Write test reports under `docs/test-reports/` at the active builder repository root unless the user explicitly chooses another root.
- Name every test report file `YYYY-MM-DD-title.md`, where the date is the local date and `title` is a short slug derived from the report title.
- Slug titles with lowercase ASCII words separated by hyphens. Remove punctuation and collapse repeated hyphens.
- Keep filenames short, descriptive, and stable enough to reference from session memory, work closures, or issues.
- Write only Markdown files. Do not create `.txt`, `.docx`, `.pdf`, or companion metadata files for test reports unless the user explicitly asks.
- If a matching dated title already exists, update that report intentionally rather than creating a near-duplicate filename.
- The helper script runs test-report quality checks before saving. Fix reported validation errors rather than bypassing the helper.

## Report Content

Write test reports as evidence artifacts, not chat transcripts. Every test report should include:

- Document Status: draft, complete, blocked, or superseded.
- Story/Issue: the story, issue, ticket, or work item being verified.
- Branch: the branch, commit, or build under test.
- App / Environment: app name, profile, port, base URL, database or fixture context, and relevant environment variables.
- Local Run Details: exact start command, process details, logs location, and whether the app was stopped or left running.
- Test Cases: the user-visible behaviors, endpoints, or flows exercised.
- Data Sent: request method, URL, headers that matter, payload/body/form data, query params, or UI input values.
- Response Received: status code, response headers that matter, body snippets, UI result, redirects, logs, or screenshots.
- Pass / Fail: result per test case and a short reason.
- Evidence: commands, timestamps, screenshots, curl output files, browser checks, or log excerpts.
- Bugs / Follow-ups: defects found, retest needs, or gaps intentionally left unverified.

Do not write a report whose only evidence is `npm test`, `pytest`, `./gradlew test`, `mvn test`, or similar automated test output. Do not require references to specs or implementation plans. Include those links only when they are directly useful for traceability.

## Workflow

1. Determine the active builder repo root before writing.
2. Start the app locally or identify the running local process under test.
3. Exercise at least one endpoint, UI flow, local webhook, CLI-to-app path, or comparable runtime behavior.
4. Draft the test report as Markdown with a clear H1 title.
5. Include enough raw request/response detail that another agent can understand exactly what was tested.
6. Choose a concise title for the filename. Prefer the story or issue title plus "test report".
7. Save the report under `docs/test-reports/YYYY-MM-DD-title.md`, preferring the helper script below.
8. If the target file already exists, read it before replacing it. Use `--overwrite` only when the new content is intended to be the complete updated report.
9. Run `validate-test-report` or rely on the helper's quality checks before treating the report as complete.
10. After the test report is saved, run `update-hub-indexes`, `validate-hub-state`, then use `commit-push-builder-main` to commit and push the builder repo changes to `main`.
11. Mention the saved test report path and commit/push result in the response.

## Helper Script

Use `scripts/save_test_report.py` to save a complete Markdown test report from stdin:

```bash
python3 /path/to/save-test-report/scripts/save_test_report.py \
  --root /path/to/builder \
  --title "Report Title" \
  <<'REPORT'
# Report Title

## Test Cases
...
REPORT
```

The script creates `docs/test-reports/` when needed and writes `YYYY-MM-DD-report-title.md`. It refuses to overwrite an existing report unless `--overwrite` is provided. Use `--date YYYY-MM-DD` only when the user asks to save a report for a specific date.

The script exits non-zero when required quality gates fail, including missing local runtime details, missing endpoint/UI interaction data, missing response output, missing pass/fail result, missing evidence, or unit-test-only evidence.

## Minimal Test Report Template

```markdown
# Title

## Document Status

## Story/Issue

## Branch

## App / Environment

## Local Run Details

## Test Cases

## Data Sent

## Response Received

## Pass / Fail

## Evidence

## Bugs / Follow-ups
```
