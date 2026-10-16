# Patch Vulnerable Dependencies and Throttle Password Reset Mail on christopherbell.dev

## Document Status
ready-for-execution

## Objective

> [!IMPORTANT]
> Production runs Jackson, Tomcat and jsoup versions with no known advisories, and one account receives at most one password reset email every five minutes, however many clients ask.

## Background
The 2026-10-16 [secure proxied cookies](2026-10-16-13-45-christopherbell-dev-mark-proxied-cookies-secure.md) review sampled the riskiest surfaces and listed what it did not cover. A follow-up review the same day, requested from that session, covered the rest: every HTML sink in the front end, password reset end to end, federation, the resolved runtime classpath's CVEs, and three open observations. Its full results, including what was found clean, are in the 2026-10-16 session memory. It confirmed two problems on `main` `c702553`:

1. **Vulnerable runtime dependencies.** GitHub's dependency graph sees only 11 manifest packages because nothing submits the resolved Gradle graph, so Dependabot raised no alerts. Querying OSV with all 146 artifacts on `:website:runtimeClasspath` found:
   - `tools.jackson.core` `jackson-core`/`jackson-databind` 3.1.5 and `com.fasterxml.jackson.core` 2.21.5: high-severity parsing denial of service (CVE-2026-89425, CVE-2026-89407, CVE-2026-91777, CVE-2026-91776, CVE-2026-68497) and two moderate ones. Every JSON request body goes through Jackson 3, so the parsing DoS is reachable by anonymous clients. Fixed in 3.1.7 and 2.21.7.
   - `tomcat-embed-core` 11.0.24: three critical advisories (CVE-2026-65905, CVE-2026-65182, CVE-2026-68525). The site uses Spring Security rather than Tomcat's DIGEST or FORM authenticators, so the two authenticator bypasses do not apply, but the access-control one is not described precisely enough to rule out. Fixed in 11.0.25.
   - `jsoup` 1.22.2: XML tree builder memory exhaustion (CVE-2026-75140) and a `Cleaner` bypass (CVE-2026-71497). The site parses untrusted remote pages with jsoup's HTML parser (link previews, site monitor) and never uses `Cleaner` or the XML parser, so neither is reachable today. Fixed in 1.23.2.
2. **Password reset mail flooding.** `PasswordResetService.requestPasswordReset` issues a new token and sends an email on every request for an existing address. Production mail is enabled (Resend). The only limit is the `auth-mutations` rule, 20 requests a minute per client address, so anyone can send a victim 1,200 reset emails an hour from one address, more from several, and each one replaces the token in the email the victim may be about to use.

## Goals
- The deployed runtime classpath has no OSV advisories for Jackson, Tomcat or jsoup (AC-1).
- Repeated reset requests for one account inside five minutes send one email and keep the first token valid (AC-2).
- Reset requests after the cooldown, unknown emails, and confirming a reset behave as before (AC-3).
- Production serves the change (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Upgrading Spring Boot past 4.1.1 | No newer 4.1 patch exists; 4.2 is a milestone |
| Tomcat 11.0.27 | Released 2026-10-06, under the two-week age bar; 11.0.26 has no advisories |
| Submitting the resolved Gradle graph to GitHub so Dependabot sees transitive CVEs | A CI workflow change, worth its own proposal |
| Hiding account existence through reset timing | Signup already answers "Account with given email or username already exists", so timing reveals nothing new |
| Survive capacity (anonymous joins fill the camp; account survivors never leave it) | Game design decisions for the user |
| `SameSite` on `XSRF-TOKEN` | Not a weakness: the double-submit header cannot be forged cross-origin, and the authentication cookies are already `SameSite=Lax` |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | `:website:runtimeClasspath` resolves Jackson 3.1.7, Jackson 2.21.7, Tomcat 11.0.26 and jsoup 1.23.2, an OSV batch query of the whole classpath returns no advisories, and `:website:build` passes with dependency verification on |
| AC-2 | A second reset request for the same account less than five minutes after the first sends no email and leaves the stored token hash and expiry unchanged, so the first link still resets the password |
| AC-3 | A request more than five minutes after the last one issues a new token and email; an unknown email sends nothing; confirming a valid token still works; the endpoint's response is unchanged |
| AC-4 | The PR is merged to `main`, production serves the merge commit, and the live reset request endpoint returns its generic 200 response |

## Inputs
- **Request:** follow-up deeper security review from the session that delivered PR #1544, 2026-10-16.
- **Evidence:** `gradlew :website:dependencies --configuration runtimeClasspath` on `c702553`; OSV `querybatch` and `vulns/<id>`; Maven Central metadata for each library; GitHub `dependency-graph/sbom` (11 packages) and Dependabot alerts (none).
- **Inspected:** spoke `christopherbell.dev` at `main` `c702553d`: `build.gradle.kts`, `website/build.gradle.kts`, `cbell-lib/build.gradle.kts`, `gradle/verification-metadata.xml`, `.github/workflows/dependency-verification.yml`, README dependency-verification section, `PasswordResetService`, `PasswordResetNotificationService`, `AccountController` reset endpoints, `RateLimitProperties`, `AccountPasswordResetRequest`, `AccountPasswordResetConfirmRequest`, `AccountServiceTest` reset tests, `application.yml`, `application-prod.yml`.

## Branch
`claude/patch-deps-throttle-reset-20261016` from `main` `c702553d` in a linked worktree under `christopherbell.dev-worktrees`.

## Assumptions
- The dependency-management plugin applies project properties named like the Boot BOM's (`jackson-bom.version`, `jackson-2-bom.version`, `tomcat.version`) to both the Boot plugin's BOM and cbell-lib's explicit import.
- Jackson 3.1.7 and 2.21.7 are drop-in patch releases for Spring Boot 4.1.1, and jsoup 1.23 keeps the `Jsoup.parse` and selector APIs the site uses.

## Open Questions
None.

## Design
**Dependencies.** Set the three BOM properties once in the root `subprojects` block, so the website and cbell-lib resolve the same versions, and raise jsoup's direct version in `website/build.gradle.kts`. Regenerate `gradle/verification-metadata.xml` with `--write-verification-metadata sha256` and review that only the expected components were added.

**Reset cooldown.** The stored expiry already records when the last token was issued (expiry minus the one-hour TTL). `requestPasswordReset` skips issuing when the account holds a token issued less than five minutes ago, logging the skip by account id. The response stays generic. No schema change.

| Alternative | Why not |
|---|---|
| A tighter per-IP rate limit on the request endpoint | Does not stop a distributed flood against one victim, and slows honest users on shared addresses |
| A separate `passwordResetRequestedOn` field | Duplicates what the expiry already encodes, and adds a stored field |
| Re-sending the existing token during the cooldown | Only its hash is stored; the plain token cannot be recovered |
| Override the Tomcat and Jackson versions only in `website` | cbell-lib's tests would keep running on vulnerable versions |

## Expected Changes

| File or area | Change |
|---|---|
| `build.gradle.kts` | Set `jackson-bom.version` 3.1.7, `jackson-2-bom.version` 2.21.7 and `tomcat.version` 11.0.26 for every subproject, with the advisories as the reason |
| `website/build.gradle.kts` | jsoup 1.22.2 to 1.23.2 |
| `gradle/verification-metadata.xml` | Checksums for the new artifacts |
| `website/src/main/java/dev/christopherbell/account/passwordreset/PasswordResetService.java` | Five-minute per-account cooldown before issuing a new token |
| `website/src/test/java/dev/christopherbell/account/AccountServiceTest.java` | Cooldown tests: within the window nothing is saved or sent; after it a new token is issued |

## Task Breakdown

### Task 1 - Patch Jackson, Tomcat and jsoup
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `build.gradle.kts`, `website/build.gradle.kts`, `gradle/verification-metadata.xml` |
| **Symbols** | Root `subprojects` block; the jsoup `implementation` line; verification `components` |
| **Inspection** | Read all three build scripts and the verification workflow at `c702553d`; the Boot 4.1.1 BOM defines `jackson-bom.version` 3.1.5, `jackson-2-bom.version` 2.21.5 and `tomcat.version` 11.0.24 |
| **Behavior** | The runtime classpath resolves the patched versions; application behavior is unchanged |
| **Invariants** | Dependency verification stays strict; no other dependency moves |
| **Boundary/API** | No public API change; the boot jar's bundled libraries change |
| **Effects and failures** | Build-time only; a missing checksum fails the build, which is the intended guard |
| **Tests and evidence** | Before: `dependencies` shows the vulnerable versions and OSV lists 19 advisory hits; after: patched versions, no OSV hits, and `:website:build` green |
| **Verification** | `ops/local/Invoke-Gradle.ps1 :website:dependencies --configuration runtimeClasspath`, the OSV batch script over its output, then `ops/local/Invoke-Gradle.ps1 :website:build` |

### Task 2 - Throttle reset email per account
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `PasswordResetService.java`, `AccountServiceTest.java` |
| **Symbols** | `PasswordResetService.requestPasswordReset` and a new private check with a `PASSWORD_RESET_COOLDOWN` constant; new `AccountServiceTest` reset-cooldown tests |
| **Inspection** | Read `PasswordResetService`, `PasswordResetNotificationService`, the reset endpoints and `AccountServiceTest` reset tests at `c702553d` |
| **Behavior** | Within five minutes of the last issued token, a request for that account does nothing; otherwise as today |
| **Invariants** | The response never reveals whether the email exists; tokens stay hashed, single use and one-hour |
| **Boundary/API** | No endpoint or response change |
| **Effects and failures** | Skipped requests write nothing and send nothing; an expired or cleared token never blocks a new one |
| **Tests and evidence** | RED: a second request one minute after the first saves and sends again; GREEN after the change; existing reset tests stay green |
| **Verification** | `ops/local/Invoke-Gradle.ps1 :website:test --tests dev.christopherbell.account.AccountServiceTest`, then the full build |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | `:website:build` with verification; `dependencies` output and the OSV batch query recorded in the report | The candidate starts, serves `/`, accepts a JSON login body and renders a link preview path without errors |
| AC-2 | New `AccountServiceTest` cooldown test | Candidate with a seeded account: two reset requests in a row; the stored hash and expiry from the first stay unchanged (read from MongoDB) and the first token resets the password |
| AC-3 | New after-cooldown test and the existing reset tests | Unknown email returns the same 200 body; the confirm call with the first token succeeds and the token is cleared |
| AC-4 | Required CI | `wait_for_github.py deployed`, then a live `POST` to the reset request endpoint with an unregistered address returns the generic 200 |

Run the candidate with verify-local-app against a disposable loopback MongoDB under the `test` profile with the spoke's `ops/local/Start-Candidate.ps1`, and save the report with write-test-report before creating the PR. Rerun the runtime checks after any runtime-affecting edit.

## Rollback or Recovery
Revert the merge commit on `main`; auto-deploy restores the previous libraries and reset behavior. No data or schema changes; tokens issued under either version stay valid.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| jsoup 1.23 changes parsing output the link preview or site monitor relies on | Low | Their unit tests run in the build; runtime check exercises the app |
| A patch release breaks a Spring integration | Low | Full build and candidate run before the PR |
| An honest user who lost the first email waits five minutes for another | Medium | The first link stays valid for an hour; five minutes is short |

## Implementation Log
No entries yet.

## Outcome
Pending.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
