# Browser Security Issues 1125-1130 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Do not dispatch subagents; the user authorized autonomous inline execution.

**Goal:** Harden browser delivery, move browser JWTs out of JavaScript-readable storage, restore CSRF, make password-reset origins canonical, validate authentication payloads, and align signup name requirements.

**Architecture:** Preserve stateless `Authorization: Bearer` authentication for explicit API clients while adding an HttpOnly JWT cookie for same-origin browser sessions. Spring Security 7.1 SPA CSRF protection guards cookie-authenticated unsafe requests while syntactically explicit bearer requests remain stateless. A non-secret readable session marker supports synchronous UI decisions without exposing credentials; protected APIs remain the authority. Typed browser-security configuration owns the canonical reset origin, cookie flags, and production HSTS behavior.

**Tech Stack:** Java 25, Spring Boot 4.1.0, Spring Security 7.1.0, Bean Validation, Thymeleaf, browser ES modules, Node test runner, Gradle.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\browser-security-1125-1130`; preserve the dirty authoritative checkout.
- Preserve bearer-token API compatibility and prioritize an explicit bearer header over the browser cookie.
- Never expose the JWT in JSON, JavaScript, localStorage, readable cookies, service-worker memory, logs, or URLs.
- Require CSRF for cookie-authenticated unsafe requests, including login and logout; exempt only explicit bearer-header requests.
- Keep shared-folder native downloads and media same-origin and authenticated through the HttpOnly cookie.
- Keep the persistent media shell frameable only by the same origin.
- Verify on a non-8080 port before production deployment.
- Treat only comments authored by `azurras` as scope changes.

---

## Document Status

complete

Completed in [PR #1249](https://github.com/azurras/christopherbell.dev/pull/1249),
squash-merged as `b6c361d1d916337679a37f04caa46c3475215e71` on 2026-07-25.

## Objective

Deliver issues #1125, #1126, #1127, #1128, #1129, and #1130 in one cohesive security PR with observed RED/GREEN evidence, isolated runtime verification, CI, deployment, and live browser acceptance.

## Goals

- Emit HSTS in production plus CSP, same-origin frame protection, strict referrer policy, MIME sniffing protection, and least-privilege permissions policy.
- Reject cookie-originated unsafe requests that omit or forge the SPA CSRF token while preserving bearer-only API calls.
- Issue and clear a one-day HttpOnly, SameSite=Lax JWT cookie; set Secure in production; return no JWT in the login response.
- Remove `cbellLoginToken` and raw JWT movement from browser code and shared-folder service-worker state.
- Build password-reset links only from a validated canonical configuration value.
- Reject malformed login and reset bodies at the controller boundary before invoking account services.
- Keep first and last name required in both signup markup and client payload validation.

## Inputs

- Approved campaign spec: `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md`.
- Trusted issue bodies #1125-#1130; none has comments.
- Refreshed spoke baseline: `08dd78af` (`Add resumable adaptive media controls (#1247)`).
- Spring Security 7.1.0 dependency evidence from `:website:dependencyInsight`.
- Spring Security's official SPA contract: `csrf.spa()` uses a readable `XSRF-TOKEN` cookie and accepts `X-XSRF-TOKEN`; login and logout must remain CSRF-protected.

## Branch

`codex/browser-security-1125-1130` in `A:\Projects\christopherbell.dev-worktrees\browser-security-1125-1130`, based on `origin/main` at `08dd78af`.

## Non-Goals

Replacing JWTs with database-backed server sessions, adding refresh tokens, changing account authorization rules, redesigning signup/login pages, enrolling the domain in the HSTS preload list, or changing unrelated external integrations.

## Assumptions

- `https://www.christopherbell.dev` remains the canonical public origin.
- A one-day authentication cookie lifetime matches the existing JWT expiration.
- SameSite=Lax plus CSRF is preferable to SameSite=Strict because authenticated top-level navigation from external links should continue to work.
- A readable `CBELL_AUTH_STATE=1` cookie is non-authoritative UI state only; no server decision trusts it.
- Same-origin media, download, and service-worker fetch requests carry the HttpOnly authentication cookie without JavaScript intervention.
- CSP must allow the current Bootstrap/Font Awesome CDNs, supported YouTube/Spotify/SoundCloud embeds, same-origin workers/media, and remote HTTPS images.

## Open Questions

None. The user granted standing approval for autonomous issue execution and the design choices above preserve the current API and UI contracts.

## Task Breakdown

### Task 1 - Define failing browser-security contracts

Sequence / dependencies:
- First; every later production edit must make an observed test failure pass.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Focused tests fail when public responses lack required headers, cookie mutations bypass CSRF, login exposes a JWT, logout fails to clear cookies, spoofed hosts affect reset links, invalid payloads reach services, or signup names remain optional.
  - Invariants: Tests exercise HTTP and exported browser boundaries rather than source-text presence; bearer compatibility and same-origin framing remain explicit.
  - Boundary/API: Production `SecurityFilterChain`, `JwtAuthenticationFilter`, AccountController MockMvc, and browser ES-module exports.
  - Effects and failures: MockMvc performs in-memory HTTP; browser tests replace only fetch/cookie/DOM boundaries; no production, email, or Mongo effect occurs.
  - Tests and evidence: Add one failing assertion per behavior, run focused Java and Node commands, and retain expected failures before Task 2.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/sharedfolder/SharedFolderSecurityIntegrationTest.java`
- Lines: 59-151
- Action: replace

Current:
```java
@WebMvcTest({
    SharedFolderReadController.class,
    SharedFolderWriteController.class,
    SharedFolderAdminController.class
})
class SharedFolderSecurityIntegrationTest {
  @DynamicPropertySource
  static void browserSecurityProperties(DynamicPropertyRegistry registry) {
    registry.add("app.browser-security.hsts-enabled", () -> "true");
  }

  @Test
  void responsesAllowSameOriginFramingForThePersistentMediaShell() throws Exception {
    mockMvc.perform(get(BASE + "/entries"))
        .andExpect(status().isForbidden())
        .andExpect(header().string("X-Frame-Options", "SAMEORIGIN"));
  }
}
```

Proposed:
```java
@WebMvcTest({
    AccountViewController.class,
    SharedFolderReadController.class,
    SharedFolderWriteController.class,
    SharedFolderAdminController.class
})
class SharedFolderSecurityIntegrationTest {
  @Test
  void publicLoginPageEmitsTheBrowserSecurityPolicy() throws Exception {
    mockMvc.perform(get("/login").secure(true))
        .andExpect(status().isOk())
        .andExpect(header().string("Strict-Transport-Security", "max-age=31536000; includeSubDomains"))
        .andExpect(header().string("X-Frame-Options", "SAMEORIGIN"))
        .andExpect(header().string("Referrer-Policy", "strict-origin-when-cross-origin"))
        .andExpect(header().string("Permissions-Policy",
            "camera=(), geolocation=(), microphone=(), payment=(), usb=()"))
        .andExpect(header().string("Content-Security-Policy",
            org.hamcrest.Matchers.containsString("frame-ancestors 'self'")));
  }

  @Test
  void cookieAuthenticatedMutationWithoutCsrfIsForbidden() throws Exception {
    mockMvc.perform(post(BASE + "/folders")
            .cookie(new Cookie(BrowserAuthenticationCookies.AUTH_COOKIE_NAME, tokenFor(Role.USER)))
            .contentType("application/json")
            .content("{\"parentPath\":\"\",\"name\":\"docs\"}"))
        .andExpect(status().isForbidden());
  }
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.sharedfolder.SharedFolderSecurityIntegrationTest --no-daemon`
- Expected RED: headers, cookie authentication, and CSRF behavior are not implemented.

#### Code Edit 1.2
- File: `website/src/test/java/dev/christopherbell/configuration/JwtAuthenticationFilterTest.java`
- Lines: 24-94
- Action: replace

Current:
```java
@Test
void doFilter_whenBearerTokenValid_setsAuthentication() throws ServletException, IOException {
  var filter = new JwtAuthenticationFilter(List.of());
  var request = new MockHttpServletRequest("GET", "/api/protected");
  request.addHeader("Authorization", "Bearer " + token(Role.USER));
}
```

Proposed:
```java
@Test
void doFilter_whenAuthenticationCookieValid_setsAuthentication() throws Exception {
  var request = new MockHttpServletRequest("GET", "/api/protected");
  request.setCookies(new Cookie(BrowserAuthenticationCookies.AUTH_COOKIE_NAME, token(Role.USER)));
  filter().doFilter(request, new MockHttpServletResponse(), new MockFilterChain());
  assertEquals("account-1", SecurityContextHolder.getContext().getAuthentication().getName());
}

@Test
void doFilter_whenBearerAndCookiePresent_prioritizesBearer() throws Exception {
  var request = new MockHttpServletRequest("GET", "/api/protected");
  request.addHeader("Authorization", "Bearer not-a-token");
  request.setCookies(new Cookie(BrowserAuthenticationCookies.AUTH_COOKIE_NAME, token(Role.USER)));
  var response = new MockHttpServletResponse();
  filter().doFilter(request, response, new MockFilterChain());
  assertEquals(401, response.getStatus());
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest --no-daemon`
- Expected RED: cookie-only authentication remains anonymous.

#### Code Edit 1.3
- File: `website/src/test/java/dev/christopherbell/account/AccountControllerTest.java`
- Lines: 536-595
- Action: replace

Current:
```java
mockMvc.perform(post("/api/accounts" + APIVersion.V20241215 + "/login")
        .with(csrf())
        .content(json)
        .contentType(MediaType.APPLICATION_JSON_VALUE))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.payload").value("jwt-token"));

verify(accountService).requestPasswordReset(
    eq(new AccountPasswordResetRequest("user@example.com")),
    eq("http://localhost"));
```

Proposed:
```java
mockMvc.perform(post(LOGIN).with(csrf()).content(validLoginJson()).contentType(APPLICATION_JSON))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.payload").doesNotExist())
    .andExpect(header().stringValues(SET_COOKIE,
        hasItem(containsString("CBELL_AUTH=jwt-token")),
        hasItem(containsString("HttpOnly")),
        hasItem(containsString("SameSite=Lax"))));

mockMvc.perform(post(LOGOUT).with(csrf()))
    .andExpect(status().isOk())
    .andExpect(header().string(SET_COOKIE, containsString("Max-Age=0")));

mockMvc.perform(post(PASSWORD_RESET_REQUEST).with(csrf())
        .header("X-Forwarded-Host", "attacker.example")
        .content(validResetRequestJson()).contentType(APPLICATION_JSON))
    .andExpect(status().isOk());
verify(accountService).requestPasswordReset(
    eq(new AccountPasswordResetRequest("user@example.com")),
    eq("https://www.christopherbell.dev"));

// Parameterized malformed login/reset request/reset confirmation bodies assert 400
// and verifyNoInteractions(accountService).
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.AccountControllerTest --no-daemon`
- Expected RED: login returns the JWT, no logout exists, forwarded host controls the reset base, and malformed DTOs enter the service.

#### Code Edit 1.4
- File: `website/src/test/js/browser-auth.test.js`
- Lines: 1
- Action: add

Proposed:
```javascript
import assert from 'node:assert/strict';
import test from 'node:test';

test('authHeaders sends the readable CSRF token but never an Authorization header', async () => {
  globalThis.document = { cookie: 'CBELL_AUTH_STATE=1; XSRF-TOKEN=csrf-value' };
  const { authHeaders } = await import('../../main/resources/static/js/lib/util.js');
  assert.deepEqual(authHeaders(), { 'X-XSRF-TOKEN': 'csrf-value' });
});

test('fetchJson includes same-origin credentials and CSRF on unsafe requests', async () => {
  let captured;
  globalThis.fetch = async (url, options) => {
    captured = { url, options };
    return { ok: true, status: 200, json: async () => ({ success: true }) };
  };
  const { fetchJson } = await import('../../main/resources/static/js/lib/util.js');
  await fetchJson('/api/example', { method: 'POST', body: '{}' });
  assert.equal(captured.options.credentials, 'same-origin');
  assert.equal(captured.options.headers['X-XSRF-TOKEN'], 'csrf-value');
});

test('browser auth helpers never read or write cbellLoginToken', async () => {
  globalThis.localStorage = {
    getItem(key) { if (key === 'cbellLoginToken') throw new Error('JWT read'); return ''; },
    setItem(key) { if (key === 'cbellLoginToken') throw new Error('JWT write'); },
    removeItem(key) { if (key === 'cbellLoginToken') throw new Error('JWT removal'); },
  };
  assert.equal((await import('../../main/resources/static/js/lib/util.js')).isLoggedIn(), true);
});
```

Verification:
- `node --test website/src/test/js/browser-auth.test.js`
- Expected RED: `authHeaders` still exposes the localStorage JWT and fetch lacks automatic CSRF.

#### Code Edit 1.5
- File: `website/src/test/js/signup-auth.test.js`
- Lines: 1
- Action: add

Proposed:
```javascript
import assert from 'node:assert/strict';
import test from 'node:test';

test('signup payload rejects blank first and last names before fetch', async () => {
  const { signupPayload } = await import('../../main/resources/static/js/auth/signup.js');
  assert.throws(
    () => signupPayload({ email: 'u@example.com', username: 'user', firstName: ' ', lastName: 'Bell', password: 'password' }),
    /First name is required/,
  );
});
```

Verification:
- Focused Node test is RED because no exported signup payload boundary exists and blank names become `null`.

### Task 2 - Configure browser headers and SPA CSRF

Sequence / dependencies:
- After Task 1 RED; establishes the global browser enforcement boundary before cookie authentication is enabled.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Every response receives the compatible CSP/referrer/permissions/frame policy; production emits one-year HSTS; SPA requests receive a CSRF cookie; unsafe cookie flows need the matching header; bearer requests remain exempt.
  - Invariants: The persistent media shell keeps SAMEORIGIN framing; Bootstrap, Font Awesome, supported embeds, remote images, workers, and local media keep working; aggregate Actuator security is unchanged.
  - Boundary/API: Typed `app.browser-security` configuration and Spring's production `SecurityFilterChain`.
  - Effects and failures: Startup rejects malformed canonical origins; security filters mutate response headers/cookies and reject invalid unsafe requests with 403.
  - Tests and evidence: Task 1 production-chain tests go GREEN; bearer mutation characterization remains GREEN.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/BrowserSecurityProperties.java`
- Lines: 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.security;

import java.net.URI;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties("app.browser-security")
public record BrowserSecurityProperties(
    URI publicBaseUrl,
    boolean authenticationCookieSecure,
    boolean hstsEnabled
) {
  public BrowserSecurityProperties {
    if (publicBaseUrl == null
        || !("http".equalsIgnoreCase(publicBaseUrl.getScheme())
            || "https".equalsIgnoreCase(publicBaseUrl.getScheme()))
        || publicBaseUrl.getHost() == null
        || publicBaseUrl.getUserInfo() != null
        || publicBaseUrl.getQuery() != null
        || publicBaseUrl.getFragment() != null
        || !(publicBaseUrl.getPath() == null || publicBaseUrl.getPath().isEmpty())) {
      throw new IllegalArgumentException(
          "app.browser-security.public-base-url must be an http(s) origin without path, query, fragment, or user info");
    }
  }
}
```

Verification:
- Add focused binding/constructor cases for canonical HTTPS, local HTTP, and rejected attacker-shaped values.

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 1-165
- Action: replace

Current:
```java
.csrf(AbstractHttpConfigurer::disable)
.headers(headers -> headers.frameOptions(frameOptions -> frameOptions.sameOrigin()))
```

Proposed:
```java
private static final String CONTENT_SECURITY_POLICY = String.join("; ",
    "default-src 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "script-src 'self' https://cdn.jsdelivr.net",
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://maxcdn.bootstrapcdn.com",
    "font-src 'self' data: https://maxcdn.bootstrapcdn.com",
    "img-src 'self' data: blob: https:",
    "connect-src 'self' https://gateway.raisingcanes.com https://order.raisingcanes.com",
    "frame-src https://www.youtube.com https://www.youtube-nocookie.com https://open.spotify.com https://w.soundcloud.com",
    "frame-ancestors 'self'",
    "media-src 'self' blob:",
    "worker-src 'self' blob:",
    "form-action 'self'");
private static final String PERMISSIONS_POLICY =
    "camera=(), geolocation=(), microphone=(), payment=(), usb=()";

.csrf(csrf -> csrf
    .spa()
    .ignoringRequestMatchers(SecurityConfig::hasExplicitBearerToken))
.headers(headers -> headers
    .contentSecurityPolicy(csp -> csp.policyDirectives(CONTENT_SECURITY_POLICY))
    .frameOptions(frameOptions -> frameOptions.sameOrigin())
    .httpStrictTransportSecurity(hsts -> hsts
        .requestMatcher(request -> browserSecurityProperties.hstsEnabled())
        .includeSubDomains(true)
        .maxAgeInSeconds(31_536_000))
    .permissionsPolicy(permissions -> permissions.policy(PERMISSIONS_POLICY))
    .referrerPolicy(referrer -> referrer
        .policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN)))

// Add V20241215 + "/logout" to PUBLIC_URLS so an expired browser session can
// still clear both cookies; SPA CSRF remains required because authorization
// permit rules do not bypass CsrfFilter.
```

Verification:
- Production filter-chain tests assert exact headers on `/login` and reject a cookie mutation lacking CSRF.
- An existing bearer mutation without CSRF still reaches its controller/capability boundary.

#### Code Edit 2.3
- File: `website/src/main/resources/application.yml`
- Lines: 65-68
- Action: replace

Current:
```yaml
app:
  jwt:
    secret: ${APP_JWT_SECRET:local-development-jwt-secret-change-me-at-least-32-bytes}
```

Proposed:
```yaml
app:
  browser-security:
    public-base-url: ${APP_PUBLIC_BASE_URL:http://localhost:8080}
    authentication-cookie-secure: false
    hsts-enabled: false
  jwt:
    secret: ${APP_JWT_SECRET:local-development-jwt-secret-change-me-at-least-32-bytes}
```

Verification:
- Local profile starts without HSTS/Secure cookies and uses the explicit localhost reset origin.

#### Code Edit 2.4
- File: `website/src/main/resources/application-prod.yml`
- Lines: 1-25
- Action: replace

Current:
```yaml
server:
  port: 8080
app:
  jwt:
    secret: ${APP_JWT_SECRET:}
```

Proposed:
```yaml
server:
  port: 8080
  forward-headers-strategy: none
app:
  browser-security:
    public-base-url: ${APP_PUBLIC_BASE_URL:https://www.christopherbell.dev}
    authentication-cookie-secure: true
    hsts-enabled: true
  jwt:
    secret: ${APP_JWT_SECRET:}
```

Verification:
- Prod-profile binding proves forwarded host/proto are not framework-authoritative and the canonical origin/cookie/HSTS defaults are secure.

### Task 3 - Move browser JWT transport to HttpOnly cookies

Sequence / dependencies:
- After Task 2; the authentication cookie is not enabled until CSRF is enforced.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Login sets HttpOnly auth and readable state cookies without returning a token; logout expires both; JWT filter authenticates cookie-only browser requests while preserving bearer precedence.
  - Invariants: Only the HttpOnly cookie contains credentials; explicit bearer behavior and one-day expiry remain compatible; marker/role UI state never authorizes a server action.
  - Boundary/API: Account login/logout HTTP responses, cookie serialization, and `JwtAuthenticationFilter` token resolution.
  - Effects and failures: Login mutates response cookies after successful account authentication; invalid cookies produce the existing anonymous/public or 401/protected outcomes.
  - Tests and evidence: Login/logout MockMvc and filter tests from Task 1 go GREEN; a repository scan finds no JWT response payload or `cbellLoginToken` production reference.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/BrowserAuthenticationCookies.java`
- Lines: 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.security;

import java.time.Duration;
import java.util.List;
import org.springframework.http.ResponseCookie;
import org.springframework.stereotype.Component;

@Component
public class BrowserAuthenticationCookies {
  public static final String AUTH_COOKIE_NAME = "CBELL_AUTH";
  public static final String AUTH_STATE_COOKIE_NAME = "CBELL_AUTH_STATE";
  private static final Duration AUTH_LIFETIME = Duration.ofDays(1);

  private final BrowserSecurityProperties properties;

  public BrowserAuthenticationCookies(BrowserSecurityProperties properties) {
    this.properties = properties;
  }

  public List<ResponseCookie> authenticated(String jwt) {
    return List.of(cookie(AUTH_COOKIE_NAME, jwt, true, AUTH_LIFETIME),
        cookie(AUTH_STATE_COOKIE_NAME, "1", false, AUTH_LIFETIME));
  }

  public List<ResponseCookie> cleared() {
    return List.of(cookie(AUTH_COOKIE_NAME, "", true, Duration.ZERO),
        cookie(AUTH_STATE_COOKIE_NAME, "", false, Duration.ZERO));
  }
}
```

Verification:
- Unit cases assert Path=/, HttpOnly only on JWT, SameSite=Lax, one-day Max-Age, profile-driven Secure, and zero-age clearing.

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java`
- Lines: 25-105
- Action: replace

Current:
```java
/** Servlet filter that authenticates requests using a JWT found in the
 * {@code Authorization: Bearer <token>} header. */
private boolean hasBearerToken(HttpServletRequest request) { ... }
private String resolveToken(HttpServletRequest request) { ... }
```

Proposed:
```java
/** Authenticates an explicit bearer JWT first, otherwise the HttpOnly browser cookie. */
private String resolveToken(HttpServletRequest request) {
  var authorization = request.getHeader(HttpHeaders.AUTHORIZATION);
  if (authorization != null && authorization.startsWith("Bearer ")) {
    return authorization.substring("Bearer ".length()).trim();
  }
  var cookie = WebUtils.getCookie(request, BrowserAuthenticationCookies.AUTH_COOKIE_NAME);
  return cookie == null || cookie.getValue().isBlank() ? null : cookie.getValue();
}

@Override
protected boolean shouldNotFilter(HttpServletRequest request) {
  return isPublicRequest(request) && resolveToken(request) == null;
}
```

Verification:
- Bearer valid/invalid, cookie valid/invalid, public anonymous, public personalized, and bearer-precedence cases pass.

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/account/AccountController.java`
- Lines: 57-380
- Action: replace

Current:
```java
@AllArgsConstructor
public class AccountController {
  private AccountService accountService;
  private PermissionService permissionService;
}

public ResponseEntity<Response<String>> loginAccount(
    @RequestBody AccountLoginRequest accountLoginRequest) throws Exception {
  return new ResponseEntity<>(Response.<String>builder()
      .payload(accountService.loginAccount(accountLoginRequest))
      .success(true).build(), HttpStatus.OK);
}
```

Proposed:
```java
private final BrowserAuthenticationCookies browserAuthenticationCookies;
private final BrowserSecurityProperties browserSecurityProperties;

public ResponseEntity<Response<Void>> loginAccount(
    @Valid @RequestBody AccountLoginRequest accountLoginRequest) throws Exception {
  var token = accountService.loginAccount(accountLoginRequest);
  return new ResponseEntity<>(Response.<Void>builder().success(true).build(),
      cookieHeaders(browserAuthenticationCookies.authenticated(token)), HttpStatus.OK);
}

@PostMapping(value = V20241215 + "/logout", produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Response<Void>> logoutAccount() {
  return new ResponseEntity<>(Response.<Void>builder().success(true).build(),
      cookieHeaders(browserAuthenticationCookies.cleared()), HttpStatus.OK);
}
```

Verification:
- MockMvc asserts no JWT body, exact cookie flags, successful cookie-authenticated `/me`, CSRF-required logout, and clearing headers.

### Task 4 - Convert browser fetch and shared-folder media flows to cookies

Sequence / dependencies:
- After Task 3; browser code switches only after the server accepts cookies.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Browser fetches send same-origin cookies and CSRF; UI auth uses only a non-secret marker; logout calls the server; native shared-folder media/download fetches forward their original cookie credentials without holding or injecting JWTs.
  - Invariants: Bearer API clients are unaffected; 401 still clears UI state; shared-folder capability checks, Range headers, one-time download URLs, denial notifications, and no-store behavior remain intact.
  - Boundary/API: `util.js`, auth page modules, nav/app pubsub, API paths, service worker, worker runtime, and media/download preparation exports.
  - Effects and failures: Browser fetch/cookie/DOM/service-worker effects stay in existing modules; logout network failure does not claim success; denied media still reports 401/403.
  - Tests and evidence: Task 1 browser tests and updated shared-folder behavior tests go GREEN; a production-source scan finds no JWT transfer or `Authorization` synthesis in browser modules.

#### Code Edit 4.1
- File: `website/src/main/resources/static/js/lib/util.js`
- Lines: 8-163
- Action: replace

Current:
```javascript
export function getAuthToken() {
  const storedToken = String(localStorage.getItem('cbellLoginToken') || '').trim();
  // decode/validate/store JWT
}

export function authHeaders(extraHeaders = {}) {
  const token = getAuthToken();
  return { ...extraHeaders, ...(token ? { Authorization: `Bearer ${token}` } : {}) };
}
```

Proposed:
```javascript
const AUTH_STATE_COOKIE = 'CBELL_AUTH_STATE';
const CSRF_COOKIE = 'XSRF-TOKEN';

export function getAuthToken() {
  return cookieValue(AUTH_STATE_COOKIE);
}

export function getAuthClaims() {
  return getAuthToken()
    ? { sub: 'browser-session', role: localStorage.getItem('cbellRole') || '' }
    : null;
}

export function authHeaders(extraHeaders = {}) {
  const csrf = cookieValue(CSRF_COOKIE);
  return { ...extraHeaders, ...(csrf ? { 'X-XSRF-TOKEN': csrf } : {}) };
}

export async function fetchJson(url, options = {}) {
  const method = String(options.method || 'GET').toUpperCase();
  const headers = SAFE_METHODS.has(method)
    ? { 'Content-Type': 'application/json', ...(options.headers || {}) }
    : authHeaders({ 'Content-Type': 'application/json', ...(options.headers || {}) });
  const resp = await fetch(url, { ...options, credentials: 'same-origin', headers });
  if (resp.status === 401) {
    clearAuthState();
    const error = Object.assign(new Error('Authentication required.'), { status: 401 });
    throw error;
  }
  const data = await resp.json().catch(() => ({}));
  if (!resp.ok || data.success === false) {
    const message = data?.messages?.[0]?.description || `Request failed: ${resp.status}`;
    throw Object.assign(new Error(message), { status: resp.status });
  }
  return data.payload ?? data;
}
```

Verification:
- Real exported helper tests assert decoded cookie values, no Authorization header, same-origin credentials, unsafe CSRF, safe GET behavior, and 401 state clearing.

#### Code Edit 4.2
- File: `website/src/main/resources/static/js/lib/api.js`
- Lines: 26-34
- Action: replace

Current:
```javascript
accounts: {
  base: '/api/accounts/2024-12-15',
  login: '/api/accounts/2024-12-15/login',
  create: '/api/accounts/2024-12-15/create',
```

Proposed:
```javascript
accounts: {
  base: '/api/accounts/2024-12-15',
  login: '/api/accounts/2024-12-15/login',
  logout: '/api/accounts/2024-12-15/logout',
  create: '/api/accounts/2024-12-15/create',
```

Verification:
- Login/logout browser tests use only these canonical paths.

#### Code Edit 4.3
- File: `website/src/main/resources/static/js/auth/login.js`
- Lines: 8-61
- Action: replace

Current:
```javascript
const resp = await fetch(API.accounts.login, { method: 'POST', ... });
return data.payload;
if (localStorage.getItem('cbellLoginToken')) { ... }
localStorage.setItem('cbellLoginToken', token);
```

Proposed:
```javascript
import { fetchJson, isLoggedIn, safeRedirectTarget } from '../lib/util.js';

export async function login(email, password) {
  await fetchJson(API.accounts.login, {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

if (isLoggedIn()) { ... }
await login(email, password);
pubsub.publish('auth:login');
window.location.href = redirectTarget();
```

Verification:
- Login test asserts CSRF/cookie credentials and proves no localStorage JWT write occurs.

#### Code Edit 4.4
- File: `website/src/main/resources/static/js/auth/forgot-password.js`
- Lines: 4-28
- Action: replace

Current:
```javascript
const resp = await fetch(API.accounts.passwordResetRequest, {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, ...
});
```

Proposed:
```javascript
import { fetchJson } from '../lib/util.js';
export function requestPasswordReset(email) {
  return fetchJson(API.accounts.passwordResetRequest, {
    method: 'POST', body: JSON.stringify({ email }),
  });
}
```

Verification:
- Browser-auth test proves password-reset request receives CSRF automatically.

#### Code Edit 4.5
- File: `website/src/main/resources/static/js/auth/reset-password.js`
- Lines: 4-28
- Action: replace

Current:
```javascript
const resp = await fetch(API.accounts.passwordResetConfirm, {
  method: 'POST', headers: { 'Content-Type': 'application/json' }, ...
});
```

Proposed:
```javascript
import { fetchJson } from '../lib/util.js';
export function resetPassword(token, password) {
  return fetchJson(API.accounts.passwordResetConfirm, {
    method: 'POST', body: JSON.stringify({ token, password }),
  });
}
```

Verification:
- Browser-auth test proves password-reset confirmation receives CSRF automatically.

#### Code Edit 4.6
- File: `website/src/main/resources/static/js/app.js`
- Lines: 7-64
- Action: replace

Current:
```javascript
installSharedFolderAuthRecovery(getAuthToken);
pubsub.subscribe('auth:logout', () => {
  clearSharedFolderStreamingAuth();
  localStorage.removeItem('cbellLoginToken');
  window.location.href = '/login';
});
```

Proposed:
```javascript
pubsub.subscribe('auth:logout', async () => {
  await fetchJson(API.accounts.logout, { method: 'POST' });
  stopSiteMediaPlayback();
  clearAuthState();
  window.location.href = '/login';
});
```

Verification:
- Logout test asserts POST plus CSRF precedes local cleanup/navigation; failures do not report a completed logout.

#### Code Edit 4.7
- File: `website/src/main/resources/static/shared-folder-auth-sw.js`
- Lines: 1-59
- Action: replace

Current:
```javascript
const clientTokens = new Map();
const downloadTokens = new Map();
const mediaAuthorizations = new Map();
// message handlers stage/recover JWTs
```

Proposed:
```javascript
import { isSharedFolderApiRequest } from './js/lib/shared-folder-streaming.js';
import { respondToSharedFolderFetch } from './js/lib/shared-folder-worker-runtime.js';

self.addEventListener('fetch', event => {
  if (!isSharedFolderApiRequest(event.request, self.location.origin)) return;
  event.respondWith(respondToSharedFolderFetch({
    request: event.request,
    clientId: event.clientId,
    clients: self.clients,
    fetchFn: fetch,
  }));
});
```

Verification:
- Worker tests prove it forwards same-origin request cookies/Range unchanged, never stages a token, and still reports 401/403.

#### Code Edit 4.8
- File: `website/src/main/resources/static/js/lib/shared-folder-worker-runtime.js`
- Lines: 1-170
- Action: replace

Current:
```javascript
let token = consumeSharedFolderDownloadAuthorization(...);
if (!token) token = clientTokens.get(clientId);
if (!token) token = await recoverClientToken(...);
const response = await fetchFn(attachSharedFolderAuthorization(request, token, origin), ...);
```

Proposed:
```javascript
export async function respondToSharedFolderFetch({ request, clientId, clients, fetchFn = fetch }) {
  const response = await fetchFn(request, { cache: 'no-store' });
  if (response.status === 401 || response.status === 403) {
    await notifySharedFolderDenial(clients, clientId, response.status);
  }
  return response;
}
```

Verification:
- Runtime tests use a Request with Cookie/Range semantics and assert the identical request reaches `fetchFn`; denial notification remains bounded to the initiating client.

#### Code Edit 4.9
- File: `website/src/main/resources/static/js/lib/shared-folder-streaming.js`
- Lines: 1-135
- Action: replace

Current:
```javascript
export function attachSharedFolderAuthorization(request, token, origin) { ... }
export async function prepareSharedFolderStreamingAuth(token) { ... }
export async function prepareSharedFolderDownloadAuth(token, requestUrl) { ... }
export async function prepareSharedFolderMediaAuth(token, requestUrl) { ... }
```

Proposed:
```javascript
export async function prepareSharedFolderStreamingAuth() {
  if (!('serviceWorker' in navigator)) {
    throw new Error('This browser cannot securely stream shared-folder files.');
  }
  await navigator.serviceWorker.register(SHARED_FOLDER_AUTH_WORKER_URL, {
    scope: '/', type: 'module',
  });
  await navigator.serviceWorker.ready;
  return waitForExpectedController();
}

export const prepareSharedFolderDownloadAuth = prepareSharedFolderStreamingAuth;
export const prepareSharedFolderMediaAuth = prepareSharedFolderStreamingAuth;
```

Verification:
- Streaming tests prove no function accepts, stores, posts, or attaches a JWT and the worker registration/controller readiness contract remains.

#### Code Edit 4.10
- File: `website/src/main/resources/static/js/shared-folder.js`
- Lines: 78-689
- Action: replace

Current:
```javascript
const token = getAuthToken();
await prepareSharedFolderStreamingAuth(token);
await prepareSharedFolderDownloadAuth(token, requestUrl);
token: getAuthToken() || null,
```

Proposed:
```javascript
await prepareSharedFolderStreamingAuth();
await prepareSharedFolderDownloadAuth();
navigator.serviceWorker.addEventListener('message', event => {
  if (event.data?.type === 'shared-folder-auth-denied') {
    handleSharedFolderAccessLoss(Number(event.data.status || 403));
  }
});
```

Verification:
- Shared-folder page initialization and streaming suites pass; unauthenticated page still redirects based on the non-secret marker.

#### Code Edit 4.11
- File: `website/src/main/resources/static/js/components/site-media-player.js`
- Lines: 420-470
- Action: replace

Current:
```javascript
await prepareSharedFolderMediaAuth(getAuthToken(), url);
```

Proposed:
```javascript
await prepareSharedFolderMediaAuth();
```

Verification:
- Media-player tests prove the worker is ready before assigning native media URLs and cookie transport contains no JavaScript credential.

#### Code Edit 4.12
- File: `website/src/main/resources/static/js/components/nav.js`
- Lines: 8-190
- Action: replace

Current:
```javascript
const token = getAuthToken();
const resp = await fetch(API.accounts.me, {
  headers: { Authorization: `Bearer ${token}` }
});
```

Proposed:
```javascript
if (!isLoggedIn()) return;
const account = await fetchJson(API.accounts.me);
localStorage.setItem('cbellUsername', account.username || '');
localStorage.setItem('cbellRole', account.role || '');
```

Verification:
- Nav tests prove the marker gates optional loads, `/me` remains authoritative, and no Authorization header is synthesized.

#### Code Edit 4.13
- File: `website/src/main/resources/static/js/back-office.js`
- Lines: 947-970
- Action: replace

Current:
```javascript
const token = localStorage.getItem('cbellLoginToken');
const resp = await fetch(API.accounts.me, {
  headers: { Authorization: `Bearer ${token}` }
});
```

Proposed:
```javascript
if (!isLoggedIn()) {
  window.location.replace('/404');
  return;
}
const account = await fetchJson(API.accounts.me, { redirectOnUnauthorized: false });
```

Verification:
- Back-office gate uses the server-reported role and cookie request; forged UI state cannot reveal a working admin API.

#### Code Edit 4.14
- File: `website/src/main/resources/static/js/command-center.js`
- Lines: 1-72
- Action: replace

Current:
```javascript
if (!localStorage.getItem('cbellLoginToken')) {
  redirectLostSignal();
  return;
}
```

Proposed:
```javascript
if (!isLoggedIn()) {
  redirectLostSignal();
  return;
}
```

Verification:
- Command-center gate tests use the non-secret marker only for early UI routing and still require the server's exact ADMIN result.

#### Code Edit 4.15
- File: `website/src/main/resources/static/js/home-feed.js`
- Lines: 1-138
- Action: replace

Current:
```javascript
const token = localStorage.getItem('cbellLoginToken');
if (token) {
  const me = await fetchJson(API.accounts.me, { headers: authHeaders() });
}
```

Proposed:
```javascript
if (isLoggedIn()) {
  const me = await fetchJson(API.accounts.me);
}
```

Verification:
- Home feed preserves anonymous rendering and obtains delete permissions only from authenticated `/me`.

#### Code Edit 4.16
- File: `website/src/main/resources/static/js/user-feed.js`
- Lines: 1-180
- Action: replace

Current:
```javascript
if (localStorage.getItem('cbellLoginToken')) {
  const me = await fetchJson('/api/accounts/2025-09-03/me', { headers: authHeaders() });
}
```

Proposed:
```javascript
if (isLoggedIn()) {
  const me = await fetchJson(API.accounts.me);
}
```

Verification:
- Public profiles remain anonymous-capable and delete/trust UI depends on the server account response.

#### Code Edit 4.17
- File: `website/src/main/resources/static/js/post.js`
- Lines: 1-360
- Action: replace

Current:
```javascript
if (localStorage.getItem('cbellLoginToken')) {
  try { me = await fetchJson(API.accounts.me, { headers: authHeaders() }); } catch (_) {}
}
```

Proposed:
```javascript
if (isLoggedIn()) {
  try { me = await fetchJson(API.accounts.me); } catch (_) {}
}
```

Verification:
- Post thread remains public while signed-in controls use cookie-authenticated `/me`; production source contains no `cbellLoginToken`.

### Task 5 - Canonicalize reset origins and validate authentication DTOs

Sequence / dependencies:
- After cookie/security configuration exists; uses the same typed browser-security properties.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Reset emails always use configured `publicBaseUrl`; malformed login/reset bodies return the standard 400 envelope before service invocation.
  - Invariants: Generic reset-request success still avoids account enumeration; password bounds match account creation; forwarded host/proto never affect links.
  - Boundary/API: Bean Validation request records and AccountController request mapping.
  - Effects and failures: Valid reset requests may store/send as before; invalid transport data has no account/email effect; property failures stop startup.
  - Tests and evidence: Parameterized Task 1 MockMvc cases and spoofed-header test go GREEN; existing AccountService reset tests remain GREEN.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/account/model/AccountLoginRequest.java`
- Lines: 1-12
- Action: replace

Current:
```java
public record AccountLoginRequest(String email, String password) {}
```

Proposed:
```java
public record AccountLoginRequest(
    @NotBlank @Email @Size(max = 254) String email,
    @NotBlank @Size(max = 128) String password
) {}
```

Verification:
- Missing/blank/malformed/oversized email and missing/blank/oversized password return 400 before login service execution.

#### Code Edit 5.2
- File: `website/src/main/java/dev/christopherbell/account/model/AccountPasswordResetRequest.java`
- Lines: 1-11
- Action: replace

Current:
```java
public record AccountPasswordResetRequest(String email) {}
```

Proposed:
```java
public record AccountPasswordResetRequest(
    @NotBlank @Email @Size(max = 254) String email
) {}
```

Verification:
- Missing/blank/malformed/oversized email returns 400 without calling reset service.

#### Code Edit 5.3
- File: `website/src/main/java/dev/christopherbell/account/model/AccountPasswordResetConfirmRequest.java`
- Lines: 1-12
- Action: replace

Current:
```java
public record AccountPasswordResetConfirmRequest(String token, String password) {}
```

Proposed:
```java
public record AccountPasswordResetConfirmRequest(
    @NotBlank @Size(max = 512) String token,
    @NotBlank @Size(min = 8, max = 128) String password
) {}
```

Verification:
- Missing/blank/oversized token and password outside 8-128 return 400 without calling reset service.

#### Code Edit 5.4
- File: `website/src/main/java/dev/christopherbell/account/AccountController.java`
- Lines: 358-464
- Action: replace

Current:
```java
public ResponseEntity<Response<String>> requestPasswordReset(
    @RequestBody AccountPasswordResetRequest requestBody,
    HttpServletRequest servletRequest) {
  accountService.requestPasswordReset(requestBody, getBaseUrl(servletRequest));
}

private String getBaseUrl(HttpServletRequest request) { ... }
```

Proposed:
```java
public ResponseEntity<Response<String>> requestPasswordReset(
    @Valid @RequestBody AccountPasswordResetRequest requestBody) {
  accountService.requestPasswordReset(
      requestBody, browserSecurityProperties.publicBaseUrl().toString());
}

public ResponseEntity<Response<String>> resetPassword(
    @Valid @RequestBody AccountPasswordResetConfirmRequest request) throws Exception {
  accountService.resetPassword(request);
  return ResponseEntity.ok(Response.<String>builder()
      .payload("Your password has been reset.")
      .success(true)
      .build());
}

// Delete getBaseUrl; no request host or forwarded header enters reset-link construction.
```

Verification:
- Spoofed `Host`, `Forwarded`, `X-Forwarded-Host`, and `X-Forwarded-Proto` leave the service argument exactly `https://www.christopherbell.dev`.

### Task 6 - Make signup names consistently required

Sequence / dependencies:
- After central CSRF/fetch changes so signup can use the same request boundary.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Before-Edit Brief:
  - Behavior: Browser-native validation and the JS payload boundary both reject blank first/last name; valid signup sends trimmed non-null names through CSRF-protected fetch.
  - Invariants: Existing server `@NotBlank` and 100-character maximum remain authoritative; page layout and redirect behavior remain unchanged.
  - Boundary/API: Signup HTML inputs and exported `signupPayload`/`signup` browser functions.
  - Effects and failures: Invalid names cause no network request; valid signup performs one same-origin POST and preserves API error messages.
  - Tests and evidence: Task 1 signup test goes GREEN; markup test asserts required/max length; AccountController create validation stays GREEN.

#### Code Edit 6.1
- File: `website/src/main/resources/templates/signup.html`
- Lines: 33-41
- Action: replace

Current:
```html
<input type="text" class="form-control" id="firstName" />
<input type="text" class="form-control" id="lastName" />
```

Proposed:
```html
<input type="text" class="form-control" id="firstName" maxlength="100" required />
<input type="text" class="form-control" id="lastName" maxlength="100" required />
```

Verification:
- Markup test asserts both labeled inputs are required and capped at 100 characters.

#### Code Edit 6.2
- File: `website/src/main/resources/static/js/auth/signup.js`
- Lines: 8-65
- Action: replace

Current:
```javascript
firstName: document.getElementById('firstName')?.value?.trim() || null,
lastName: document.getElementById('lastName')?.value?.trim() || null,
```

Proposed:
```javascript
export function signupPayload(values) {
  const firstName = String(values.firstName || '').trim();
  const lastName = String(values.lastName || '').trim();
  if (!firstName) throw new Error('First name is required.');
  if (!lastName) throw new Error('Last name is required.');
  return { ...values, firstName, lastName };
}

export function signup(payload) {
  return fetchJson(API.accounts.create, {
    method: 'POST', body: JSON.stringify(signupPayload(payload)),
  });
}
```

Verification:
- Unit tests cover blank/whitespace names, trimmed valid names, no-fetch invalid behavior, CSRF-protected valid request, and existing redirect/error rendering.

### Task 7 - Verify, review, deploy, and close

Sequence / dependencies:
- Last; only after Tasks 1-6 are GREEN and the diff is cohesive.

Implementation notes:
- No code edits. Invoke `write-chris-street-style-code` Review Mode, `superpowers:verification-before-completion`, and `superpowers:requesting-code-review` before merge.
- Review security boundaries for bearer bypass, cookie flags, CSRF coverage, CSP compatibility, credential leakage, reset-host trust, and validation side effects.

#### Code Edit 7.1
- File: `README.md`
- Lines: 79-110
- Action: replace

Current:
```markdown
Useful environment variables:

export APP_JWT_SECRET=replace-with-at-least-32-random-characters
```

Proposed:
```markdown
Useful environment variables include `APP_JWT_SECRET` and `APP_PUBLIC_BASE_URL`.

Set `APP_PUBLIC_BASE_URL` to the canonical public origin used in password-reset links.
Browser login uses an HttpOnly, SameSite cookie (Secure in production); explicit API clients
may continue to use bearer tokens. Browser mutations send Spring's `X-XSRF-TOKEN` value in
the `X-XSRF-TOKEN` header. Production enables HSTS and never trusts forwarded hosts for reset URLs.
```

Verification:
- Documentation names the supported environment key and operational invariants and contains no secret/token example.

## Code Changes

- Security configuration: add `BrowserSecurityProperties`, configure headers/SPA CSRF, and set local/prod defaults.
- Authentication transport: add `BrowserAuthenticationCookies`, extend `JwtAuthenticationFilter`, change login response, and add logout.
- Browser client: replace JWT localStorage/header flow with cookie credentials, XSRF headers, and non-secret marker state.
- Shared-folder client: remove JWT service-worker transfer/staging and forward same-origin cookie-bearing requests.
- Reset/validation: remove request-derived origin and add Bean Validation annotations/`@Valid`.
- Signup: mark first/last required in markup and enforce trimmed non-blank payloads in JS.
- Tests/docs: expand production-chain, controller, filter, browser, worker, and markup coverage; document operations.

## Files and Modules

- `website/src/main/java/dev/christopherbell/configuration/security/BrowserSecurityProperties.java`
- `website/src/main/java/dev/christopherbell/configuration/security/BrowserAuthenticationCookies.java`
- `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java`
- `website/src/main/java/dev/christopherbell/account/AccountController.java`
- `website/src/main/java/dev/christopherbell/account/model/AccountLoginRequest.java`
- `website/src/main/java/dev/christopherbell/account/model/AccountPasswordResetRequest.java`
- `website/src/main/java/dev/christopherbell/account/model/AccountPasswordResetConfirmRequest.java`
- `website/src/main/resources/application.yml`
- `website/src/main/resources/application-prod.yml`
- `website/src/main/resources/static/js/lib/util.js`
- `website/src/main/resources/static/js/lib/api.js`
- `website/src/main/resources/static/js/auth/{login,signup,forgot-password,reset-password}.js`
- `website/src/main/resources/static/js/app.js`
- `website/src/main/resources/static/js/components/{nav,site-media-player}.js`
- `website/src/main/resources/static/{shared-folder-auth-sw.js,js/shared-folder.js}`
- `website/src/main/resources/static/js/lib/{shared-folder-streaming,shared-folder-worker-runtime}.js`
- `website/src/main/resources/templates/signup.html`
- Focused Java/JavaScript tests and `docs/README.md`.

## Unit Testing

- Observe RED then GREEN:
  - `./gradlew :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest --no-daemon`
  - `./gradlew :website:test --tests dev.christopherbell.account.AccountControllerTest --no-daemon`
  - `./gradlew :website:test --tests dev.christopherbell.sharedfolder.SharedFolderSecurityIntegrationTest --no-daemon`
  - `./gradlew :website:jsTest --no-daemon`
- Add property/cookie unit coverage for valid/invalid canonical origins and exact Set-Cookie flags.
- Preserve existing account-service, shared-folder worker/runtime/streaming, nav, media-player, and accessibility tests.

## Local Testing

1. Run `./gradlew clean build --no-daemon` with an isolated `GRADLE_USER_HOME` if the shared registry is locked.
2. Launch the built JAR on a non-8080 port with local profile and test credentials.
3. In a clean browser context, verify `/login` creates `XSRF-TOKEN`; successful login creates `CBELL_AUTH` as HttpOnly/SameSite=Lax and creates only the non-secret readable marker; localStorage contains no JWT.
4. Verify `/api/accounts/2025-09-03/me`, a protected POST, logout, signup, forgot-password, reset-password, nav state, shared-folder listing, native download, and media Range playback.
5. Verify an unsafe cookie request without `X-XSRF-TOKEN` returns 403; the same request with the token reaches its normal boundary; explicit bearer mutation works without CSRF.
6. Verify forwarded-host spoof headers never alter the reset base passed to the service/mail fixture.
7. Inspect CSP console output on representative public/auth/shared-folder/feed pages and supported YouTube/Spotify/SoundCloud embeds.
8. Use `curl.exe -I` against the alternate port and production HTTPS to inspect all required headers and cookie flags.

## Validation

- No production browser source contains `cbellLoginToken`, decodes a JWT, synthesizes `Authorization`, posts a JWT to a worker, or returns a login JWT.
- Public page has the required CSP, SAMEORIGIN/frame-ancestors policy, referrer policy, permissions policy, nosniff, and production HSTS.
- Cookie-auth unsafe requests are rejected without valid CSRF; bearer calls remain explicit/stateless.
- Login/logout/cookie-authenticated `/me` and shared-folder media/download paths work end to end.
- All malformed authentication/reset payload partitions return the normal 400 envelope before service effects.
- Reset URL origin is configuration-owned and ignores spoofed forwarding/host headers.
- Signup browser and server both require first/last names.
- Full Gradle build, PR checks, CodeQL, and dependency review pass before merge.
- Native Windows auto-deployment reaches the merge SHA and live smoke/browser acceptance passes.

## Rollback or Recovery

- Revert the squash merge to restore the previous bearer-only browser behavior if production login or media fails.
- Do not disable CSRF as a hotfix. If token delivery alone fails, repair/roll back the browser cookie change together with its CSRF dependency.
- Cookie names are additive; rollback clients ignore them. Expire `CBELL_AUTH` and `CBELL_AUTH_STATE` through a temporary response rule if rollback leaves stale browser cookies.
- Restore the previous CSP/header block independently only if a required third-party source was missed; record the exact blocked origin before widening policy.
- `APP_PUBLIC_BASE_URL` can be corrected through production configuration without accepting request-supplied hosts.

## Risks

- CSP can silently break third-party styles, fonts, embeds, remote images, workers, or media. Mitigate with audited source lists, console inspection, and representative browser flows.
- CSRF changes affect every mutation. Mitigate with central `fetchJson`/`authHeaders` behavior, raw-fetch inventory, negative tests, and full JS/controller suites.
- HttpOnly cookies change native media authentication. Mitigate by removing bearer injection entirely and testing browser/service-worker cookie forwarding with Range and download requests.
- A readable marker can be stale or attacker-modified. Treat it only as display state and clear it on 401; every server endpoint remains authoritative.
- Bearer CSRF exemption could be broadened accidentally. Match only an explicit nonblank `Authorization: Bearer ...` header and keep browser code from generating it.
- Production origin sees HTTP behind Cloudflare. HSTS is driven by validated production configuration, not untrusted forwarded headers.
- One cohesive batch touches Java, configuration, templates, and browser modules. Keep task commits narrow, review the complete auth data flow, and exclude unrelated refactors.

## Completion Criteria

- Every Task 1 test was observed RED for the intended missing behavior and GREEN after implementation.
- Focused and full builds pass with clean output except documented pre-existing Gradle deprecation warnings.
- The final diff passes the Jane Street-style review rubric with no blockers.
- PR CI, CodeQL, and dependency review pass; independent review has no blocker.
- Issues #1125-#1130 close through the merged PR or receive evidence-backed closure comments.
- Non-8080 candidate, native Windows production deployment, and live browser/header/auth/CSRF acceptance all pass.
- Builder test report, spoke review/update, campaign ledger, issue closure record, and session memory are saved, indexed, validated, committed, and pushed.
