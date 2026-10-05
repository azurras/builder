# Decode Git Output as UTF-8 for Spoke Preflight: Test Report

## Story/Issue
Builder workflow correction discovered while publishing the christopherbell.dev runtime report: Windows preflight misread UTF-8 report markers using the ANSI code page.

## Branch
main at 8d7e2b5

## Pass / Fail

> [!TIP]
> **3 of 3 passed** on Builder candidate 8d7e2b5.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Unicode Git output regression | ✅ PASS | A temporary Git repository round-tripped the committed ✅ PASS marker exactly. |
| 2 | Standard spoke preflight | ✅ PASS | Without Python UTF-8 mode overrides, preflight confirmed the published Builder report was identical to origin/main. |
| 3 | Builder hub validation | ✅ PASS | Hub indexes, paths, and schemas passed; only known historical-plan warnings remained. |

## Test Cases
1. **Unicode Git output regression:** committed a report marker to a temporary Git repository and read it back through the shared helper.
2. **Standard spoke preflight:** compared the published christopherbell.dev report with Builder origin/main using the normal Windows command.
3. **Builder hub validation:** checked Builder indexes, paths, links, metadata and document schemas.

## App / Environment

| Setting | Value |
|---|---|
| App | Builder spoke preflight CLI |
| OS / runtime | Windows 11, Python 3.12, Git |
| Candidate | Builder main commit 8d7e2b5 |
| Repository | A:\Projects\builder |
| Temporary fixture | Temporary Git repository containing one committed UTF-8 report |

## Local Run Details
- **Local CLI command:** python .agents/skills/publish-spoke-changes/scripts/preflight_spoke_pr.py --spoke christopherbell-dev --path A:\Projects\christopherbell.dev-worktrees\chris-street-style-audit-20261005 --report docs/test-reports/2026-10-05-08-15-christopherbell-dev-bootstrap-empty-isolated-website-test-databases.md
- **Working directory:** A:\Projects\builder
- **Candidate identity:** main at 8d7e2b5.
- **Cleanup:** unittest TemporaryDirectory removed the isolated Git fixture; no long-running processes were started.

## Data Sent

### 1. Unicode Git output regression

~~~text
Command arguments: python -m unittest discover -s .agents/skills/publish-spoke-changes/tests -v
Fixture report content: ✅ PASS
~~~

### 2. Standard spoke preflight

~~~text
Command arguments: --spoke christopherbell-dev --path A:\Projects\christopherbell.dev-worktrees\chris-street-style-audit-20261005 --report docs/test-reports/2026-10-05-08-15-christopherbell-dev-bootstrap-empty-isolated-website-test-databases.md
~~~

### 3. Builder hub validation

~~~text
Command arguments: python .agents/skills/publish-builder-changes/scripts/check_hub.py check --root .
~~~

## Response Received

### 1. Unicode Git output regression

~~~text
Exit status: 0
Ran 1 test in 0.233s
OK
~~~

### 2. Standard spoke preflight

~~~text
Exit status: 0
[pass] report: complete report
[pass] report project: christopherbell-dev
[pass] report published: identical on Builder origin/main
[pass] report names candidate: dd206c0ef2498e0d400eccce519990e8050bd021
Candidate dd206c0ef2498e0d400eccce519990e8050bd021 is ready.
~~~

### 3. Builder hub validation

~~~text
Exit status: 0
Hub indexes are current.
Hub state validation passed.
Warnings: eight existing historical plans predate the current quality schema.
~~~

## Evidence
- The pre-fix standard preflight returned “local report differs from Builder origin/main”; Python UTF-8 mode made it pass, confirming a default decoder mismatch.
- The regression test passed on committed Builder helper change 8d7e2b5.
- The normal preflight passed and recognized the report as identical after newline normalization.
- Hub validation passed after publication of the helper and test.

## Bugs / Follow-ups
None.

## Document Status
complete

## Project
builder
