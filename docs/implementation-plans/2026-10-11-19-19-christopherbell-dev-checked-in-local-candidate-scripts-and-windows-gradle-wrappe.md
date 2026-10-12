# Checked-In Local Candidate Scripts and Windows Gradle Wrapper

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> christopherbell.dev ships scripts that start and stop an isolated local candidate, plus a Gradle wrapper that handles the JDK's Unix-socket directory on Windows. The README's manual candidate procedure and per-session environment workarounds go away.

## Background
The [Builder helper plan](2026-10-11-19-10-builder-deploy-aware-merges-and-shared-verification-helpers.md) left the spoke-owned pieces of the user's items 2 and 7 to this plan.

1. **Candidate procedure:** the README documents a roughly 90-line manual PowerShell procedure for starting a candidate against a disposable MongoDB. I re-ran it from a scratchpad copy, `start-candidate.ps1`, on every slice of the style migration. That copy also leaked the candidate's environment variables into the calling shell.
2. **Gradle sockets:** on this Windows host, Gradle in an agent shell cannot start its daemon unless `JAVA_TOOL_OPTIONS` moves the JDK's Unix-socket directory off `%TEMP%`. On 2026-10-11, with only `GRADLE_OPTS` set, the build failed: "A new daemon was started but could not be connected to." Builder's verify-local-app recommends `GRADLE_OPTS`, but that reaches only the client JVM. Every Gradle command therefore needed both variables, as recorded in session memory.

## Goals
- One command starts an isolated candidate and writes its state, and one command stops it and removes only what it created (AC-1, AC-3).
- Gradle runs on Windows through a checked-in wrapper with no manual environment setup (AC-2).
- The README and AGENTS.md point at the scripts (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing machine-wide settings such as `~/.gradle/gradle.properties` or user environment variables | They would change other Gradle projects and Java programs on the machine |
| A test ADMIN account | Delivered under its own security plan |
| Running the candidate on Linux or macOS | The documented flow and production are Windows |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `ops/local/Start-Candidate.ps1` starts a disposable loopback MongoDB on an OS-selected port and the built jar with exactly profile `test` on database `test`. It writes a JSON state file, waits for readiness, and leaves the caller's environment unchanged |
| AC-2 | `ops/local/Invoke-Gradle.ps1 <arguments>` runs the Gradle wrapper with a short Unix-socket directory in `JAVA_TOOL_OPTIONS` for that child only, and returns Gradle's exit code |
| AC-3 | `ops/local/Stop-Candidate.ps1` stops only the recorded process trees, confirms their ports are free, optionally copies logs, and removes only the temporary directories the start script created |
| AC-4 | Pester tests for the module's guards run in `automationPester`; `:website:check :cbell-lib:check :website:bootJar` passes through the wrapper; a test report records a real start, a readiness check and a stop |

## Inputs
- **Request:** "Fix 2, 3, 4, 5, 7", items 2 and 7.
- **Inspected at spoke `280b3c61`:**
  - `README.md` "Isolated MongoDB for Candidate Verification (Windows)".
  - The `AGENTS.md` isolated runtime section.
  - `website/build.gradle.kts`, for the Pester tasks and `automationPester`.
  - `.github/workflows/ci.yml`: Windows, with `gradlew build` running Pester.
  - The `ops/production/windows/tests` conventions.
- **Also inspected:** the scratchpad `start-candidate.ps1` and `stop-candidate.ps1`, and a 2026-10-11 probe of the Gradle daemon without `JAVA_TOOL_OPTIONS`.

## Branch
`claude/local-candidate-tooling-20261011` from spoke `origin/main` `280b3c61`.

## Assumptions
None.

## Open Questions
None.

## Design
- **`ops/local/CandidateRuntime.psm1`:**
  - `Resolve-MongodExecutable`: an explicit path, then `mongod.exe` on PATH, then the newest `%ProgramFiles%\MongoDB\Server\<version>\bin\mongod.exe`.
  - `Get-FreeLoopbackPort`: returns an OS-selected port, never 27017, 8080 or 8081.
  - `New-OwnedTemporaryDirectory` and `Test-OwnedTemporaryDirectory`: a direct child of a known parent named `<prefix><32 hex>`.
  - `Get-JdkSocketToolOptions`: the existing `JAVA_TOOL_OPTIONS` plus `-Djdk.net.unixdomain.tmpdir=<dir>`, unless one is already present.
- **`Start-Candidate.ps1`:**
  - Requires a built `website\build\libs\website.jar`.
  - Sets the candidate's environment (profile, URI, JWT secret, socket options and optional federation) only around `Start-Process` and restores the caller's values in `finally`.
  - Verifies that the MongoDB listener belongs to the launched process.
  - Writes PIDs, ports, the base URL, roots, log paths and readiness to the state file.
- **`Stop-Candidate.ps1`:**
  - Stops the recorded process trees, then reports the listeners on each port.
  - With `-LogDestination`, copies the candidate logs.
  - Removes the roots only when `Test-OwnedTemporaryDirectory` passes.
- **`Invoke-Gradle.ps1`:**
  - Uses `%SystemDrive%\Temp\jdk-unix-sockets`, a fixed directory so compatible daemons are reused.
  - Sets `JAVA_TOOL_OPTIONS` for the wrapper's child process, so the daemon and its forked test JVMs inherit it, and restores the old value afterwards.

## Expected Changes

| File | Change |
|---|---|
| `ops/local/CandidateRuntime.psm1` | New module |
| `ops/local/Start-Candidate.ps1`, `ops/local/Stop-Candidate.ps1`, `ops/local/Invoke-Gradle.ps1` | New scripts |
| `ops/local/tests/CandidateRuntime.Tests.ps1` | New Pester tests |
| `website/build.gradle.kts` | Add `ops/local` to the `automationPester` files and inputs |
| `README.md` | Replace the manual procedure with the scripts; Windows Gradle note |
| `AGENTS.md` | Isolated runtime section uses the scripts and wrapper |

## Task Breakdown

### Task 1 - Scripts, module and tests

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `ops/local/*` and `website/build.gradle.kts` |
| **Symbols** | `Resolve-MongodExecutable`, `Get-FreeLoopbackPort`, `New-OwnedTemporaryDirectory`, `Test-OwnedTemporaryDirectory`, `Get-JdkSocketToolOptions` |
| **Inspection** | Inputs |
| **Behavior** | As in Design |
| **Invariants** | Never port 27017 or the `christopherbell` database; never removes a path the scripts did not create; the caller's environment is unchanged |
| **Boundary/API** | New operator scripts |
| **Effects and failures** | Startup failure prints the candidate log tail and still writes the state file so stop can clean up |
| **Tests and evidence** | Pester for the module; a real run for the scripts |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 :website:automationPester` |

### Task 2 - Documentation

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 |
| **Files** | `README.md`, `AGENTS.md` |
| **Symbols** | None |
| **Inspection** | Inputs |
| **Behavior** | The docs describe the scripts and keep the isolation rules |
| **Invariants** | The isolation and cleanup rules stay stated |
| **Boundary/API** | None |
| **Effects and failures** | None |
| **Tests and evidence** | Review |
| **Verification** | Review |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Pester for the module's guards | verify-local-app: run Start-Candidate against the built jar; check readiness, `db.getName()` and the caller's unchanged environment |
| AC-2 | Full check through `Invoke-Gradle.ps1` with `JAVA_TOOL_OPTIONS` unset in the calling shell | Same |
| AC-3 | Pester | Stop-Candidate frees both ports and removes both roots; logs are copied |
| AC-4 | `automationPester`, full check | Test report |

## Rollback or Recovery
Revert the squash-merge commit. The scripts are operator tools, and the deployed application does not change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Stop removes the wrong directory | Very low | Removal requires a direct child of the expected parent with the generated name |

## Implementation Log

### 2026-10-11 - Candidate launched through cmd

- **Change:** `Start-Candidate.ps1` now starts the jar through `cmd /d /s /c` with `>` and `2>` redirection, not `Start-Process -RedirectStandardOutput`. `candidatePid` records the `cmd` launcher, and the stop script's tree kill still stops `java`.
- **Reason:** The first runtime run hung. With `Start-Process` redirection, `java` inherited the script's own output handles, so any caller capturing `Start-Candidate.ps1` output (here `record_run.py`) waited until the candidate exited. That candidate was ready in about 8 seconds and was stopped with `Stop-Candidate.ps1`, which freed both ports and removed both directories.
- **Impact:** Design for `Start-Candidate.ps1`; commit `e30f63f2`. The full check ran on `d88278d8`, which differs only in that launch; the runtime report covers `e30f63f2`.

### 2026-10-11 - Discarded runtime run with a broad log check

- **Change:** One runtime run was discarded. Its log check counted two OSHI `WARN` lines containing "Error 0x80070057" as errors.
- **Reason:** The harness's `Select-String` was case-insensitive. The check now matches only the `ERROR` log level.
- **Impact:** None on the product. The reported run has no ERROR-level lines.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
