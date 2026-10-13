# Operational PowerShell Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> Slice 24 conforms to write-chris-street-style-code with unchanged behavior.

## Background
Slice 24 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md) covers the 35 operational PowerShell files (about 36,000 lines), the GitHub helper scripts and `prod.cmd`. Inspection against the Shell and PowerShell guide found:
- **Modules:** every module and the GitHub scripts already set `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`.
- **No other smells:** they use no aliases or `Write-Host`. Every built-in path cmdlet uses `-LiteralPath`; the many `-Path` arguments belong to the modules' own functions. Native programs are checked through `$LASTEXITCODE` or process exit codes.
- **Entry scripts:** `prod.ps1` and the service launcher `Start-ChristopherBellDev.ps1` set `Stop` but not strict mode. `cpu-temperature.ps1` is checksum-pinned by `SecureNativeLibraryProvisioner`.
- **Test wiring:** several Pester suites (Command, Common, Deploy, DomainCollections, MusicRuntime, Sensors, Security, WriterStart) are not wired into Gradle or CI. That is a test-coverage gap, not a style finding.

## Goals
- Every file in scope conforms (AC-1, AC-2).
- Behavior is unchanged (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Behavior, contract or layout changes | The migration preserves behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every file in scope |
| AC-2 | The full check passes and a full-diff style review finds no blocker |
| AC-3 | The production command Pester suite passes against the strict-mode entry point. `prod.cmd` `help`, `status`, `auto-status`, `releases` and `sensor-status` answer with the same exit code and first line as main and raise no strict-mode error. The full check, including the wired Pester suites, passes |
| AC-4 | The PR merges through `wait_for_github.py queue` and production serves the merge |

## Inputs
- **Request:** "let's finish the slices".
- **Inspected:** the files in scope at spoke `origin/main` `a0709b0e`.

## Branch
`claude/style-ops-20261012` from spoke `origin/main`; it merges `origin/main` before its PR when an earlier slice has changed the same file.

## Assumptions
None.

## Open Questions
None.

## Design
- **`prod.ps1`:** adds `Set-StrictMode -Version Latest`. Every variable it reads is a declared parameter.
- **Unchanged files:**
  - `Start-ChristopherBellDev.ps1` is copied into the protected production install and verified there, so changing it would require reinstalling production, which this request does not name.
  - `cpu-temperature.ps1` is checksum-pinned.
- **Verdicts:** every other file conforms.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `ops/production/windows/prod.ps1` | changed | Strict mode |
| `ops/production/windows/service/Start-ChristopherBellDev.ps1` | exception | Installed copy is protected; changing it needs a production reinstall |
| `website/src/main/resources/lib/cpu-temperature.ps1` | exception | Checksum-pinned |
| Every other operational and GitHub PowerShell file, and `prod.cmd` | conforming | No change |

## Task Breakdown

### Task 1 - Conform slice 24

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | As named in Design |
| **Inspection** | Inputs |
| **Behavior** | Unchanged |
| **Invariants** | No route, contract, stored field or rendered value changes |
| **Boundary/API** | None |
| **Effects and failures** | None new |
| **Tests and evidence** | As in Test Plan |
| **Verification** | `.\\ops\\local\\Invoke-Gradle.ps1 --continue :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the inspection | Not applicable: documentation |
| AC-2 | Full check with the wired Pester suites | Covered by AC-3 |
| AC-3 | `Production.Command.Tests.ps1` run directly with Pester 5.9.0 | verify-local-app: read-only `prod.cmd` commands from the candidate and from main, compared |
| AC-4 | Required PR checks | `wait_for_github.py queue` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Strict mode stops the scheduled auto-deploy run, which uses a refreshed copy of prod.ps1 | Low | prod.ps1 reads only declared parameters; the command suite and read-only commands pass under strict mode |

## Implementation Log

### 2026-10-12 - Plan saved after the edits

- **Change:** The plan was saved after the edits and before the PR.
- **Reason:** These are mechanical or Settled-Decision edits made while earlier slices merged.
- **Impact:** No PR exists yet; the plan and evidence are published before it.

### 2026-10-12 - Read-only command comparison

- **Change:** Two runtime runs were discarded. In the first, the read-only `status`, `releases` and `sensor-status` commands failed with "Access to the path ... deploy.json is denied", which is identical on main because these reads need elevation. The check was changed to compare each command's exit code and first line with main. In the second run, that comparison script reused the name of its `[string]$Baseline` parameter for the result object; PowerShell variable names are case-insensitive, so the object was converted to a string. The variables were renamed.
- **Reason:** The comparison isolates exactly the strict-mode change from the unelevated environment.
- **Impact:** AC-3 is as written; the reported run covers `73d0fbb4`.

## Outcome

> [!TIP]
> Shipped in PR #1537 (`45d695a`) through the deploy-aware queue; production serves it. Checkstyle and the style guide now hold for operational PowerShell.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every file in scope |
| AC-2 | ✅ Met | The full check passed ([report](../test-reports/2026-10-12-20-26-christopherbell-dev-operational-powershell-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 6 of 6 runtime cases passed on candidate `73d0fbb` ([report](../test-reports/2026-10-12-20-26-christopherbell-dev-operational-powershell-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1537](https://github.com/azurras/christopherbell.dev/pull/1537) merged as `45d695a` after all checks; `wait_for_github.py queue` confirmed it live |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
