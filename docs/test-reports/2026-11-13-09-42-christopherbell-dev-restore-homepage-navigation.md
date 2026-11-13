# Restore authorized homepage navigation: Test Report

## Story/Issue
Restore admin and file-sharing links in the shared menu for authorized accounts. Keep the homepage cards public.

## Branch
`codex/restore-home-navigation-20261113` at candidate `98e1dbc`

## Pass / Fail

> [!TIP]
> 1 of 1 cases passed on candidate `98e1dbc`.

| # | Test case | Result | Why |
|---|---|---|---|
| 1 | Homepage navigation with guest and admin accounts | ✅ PASS | Expected exit code 0 |

## Test Cases
1. **Homepage navigation with guest and admin accounts**: command `python C:\Users\CHRIST~1\AppData\Local\Temp\cbell-home-nav-98e1dbce\verify_home.py 98e1dbce33ab14ee4c8fb1819a4b3fe284255ea2`

## App / Environment

| Setting | Value |
|---|---|
| Base URL | http://127.0.0.1:54800 |
| MongoDB | 127.0.0.1:54799/test |
| Runtime | Java 25, test profile, local Chrome |

## Local Run Details
- **Local command:** `python C:\Users\CHRIST~1\AppData\Local\Temp\cbell-home-nav-98e1dbce\verify_home.py 98e1dbce33ab14ee4c8fb1819a4b3fe284255ea2` in `A:\Projects\christopherbell.dev.worktrees\home-nav-restore`
- **Candidate identity:** `98e1dbc`
- **Cleanup:** Stopped the candidate and disposable MongoDB using Stop-Candidate.ps1.

## Data Sent

### 1. Homepage navigation with guest and admin accounts

```text
python C:\Users\CHRIST~1\AppData\Local\Temp\cbell-home-nav-98e1dbce\verify_home.py 98e1dbce33ab14ee4c8fb1819a4b3fe284255ea2
```

## Response Received

### 1. Homepage navigation with guest and admin accounts

```text
exit code: 0
--- stdout ---
GET /actuator/info 200, candidate 98e1dbce33ab14ee4c8fb1819a4b3fe284255ea2; health UP; test MongoDB loopback:54799
GET / 200 at 1440x950: six direct cards, 3 columns, no horizontal overflow, secondary Void link, no feed polling
GET / 200 at 390x844: six direct cards, 1 columns, no horizontal overflow, secondary Void link, no feed polling
GET /wfl 200
GET /canes-box-tracker 200
GET /vin-decoder 200
GET /zip-coordinates 200
GET /site-monitor 200
GET /survive 200
GET /void 200
Signed in through the browser as isolated ADMIN: homepage Tools menu shows six public routes plus Back Office, Command Center, Shared Folder, and Music
Signed-in Void page: Back Office and Shared Folder remain available in Tools
```

## Evidence
- Case 1 started 2026-11-13T09:41:54-06:00, took 4047 ms, candidate `98e1dbc`

## Bugs / Follow-ups
None

## Document Status
complete

## Project
christopherbell-dev
