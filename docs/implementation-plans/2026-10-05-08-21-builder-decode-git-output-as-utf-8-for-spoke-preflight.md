# Decode Git Output as UTF-8 for Spoke Preflight

## Document Status
ready-for-execution

## Objective

> [!IMPORTANT]
> Make spoke PR preflight compare published report text accurately on Windows by decoding Git output as UTF-8, including emoji result markers.

## Background
The spoke preflight reads a UTF-8 Builder report and compares it with git show origin/main:<report>. Python's default Windows subprocess decoding used the ANSI code page for Git's UTF-8 bytes, turning ✅ into mojibake and falsely reporting a published report as different. Running the helper in Python UTF-8 mode masked the defect but did not fix the default workflow.

## Goals
- Decode Git text output as UTF-8 consistently on Windows and other hosts (AC-1).
- Add a regression test that fails when Git UTF-8 text is decoded using the system code page (AC-2).
- Run the normal spoke preflight command successfully against the already published Unicode test report (AC-3).
- Publish the helper and its regression test to Builder origin/main (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Rewriting every Builder subprocess call | Scope is the shared Git text helper used by preflight and repository inspection. |
| Changing report contents or removing emoji markers | These markers are part of the published report format. |
| Modifying the website spoke candidate | The application candidate is already verified and committed. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | The shared Git helper decodes git show output as UTF-8 regardless of Windows locale defaults. |
| AC-2 | A native Python regression test preserves ✅ PASS from a committed temporary Git file. |
| AC-3 | The regular preflight invocation, without -X utf8, confirms the Builder report is identical to origin/main. |
| AC-4 | The helper and regression test are committed and read back on Builder origin/main. |

## Inputs
- **Request:** User approved fixing issues discovered to complete the christopherbell.dev style audit and asked that future agents not encounter the runtime blocker.
- **Inspected:** Builder AGENTS.md, .agents/lib/spoke_state.py, preflight_spoke_pr.py, report validator, and the published report comparison at Builder commit 4f6c75d.
- **Observed:** Default Python subprocess decoding changed the UTF-8 checkmark from ✅ to âœ…; the same preflight passed under python -X utf8.

## Branch
Builder primary checkout on main, based on origin/main at 4f6c75d.

## Assumptions
- Git writes repository text as UTF-8; paths with unusual characters are quoted or emitted as UTF-8 under the current repository configuration.
- The existing shared git() helper is the narrow common boundary for text-returning Git commands.

## Open Questions
None.

## Design
Set encoding="utf-8" in .agents/lib/spoke_state.py's shared text-mode subprocess.run call. Add a standard-library unittest that creates a temporary Git repository, commits a report containing ✅ PASS, and verifies the helper returns the exact Unicode text. Then rerun the standard preflight without a Python UTF-8 mode override.

| Alternative | Why not |
|---|---|
| Require each Windows agent to use python -X utf8 | Hides a helper defect and is easy to omit. |
| Strip or ASCII-encode report markers | Damages the report format to accommodate incorrect decoding. |

## Expected Changes
| File or area | Change |
|---|---|
| .agents/lib/spoke_state.py | Decode all shared Git text output explicitly as UTF-8. |
| .agents/skills/publish-spoke-changes/tests/test_spoke_state.py | Add a regression test for Unicode output from a temporary committed Git file. |

## Task Breakdown

### Task 1 - Make Git text decoding explicit

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None. |
| **Files** | .agents/lib/spoke_state.py; new .agents/skills/publish-spoke-changes/tests/test_spoke_state.py. |
| **Symbols** | spoke_state.git; a unittest for Unicode Git output. |
| **Inspection** | Read the current shared helper, all current callers, and the preflight comparison at Builder 4f6c75d. |
| **Behavior** | Text returned by Git preserves Unicode bytes as UTF-8 on Windows and other hosts. |
| **Invariants** | Git errors remain explicit; repository contents and report format stay unchanged. |
| **Boundary/API** | Keep git(repo, *args) -> str signature and trimming behavior unchanged. |
| **Effects and failures** | Git remains a read-only subprocess; strict decoding exposes invalid output instead of silently corrupting text. |
| **Tests and evidence** | A temporary Git repository with committed ✅ PASS text fails before the fix and passes after; normal preflight confirms the published report. |
| **Verification** | python -m unittest discover -s .agents/skills/publish-spoke-changes/tests -v; run the standard preflight command without UTF-8 flags. |

## Test Plan
| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Regression unittest and existing Builder hub check. | No application runtime applies: this is a read-only Builder Git helper; exercise the real preflight command. |
| AC-2 | Temporary Git repository test proves exact UTF-8 output. | Not applicable; no runnable application. |
| AC-3 | Standard preflight reports published report identical to Builder origin/main. | Not applicable; no application process or external service is required. |
| AC-4 | Builder hub check and publication helper validation. | Read back the committed helper and test from origin/main. |

Regression cases: Unicode result markers round-trip exactly; ordinary ASCII Git output still passes; Git failures retain their nonzero error path.

## Rollback or Recovery
Revert the one helper change and its regression test. No repository data or remote state is modified by the helper.

## Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A Git error message uses a legacy encoding | Low | Git's supported Windows output is UTF-8 in this repository; retain command and return-code diagnostics, and run the existing helper consumers. |

## Implementation Log

### 2026-10-05 - Preserve Git's UTF-8 report output

- **Change:** Added explicit UTF-8 decoding to the shared Git text helper and a temporary-repository unittest that commits and reads back a Unicode report marker.
- **Reason:** On Windows the helper otherwise decoded Git's UTF-8 bytes as the local ANSI code page, causing a false published-report mismatch.
- **Impact:** The new unittest passed and the normal spoke preflight command (without a Python UTF-8 mode override) now confirms the published report is identical to Builder origin/main. This Builder helper has no application runtime; native CLI checks cover its behavior.

## Outcome
Pending.

## Project
builder

## Plan Format
task-contract-v2
