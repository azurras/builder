# Account Slice Conforms to Chris Street Style

## Document Status
complete

## Objective

> [!IMPORTANT]
> Every file in the account slice conforms to write-chris-street-style-code, and sign-up, login, sessions, password reset, profiles, follows, trust, moderation, capabilities and deletion behave as before.

## Background
This is slice 14 of the [full conformance migration](2026-10-05-20-05-christopherbell-dev-bring-all-christopherbell-dev-code-to-chris-street-style-con.md). Inspection at `8bd5e2f4` covered the 71 main Java files, 9 READMEs and 28 test files. It found:

1. **Hidden time.** These read `Instant.now()`:
   - `AccountService.createAccountEntity`.
   - `AccountAuthenticationService` at login.
   - `PasswordResetService` in three places.
   - `AccountDeletionJob` in five methods.
2. **Broad exceptions.** 18 `AccountController` endpoints and `AccountService.loginAccount` declare `throws Exception`.
3. **Optional misuse:**
   - `AccountProfileService.toPublicProfile` takes an `Optional` parameter.
   - `LoginTokens.resolveSecret`, `AccountDeletionService` and `AccountModerationService` call `isPresent()` then `get()`.
   - `PasswordResetService` unwraps with `orElse(null)`.
4. **Duplication.** `updateSharedFolderPermissions` and `updateMusicPermissions` are the same 50 lines with different names.
5. **Smaller issues:**
   - An unnamed lease string and duration in deletion.
   - Fully qualified names in main code and in most test files.
   - Single-letter exception names.
   - `private final static`.
   - Repository docs that still describe Spring Data derived queries.
   - One-line Mongo adapter methods.

## Goals
- Every slice file has a recorded verdict and conforms (AC-1, AC-2).
- The account API behaves as before at runtime, including authentication and session paths (AC-3).
- The slice ships as its own merged and deployed PR (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing the login path's nullable account | It keeps the dummy-hash timing defense for unknown emails line for line; restructuring security-sensitive control flow is not worth the risk |
| Renaming the `site-monitor-pilot` lease used by deletion | It intentionally serializes deletion with monitor writes; the name is shared with site monitor. It is now a named constant with that reason |
| Changing routes, JSON, stored fields, token format, session cookies or audit actions | Public and security contracts |
| Brace style on one-line `if` statements | The formatter accepts them and the guide sets no rule |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | Expected Changes records a verdict for every slice file |
| AC-2 | `:website:check :cbell-lib:check :website:bootJar` pass and a style review of the full diff finds no blocker |
| AC-3 | On isolated MongoDB `test` with disposable USERs, the published test report records: sign-up and duplicate sign-up; a wrong password; cookie-mode login, `/me` through the cookie and logout; generic password-reset replies and a rejected bogus token; profile, follow, unfollow and self-follow; username search; mute and clear; federation consent; USER rejection from admin and capability endpoints; anonymous reads matching production |
| AC-4 | The PR merges after required checks pass and production `/actuator/info` reports the merge commit |

## Inputs
- **Request:** umbrella plan slice 14; the user said to keep going without review stops.
- **Inspected:** spoke `origin/main` `8bd5e2f4`:
  - All `account` main and test sources.
  - The callers `SocialDomainRepositoryMongoContractTest` and the shared `ControllerExceptionHandler` status mappings.
  - `ApplicationClockConfiguration`, which provides `Clock.systemUTC()`.

## Branch
`claude/style-account-20261009` from spoke `origin/main` `8bd5e2f4`.

## Assumptions
- The application `Clock` stays `Clock.systemUTC()`.
- A new account's `createdOn` and `lastUpdatedOn` now share one instant instead of two reads microseconds apart.

## Open Questions
None.

## Design
- **Time:**
  - `AccountService`, `AccountAuthenticationService`, `PasswordResetService` and `AccountDeletionService` receive the application `Clock`.
  - `AccountDeletionJob` methods take the time from the service.
- **Exceptions:** each endpoint declares what its service declares, and the Javadoc names the same exceptions.
- **Capabilities:**
  - `replaceCapabilities` holds the shared logic.
  - A private `CapabilityFamily` enum carries the label, audit action and permission pair.
  - Both request records implement a new `CapabilityPairUpdate`.
  - Messages, audit actions and session revocation are unchanged.
- **Profiles:**
  - `toPublicProfile(account, viewer)` requires a viewer.
  - Anonymous profiles use the private `profile(account, false, false)`, as before.
- **Optional:**
  - `resolveSecret` uses `orElseGet` with `developmentSecret`.
  - The password-reset request uses `ifPresent(sendResetLink)`.
  - Moderation uses `filter(...).isPresent()`.
  - Deletion reads an existing job once.

| Alternative | Why not |
|---|---|
| Keep two copies of the capability update | Every fix would have to be made twice; the copies already differ only by names |
| `Optional<Account>` through the whole login path | See Non-Goals |

## Expected Changes

| File | Verdict | Change and rule |
|---|---|---|
| `website/src/main/java/dev/christopherbell/account/model/dto/CapabilityPairUpdate.java` | new | Shared shape for the two capability requests |
| `website/src/main/java/dev/christopherbell/account/model/dto/MusicPermissionUpdate.java`, `SharedFolderPermissionUpdate.java` | changed | Implement `CapabilityPairUpdate` |
| `website/src/main/java/dev/christopherbell/account/AccountController.java` | changed | Narrow `throws` and Javadoc |
| `website/src/main/java/dev/christopherbell/account/AccountService.java` | changed | `Clock`, narrow login, one capability update, exception names |
| `website/src/main/java/dev/christopherbell/account/auth/AccountAuthenticationService.java`, `passwordreset/PasswordResetService.java`, `passwordreset/PasswordResetNotificationService.java` | changed | `Clock`, `Optional` handling, exception names |
| `website/src/main/java/dev/christopherbell/account/deletion/AccountDeletionJob.java`, `AccountDeletionService.java` | changed | Explicit time, named lease and duration, one job read |
| `website/src/main/java/dev/christopherbell/account/profile/AccountProfileService.java`, `follow/AccountFollowService.java` | changed | No `Optional` parameter |
| `website/src/main/java/dev/christopherbell/account/moderation/AccountModerationService.java`, `api/LoginTokens.java`, `api/MonitorAccountAccess.java`, `AdminAccountQueryService.java`, `AccountControllerExceptionHandler.java`, `AccountRepository.java` | changed | `Optional` use, imported names, modifiers, true docs |
| `website/src/main/java/dev/christopherbell/account/MongoAccountRepository.java`, `deletion/MongoAccountDeletionJobRepository.java`, `trust/MongoAccountTrustRepository.java` | changed | One statement per line |
| Remaining 51 account main Java files (models, DTOs, ports, Mongo adapters for login, follow and deletion, trust controller and service, mapper, query record) and the 9 READMEs | conforming | No change |
| `website/src/test/java/dev/christopherbell/account/AccountServiceTest.java`, `deletion/AccountDeletionServiceTest.java`, `deletion/AccountDeletionParityContract.java`, `follow/AccountFollowServiceTest.java`, `architecture/SocialDomainRepositoryMongoContractTest.java` | changed | New constructors and signatures; imported names |
| `website/src/test/java/dev/christopherbell/account/AccountControllerTest.java`, `AccountRepositoryParityContract.java`, `AdminAccountQueryParityContract.java`, `AdminAccountQueryServiceTest.java`, `auth/AccountLoginParityContract.java`, `auth/MongoAccountLoginStoreTest.java`, `deletion/MongoAccountDeletionOperationsTest.java`, `follow/AccountFollowStoreTest.java`, `moderation/AccountModerationAuditTest.java`, `trust/IdentityRelationshipParityContract.java` | changed | Imported names instead of fully qualified ones |
| Remaining 14 account test files | conforming | No change |

## Task Breakdown

### Task 1 - Conform the account slice

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None beyond current main |
| **Files** | As listed in Expected Changes |
| **Symbols** | `AccountController` endpoints; `AccountService.loginAccount`, `createAccountEntity`, `replaceCapabilities`, `CapabilityFamily`; `AccountDeletionJob.started`, `resume`, `advance`, `fail`, `complete`; `AccountProfileService.toPublicProfile`, `profile`; `PasswordResetService.sendResetLink`; `LoginTokens.resolveSecret`, `developmentSecret` |
| **Inspection** | All files in Inputs at `8bd5e2f4` |
| **Behavior** | Same statuses, messages, audits, session revocations, deletion checkpoints, token secret precedence and production refusal |
| **Invariants** | Routes, JSON, stored documents, JWT claims and cookies unchanged |
| **Boundary/API** | Constructors gain `Clock`; `toPublicProfile` takes the viewer; `AccountDeletionJob` methods take time; callers are in this change |
| **Effects and failures** | None new |
| **Tests and evidence** | Account suites, social and architecture contract tests; runtime checks below |
| **Verification** | `./gradlew.bat :website:check :cbell-lib:check :website:bootJar` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Plan review against the diff | Not applicable: documentation |
| AC-2 | Full check; full-diff style review | Covered by AC-3 |
| AC-3 | Account suites | verify-local-app: the flows in AC-3. Admin success paths (moderation, capability grants, deletion) need an ADMIN, which has no supported local path, so they rely on `AccountServiceTest`, `AccountDeletionServiceTest` and the Mongo contract tests |
| AC-4 | Required PR checks | `wait_for_github.py live` |

## Rollback or Recovery
Revert the squash-merge commit; auto-deploy rolls forward. No data change.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Login or session behavior changes | Low | Login code is unchanged except the clock; runtime cookie, bearer, wrong-password and logout checks |
| Capability grants change | Low | `AccountServiceTest` covers both families, audits and revocation; the helper keeps each message and action |

## Implementation Log

### 2026-10-09 - Plan published after the edits

- **Change:** This plan was saved after the code edits, while the full check ran.
- **Reason:** I worked ahead while earlier slices were in CI.
- **Impact:** No PR exists yet; the plan and report are published before it.

### 2026-10-09 - First runtime run discarded

- **Change:** The first runtime run reported two failures, so I discarded it and ran again on a fresh database.
  - The fresh disposable database had no unique `email` or `username` index on `accounts`, so a duplicate sign-up succeeded. Every later check that looked up `acct_cookie` then hit two matching accounts.
  - Two expected messages were wrong: the shared `ControllerExceptionHandler` answers `INVALID_TOKEN` with "Authentication is required." for both a wrong password and a bogus reset token.
  - The rerun dropped the duplicate sign-up case and expects `INVALID_TOKEN` with status 401. All 21 cases passed.
- **Reason:** Production applies the domain manifest indexes through `ops/production/windows/scripts/DomainCollectionManifest.js`, and `V015RequireDomainCollectionSchema` blocks startup until the cutover ledger is ready. No migration creates these indexes in a fresh local database, so duplicate rejection cannot be shown locally without writing to the database directly, which this migration avoids.
- **Impact:** Two consequences.
  - Duplicate sign-up rejection is covered by the code path (`DuplicateKeyException` maps to 409) and production's indexes, not by local runtime evidence.
  - Follow-up for the user: local disposable databases lack the manifest indexes.

## Outcome

> [!TIP]
> Shipped in PR #1504 (`8d5c68f`) and auto-deployed. Production serves the merge commit; a public profile returns 200 and anonymous account-list and `/me` reads still return 403. Login itself was verified locally (cookie and bearer modes); a production sign-in by the owner remains the final confirmation.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | Expected Changes records verdicts for every slice file |
| AC-2 | ✅ Met | Full check passed ([report](../test-reports/2026-10-09-10-40-christopherbell-dev-account-slice-conforms-to-chris-street-style.md)) |
| AC-3 | ✅ Met | 21 of 21 runtime cases on a fresh database, after the discarded first run logged above ([report](../test-reports/2026-10-09-10-40-christopherbell-dev-account-slice-conforms-to-chris-street-style.md)) |
| AC-4 | ✅ Met | [PR #1504](https://github.com/azurras/christopherbell.dev/pull/1504) merged as `8d5c68f` after its branch was updated with main and all checks passed; production `/actuator/info` reports `8d5c68f` |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
