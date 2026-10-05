# Make Plans and Test Reports Pleasant to Read: Test Report

## Story/Issue
User request on 2026-10-04: make the implementation plan and test report pleasant for humans to read. [Plan](../implementation-plans/2026-10-04-make-plans-and-test-reports-pleasant-to-read.md).

## Branch
Builder `main` at `d769e30`

## Pass / Fail

> [!TIP]
> **6 of 6 passed** on candidate `d769e30`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Save the new report example through PowerShell | ✅ PASS | Exit code 0; the stored table keeps `✅ PASS` |
| 2 | Save the new plan example through PowerShell | ✅ PASS | Exit code 0; the stored Outcome keeps `✅ Met` |
| 3 | Reject an empty contract table cell | ✅ PASS | Exit code 1 with `Task 1 missing Behavior` |
| 4 | Validate the new examples and older real documents | ✅ PASS | Both validators exit 0 for the new examples and the earlier-format plan and report |
| 5 | Hub check over every document | ✅ PASS | `Hub state validation passed.` over 206 plans and reports |
| 6 | Native test suite | ✅ PASS | 113 tests OK |

Case 1 was first run against `e9385e6` through a bash pipe and stored `âœ…` instead of `✅`. Commit `d769e30` fixed that; see the plan's log entry "Read helper stdin as UTF-8".

## Test Cases
1. **Save the new report example through PowerShell:** `save_test_report.py` stores a verdict-first report with result markers intact.
2. **Save the new plan example through PowerShell:** `save_implementation_plan.py` stores a plan with table contracts and result markers intact.
3. **Reject an empty contract table cell:** the widened validator still refuses a table-form task with no Behavior.
4. **Validate the new examples and older real documents:** the validators accept the new layout and the existing plain layout.
5. **Hub check over every document:** no existing plan or report changes verdict.
6. **Native test suite:** the full `.agents/tests` suite.

## App / Environment

| Setting | Value |
|---|---|
| App | Builder helper scripts (no runnable application; the helpers are the runtime surface) |
| Shell | PowerShell 7.6.6 for cases 1 to 3; Git Bash for cases 4 to 6 |
| Python stdin encoding | `cp1252` (console default on this machine) |
| Fixture root | Scratchpad folder `probe-d769e30` with a copy of `spokes.json`; the examples' project changed to `builder` |

## Local Run Details
- **Local command:** `$report | python .agents/skills/write-test-report/scripts/save_test_report.py --root $root --date 2099-04-05 --title 'Example probe'`
- **Working directory:** the primary Builder checkout at `d769e30`.
- **Logs:** console output, captured below.
- **Cleanup:** the probe documents stay in the session scratchpad only; nothing was written under `docs/`.

## Data Sent

### 1. Save the new report example through PowerShell

```text
stdin: .agents/skills/write-test-report/references/example.md with "example-app" replaced by "builder"
Command arguments: --root <probe> --date 2099-04-05 --title 'Example probe'
```

### 2. Save the new plan example through PowerShell

```text
stdin: .agents/skills/write-implementation-plan/references/example.md with "example-app" replaced by "builder"
Command arguments: --root <probe> --date 2099-04-05 --title 'Example probe'
```

### 3. Reject an empty contract table cell

```text
stdin: the plan example with its Behavior row replaced by "| **Behavior** | |"
Command: python .agents/skills/write-implementation-plan/scripts/validate_implementation_plan.py
```

### 4. Validate the new examples and older real documents

```text
Command arguments: validate_implementation_plan.py references/example.md docs/implementation-plans/2026-10-04-repair-the-historical-migration-audit.md
Command arguments: validate_test_report.py references/example.md docs/test-reports/2026-10-04-christopherbell-dev-chris-street-style-audit.md
```

### 5. Hub check over every document

```text
Command arguments: check_hub.py check --root .
```

### 6. Native test suite

```text
Command arguments: python -m unittest discover -s .agents/tests
```

## Response Received

### 1. Save the new report example through PowerShell

```text
...\probe-d769e30\docs\test-reports\2099-04-05-builder-example-probe.md
exit code: 0
| 1 | Health with the secret set | ✅ PASS | `/actuator/health` returned 200 `{"status":"UP"}` |
| 2 | Startup without the secret | ✅ PASS | Startup stopped with `JWT_SECRET is required`; the value never appeared |
```

### 2. Save the new plan example through PowerShell

```text
...\probe-d769e30\docs\implementation-plans\2099-04-05-builder-example-probe.md
exit code: 0
| AC-1 | ✅ Met | Startup fails with "JWT_SECRET is required"; test report `2026-10-04-example-app-require-jwt-secret.md` |
```

### 3. Reject an empty contract table cell

```text
Implementation plan quality checks failed:
- Task 1 missing Behavior: supply a task contract or legacy Code Edit block
exit code: 1
```

### 4. Validate the new examples and older real documents

```text
Implementation plan quality checks passed.
exit code: 0
Test report quality checks passed.
exit code: 0
```

### 5. Hub check over every document

```text
Hub state validation passed.
```

### 6. Native test suite

```text
Ran 113 tests in 42.011s
OK
```

## Evidence
- Cases 1 to 3 ran at 21:53 CDT on `d769e30` in PowerShell 7.6.6; cases 4 to 6 followed on the same commit.
- Before `d769e30`, the same save stored `| 1 | Health with the secret set | âœ… PASS |` (observed at `e9385e6`), which is why the stdin fix exists.
- Both new examples were rendered with GitHub's Markdown API (`gh api -X POST markdown`, `gfm` mode) and viewed in the browser pane: callouts render as colored alert boxes, tables and markers display, and the report opens with its verdict.

## Bugs / Follow-ups
- Windows PowerShell 5.1 sends ASCII to native programs by default, so markers would arrive as `?` there. The documented shell is PowerShell 7, which sends UTF-8.

## Document Status
complete

## Project
builder
