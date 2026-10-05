# christopherbell.dev Authentication Request Efficiency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate authentication database work for public static assets and reduce normal browser-cookie authentication to one MongoDB read without weakening revocation or rotation.

**Architecture:** Static-resource recognition becomes an explicit security boundary shared by authorization and the authentication filter. Browser sessions carry the validated account role snapshot, use conditional Mongo updates for coalesced activity and rotation, and are revoked at every account-security mutation boundary.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Security 7, Spring Data MongoDB, JUnit 5, Mockito.

## Global Constraints

- Static asset requests perform zero authentication-related MongoDB queries, even when cookies or bearer headers are present.
- Public APIs that tailor responses for a signed-in viewer must continue to authenticate supplied credentials.
- Missing legacy session snapshot fields fail closed; no role or active state may be assumed.
- Account suspension, role/permission/password changes, deletion, logout, and explicit revocation must invalidate browser sessions.
- Token rotation preserves the existing one-day interval and two-minute previous-token overlap.
- Interactive activity writes are coalesced to at most one durable touch per five minutes per session.
- Do not modify the dirty checkout at `A:\Projects\christopherbell.dev`; create an isolated `codex/` worktree from refreshed `origin/main` at execution time.
- Invoke `write-chris-street-style-code` and `superpowers:test-driven-development` before every production behavior edit.
- Implementation requires separate explicit user authorization.

---

## Document Status

ready-for-execution

## Objective

Implement the first backend hot-path batch from the approved performance specification, with measured before/after Mongo command counts and deterministic concurrency coverage.

## Goals

- Zero session/account repository calls for unversioned and versioned static assets.
- One session read and zero account reads on the normal cookie-authentication path.
- No full-document session save for ordinary interactive activity.
- Safe compare-and-set token rotation and fail-closed legacy-session handling.
- Central, tested browser-session revocation from every security-state mutation path.

## Inputs

- Approved spec: `docs/specs/2026-07-29-christopherbell-dev-performance-scalability-library-optimization.md` in Builder.
- Current source inspected at `origin/main` commit `f31535f29312d24573a6031b0162aa8ebc4b5318`.
- Existing public asset namespaces in `SecurityConfig.PUBLIC_URLS`.
- Existing browser-session lifetimes in `BrowserSessionService`.

## Branch

- Create `codex/auth-request-efficiency` from refreshed `origin/main` in a new isolated worktree.
- Re-inspect the listed ranges after branch creation. If current main moved, update this plan's ranges before editing rather than applying stale hunks.

## Non-Goals

- Do not change bearer-token account freshness behavior.
- Do not make protected Shared Folder/Music media or API responses public.
- Do not introduce Redis or a distributed HTTP-session framework.
- Do not change cookie names, CSRF behavior, login response shapes, or session lifetimes.

## Assumptions

- Static files under `/css`, `/images`, `/js`, `/vendor`, `/webjars/bootstrap/5.3.3`, and the version-prefixed equivalents are public and cannot use an authenticated security context.
- A browser session is created only after the account is active and the login JWT fingerprint matches current account state.
- MongoDB is the authoritative store for browser sessions and supports atomic conditional updates.

## Open Questions

None.

## File Structure

- `StaticAssetRequestMatcher` owns the exact always-anonymous static namespace.
- `BrowserSessionActivityStore` owns conditional Mongo writes; `BrowserSessionService` owns credential/session policy.
- `AccountSessionRevoker` is the narrow account-domain port used by mutation services; `BrowserSessionService` implements it.
- Existing feature services retain ownership of their account writes and call the revocation port only after a security-state write succeeds.

## Task Breakdown

### Task 1 - Make static assets always anonymous

Sequence / dependencies:
- Runs first because it is an independent hot-path change and establishes the zero-query assertion before session internals change.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke `superpowers:test-driven-development` for the behavior change.
- Before-Edit Brief:
  - Behavior: requests for recognized public static resources bypass authentication even when they carry a stale or valid cookie/bearer credential.
  - Invariants: protected APIs and viewer-aware public APIs continue to authenticate credentials; worker authorization and media APIs are not static assets.
  - Boundary/API: servlet request matching only; no public HTTP route is added.
  - Effects and failures: the bypass performs no database or cookie-clearing effect; malformed credentials on non-static routes retain current handling.
  - Tests and evidence: first add cookie/bearer static-resource tests that currently call authentication or reject; finish with filter and security configuration tests.

- [ ] Add failing tests for unversioned and versioned assets with credentials and verify the session/account collaborators have zero interactions.
- [ ] Run the focused test and capture the expected RED interaction/rejection.
- [ ] Add the exact static matcher and place it before credential resolution in `shouldNotFilter`.
- [ ] Run focused filter/security tests and inspect the production/test diff.
- [ ] Commit this independently testable behavior.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/configuration/JwtAuthenticationFilterTest.java`
- Lines: after 180
- Action: add

Proposed:
```java
  @Test
  @DisplayName("Static assets skip cookie authentication unconditionally")
  void doFilter_whenStaticAssetHasBrowserCookie_skipsSessionLookup()
      throws ServletException, IOException {
    var sessions = mock(BrowserSessionService.class);
    var filter = new JwtAuthenticationFilter(
        List.of(request -> true), sessions, new InteractiveBrowserRequest(), cookies());
    var request = new MockHttpServletRequest("GET", "/js/app.js");
    request.setCookies(new Cookie("CBELL_AUTH", "session-id.secret"));
    var response = new MockHttpServletResponse();

    filter.doFilter(request, response, new MockFilterChain());

    org.mockito.Mockito.verifyNoInteractions(sessions);
    assertEquals(200, response.getStatus());
  }

  @Test
  @DisplayName("Versioned static assets skip bearer authentication unconditionally")
  void doFilter_whenVersionedStaticAssetHasBearer_skipsAccountLookup()
      throws ServletException, IOException {
    var accounts = mock(AccountRepository.class);
    var filter = new JwtAuthenticationFilter(
        List.of(request -> true), null, null, null, accounts);
    var request = new MockHttpServletRequest(
        "GET", "/0123456789abcdef0123456789abcdef01234567/css/main.css");
    request.addHeader("Authorization", "Bearer invalid-but-irrelevant-for-static-content");
    var response = new MockHttpServletResponse();

    filter.doFilter(request, response, new MockFilterChain());

    org.mockito.Mockito.verifyNoInteractions(accounts);
    assertEquals(200, response.getStatus());
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest`
- RED expectation before production edit: at least one new test reports an authentication collaborator interaction or non-200 response.

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/StaticAssetRequestMatcher.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.security;

import jakarta.servlet.http.HttpServletRequest;
import java.util.List;
import org.springframework.http.HttpMethod;
import org.springframework.security.web.servlet.util.matcher.PathPatternRequestMatcher;
import org.springframework.security.web.util.matcher.RequestMatcher;

/** Matches only public cacheable resources that never consume an authenticated principal. */
public final class StaticAssetRequestMatcher implements RequestMatcher {
  private static final List<RequestMatcher> MATCHERS = List.of(
      get("/favicon.ico"),
      get("/css/**"),
      get("/images/**"),
      get("/js/**"),
      get("/vendor/**"),
      get("/webjars/bootstrap/5.3.3/**"),
      get("/{assetVersion}/favicon.ico"),
      get("/{assetVersion}/css/**"),
      get("/{assetVersion}/images/**"),
      get("/{assetVersion}/js/**"),
      get("/{assetVersion}/vendor/**"));

  @Override
  public boolean matches(HttpServletRequest request) {
    return MATCHERS.stream().anyMatch(matcher -> matcher.matches(request));
  }

  private static RequestMatcher get(String pattern) {
    return PathPatternRequestMatcher.pathPattern(HttpMethod.GET, pattern);
  }
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest --tests dev.christopherbell.configuration.SecurityConfigTest`

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java`
- Lines: 38-42
- Action: replace

Current:
```java
  private final List<RequestMatcher> skipMatchers = new ArrayList<>();
  private final BrowserSessionService browserSessions;
  private final InteractiveBrowserRequest interactiveRequests;
  private final BrowserAuthenticationCookies browserCookies;
  private final AccountRepository accounts;
```

Proposed:
```java
  private final List<RequestMatcher> skipMatchers = new ArrayList<>();
  private final RequestMatcher staticAssets = new StaticAssetRequestMatcher();
  private final BrowserSessionService browserSessions;
  private final InteractiveBrowserRequest interactiveRequests;
  private final BrowserAuthenticationCookies browserCookies;
  private final AccountRepository accounts;
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest`

#### Code Edit 1.4
- File: `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java`
- Lines: 75-80
- Action: replace

Current:
```java
  @Override
  protected boolean shouldNotFilter(HttpServletRequest request) {
    return isPublicRequest(request)
        && resolveBearerToken(request) == null
        && resolveCookieToken(request) == null;
  }
```

Proposed:
```java
  @Override
  protected boolean shouldNotFilter(HttpServletRequest request) {
    if (staticAssets.matches(request)) {
      return true;
    }
    return isPublicRequest(request)
        && resolveBearerToken(request) == null
        && resolveCookieToken(request) == null;
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest`

### Task 2 - Make the session document sufficient for normal authentication

Sequence / dependencies:
- Runs after Task 1. It changes the cookie-authentication trust boundary and must land with legacy-session and snapshot tests.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: a valid current session supplies account id and role from one session read; sessions without a role/fingerprint are deleted and rejected.
  - Invariants: only active accounts create sessions; role is never defaulted; creation still validates the login JWT against the current account.
  - Boundary/API: persisted `browser_sessions` gains nullable legacy-compatible `role`; authenticated request principal shape is unchanged.
  - Effects and failures: malformed, expired, incomplete, or invalid credentials delete the session when identifiable and return anonymous/401 through the existing filter.
  - Tests and evidence: change the existing invalidation test into explicit revocation tests in Task 4; add one-read and legacy fail-closed tests here.

- [ ] Add tests asserting zero account reads during `authenticate` and fail-closed missing-role behavior.
- [ ] Run the tests and capture RED because authentication currently reads `accounts.findById`.
- [ ] Persist `role` at creation and resolve the principal from the session snapshot.
- [ ] Run focused tests and commit the snapshot change.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSession.java`
- Lines: 19-29
- Action: replace

Current:
```java
  @Id private String id;
  @Indexed private String accountId;
  private String tokenHash;
  private String previousTokenHash;
  private Instant previousTokenExpiresOn;
  private String accountSecurityFingerprint;
  private Instant createdOn;
  private Instant lastSeenOn;
  private Instant rotatedOn;
  private Instant idleExpiresOn;
  @Indexed(expireAfter = "0s") private Instant absoluteExpiresOn;
```

Proposed:
```java
  @Id private String id;
  @Indexed private String accountId;
  private dev.christopherbell.account.model.Role role;
  private String tokenHash;
  private String previousTokenHash;
  private Instant previousTokenExpiresOn;
  private String accountSecurityFingerprint;
  private Instant createdOn;
  private Instant lastSeenOn;
  private Instant rotatedOn;
  private Instant idleExpiresOn;
  @Indexed(expireAfter = "0s") private Instant absoluteExpiresOn;
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 53-63
- Action: replace

Current:
```java
    sessions.save(BrowserSession.builder()
        .id(credential.sessionId())
        .accountId(account.getId())
        .tokenHash(hash(credential.secret()))
        .accountSecurityFingerprint(AccountSecurityFingerprint.from(account))
        .createdOn(now)
        .lastSeenOn(now)
        .rotatedOn(now)
        .idleExpiresOn(now.plus(IDLE_LIFETIME))
        .absoluteExpiresOn(now.plus(ABSOLUTE_LIFETIME))
        .build());
```

Proposed:
```java
    sessions.save(BrowserSession.builder()
        .id(credential.sessionId())
        .accountId(account.getId())
        .role(account.getRole())
        .tokenHash(hash(credential.secret()))
        .accountSecurityFingerprint(AccountSecurityFingerprint.from(account))
        .createdOn(now)
        .lastSeenOn(now)
        .rotatedOn(now)
        .idleExpiresOn(now.plus(IDLE_LIFETIME))
        .absoluteExpiresOn(now.plus(ABSOLUTE_LIFETIME))
        .build());
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest`

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 81-87
- Action: replace

Current:
```java
    var account = accounts.findById(session.getAccountId()).orElse(null);
    if (account == null || !isActive(account)
        || !constantTimeEquals(
            session.getAccountSecurityFingerprint(), AccountSecurityFingerprint.from(account))) {
      sessions.delete(session);
      return Optional.empty();
    }
```

Proposed:
```java
    if (session.getAccountId() == null || session.getAccountId().isBlank()
        || session.getRole() == null
        || session.getAccountSecurityFingerprint() == null
        || session.getAccountSecurityFingerprint().isBlank()) {
      sessions.delete(session);
      return Optional.empty();
    }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest`

#### Code Edit 2.4
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 104-105
- Action: replace

Current:
```java
    return Optional.of(new AuthenticatedBrowserSession(
        account.getId(), account.getRole(), rotatedToken));
```

Proposed:
```java
    return Optional.of(new AuthenticatedBrowserSession(
        session.getAccountId(), session.getRole(), rotatedToken));
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest`

#### Code Edit 2.5
- File: `website/src/test/java/dev/christopherbell/configuration/security/browser/BrowserSessionServiceTest.java`
- Lines: 80-87
- Action: replace

Current:
```java
  @Test
  void passwordRolePermissionOrStatusChangeInvalidatesTheSession() {
    var fixture = new Fixture(START);
    String token = fixture.create();
    fixture.account.setPermissions(Set.of(AccountPermission.MUSIC_READ));

    assertFalse(fixture.authenticate(token, true).isPresent());
  }
```

Proposed:
```java
  @Test
  void authenticationUsesTheStoredRoleWithoutLoadingTheAccount() {
    var fixture = new Fixture(START);
    String token = fixture.create();
    org.mockito.Mockito.clearInvocations(fixture.accounts);

    var authenticated = fixture.authenticate(token, false).orElseThrow();

    org.assertj.core.api.Assertions.assertThat(authenticated.role()).isEqualTo(Role.USER);
    org.mockito.Mockito.verifyNoInteractions(fixture.accounts);
  }

  @Test
  void legacySessionWithoutRoleIsDeletedAndRejected() {
    var fixture = new Fixture(START);
    String token = fixture.create();
    fixture.session().setRole(null);

    assertFalse(fixture.authenticate(token, false).isPresent());

    org.mockito.Mockito.verify(fixture.sessions).delete(fixture.session());
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest`

### Task 3 - Coalesce activity writes and rotate with compare-and-set

Sequence / dependencies:
- Runs after Task 2 because the activity store operates on the new authoritative session snapshot.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: interactive use within five minutes performs no write; a due touch performs one conditional field update; due rotation performs one conditional atomic rotation.
  - Invariants: absolute expiry never moves, idle expiry never exceeds it, previous-token overlap remains two minutes, and a failed conditional write cannot resurrect a revoked session.
  - Boundary/API: new package-private persistence boundary; public session service API is unchanged.
  - Effects and failures: Mongo update failure fails authentication safely; no full document is saved during authentication.
  - Tests and evidence: deterministic fixed-clock tests for coalescing, CAS loss, rotation overlap, and revocation/rotation ordering; no sleeps.

- [ ] Add RED tests for no write inside the window, one write after it, and no `save` during authentication.
- [ ] Implement the conditional Mongo update store.
- [ ] Replace in-memory mutation/full saves with explicit store calls.
- [ ] Run focused concurrency tests and commit.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionActivityStore.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.security.browser;

import java.time.Instant;
import java.util.Optional;

/** Atomic persistence operations for activity and credential rotation. */
public interface BrowserSessionActivityStore {
  Optional<BrowserSession> touch(
      String sessionId, Instant observedLastSeenOn, Instant now, Instant idleExpiresOn);

  Optional<BrowserSession> rotate(
      String sessionId,
      String observedTokenHash,
      Instant observedRotatedOn,
      String nextTokenHash,
      Instant now,
      Instant previousTokenExpiresOn,
      Instant idleExpiresOn);
}
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/MongoBrowserSessionActivityStore.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.security.browser;

import java.time.Instant;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.springframework.data.mongodb.core.FindAndModifyOptions;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;

@Repository
@RequiredArgsConstructor
public final class MongoBrowserSessionActivityStore implements BrowserSessionActivityStore {
  private final MongoTemplate mongo;

  @Override
  public Optional<BrowserSession> touch(
      String sessionId, Instant observedLastSeenOn, Instant now, Instant idleExpiresOn) {
    var query = touchQuery(sessionId, observedLastSeenOn, now);
    var update = new Update().set("lastSeenOn", now).set("idleExpiresOn", idleExpiresOn);
    var touched = mongo.findAndModify(
        query, update, FindAndModifyOptions.options().returnNew(true), BrowserSession.class);
    return touched != null ? Optional.of(touched) : reloadLive(sessionId, now);
  }

  @Override
  public Optional<BrowserSession> rotate(
      String sessionId,
      String observedTokenHash,
      Instant observedRotatedOn,
      String nextTokenHash,
      Instant now,
      Instant previousTokenExpiresOn,
      Instant idleExpiresOn) {
    var query = rotationQuery(sessionId, observedTokenHash, observedRotatedOn, now);
    var update = new Update()
        .set("previousTokenHash", observedTokenHash)
        .set("previousTokenExpiresOn", previousTokenExpiresOn)
        .set("tokenHash", nextTokenHash)
        .set("rotatedOn", now)
        .set("lastSeenOn", now)
        .set("idleExpiresOn", idleExpiresOn);
    var rotated = mongo.findAndModify(
        query, update, FindAndModifyOptions.options().returnNew(true), BrowserSession.class);
    return rotated != null ? Optional.of(rotated) : reloadLive(sessionId, now);
  }

  private Optional<BrowserSession> reloadLive(String sessionId, Instant now) {
    var live = new Query(new Criteria().andOperator(
        Criteria.where("_id").is(sessionId),
        Criteria.where("absoluteExpiresOn").gt(now)));
    return Optional.ofNullable(mongo.findOne(live, BrowserSession.class));
  }

  static Query touchQuery(String sessionId, Instant observedLastSeenOn, Instant now) {
    return new Query(new Criteria().andOperator(
        Criteria.where("_id").is(sessionId),
        Criteria.where("lastSeenOn").is(observedLastSeenOn),
        Criteria.where("absoluteExpiresOn").gt(now)));
  }

  static Query rotationQuery(
      String sessionId, String observedTokenHash, Instant observedRotatedOn, Instant now) {
    return new Query(new Criteria().andOperator(
        Criteria.where("_id").is(sessionId),
        Criteria.where("tokenHash").is(observedTokenHash),
        Criteria.where("rotatedOn").is(observedRotatedOn),
        Criteria.where("absoluteExpiresOn").gt(now)));
  }
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.MongoBrowserSessionActivityStoreTest`

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 22-31
- Action: replace

Current:
```java
  static final Duration IDLE_LIFETIME = Duration.ofDays(7);
  static final Duration ABSOLUTE_LIFETIME = Duration.ofDays(30);
  static final Duration ROTATION_INTERVAL = Duration.ofDays(1);
  static final Duration ROTATION_OVERLAP = Duration.ofMinutes(2);
  private static final int TOKEN_BYTES = 32;

  private final BrowserSessionRepository sessions;
  private final AccountRepository accounts;
  private final Clock clock;
  private final SecureRandom random = new SecureRandom();
```

Proposed:
```java
  static final Duration IDLE_LIFETIME = Duration.ofDays(7);
  static final Duration ABSOLUTE_LIFETIME = Duration.ofDays(30);
  static final Duration ROTATION_INTERVAL = Duration.ofDays(1);
  static final Duration ROTATION_OVERLAP = Duration.ofMinutes(2);
  static final Duration ACTIVITY_WRITE_INTERVAL = Duration.ofMinutes(5);
  private static final int TOKEN_BYTES = 32;

  private final BrowserSessionRepository sessions;
  private final BrowserSessionActivityStore activity;
  private final AccountRepository accounts;
  private final Clock clock;
  private final SecureRandom random = new SecureRandom();
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 3.3a
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 33-40
- Action: replace

Current:
```java
  public BrowserSessionService(
      BrowserSessionRepository sessions,
      AccountRepository accounts,
      Clock clock) {
    this.sessions = sessions;
    this.accounts = accounts;
    this.clock = clock;
  }
```

Proposed:
```java
  public BrowserSessionService(
      BrowserSessionRepository sessions,
      BrowserSessionActivityStore activity,
      AccountRepository accounts,
      Clock clock) {
    this.sessions = sessions;
    this.activity = activity;
    this.accounts = accounts;
    this.clock = clock;
  }
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 3.4
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 89-103
- Action: replace

Current:
```java
    Optional<String> rotatedToken = Optional.empty();
    if (interactive) {
      session.setLastSeenOn(now);
      session.setIdleExpiresOn(earlier(now.plus(IDLE_LIFETIME), session.getAbsoluteExpiresOn()));
      if (!now.isBefore(session.getRotatedOn().plus(ROTATION_INTERVAL))) {
        var rotated = credential(session.getId());
        session.setPreviousTokenHash(session.getTokenHash());
        session.setPreviousTokenExpiresOn(earlier(
            now.plus(ROTATION_OVERLAP), session.getAbsoluteExpiresOn()));
        session.setTokenHash(hash(rotated.secret()));
        session.setRotatedOn(now);
        rotatedToken = Optional.of(rotated.raw());
      }
      sessions.save(session);
    }
```

Proposed:
```java
    Optional<String> rotatedToken = Optional.empty();
    if (interactive) {
      var idleExpiresOn = earlier(now.plus(IDLE_LIFETIME), session.getAbsoluteExpiresOn());
      if (!now.isBefore(session.getRotatedOn().plus(ROTATION_INTERVAL))
          && constantTimeEquals(session.getTokenHash(), hash(parsed.get().secret()))) {
        var rotated = credential(session.getId());
        var updated = activity.rotate(
            session.getId(), session.getTokenHash(), session.getRotatedOn(),
            hash(rotated.secret()), now,
            earlier(now.plus(ROTATION_OVERLAP), session.getAbsoluteExpiresOn()),
            idleExpiresOn);
        if (updated.isEmpty()) return Optional.empty();
        session = updated.orElseThrow();
        if (constantTimeEquals(session.getTokenHash(), hash(rotated.secret()))) {
          rotatedToken = Optional.of(rotated.raw());
        } else if (!validCredential(session, parsed.get().secret(), now)) {
          return Optional.empty();
        }
      } else if (!now.isBefore(session.getLastSeenOn().plus(ACTIVITY_WRITE_INTERVAL))) {
        var updated = activity.touch(
            session.getId(), session.getLastSeenOn(), now, idleExpiresOn);
        if (updated.isEmpty()
            || !validCredential(updated.orElseThrow(), parsed.get().secret(), now)) {
          return Optional.empty();
        }
        session = updated.orElseThrow();
      }
    }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest --tests dev.christopherbell.configuration.security.browser.MongoBrowserSessionActivityStoreTest`

#### Code Edit 3.5
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 243-248
- Action: replace

Current:
```java
  @Bean
  public BrowserSessionService browserSessionService(
      BrowserSessionRepository browserSessions,
      AccountRepository accounts) {
    return new BrowserSessionService(browserSessions, accounts, Clock.systemUTC());
  }
```

Proposed:
```java
  @Bean
  public BrowserSessionService browserSessionService(
      BrowserSessionRepository browserSessions,
      dev.christopherbell.configuration.security.browser.BrowserSessionActivityStore activity,
      AccountRepository accounts) {
    return new BrowserSessionService(browserSessions, activity, accounts, Clock.systemUTC());
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.SecurityConfigTest`

#### Code Edit 3.6
- File: `website/src/test/java/dev/christopherbell/configuration/security/browser/BrowserSessionServiceTest.java`
- Lines: 100-146
- Action: replace

Current:
```java
  private static final class Fixture {
    private final BrowserSessionRepository sessions = mock(BrowserSessionRepository.class);
    private final AccountRepository accounts = mock(AccountRepository.class);
    private final ArgumentCaptor<BrowserSession> saved = ArgumentCaptor.forClass(BrowserSession.class);
```

Proposed:
```java
  private static final class Fixture {
    private final BrowserSessionRepository sessions = mock(BrowserSessionRepository.class);
    private final BrowserSessionActivityStore activity = mock(BrowserSessionActivityStore.class);
    private final AccountRepository accounts = mock(AccountRepository.class);
    private final ArgumentCaptor<BrowserSession> saved = ArgumentCaptor.forClass(BrowserSession.class);
```

Add to the existing fixture constructor after the repository stubs:
```java
      when(activity.touch(anyString(), any(), any(), any())).thenAnswer(invocation -> {
        var current = session();
        current.setLastSeenOn(invocation.getArgument(2));
        current.setIdleExpiresOn(invocation.getArgument(3));
        return Optional.of(current);
      });
      when(activity.rotate(anyString(), anyString(), any(), anyString(), any(), any(), any()))
          .thenAnswer(invocation -> {
            var current = session();
            current.setPreviousTokenHash(invocation.getArgument(1));
            current.setPreviousTokenExpiresOn(invocation.getArgument(5));
            current.setTokenHash(invocation.getArgument(3));
            current.setRotatedOn(invocation.getArgument(4));
            current.setLastSeenOn(invocation.getArgument(4));
            current.setIdleExpiresOn(invocation.getArgument(6));
            return Optional.of(current);
          });
```

Current:
```java
    private BrowserSessionService service() {
      return new BrowserSessionService(
          sessions, accounts, Clock.fixed(now, ZoneOffset.UTC));
    }
```

Proposed:
```java
    private BrowserSessionService service() {
      return new BrowserSessionService(
          sessions, activity, accounts, Clock.fixed(now, ZoneOffset.UTC));
    }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest`

#### Code Edit 3.7
- File: `website/src/test/java/dev/christopherbell/configuration/security/browser/MongoBrowserSessionActivityStoreTest.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.security.browser;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Instant;
import org.junit.jupiter.api.Test;
import org.springframework.data.mongodb.core.query.Query;

class MongoBrowserSessionActivityStoreTest {
  @Test
  void touchCasQueryRequiresTheObservedTimestampAndLiveAbsoluteExpiry() {
    Instant observed = Instant.parse("2026-07-29T12:00:00Z");
    Instant now = observed.plusSeconds(300);

    Query query = MongoBrowserSessionActivityStore.touchQuery("session-1", observed, now);

    assertThat(query.getQueryObject().toJson())
        .contains("session-1", "lastSeenOn", "absoluteExpiresOn");
  }

  @Test
  void rotationCasQueryRequiresTheObservedCredentialAndRotationTime() {
    Instant observed = Instant.parse("2026-07-29T12:00:00Z");

    Query query = MongoBrowserSessionActivityStore.rotationQuery(
        "session-1", "token-hash", observed, observed.plusSeconds(86_400));

    assertThat(query.getQueryObject().toJson())
        .contains("session-1", "tokenHash", "rotatedOn", "absoluteExpiresOn");
  }
}
```

Implementation note:
- Service tests own race behavior; these tests lock the package-private persistence predicates without requiring a live Mongo process.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.MongoBrowserSessionActivityStoreTest`

### Task 4 - Revoke sessions at account-security mutation boundaries

Sequence / dependencies:
- Runs after Task 2 so the session snapshot is safe only when this invalidation coverage is complete.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits; invoke `superpowers:test-driven-development`.
- Before-Edit Brief:
  - Behavior: every successful mutation of password hash, role, status, or permissions deletes all browser sessions for that account; account deletion deletes them as private data.
  - Invariants: failed writes do not revoke; non-security profile/follow changes do not revoke; bearer-token fingerprint validation remains unchanged.
  - Boundary/API: account features depend on a narrow `AccountSessionRevoker`; browser security supplies the implementation.
  - Effects and failures: revocation is a Mongo delete after the authoritative account write. A revocation failure is not swallowed; callers surface the existing service-unavailable/error boundary rather than claiming success with stale sessions.
  - Tests and evidence: unit tests verify revocation on password reset, moderation, permissions, report suspension, login rehash, and deletion; verify no revocation for profile-only moderation updates.

- [ ] Add failing revocation interaction tests in each owning feature test.
- [ ] Add the account-domain revocation port and implement it in the browser-session service.
- [ ] Wire each security mutation after its successful write.
- [ ] Add account deletion cleanup for `browser_sessions`.
- [ ] Run account/report/browser-session suites and commit.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/account/auth/AccountSessionRevoker.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.account.auth;

/** Revokes browser credentials after a durable account-security state change. */
@FunctionalInterface
public interface AccountSessionRevoker {
  void revokeAll(String accountId);
}
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 20-21
- Action: replace

Current:
```java
/** Creates, resolves, rotates, and revokes opaque browser sessions. */
public class BrowserSessionService {
```

Proposed:
```java
/** Creates, resolves, rotates, and revokes opaque browser sessions. */
public class BrowserSessionService
    implements dev.christopherbell.account.auth.AccountSessionRevoker {
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 4.2a
- File: `website/src/main/java/dev/christopherbell/configuration/security/browser/BrowserSessionService.java`
- Lines: 114-116
- Action: replace

Current:
```java
  public void revokeAll(String accountId) {
    if (accountId != null && !accountId.isBlank()) sessions.deleteByAccountId(accountId);
  }
```

Proposed:
```java
  @Override
  public void revokeAll(String accountId) {
    if (accountId != null && !accountId.isBlank()) sessions.deleteByAccountId(accountId);
  }
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/account/moderation/AccountModerationService.java`
- Lines: 30-34
- Action: replace

Current:
```java
  private final AccountRepository accountRepository;
  private final AccountMapper accountMapper;
  private final AdminActivityService adminActivityService;
  private final PermissionService permissionService;
```

Proposed:
```java
  private final AccountRepository accountRepository;
  private final AccountMapper accountMapper;
  private final AdminActivityService adminActivityService;
  private final PermissionService permissionService;
  private final dev.christopherbell.account.auth.AccountSessionRevoker sessionRevoker;
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.moderation.AccountModerationAuditTest`

#### Code Edit 4.4
- File: `website/src/main/java/dev/christopherbell/account/moderation/AccountModerationService.java`
- Lines: 62-68
- Action: replace

Current:
```java
    applyUpdates(existing, request);
    existing.setPendingModerationAudit(auditCommand);
    var saved = accountRepository.save(existing);
    if (moderated) {
      saved = completePendingAudit(saved);
    }
    return accountMapper.toAccount(saved);
```

Proposed:
```java
    applyUpdates(existing, request);
    existing.setPendingModerationAudit(auditCommand);
    var saved = accountRepository.save(existing);
    if (moderated) {
      sessionRevoker.revokeAll(saved.getId());
      saved = completePendingAudit(saved);
    }
    return accountMapper.toAccount(saved);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.moderation.AccountModerationAuditTest`

#### Code Edit 4.5
- File: `website/src/main/java/dev/christopherbell/account/passwordreset/PasswordResetService.java`
- Lines: 34-35
- Action: replace

Current:
```java
  private final AccountRepository accountRepository;
  private final PasswordResetNotificationService passwordResetNotificationService;
```

Proposed:
```java
  private final AccountRepository accountRepository;
  private final PasswordResetNotificationService passwordResetNotificationService;
  private final dev.christopherbell.account.auth.AccountSessionRevoker sessionRevoker;
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.PasswordResetNotificationServiceTest --tests dev.christopherbell.account.AccountServiceTest`

#### Code Edit 4.6
- File: `website/src/main/java/dev/christopherbell/account/passwordreset/PasswordResetService.java`
- Lines: 90-97
- Action: replace

Current:
```java
    try {
      account.setPasswordSalt(null);
      account.setPasswordHash(PasswordUtil.hashPassword(request.password()));
      clearPasswordResetToken(account);
      account.setLastUpdatedOn(Instant.now());
      accountRepository.save(account);
      log.info("Password reset completed for account id: {}", account.getId());
```

Proposed:
```java
    try {
      account.setPasswordSalt(null);
      account.setPasswordHash(PasswordUtil.hashPassword(request.password()));
      clearPasswordResetToken(account);
      account.setLastUpdatedOn(Instant.now());
      accountRepository.save(account);
      sessionRevoker.revokeAll(account.getId());
      log.info("Password reset completed for account id: {}", account.getId());
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.AccountServiceTest`

#### Code Edit 4.6a
- File: `website/src/main/java/dev/christopherbell/account/AccountService.java`
- Lines: 65-75
- Action: replace

Current:
```java
  private final AccountMapper accountMapper;
  private final AccountRepository accountRepository;
  private final AccountDeletionService accountDeletionService;
  private final AccountAuthenticationService accountAuthenticationService;
  private final PasswordResetService passwordResetService;
  private final AccountProfileService accountProfileService;
  private final AccountFollowService accountFollowService;
  private final AccountModerationService accountModerationService;
  private final SharedFolderAuditRecorder sharedFolderAudit;
  private final SharedFolderAccessService sharedFolderAccess;
  private final FederationConsentService federationConsent;
```

Proposed:
```java
  private final AccountMapper accountMapper;
  private final AccountRepository accountRepository;
  private final AccountDeletionService accountDeletionService;
  private final AccountAuthenticationService accountAuthenticationService;
  private final PasswordResetService passwordResetService;
  private final AccountProfileService accountProfileService;
  private final AccountFollowService accountFollowService;
  private final AccountModerationService accountModerationService;
  private final SharedFolderAuditRecorder sharedFolderAudit;
  private final SharedFolderAccessService sharedFolderAccess;
  private final FederationConsentService federationConsent;
  private final dev.christopherbell.account.auth.AccountSessionRevoker sessionRevoker;
```

Verification:
- `./gradlew :website:compileJava`

#### Code Edit 4.6b
- File: `website/src/main/java/dev/christopherbell/account/AccountService.java`
- Lines: 398-448
- Action: replace

Current:
```java
      account.setPermissions(next);
      AccountDetail saved = accountMapper.toAccount(accountRepository.save(account));
      sharedFolderAudit.recordCurrent(
          "PERMISSION_CHANGE", auditResource, null, "accepted", null);
      return saved;
```

Proposed:
```java
      boolean permissionsChanged = !next.equals(
          account.getPermissions() == null ? java.util.Set.of() : account.getPermissions());
      account.setPermissions(next);
      AccountDetail saved = accountMapper.toAccount(accountRepository.save(account));
      if (permissionsChanged) sessionRevoker.revokeAll(account.getId());
      sharedFolderAudit.recordCurrent(
          "PERMISSION_CHANGE", auditResource, null, "accepted", null);
      return saved;
```

Current:
```java
      account.setPermissions(next);
      AccountDetail saved = accountMapper.toAccount(accountRepository.save(account));
      sharedFolderAudit.recordCurrent(
          "MUSIC_PERMISSION_CHANGE", auditResource, null, "accepted", null);
      return saved;
```

Proposed:
```java
      boolean permissionsChanged = !next.equals(
          account.getPermissions() == null ? java.util.Set.of() : account.getPermissions());
      account.setPermissions(next);
      AccountDetail saved = accountMapper.toAccount(accountRepository.save(account));
      if (permissionsChanged) sessionRevoker.revokeAll(account.getId());
      sharedFolderAudit.recordCurrent(
          "MUSIC_PERMISSION_CHANGE", auditResource, null, "accepted", null);
      return saved;
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.AccountServiceTest`

#### Code Edit 4.6c
- File: `website/src/main/java/dev/christopherbell/account/auth/AccountAuthenticationService.java`
- Lines: 26-58
- Action: replace

Current:
```java
  private final AccountRepository accountRepository;
  private final AccountLoginStore accountLoginStore;
```

Proposed:
```java
  private final AccountRepository accountRepository;
  private final AccountLoginStore accountLoginStore;
  private final AccountSessionRevoker sessionRevoker;
```

Current:
```java
      var currentHash = PasswordUtil.needsRehash(
          account.getPasswordSalt(), account.getPasswordHash())
              ? PasswordUtil.upgradePassword(
                  password, account.getPasswordSalt(), account.getPasswordHash())
              : account.getPasswordHash();
      var current = accountLoginStore.completeLogin(account, currentHash, Instant.now())
          .filter(updated -> updated.getStatus() == AccountStatus.ACTIVE)
          .orElseThrow(this::rejectedLogin);
      log.info("Successful login for account with id: {}", current.getId());
      return PermissionService.generateToken(current);
```

Proposed:
```java
      boolean rehashRequired = PasswordUtil.needsRehash(
          account.getPasswordSalt(), account.getPasswordHash());
      var currentHash = rehashRequired
          ? PasswordUtil.upgradePassword(
              password, account.getPasswordSalt(), account.getPasswordHash())
          : account.getPasswordHash();
      var current = accountLoginStore.completeLogin(account, currentHash, Instant.now())
          .filter(updated -> updated.getStatus() == AccountStatus.ACTIVE)
          .orElseThrow(this::rejectedLogin);
      if (rehashRequired) sessionRevoker.revokeAll(current.getId());
      log.info("Successful login for account with id: {}", current.getId());
      return PermissionService.generateToken(current);
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.AccountServiceTest`

#### Code Edit 4.6d
- File: `website/src/main/java/dev/christopherbell/report/moderation/ReportModerationService.java`
- Lines: 34-212
- Action: replace

Current:
```java
  private final PostRepository postRepository;
  private final AccountRepository accountRepository;
  private final AdminActivityService adminActivityService;
  private final PermissionService permissionService;
  private final ReportRepository reportRepository;
```

Proposed:
```java
  private final PostRepository postRepository;
  private final AccountRepository accountRepository;
  private final AdminActivityService adminActivityService;
  private final PermissionService permissionService;
  private final ReportRepository reportRepository;
  private final dev.christopherbell.account.auth.AccountSessionRevoker sessionRevoker;
```

Current:
```java
    var suspendedAccount = accountRepository.findById(report.getReportedAccountId());
    String suspendedUsername = suspendedAccount
        .map(Account::getUsername)
        .orElse(report.getReportedUsername());
    suspendedAccount.ifPresent(account -> {
      account.setStatus(AccountStatus.SUSPENDED);
      accountRepository.save(account);
    });
```

Proposed:
```java
    var suspendedAccount = accountRepository.findById(report.getReportedAccountId());
    String suspendedUsername = suspendedAccount
        .map(Account::getUsername)
        .orElse(report.getReportedUsername());
    suspendedAccount.ifPresent(account -> {
      account.setStatus(AccountStatus.SUSPENDED);
      accountRepository.save(account);
      sessionRevoker.revokeAll(account.getId());
    });
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.report.ReportServiceTest --tests dev.christopherbell.report.moderation.ReportModerationLifecycleTest`

#### Code Edit 4.6e
- File: `website/src/test/java/dev/christopherbell/account/AccountServiceTest.java`
- Lines: 79-980
- Action: replace

Current:
```java
  @Mock private FederationConsentService federationConsent;
  private AccountService accountService;
```

Proposed:
```java
  @Mock private FederationConsentService federationConsent;
  @Mock private dev.christopherbell.account.auth.AccountSessionRevoker sessionRevoker;
  private AccountService accountService;
```

Implementation:
- Pass `sessionRevoker` into `AccountAuthenticationService`, `PasswordResetService`, `AccountModerationService`, and the final `AccountService` constructor argument in `setUp`.
- In the existing shared-folder and Music permission tests, verify `sessionRevoker.revokeAll(account.getId())` once when the permission set changes and never when the submitted set is unchanged.
- In the existing login rehash test, verify revocation; in the current-hash login test, verify no revocation.
- In the password-reset and moderation tests, verify revocation occurs after the repository save returns. Use Mockito `InOrder`; do not use sleeps.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.AccountServiceTest --tests dev.christopherbell.account.moderation.AccountModerationAuditTest`

#### Code Edit 4.6f
- File: `website/src/test/java/dev/christopherbell/report/ReportServiceTest.java`
- Lines: 145-195
- Action: replace

Current:
```java
    ReportRepository reportRepository = Mockito.mock(ReportRepository.class);
```

Proposed:
```java
    ReportRepository reportRepository = Mockito.mock(ReportRepository.class);
    var sessionRevoker = Mockito.mock(
        dev.christopherbell.account.auth.AccountSessionRevoker.class);
```

Implementation:
- Pass `sessionRevoker` as the final `ReportModerationService` constructor argument.
- After resolving `DELETE_POST_AND_SUSPEND_USER`, verify `sessionRevoker.revokeAll("u1")`.
- Update `ReportModerationLifecycleTest` setup with the same mock and verify non-suspension resolutions never revoke.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.report.ReportServiceTest --tests dev.christopherbell.report.moderation.ReportModerationLifecycleTest`

#### Code Edit 4.7
- File: `website/src/main/java/dev/christopherbell/account/deletion/MongoAccountDeletionOperations.java`
- Lines: 60-79
- Action: replace

Current:
```java
  public void removePrivateData(String accountId) {
    remove("messages", accountId,
        "participantIds", "senderAccountId", "recipientAccountId");
    remove("notifications", accountId, "accountId", "actorAccountId");
    remove("notification_preferences", accountId, "accountId");
    remove("notification_delivery_guards", accountId,
        "accountId", "actorAccountId", "recipientAccountId");
    remove("notification_rate_limits", accountId, "accountId", "actorAccountId");
    remove("account_trust_relationships", accountId,
        "ownerAccountId", "targetAccountId");
    remove("hidden_post_threads", accountId, "accountId");
    remove("whatsforlunch_preferences", accountId, "accountId");
    remove("whatsforlunch_favorites", accountId, "accountId");
    remove("whatsforlunch_ratings", accountId, "accountId");
    remove("whatsforlunch_sessions", accountId,
        "createdByAccountId", "participantAccountIds");
    remove("conversation_archive_states", accountId,
        "ownerAccountId", "participantIds");
  }
```

Proposed:
```java
  public void removePrivateData(String accountId) {
    remove("browser_sessions", accountId, "accountId");
    remove("messages", accountId,
        "participantIds", "senderAccountId", "recipientAccountId");
    remove("notifications", accountId, "accountId", "actorAccountId");
    remove("notification_preferences", accountId, "accountId");
    remove("notification_delivery_guards", accountId,
        "accountId", "actorAccountId", "recipientAccountId");
    remove("notification_rate_limits", accountId, "accountId", "actorAccountId");
    remove("account_trust_relationships", accountId,
        "ownerAccountId", "targetAccountId");
    remove("hidden_post_threads", accountId, "accountId");
    remove("whatsforlunch_preferences", accountId, "accountId");
    remove("whatsforlunch_favorites", accountId, "accountId");
    remove("whatsforlunch_ratings", accountId, "accountId");
    remove("whatsforlunch_sessions", accountId,
        "createdByAccountId", "participantAccountIds");
    remove("conversation_archive_states", accountId,
        "ownerAccountId", "participantIds");
  }
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.account.deletion.MongoAccountDeletionOperationsTest`

#### Code Edit 4.8
- File: `website/src/main/java/dev/christopherbell/account/README.md`
- Lines: after 20
- Action: add

Proposed:
```markdown
- Opaque browser sessions carry a fail-closed account-role snapshot so normal cookie
  authentication uses one session read. Security-state mutations revoke every session;
  interactive activity writes are conditional and coalesced to five-minute intervals.
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.security.browser.BrowserSessionServiceTest`

### Task 5 - Prove query counts and runtime behavior

Sequence / dependencies:
- Runs after Tasks 1-4 and is the merge gate for this plan.

Implementation notes:
- Required skill: `write-chris-street-style-code` before edits to executable test tooling.
- Before-Edit Brief:
  - Behavior: the evidence harness reports zero auth Mongo commands for static assets and one session read for normal cookie authentication.
  - Invariants: measurements use the same route/data setup before and after and never target port 8080.
  - Boundary/API: test-only command listener and alternate-port local HTTP flows.
  - Effects and failures: disposable test data only; stop the alternate-port process on every exit path.
  - Tests and evidence: focused tests, full website check, and alternate-port anonymous/authenticated smoke.

- [ ] Capture Mongo command counts with a temporary command listener attached only to the alternate-port verification process; do not commit diagnostic-only instrumentation.
- [ ] Run the full focused suite, then `:website:check`.
- [ ] Start with disposable data on a non-8080 port and exercise login, static assets, a protected API, logout, and stale-cookie behavior.
- [ ] Record before/after counts and latency percentiles in the required Builder test report during execution.
- [ ] Commit, publish a PR, wait for required CI, and perform production-safe verification only under the separate execution authorization.

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.JwtAuthenticationFilterTest --tests dev.christopherbell.configuration.security.browser.* --tests dev.christopherbell.account.* --tests dev.christopherbell.report.moderation.*`
- `./gradlew :website:check`

## Code Changes

- Add `StaticAssetRequestMatcher`; use it before token parsing in `JwtAuthenticationFilter`.
- Add `role` to `BrowserSession`; stop reading `AccountRepository` during normal session authentication.
- Add `BrowserSessionActivityStore` and Mongo compare-and-set implementation for touch/rotation.
- Add `AccountSessionRevoker`; wire role/status/password/permission/report/deletion mutation owners.
- Update account/security documentation and query-count evidence.

## Files and Modules

- Security filter/configuration and browser-session package.
- Account authentication, moderation, password reset, permission update, and deletion packages.
- Report moderation suspension path.
- Focused security/account tests and package documentation.

## Unit Testing

- RED/GREEN filter tests for cookie and bearer static requests.
- Session snapshot, legacy fail-closed, expiry, coalescing, rotation-overlap, CAS-loss, and revocation tests.
- Mutation-owner tests verifying `revokeAll` occurs only after successful security writes.
- Mongo activity-store query/update shape tests.

## Local Testing

- Use an isolated `GRADLE_USER_HOME` if Windows Gradle locks occur.
- Run `./gradlew :website:check` from the isolated website worktree.
- Start on a non-production port such as 8091 with disposable Mongo data; never replace the port-8080 listener during candidate validation.
- Verify `/login`, versioned `/js/app.js`, a protected account endpoint, logout, and stale-cookie cleanup.

## Validation

- Static asset requests with cookies and bearer headers perform zero session/account Mongo commands.
- A normal protected cookie request performs one `browser_sessions` read and zero `accounts` reads.
- Repeated interactive requests inside five minutes do not write session state.
- Rotation and revocation races are deterministic and fail closed.
- Full website checks and required CI are green.

## Rollback or Recovery

- Revert the batch commit to restore per-request account validation and full session saves; persisted `role` is additive and harmless to the old reader.
- If revocation coverage is incomplete, do not merge the account-read removal; retain Task 1 independently.
- If rotation CAS behavior fails under concurrency, keep the snapshot read optimization disabled until the atomic tests pass.
- Production rollback uses the existing release-junction process and does not reverse Mongo data; the added nullable field requires no data rollback.

## Risks

- Missing a security mutation could leave a session role active until expiry. Mitigation: explicit mutation inventory and tests in Task 4; this is a merge blocker.
- A lost rotation response can leave the browser on the overlap token. Mitigation: only the winning CAS emits a cookie and concurrent response-order tests cover the browser outcome.
- Static matching that is too broad could bypass protected content. Mitigation: exact namespaces, GET-only matching, and negative protected-media/API tests.
- Current mainline can move before execution. Mitigation: refresh and update literal ranges before the first edit.

## Completion Criteria

- All task checkboxes and RED/GREEN evidence are recorded.
- Acceptance criteria 1-3 from the approved spec pass.
- Focused tests and `:website:check` pass.
- Alternate-port runtime evidence is saved in a Builder test report.
- PR review, required CI, merge, production-safe verification, documentation, and Builder closeout are complete under explicit execution authorization.
