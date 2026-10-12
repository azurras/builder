# Test-Profile Administrator for Local Candidate Verification

## Document Status
complete

## Objective

> [!IMPORTANT]
> A local candidate on the isolated `test` database can be started with an ADMIN account, so runtime checks can exercise admin routes and grant shared-folder access through the API. No other profile or database can create one.

## Background
The style migration's runtime proof was weaker than it should have been. In slices 19a to 19d, the recycle, admin audit, restore and purge routes, and every granted shared-folder operation, need an ADMIN or a grant. Account creation always assigns `Role.USER`, and nothing promotes an account. So each plan's Test Plan recorded those paths as untestable locally. The user asked for item 4: a supported local ADMIN and grant fixture.

`DomainCollectionCutoverLedger` already proves, for profile `test`, that the connection is a single loopback server on a port other than 27017 and that the database is `test`. The [local candidate scripts plan](2026-10-11-19-19-christopherbell-dev-checked-in-local-candidate-scripts-and-windows-gradle-wrappe.md) adds `Start-Candidate.ps1`, which this plan extends.

## Goals
- A test-profile candidate can create one ADMIN account from startup settings, behind the existing isolation proof (AC-1, AC-2).
- `Start-Candidate.ps1` can generate those credentials into a disposable file (AC-3).
- A runtime check proves that the ADMIN reaches admin routes and grants shared-folder access to a USER (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Any API route that creates or promotes an ADMIN | Production must never gain a promotion path |
| Seeding other data such as posts or grants | ADMIN plus the existing APIs creates everything else through the application |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `TestAdministratorBootstrap` exists only under profile `test`. With all three `app.test-administrator.*` settings, on application ready, it requires the exact isolated test connection, then creates the account through `AccountService` and stores it with `Role.ADMIN`. With none set it does nothing; with only some set it fails startup |
| AC-2 | `IsolatedTestDatabase.requireIsolatedTestConnection()` (in `configuration.persistence`, used by the cutover ledger too) rejects any profile other than exactly `test`, port 27017, a non-loopback host and a database other than `test`. Unit tests cover the bootstrap and the guard |
| AC-3 | `Start-Candidate.ps1 -WithTestAdministrator` generates a username, email and random password. It passes them only to the candidate, writes them to a credential file inside the disposable MongoDB root, records that path in the state file and never prints the password |
| AC-4 | On isolated MongoDB `test`, the published report records the ADMIN logging in, reading `/api/shared-folder/2026-07-17/admin/recycle` and `/admin/audit`, and granting a USER read access through the account API. The USER can then list entries, and a USER without a grant cannot. The full check passes |

## Inputs
- **Request:** "Fix 2, 3, 4, 5, 7", item 4.
- **Inspected at spoke `280b3c61`:**
  - `AccountService.createAccount` and `createAccountEntity`, which always assign USER.
  - `Role`.
  - `AccountCreateRequest` validation.
  - `AccountController` shared-folder permissions (ADMIN).
  - `SharedFolderAdminController` routes.
  - `DomainCollectionCutoverLedger` and its tests.
  - Existing `ApplicationReadyEvent` listeners.

## Branch
`claude/test-administrator-20261011` from spoke `origin/main` `a18b81b2`; it merges `origin/main` once the candidate scripts land, before the script task.

## Assumptions
None.

## Open Questions
None.

## Design
- **Guard:** the ledger's private connection check moves, with unchanged messages, to `configuration.persistence.IsolatedTestDatabase`, a shared cross-area package the architecture rules let `account` use. `requireConnection` is static, and the ledger calls it as before. `requireIsolatedTestConnection()` adds the exact-`test`-profile check for fixtures.
- **Bootstrap:** `account.bootstrap.TestAdministratorBootstrap` is annotated `@Profile("test")` and listens for `ApplicationReadyEvent`.
  - It reads `app.test-administrator.username`, `.email` and `.password` from `Environment`.
  - It calls the guard, then `AccountService.createAccount`.
  - It then loads the stored account through `AccountRepository`, sets `Role.ADMIN` and saves it.
  - It logs the username, never the password.
  - A failure propagates and stops startup.
- **Script:** `-WithTestAdministrator` puts `APP_TESTADMINISTRATOR_USERNAME`, `_EMAIL` and `_PASSWORD` into the candidate-only environment. It writes `test-administrator.json` under the disposable MongoDB root, so `Stop-Candidate.ps1` removes it.

## Expected Changes

| File | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/configuration/persistence/IsolatedTestDatabase.java` | New guard, moved from the ledger |
| `website/src/main/java/dev/christopherbell/configuration/mongo/migration/DomainCollectionCutoverLedger.java` | Delegates to `IsolatedTestDatabase` |
| `website/src/test/java/dev/christopherbell/configuration/persistence/IsolatedTestDatabaseTest.java` | New |
| `website/src/main/java/dev/christopherbell/account/bootstrap/TestAdministratorBootstrap.java` | New |
| `website/src/test/java/dev/christopherbell/account/bootstrap/TestAdministratorBootstrapTest.java` | New |
| `ops/local/Start-Candidate.ps1` | `-WithTestAdministrator` |
| `website/src/main/java/dev/christopherbell/account/README.md`, `website/src/main/java/dev/christopherbell/configuration/README.md`, `README.md` | Documentation |

## Task Breakdown

### Task 1 - Guard and bootstrap

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Candidate scripts merged |
| **Files** | Java files in Expected Changes |
| **Symbols** | `IsolatedTestDatabase.requireIsolatedTestConnection`, `IsolatedTestDatabase.requireConnection`, `TestAdministratorBootstrap.createConfiguredAdministrator` |
| **Inspection** | Inputs |
| **Behavior** | As in Design |
| **Invariants** | No bean outside profile `test`; no write before the guard passes; no password in logs |
| **Boundary/API** | New test-profile settings only |
| **Effects and failures** | Partial settings, a failed guard or a duplicate account fail startup |
| **Tests and evidence** | Unit tests for every branch |
| **Verification** | `.\ops\local\Invoke-Gradle.ps1 :website:test --tests '*TestAdministratorBootstrap*' --tests '*DomainCollectionCutoverLedger*' --tests '*Architecture*'` |

### Task 2 - Script and documentation

Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | Task 1 |
| **Files** | `ops/local/Start-Candidate.ps1`, READMEs |
| **Symbols** | `Start-Candidate.ps1 -WithTestAdministrator` |
| **Inspection** | Inputs |
| **Behavior** | As in Design |
| **Invariants** | The credential file lives only inside the disposable root |
| **Boundary/API** | New switch |
| **Effects and failures** | None new |
| **Tests and evidence** | Runtime |
| **Verification** | Runtime check |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | Bootstrap unit tests | verify-local-app: start with `-WithTestAdministrator`; the ADMIN logs in |
| AC-2 | Guard unit tests | Covered by AC-1 |
| AC-3 | Review | The state file names the credential file; stop removes it |
| AC-4 | Full check | The admin and grant checks in the report |

## Rollback or Recovery
Revert the squash-merge commit. Production never activates the test profile, so no data changes.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The bootstrap runs against real data | Very low | It requires `@Profile("test")`, exactly the `test` profile, a loopback non-27017 server and the `test` database, all before any write |

## Implementation Log

### 2026-10-11 - Guard moved to the shared persistence package

- **Change:** The isolation guard lives in `configuration.persistence.IsolatedTestDatabase`, not on `DomainCollectionCutoverLedger`. The ledger delegates to it with the same messages.
- **Reason:** `LegacyModuleDependencyRules` lets a business area such as `account` depend only on another area's published API or on the shared `configuration.persistence` and `configuration.mongo.domain` packages. The ledger is in `configuration.mongo.migration`.
- **Impact:** AC-2, Design, Expected Changes and Task 1 Symbols were updated. The Java work was drafted while the candidate scripts were in review, and this plan was published before any commit.

### 2026-10-11 - Shared folder enabled for local candidates

- **Change:** `Start-Candidate.ps1` gains `-EnableSharedFolder`. It enables the shared folder with shared and system roots inside the disposable root and a 1GB free-space floor.
- **Reason:** In the first runtime run the administrator logged in, read the audit log and granted access. The recycle read returned 503 "Shared-folder recycle is unavailable", though, and the granted listing returned 404, because the shared folder is disabled by default and its roots did not exist. Neither was an authorization failure, but neither proved the grant does real work.
- **Impact:** Design and AC-3 cover the extra switch, in commit `9e92ad15`. The architecture baseline `LegacyMongoAccessBaselineTest` also lists `IsolatedTestDatabase` as approved direct-Mongo infrastructure, because it carries the connection check the ledger already ran.

## Outcome

> [!TIP]
> Shipped in PR #1528 (`f9789ca`) through the deploy-aware queue; production serves `f9789ca`. Local candidates can now verify admin routes and shared-folder grants.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | `TestAdministratorBootstrapTest` covers no settings, partial settings, a refused guard, creation and a duplicate; at runtime the log names the created administrator ([report](../test-reports/2026-10-11-20-03-christopherbell-dev-test-profile-administrator.md)) |
| AC-2 | ✅ Met | `IsolatedTestDatabaseTest` and the unchanged ledger tests pass; the architecture baseline approves the guard |
| AC-3 | ✅ Met | The state file names a credential file inside the disposable root; the password never reached the log, and stop removed the root ([report](../test-reports/2026-10-11-20-03-christopherbell-dev-test-profile-administrator.md)) |
| AC-4 | ✅ Met | The ADMIN read the admin recycle bin and audit log and granted a USER read, which could then list entries but not write; the full check passed; [PR #1528](https://github.com/azurras/christopherbell.dev/pull/1528) merged after all checks |

## Project
christopherbell-dev

## Plan Format
task-contract-v2
