# Separate Survive movement and command rate limits

## Document Status
ready-for-review

## Objective
Let a group on a shared network move at the normal browser cadence without exhausting their game command quota.

## Background
The isolated camp workload hit the generic API mutation budget. At 20 sessions it returned 420 throttles out of 480 measured movement requests on 48d17010. A leave request was also throttled. The default mutation bucket allows 300 requests per minute per IP, and each active browser can send 120 movement requests per minute.

## Goals
- Move the exact movement POST into its own bounded IP budget (AC-1).
- Verify the plan's 2, 5, 10 and 20 session camp workload and keep leave and commands available (AC-2).

## Non-Goals
| Area | Scope |
|---|---|
| Capacity claims | This measures a clustered loopback workload. Geographic distribution, full party commands and long sessions have separate acceptance checks. |

## Acceptance Criteria
| ID | Done when |
|---|---|
| AC-1 | The movement POST has a bounded dedicated bucket. Saturating it still permits an action and leave on the same IP. Missing, forged and expired owner credentials never read Mongo for movement. |
| AC-2 | 20 clustered sessions at 2 Hz complete the measured stages, with percentiles, errors and Mongo counts recorded. |
| AC-3 | Native checks, isolated candidate proof, report, CI and deployment are recorded. |

## Inputs
- Parent PERF-01 and AC-6 in 2026-11-05-14-54-christopherbell-dev-survive-final-fantasy-xi-parity.md.
- Current main bf51abaf, RateLimitProperties, RateLimitFilter and Survive movement cadence.

## Branch
The experiment started on codex/survive-movement-rate-limit at bf51abaf. The release candidate is codex/survive-movement-admission-compat, integrated with e5d948e2.

## Assumptions
20 browsers at 2 Hz offer 40 requests per second. The proposed movement budget refills at 50 per second with a 250-request burst, below the old generic 300-request burst on that route.

## Open Questions
Production sizing and distributed clients remain part of the parent performance plan.

## Design
Insert a default rate rule for POST /api/survive/v1/movement before the generic mutation rule. Reuse IP resolution and the existing bounded bucket store. Reject unrecognized or expired owners against a published index of durable saves before the world monitor. Recheck under the monitor and after the version-checked read. Leave, game actions, and unrelated endpoints retain their current rules.

## Expected Changes
| Area | Change |
|---|---|
| Rate limit defaults | Dedicated 250-request, five-second movement rule |
| Rate limit filter tests | Saturation, independent command and leave budget, and exact route matching |
| Configuration documentation | Document the cadence, budget and dedicated route |

## Task Breakdown
### Task 1 - Isolate the movement quota
Required skill: write-chris-street-style-code
| Contract | Detail |
|---|---|
| Dependencies | Existing rate filter and bucket store |
| Files | RateLimitProperties.java, RateLimitFilterTest.java, configuration README |
| Symbols | RateLimitProperties.defaultRules |
| Inspection | Follow first-match route and IP bucket selection |
| Behavior | Normal movement is bounded separately from game commands |
| Invariants | Scope is exact POST movement path. Existing bucket storage limit, error body and owner checks still apply. |
| Boundary/API | Existing rate-limit rule configuration and response headers |
| Effects and failures | Movement can still return 429 with Retry-After when the dedicated bucket is exhausted |
| Tests and evidence | Filter regression before and after plus isolated workload with the exact candidate |
| Verification | Targeted rate tests, full Java suite, exact bootJar and camp workload |

## Test Plan
| AC | Check |
|---|---|
| AC-1 | Filter tests for exhaustion and independent command/leave allowance |
| AC-2 | Loopback baseline and candidate with normal limits, 2, 5, 10 and 20 independent cookies |
| AC-3 | Published report, CI and production readback |

## Rollback or Recovery
Revert the dedicated rule. No data migration.

## Risks
The dedicated refill admits more invalid HTTP requests to the cheap owner check. The owner index must keep these requests outside the world lock and Mongo. A fresh process needs a join or status read before movement resumes.

## Implementation Log

### 2026-11-07 - Hold the higher quota pending owner admission

- **Change:** Tested the dedicated rule and commissioned a read-only review of its admission boundary.
- **Reason:** The original rule capped legitimate group movement. The higher candidate refill also admits invalid survivor requests before the existing database-backed owner check.
- **Impact:** AC-2 passed for the short legitimate workload. AC-1 still needs an admission check that prevents missing and forged credentials from repeatedly reaching Mongo at the higher quota. Preserve compatibility for active sessions and the normal owner check after admission. Add a zero-Mongo regression for invalid input and assert the production quota values before rerunning. AC-3 awaits a corrected candidate. [Runtime report](../test-reports/2026-11-07-12-40-christopherbell-dev-survive-shared-network-movement-quota.md)

### 2026-11-07 - Admit movement from the durable owner index

- **Change:** Add a lock-free admission check over owner keys and last-seen timestamps from the last durable snapshot. Recheck while holding the monitor, then keep the version check and durable owner validation.
- **Reason:** Invalid or expired credentials must fail before the shared game monitor and Mongo. Using the existing status read avoids adding a second credential and leaves one authoritative saved owner.
- **Impact:** After a cold restart, a join or game read primes the index before movement. The browser already reads the game on entry and during play. Direct movement clients need the same bootstrap. Treat persisted guest spellings as durable keys so a legacy UUID cannot break another player's status. Verify zero Mongo accesses on missing, malformed and forged credentials with the profiler and repeat the fixed legitimate workload.

### 2026-11-07 - Verify owner admission and legacy saves

- **Change:** Added durable owner admission ahead of the dedicated movement budget's database path. Fixed compatibility with legacy persisted UUID spellings.
- **Reason:** Unknown and expired credentials should stop before the shared game monitor or Mongo. Movement still verifies the latest owner after admission.
- **Impact:** Final candidate 33e8270b accepted 888 of 888 pulses and all departures in the short ladder. The positive control accessed the world once, and 102 invalid credentials accessed it zero times. The full native suites and isolated proof passed. Release and longer workloads remain open. [Child plan](2026-11-07-12-34-christopherbell-dev-survive-movement-rate-limit.md) · [Runtime report](../test-reports/2026-11-07-12-40-christopherbell-dev-survive-shared-network-movement-quota.md)

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
