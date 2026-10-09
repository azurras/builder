# Configuration Filters Conform to Chris Street Style

## Document Status
in-progress

## Objective

> [!IMPORTANT]
> The `configuration.filter` package conforms to write-chris-street-style-code, and rate limiting, request size limits, correlation IDs and static asset caching behave as before.

## Background
This is slice 18b of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). The split is listed in [slice 18a](2026-10-09-15-25-christopherbell-dev-configuration-root-mail-and-persistence-conform-to-chris-str.md). Inspection of the 7 filter files at `787a2812` found:

1. **`RateLimitFilter`:**
   - Three public constructors have no caller anywhere, and two of them hard-code `Clock.systemUTC()`.
   - The fallback rule restates every default of `RateLimitProperties.Rule` as literals.
   - A catch is named `ignored` although it handles overflow.
2. **`RequestSizeLimitFilter`:**
   - Two public constructors (no-argument and single limit) have no caller, and they carry hard-coded 1 MB and 8 MiB defaults that the class Javadoc advertises.
   - Two wrappers repeat the same reader construction.
   - A fully qualified `java.util.regex.Pattern`.
   - Single-letter catch names.
3. **`RateLimitBucketStore`:** two catches are named `ignored` although they saturate on overflow.
4. **Conforming:** `ApiErrorResponseWriter`, `RequestCorrelationFilter`, `RequestPayloadTooLargeException` and `VersionedStaticAssetCacheFilter`.

## Goals
- Every filter file has a recorded verdict and conforms (AC-1, AC-2).
- Rate limiting and size limits behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| The production `RateLimitFilter` bean passing `Clock.systemUTC()` in `SecurityConfig` | `SecurityConfig` is slice 18c, which will inject the application `Clock` |
| The test-only convenience constructors that keep a system clock or default writer | They are the seams `RateLimitFilterTest` and `SharedFolderUploadServiceTest` use |
| The bucket store's `System::nanoTime` ticker | A monotonic ticker for token refill, not wall-clock time |
| Rule values, limits and response bodies | Security behavior |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every filter file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the rate-limit headers appear on a response; repeated login attempts are throttled at the `auth-mutations` limit with `Retry-After` and the `RATE_LIMITED` body; a JSON body over the default size limit gets 413 with `REQUEST_TOO_LARGE`; and responses carry `X-Request-Id` |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 18; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `787a2812`:
  - All 7 `configuration/filter` files.
  - Every `new RateLimitFilter(` and `new RequestSizeLimitFilter(` call in main and test sources.
  - `RateLimitFilterTest`, `RequestSizeLimitFilterTest`, `filter/RateLimitBucketStoreTest`, `filter/RequestCorrelationFilterTest` and `SharedFolderUploadServiceTest`.

## Branch
`claude/style-config-filter-20261009` from spoke `origin/main` `787a2812`.

## Assumptions
None.

## Open Questions
None.

## Design
- **Unused constructors:** they are removed, and with them the hard-coded defaults.
- **Fallback rule:** `new RateLimitProperties.Rule()` returns the same name, capacity, window, methods and paths.
- **`readerFor(request, body)`:** decodes a body in its declared charset or UTF-8, and both request wrappers call it.
- **Catch names:** they say what they handle.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitFilter.java` | changed | Unused constructors removed; default rule reused; catch name |
| `website/src/main/java/dev/christopherbell/configuration/filter/RequestSizeLimitFilter.java` | changed | Unused constructors and defaults removed; true Javadoc; shared reader helper; imported `Pattern`; catch names |
| `website/src/main/java/dev/christopherbell/configuration/filter/RateLimitBucketStore.java` | changed | Catch names |
| `ApiErrorResponseWriter`, `RequestCorrelationFilter`, `RequestPayloadTooLargeException`, `VersionedStaticAssetCacheFilter` | conforming | No change |
| `RateLimitFilterTest`, `RequestSizeLimitFilterTest`, `filter/RateLimitBucketStoreTest`, `filter/RequestCorrelationFilterTest` | conforming | No change; they pass unchanged |

## Task Breakdown

### Task 1 - Conform the configuration filters

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `RateLimitFilter` constructors and `matchingRule`; `RequestSizeLimitFilter` constructors and `readerFor`; `RateLimitBucketStore.positiveNanos`, `saturatingAdd` |
| **Inspection** | All files in Inputs at `787a2812` |
| **Behavior** | Same buckets, headers, rejections, limits and decoding |
| **Invariants** | Rule names, limits, status codes and error codes unchanged |
| **Boundary/API** | Five uncalled public constructors removed |
| **Effects and failures** | None new |
| **Tests and evidence** | Configuration, shared-folder upload and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Filter and bucket store tests | verify-local-app: the requests in AC-3 against the candidate |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A removed constructor had a reflective caller | Low | Spring builds both filters through `SecurityConfig` bean methods with the remaining constructors; the candidate start proves it |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 18a was in its full check.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
