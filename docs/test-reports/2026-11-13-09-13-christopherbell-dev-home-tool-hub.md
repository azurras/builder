# Public homepage tools hub: Test Report

## Story/Issue
Make the homepage a public tool hub with the Void as a secondary link.

## Branch
`codex/home-tool-hub-20261113` at candidate `905b462`

## Pass / Fail

> [!TIP]
> 1 of 1 cases passed on candidate `905b462`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Packaged homepage in Chrome | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Packaged homepage in Chrome**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\cbell-home-hub-905b4629\verify_home.py 905b4629369380ccdc6c874426e40b252211bff8`

## App / Environment

| Setting | Value |
|---|---|
| Base URL | http://127.0.0.1:60488 |
| Runtime | Java 25, test profile, local Chrome |
| MongoDB | 127.0.0.1:60487/test |

## Local Run Details
- **Local command:** `.\ops\local\Start-Candidate.ps1 -StateFile $stateFile -WithTestAdministrator -EnableSharedFolder`
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\cbell-home-hub-905b4629\verify_home.py 905b4629369380ccdc6c874426e40b252211bff8` in `A:\Projects\christopherbell.dev.worktrees\home-tool-hub`
- **Candidate identity:** `905b462`
- **Cleanup:** Stop-Candidate reported zero listeners on both ports and removed the disposable database and JDK socket directories.

## Data Sent

### 1. Packaged homepage in Chrome

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\cbell-home-hub-905b4629\verify_home.py 905b4629369380ccdc6c874426e40b252211bff8
```

## Response Received

### 1. Packaged homepage in Chrome

```text
exit code: 0
--- stdout ---
GET /actuator/info 200, candidate 905b4629369380ccdc6c874426e40b252211bff8; health UP; test MongoDB loopback:60487
GET / 200 at 1440x950: six direct cards, 3 columns, no horizontal overflow, secondary Void link, no feed polling
GET / 200 at 390x844: six direct cards, 1 columns, no horizontal overflow, secondary Void link, no feed polling
GET /wfl 200
GET /canes-box-tracker 200
GET /vin-decoder 200
GET /zip-coordinates 200
GET /site-monitor 200
GET /survive 200
GET /void 200
Signed in through the browser as isolated ADMIN: homepage Tools menu shows only the same six public routes
Signed-in Void page: Back Office and Shared Folder remain available in Tools
```

## Evidence
- Gradle :website:check and :website:bootJar passed before candidate startup. All 476 JavaScript tests passed.
- Chrome screenshots inspected at desktop and mobile widths. The initial browser probe used a string predicate disallowed by CSP. The repeat used DOM assertions with the same candidate and original CSP.
- Case 1 started 2026-11-13T09:12:35-06:00, took 1672 ms, candidate `905b462`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
