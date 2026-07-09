---
name: validate-test-report
description: Use when reviewing, saving, or closing work from a Builder local app test report that must prove what was tested, what data was sent, what response was received, pass/fail status, and evidence.
---

# Validate Test Report

## Overview

Reject incomplete local app test reports before closure. A report is only complete when it records the tested story/issue, branch, app/environment, local run details, test cases, data sent, responses received, pass/fail result, evidence, and follow-ups.

## Workflow

1. Read the test report Markdown.
2. Run the helper script below.
3. Treat missing request data, response data, pass/fail result, or evidence as a blocker for story/issue closure.

## Helper Script

```bash
python3 .agents/skills/validate-test-report/scripts/validate_test_report.py \
  docs/test-reports/YYYY-MM-DD-title.md
```

The script exits non-zero when required sections or evidence fields are missing.
