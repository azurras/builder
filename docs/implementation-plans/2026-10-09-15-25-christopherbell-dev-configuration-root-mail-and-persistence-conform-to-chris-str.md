# Configuration Root, Mail and Persistence Conform to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> The `configuration` root, `mail` and `persistence` packages conform to write-chris-street-style-code, and startup validation, client IP resolution, sitemaps and media retention cleanup behave as before.

## Background
This is slice 18a of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Slice 18 (`configuration`, 90 main files, 8,297 lines) is split by subpackage, smallest first:

| Part | Scope |
|---|---|
| 18a | Root (15 files), `mail` (2) and `persistence` (4) |
| 18b | `filter` (7) |
| 18c | `security` (17) |
| 18d | `mongo` (45), split further when planned |

Inspection at `67abb24d` found:

1. **`MediaPersistenceRetentionCleanupJob`:** its Spring constructor creates `Clock.systemUTC()` instead of taking the application `Clock`, and a validation check is a one-line `if`.
2. **`FederationSecretApplicationContextInitializer`:** it recognizes its own failures by searching an exception message for a property name.
3. **`ClientIpResolver`:**
   - Seven one-line `if` statements.
   - Unnamed IPv4 and IPv6 prefix lengths and octet limit.
   - IPv4 parsing inlined in the literal check.
4. **`ProductionSettingsApplicationContextInitializer`:** an unnamed minimum JWT secret length and a catch named `ignored` that is not ignored.
5. **`SharedFolderCatalogProperties`:** an unnamed page-size limit beside its named siblings.
6. **`PublicSitemapService` and three tests:** fully qualified names.

## Goals
- Every file in these packages has a recorded verdict and conforms (AC-1, AC-2).
- Startup, client IP resolution and sitemaps behave as before at runtime (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| The production secret path literal in the federation initializer | It is a deliberate security allow-list for one machine, not a portable configuration value |
| Rate-limit rule values | Product and security behavior |
| `filter`, `security` and `mongo` | Slices 18b to 18d |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every file in the three packages |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test`, the published test report records that the candidate starts with the cleanup job wired to the application `Clock` and logs no errors; `robots.txt` is byte-identical to production; and `sitemap.xml` is a URL set that lists production's static public URLs |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 18; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `67abb24d`:
  - All 21 files in the three packages.
  - Their tests: `ClientIpResolverTest`, `FederationSecretApplicationContextInitializerTest`, `ProductionSettingsApplicationContextInitializerTest`, `PublicSitemapServiceTest`, `MediaPersistenceRetentionCleanupJobTest` and the properties tests.
  - The cleanup job's only test, which uses the package-private constructor.

## Branch
`claude/style-config-small-20261009` from spoke `origin/main` `67abb24d`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`.

## Open Questions
None.

## Design
- **Cleanup job:** its Spring constructor takes the application `Clock`.
- **Federation initializer:** a private `InvalidSecretFileException extends IllegalStateException` marks the initializer's own explanations, which are rethrown as is; every other failure is wrapped as before. Callers still see an `IllegalStateException` with the same message.
- **Client IP resolver:** `isIpv4Literal` holds the dotted-quad rule. `IPV4_PREFIX_BITS`, `IPV6_PREFIX_BITS` and `MAX_OCTET` name the limits.
- **Production settings:** `MIN_JWT_SECRET_LENGTH`.
- **Catalog properties:** `MAX_PAGE_SIZE_LIMIT`.

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/configuration/persistence/MediaPersistenceRetentionCleanupJob.java` | changed | Injected `Clock`; block `if` |
| `website/src/main/java/dev/christopherbell/configuration/FederationSecretApplicationContextInitializer.java` | changed | Typed own-failure exception |
| `website/src/main/java/dev/christopherbell/configuration/ClientIpResolver.java` | changed | Block `if`s, named limits, `isIpv4Literal` |
| `website/src/main/java/dev/christopherbell/configuration/ProductionSettingsApplicationContextInitializer.java` | changed | Named minimum; catch name |
| `website/src/main/java/dev/christopherbell/configuration/SharedFolderCatalogProperties.java` | changed | Named limit |
| `website/src/main/java/dev/christopherbell/configuration/PublicSitemapService.java` | changed | Imported names |
| The other 15 files (`ApplicationClockConfiguration`, `ClientIpProperties`, `SchedulingConfiguration`, `ApiUtilProperties`, `RequestSizeProperties`, `SharedFolderConfiguration`, `PublicMetadataController`, `SharedFolderProperties`, `SharedFolderMediaProperties`, `RateLimitProperties`, `mail/MailConfiguration`, `mail/MailProperties`, `persistence/MediaPersistenceCleanupResult`, `persistence/MongoBackendComponent`, `persistence/MongoPersistence`) | conforming | No change |
| `website/src/test/java/dev/christopherbell/configuration/ClientIpResolverTest.java`, `FederationSecretApplicationContextInitializerTest.java`, `PublicSitemapServiceTest.java` | changed | Imported names |
| The other tests for these packages | conforming | No change |

## Task Breakdown

### Task 1 - Conform configuration root, mail and persistence

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `MediaPersistenceRetentionCleanupJob`; `FederationSecretApplicationContextInitializer.initialize`, `InvalidSecretFileException`; `ClientIpResolver.isIpLiteral`, `isIpv4Literal`; `ProductionSettingsApplicationContextInitializer.validateJwt` |
| **Inspection** | All files in Inputs at `67abb24d` |
| **Behavior** | Same validations, messages, resolved addresses, sitemaps and cleanup batches |
| **Invariants** | Configuration keys, routes and exception types seen by callers unchanged |
| **Boundary/API** | The cleanup job's Spring constructor gains `Clock` |
| **Effects and failures** | None new |
| **Tests and evidence** | Configuration and architecture suites; runtime below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Resolver, initializer, sitemap and cleanup tests | verify-local-app: startup log, `robots.txt` and `sitemap.xml` compared with production. Client IP resolution behind the production proxy cannot be reproduced locally, so `ClientIpResolverTest` covers it. The production-only initializers run only under the `prod` profile, which a local candidate must not use, so their tests cover them |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| A forwarded address resolves differently | Low | `ClientIpResolverTest` covers trusted, untrusted, malformed and IPv6 hops; the rules are unchanged |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the edits, while slice 17 parts were in CI.
- **Reason:** I worked ahead on files that no open slice touches.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - First runtime run discarded

- **Change:** The first run of the robots and sitemap cases failed in the harness, not the application. The shared comparison helper requested JSON, so both hosts answered `robots.txt` with the same 406, and production's edge refused Python's default user agent for `sitemap.xml`. A plain-text comparison helper and an explicit user agent were added, and all cases were rerun on the same candidate.
- **Reason:** The evidence must compare what a crawler receives.
- **Impact:** None on the code; the report records the discarded run.

## Outcome

> [!TIP]
> Shipped in PR #1516 (`080a67e`) and auto-deployed. Production serves `080a67e`, and `/robots.txt` returns 200. The production-only initializers ran in production startup with the new code, which the deploy itself confirms.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every file in the three packages |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-15-33-christopherbell-dev-configuration-root-mail-and-persistence-conform-to-chris-str.md)) |
| AC-3 | ✅ Met | 5 of 5 runtime cases passed on candidate `4287ffe`, after the discarded first run logged above ([report](../test-reports/2026-10-09-15-33-christopherbell-dev-configuration-root-mail-and-persistence-conform-to-chris-str.md)) |
| AC-4 | ✅ Met | [PR #1516](https://github.com/azurras/christopherbell.dev/pull/1516) merged as `080a67e` after all checks passed; production `/actuator/info` reports `080a67e` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
