---
name: validate-test-report
description: Use when reviewing, saving, or closing work from a Builder local app test report that must prove what was tested, what data was sent, what response was received, pass/fail status, and evidence.
---

# Validate Test Report

## Overview

Reject incomplete local app test reports before closure. A report is only complete when it proves the app was run locally and exercised through an endpoint, browser/UI flow, local webhook, CLI-to-app path, or comparable runtime interaction. Unit test output alone is not a test report.

## Workflow

1. Read the test report Markdown.
2. Run the helper script below.
3. Treat missing local runtime details, request/UI input data, response/UI output data, pass/fail result, or evidence as a blocker for story/issue closure.
4. Reject reports whose only evidence is `npm test`, `pytest`, `./gradlew test`, `mvn test`, or another unit-test command.

## Helper Script

```bash
python3 .agents/skills/validate-test-report/scripts/validate_test_report.py \
  docs/test-reports/YYYY-MM-DD-title.md
```

The script exits non-zero when required sections or runtime evidence fields are missing, or when the report only contains automated unit test evidence.
