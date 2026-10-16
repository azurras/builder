# Mark Proxied Cookies Secure on christopherbell.dev

## Document Status
complete

## Objective

> [!IMPORTANT]
> In production, the survive game's session cookie and the site's CSRF token cookie carry the `Secure` attribute, so browsers never send them over plain HTTP.

## Background
The user asked for a security review of the website, with fixes for anything it found, on 2026-10-16. The review covered the security filter chain, JWT and browser-session authentication, public route matchers, controller authorization, the site monitor's SSRF policy, the shared-folder and music file-serving headers, open redirects, template and JavaScript HTML sinks, rate limits, production settings, dependency versions and the live response headers.

The 2026-07-29 [website-wide security remediation](2026-07-29-website-wide-security-remediation.md) had already closed the larger findings. This review confirmed two that remain, both on the live site at `2528e37`, and both from one cause. Production runs with `server.forward-headers-strategy: none` behind Cloudflare and a local reverse proxy, so `HttpServletRequest.isSecure()` is false even for HTTPS traffic:

1. `SurviveController` sets the `CBELL_SURVIVOR` guest token cookie with `.secure(httpRequest.isSecure())`. A live join returned `Set-Cookie: CBELL_SURVIVOR=...; Path=/api/survive/v1; HttpOnly; SameSite=Strict`, with no `Secure`.
2. `csrf.spa()` uses `CookieCsrfTokenRepository`, which also derives `Secure` from `request.isSecure()`. A live `GET /` returned `Set-Cookie: XSRF-TOKEN=...; Path=/`, with no `Secure`.

The authentication cookies already use the configured `app.browser-security.authentication-cookie-secure` (true in production). HSTS with `includeSubDomains` limits the exposure, but the domain is not preloaded, so a browser's first plain-HTTP request, or one after its HSTS entry expires, would send both values in clear text before the 301 redirect. Severity is low: the survive token controls only a guest game character, and the CSRF token is useful only with a session.

## Goals
- The survive guest cookie is `Secure` whenever the site's cookies are configured as secure, whatever the request scheme looks like behind the proxy (AC-1).
- The CSRF token cookie follows the same setting (AC-2).
- CSRF protection, the cookie path, `HttpOnly` and `SameSite` behavior are unchanged (AC-3).
- Production serves the fix (AC-4).

## Non-Goals

| Not doing | Why |
|---|---|
| Changing `forward-headers-strategy` so `isSecure()` follows the proxy | It changes how every request's scheme and client address are trusted, a wider boundary than these two cookies need |
| Adding `SameSite` to the CSRF cookie | It is defense in depth beyond this finding; the existing CSRF behavior is out of scope |
| HSTS preload submission | An operator decision about the domain, outside this repository |
| Capping registered-account survivors, which never expire from the shared camp | A product question about the game, not a confirmed vulnerability |

## Acceptance Criteria

| ID | Done when |
|---|---|
| AC-1 | With `authentication-cookie-secure=true`, a non-secure (proxied) survive join returns a `CBELL_SURVIVOR` cookie with `Secure`, `HttpOnly`, `SameSite=Strict` and `Path=/api/survive/v1` |
| AC-2 | With `authentication-cookie-secure=true`, the `XSRF-TOKEN` cookie set on a non-secure request carries `Secure` and stays readable by JavaScript (no `HttpOnly`) |
| AC-3 | Mutations without a CSRF token are still rejected with 403, existing survive and security tests pass, and a local candidate with the default (insecure) setting still lets the browser join the game over `http://localhost` |
| AC-4 | The PR is merged to `main`, production serves the merge commit, and live responses show `Secure` on both cookies |

## Inputs
- **Request:** "can you do a security review on the website and fix anything you find?" (2026-10-16).
- **Live probes:** `GET https://www.christopherbell.dev/` and a CSRF-protected `POST /api/survive/v1/game` on 2026-10-16 against `2528e37`.
- **Inspected:** spoke `christopherbell.dev` at `main` `2528e371`: `SecurityConfig`, `JwtAuthenticationFilter`, `BrowserAuthenticationCookies`, `BrowserSecurityProperties`, `SurviveController`, `SurviveService`, `SurviveControllerTest`, `SecurityConfigTest`, `application.yml` and `application-prod.yml`.

## Branch
`claude/secure-proxied-cookies-20261016` from `main` `2528e371` in the linked worktree `christopherbell.dev.worktrees/secure-proxied-cookies`.

## Assumptions
- Spring Security's `CookieCsrfTokenRepository` applies its cookie customizer after its own `secure(request.isSecure())` default, so the customizer decides the attribute.
- Calling `csrfTokenRepository(...)` after `spa()` replaces the repository but keeps the SPA request handler.

## Open Questions
None.

## Design
Both cookies take their `Secure` attribute from `BrowserSecurityProperties.authenticationCookieSecure()`, the setting that already governs the authentication cookies. `SurviveController` reads the same property by name with `@Value`, because the architecture rules keep business areas from depending on `configuration` types. `SecurityConfig` builds `CookieCsrfTokenRepository.withHttpOnlyFalse()` with a cookie customizer that sets `secure` from the same property, and passes it to the CSRF configurer after `spa()`.

| Alternative | Why not |
|---|---|
| Trust forwarded headers so `isSecure()` is accurate | Widens client-address and scheme trust for every request; the July remediation deliberately kept proxy trust narrow |
| Always set `Secure` | Local development over `http://localhost` would lose both cookies in non-Chromium browsers, breaking the game and every CSRF-protected form there |
| A new, separate property for these cookies | Two switches for one fact (whether the site is served over HTTPS) could drift apart |

## Expected Changes

| File or area | Change |
|---|---|
| `website/src/main/java/dev/christopherbell/survive/SurviveController.java` | Read `app.browser-security.authentication-cookie-secure` with `@Value`; set the survivor cookie's `Secure` from it; drop the `HttpServletRequest` parameter |
| `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java` | Configure the CSRF cookie repository with the configured `Secure` attribute |
| `website/src/test/java/dev/christopherbell/survive/SurviveControllerTest.java` | Run with secure cookies configured; join without `.secure(true)` and assert both cookies carry `Secure` |

## Task Breakdown

### Task 1 - Take both cookies' Secure attribute from configuration
Required skill: write-chris-street-style-code

| Contract | Detail |
|---|---|
| **Dependencies** | None |
| **Files** | `SurviveController.java`, `SecurityConfig.java`, `SurviveControllerTest.java` |
| **Symbols** | `SurviveController` constructor and `joinGame`; `SecurityConfig.securityFilterChain` and a new private `csrfTokenCookies` helper; `SurviveControllerTest` class configuration and `anonymousJoinNeedsCsrfAndUsesPrivateCookieWithoutExposingToken` |
| **Inspection** | Read each file at `2528e371`; `BrowserAuthenticationCookies.cookie` shows the existing property-driven pattern; the live probes show the missing attribute |
| **Behavior** | With secure cookies configured, the survivor and CSRF cookies carry `Secure` on proxied requests; with them off, neither does |
| **Invariants** | CSRF stays enforced with the SPA handler and the bearer/legacy-login exemptions; the survivor cookie keeps `HttpOnly`, `SameSite=Strict` and its path; the CSRF cookie stays readable by JavaScript |
| **Boundary/API** | No endpoint, request or response body changes; only `Set-Cookie` attributes change |
| **Effects and failures** | None new: cookie construction only; configuration binding already validates the properties |
| **Tests and evidence** | RED: the updated join test fails on the missing `Secure` for both cookies; GREEN after the fix; the whole survive and security suites still pass |
| **Verification** | `./gradlew.bat :website:test --tests 'dev.christopherbell.survive.*' --tests 'dev.christopherbell.configuration.*' --no-daemon`, then `./gradlew.bat :website:build --no-daemon` |

## Test Plan

| AC | Native check | Local runtime check |
|---|---|---|
| AC-1 | `SurviveControllerTest` join without `.secure(true)` asserts `Secure` with the property on | Candidate started with `--app.browser-security.authentication-cookie-secure=true`: `curl` join shows `Secure` on `CBELL_SURVIVOR` |
| AC-2 | `SurviveControllerTest` asserts `XSRF-TOKEN` has `Secure` and no `HttpOnly` | The same candidate's `GET /survive` shows `Secure` on `XSRF-TOKEN` |
| AC-3 | The existing 403-without-CSRF assertions and the full `:website:test` in `build` | A default-setting candidate: join over `http://localhost` succeeds with the returned cookies, and a POST without a token gets 403 |
| AC-4 | Required CI on the PR | `wait_for_github.py deployed` for the merge, then live `curl` of both cookies |

Run the candidate with verify-local-app against a disposable loopback MongoDB under the `test` profile, as the spoke's AGENTS.md requires, and save the report with write-test-report before creating the PR. Rerun both runtime checks after any runtime-affecting edit.

## Rollback or Recovery
Revert the merge commit on `main`; auto-deploy restores the previous cookie attributes. No data or schema changes. Browsers that hold `Secure` cookies keep them until they expire; that is harmless.

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| The customizer runs before Spring's own `secure` default, leaving `Secure` off | Low | The test asserts the attribute on a non-secure request; the live check confirms it after deployment |
| Overriding the repository after `spa()` drops the SPA token handler and breaks browser CSRF | Low | Existing CSRF tests plus a runtime join through the real form in the candidate |

## Implementation Log

### 2026-10-16 - Read the survive cookie setting through @Value

- **Change:** `SurviveController` takes `@Value("${app.browser-security.authentication-cookie-secure}") boolean secureCookies` instead of injecting `BrowserSecurityProperties`. The branch is `claude/secure-proxied-cookies-20261016` (the publish-spoke-changes naming for Claude Code), not `codex/secure-proxied-cookies`.
- **Reason:** The first full build failed two `ModularMonolithArchitectureTest` rules: the `survive` business area may not depend on `configuration`. Reading the same property by name keeps one setting with no cross-area type dependency, the pattern `LoginTokensConfiguration` already uses.
- **Impact:** Design and Expected Changes now name `@Value`; acceptance criteria are unchanged. The rebuilt candidate `aeca69c` passed `:website:build` (2,138 tests) and the [runtime report](../test-reports/2026-10-16-14-02-christopherbell-dev-mark-proxied-cookies-secure.md).

## Outcome

> [!TIP]
> Both cookies carry `Secure` in production. [PR #1544](https://github.com/azurras/christopherbell.dev/pull/1544) merged head `aeca69c` as `c702553`, and production serves `c702553`.

| AC | Result | Evidence |
|---|---|---|
| AC-1 | ✅ Met | `SurviveControllerTest` (RED, then GREEN); [runtime report](../test-reports/2026-10-16-14-02-christopherbell-dev-mark-proxied-cookies-secure.md) case 3 shows `CBELL_SURVIVOR=...; Path=/api/survive/v1; Secure; HttpOnly; SameSite=Strict` on a plain-HTTP join |
| AC-2 | ✅ Met | Same test; [runtime report](../test-reports/2026-10-16-14-02-christopherbell-dev-mark-proxied-cookies-secure.md) case 3 shows `XSRF-TOKEN=...; Path=/; Secure` with no `HttpOnly` |
| AC-3 | ✅ Met | `:website:build` on `aeca69c`, 2,138 tests and 0 failed; [runtime report](../test-reports/2026-10-16-14-02-christopherbell-dev-mark-proxied-cookies-secure.md) cases 6 to 8: with the default setting, local HTTP joins and plays a turn, and a join without the CSRF header gets 403 |
| AC-4 | ✅ Met | [PR #1544](https://github.com/azurras/christopherbell.dev/pull/1544) `MERGED` as `c702553` after required CI; `wait_for_github.py queue` confirmed production serves `c702553`; a live readback on 2026-10-16 showed `Secure` on both cookies and 403 for a join without CSRF |

Shipped as planned, except that the survive setting is read with `@Value` (see the Implementation Log). The live checks left two guest survivors named `sec-review-probe` in the production camp; they expire after two idle hours. The review's unfixed observations are listed in the 2026-10-16 session memory.

## Project
christopherbell-dev

## Plan Format
task-contract-v2
