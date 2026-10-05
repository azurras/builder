# Account Security and Lifecycle Issues 1258-1264 Implementation Plan

## Document Status

complete

## Objective

Resolve #1258-#1264 by making bearer and browser credentials reflect current account security state, normalizing failed login behavior, introducing versioned password hashes with opportunistic migration, hardening API errors and proxy trust, removing the dormant approval flag in favor of status, and correcting account HTTP contracts.

## Goals

- Reject credentials immediately after password, deletion, status, role, or permission changes.
- Make every unauthenticated login rejection externally identical while retaining safe internal categories.
- Write a self-describing PBKDF2 hash and upgrade legacy salt/hash pairs on successful login.
- Return stable request errors without exposing parser details or emitting routine 4xx stack traces at ERROR.
- Resolve forwarding chains only through validated trusted proxy ranges configured in production.
- Make `AccountStatus` the single lifecycle authority and remove approval-only API/UI/schema state.
- Return 201 plus `Location` for account creation, 200 for synchronous update/delete, and accept bodyless DELETE calls without `Content-Type`.

## Inputs

- Project spec: `docs/specs/2026-07-29-complete-christopherbell-dev-issues-1258-1307.md`.
- GitHub issues #1258-#1264, all authored by `azurras` with zero comments.
- Refreshed spoke baseline `8405cd77d0f1743fe33d70cc80b47e37048090a0`.
- Baseline `:website:check`: BUILD SUCCESSFUL in 3m44s on 2026-07-29.
- Mandatory implementation standards: `chris-street-style` and test-first RED/GREEN evidence.

## Branch

Execute on `codex/all-open-issues-20260729` in `A:\Projects\christopherbell.dev-worktrees\all-open-issues-20260729`, based on `origin/main` at `8405cd77`.

## Non-Goals

- Replacing JWTs or opaque browser sessions with a new identity provider.
- Adding manual signup approval or blocking newly created accounts pending moderation.
- Changing password complexity rules, JWT lifetime, or browser-session rotation policy.
- Trusting arbitrary DNS names as proxies or enabling Spring's global forwarded-header rewriting.
- Refactoring account CRUD, moderation audit, or unrelated API response models.

## Assumptions

- JWT subjects are account IDs, as produced by `PermissionService.generateToken` and consumed by current authorization code.
- Existing browser sessions may be invalidated by deployment if their stored fingerprint includes removed approval state; forced reauthentication is safe for this security release.
- Existing accounts are active unless their authoritative `status` says otherwise; `isApproved` does not independently block login today.
- `IpAddressMatcher` from Spring Security is available and supports exact IPv4/IPv6 addresses and CIDR ranges.
- Mongo migration `008` is the next immutable ID after current `001`-`007`.

## Open Questions

None.

## Task Breakdown

### Task 1 - Revalidate bearer credentials against current account state (#1258)

Sequence / dependencies:
- Runs first because later password, lifecycle, and permission edits must all feed one revocation invariant.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: a bearer JWT and opaque browser session authenticate only while the referenced account exists, is active, and has the same password hash, role, status, and permissions as at issuance.
  - Invariants: stale/missing fingerprint claims fail closed; authorities come from the current account; public routes remain anonymous when invalid cookies are cleared.
  - Boundary/API: `JwtAuthenticationFilter` remains the Spring authentication boundary and `PermissionService` retains its public JWT API.
  - Effects and failures: bearer authentication adds one indexed account lookup per credentialed request; absence or mismatch is an authentication rejection, while repository faults also fail closed without leaking detail.
  - Tests and evidence: first add filter tests proving password/role/permission changes reject a previously issued token; witness RED, then pass focused JWT and browser-session tests.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/permission/PermissionService.java`
- Lines: 88-100
- Action: replace

Current:
```java
public static String generateToken(Account account) {
  var claims = new HashMap<String, Object>();
  claims.put(Account.PROPERTY_ROLE, account.getRole());

  return Jwts.builder()
      .claims(claims)
      .id(UUID.randomUUID().toString())
      .subject(account.getId())
      .issuedAt(new Date())
      .expiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
      .signWith(key)
      .compact();
}
```

Proposed:
```java
public static String generateToken(Account account) {
  var claims = new HashMap<String, Object>();
  claims.put(Account.PROPERTY_ROLE, account.getRole());
  claims.put(AccountSecurityFingerprint.CLAIM,
      AccountSecurityFingerprint.from(account));

  return Jwts.builder()
      .claims(claims)
      .id(UUID.randomUUID().toString())
      .subject(account.getId())
      .issuedAt(new Date())
      .expiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
      .signWith(key)
      .compact();
}
```

Verification:
- `./gradlew.bat :website:test --tests '*PermissionServiceTest' --tests '*JwtAuthenticationFilterTest' --tests '*BrowserSessionServiceTest'`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/account/auth/AccountSecurityFingerprint.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.account.auth;

import dev.christopherbell.account.model.Account;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Comparator;
import java.util.HexFormat;

/** Stable digest of account state whose mutation must revoke credentials. */
public final class AccountSecurityFingerprint {
  public static final String CLAIM = "account-security";

  private AccountSecurityFingerprint() {}

  public static String from(Account account) {
    var source = new StringBuilder()
        .append(account.getId()).append('\n')
        .append(account.getPasswordHash()).append('\n')
        .append(account.getRole()).append('\n')
        .append(account.getStatus()).append('\n');
    if (account.getPermissions() != null) {
      account.getPermissions().stream()
          .sorted(Comparator.comparing(Enum::name))
          .forEach(permission -> source.append(permission.name()).append('\n'));
    }
    try {
      return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256")
          .digest(source.toString().getBytes(StandardCharsets.UTF_8)));
    } catch (NoSuchAlgorithmException impossible) {
      throw new IllegalStateException("SHA-256 is unavailable.", impossible);
    }
  }

  public static boolean matches(String expected, Account account) {
    if (expected == null || account == null) return false;
    return MessageDigest.isEqual(
        expected.getBytes(StandardCharsets.US_ASCII),
        from(account).getBytes(StandardCharsets.US_ASCII));
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests '*AccountSecurityFingerprintTest'`

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/configuration/security/JwtAuthenticationFilter.java`
- Lines: 85-114
- Action: replace

Current:
```java
try {
  if (bearerToken != null && Objects.nonNull(PermissionService.validateToken(bearerToken))) {
    Authentication authenticationToken = getAuthentication(bearerToken);
    SecurityContextHolder.getContext().setAuthentication(authenticationToken);
    if (authenticationToken.isAuthenticated()) {
      chain.doFilter(request, response);
    } else {
      response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
    }
    return;
  }
  if (cookieToken != null && browserSessions != null) {
    var resolved = browserSessions.authenticate(
        cookieToken,
        interactiveRequests != null && interactiveRequests.matches(request));
    if (resolved.isPresent()) {
      var session = resolved.get();
      SecurityContextHolder.getContext().setAuthentication(getAuthentication(session));
      if (browserCookies != null) {
        session.rotatedToken().ifPresent(token -> addCookies(
            response, browserCookies.authenticated(token)));
      }
      chain.doFilter(request, response);
      return;
    }
  }
  rejectCredential(publicRequest, response, chain, request, cookieToken != null);
} catch (Exception e) {
  rejectCredential(publicRequest, response, chain, request, cookieToken != null);
}
```

Proposed:
```java
try {
  if (bearerToken != null) {
    var claims = PermissionService.validateToken(bearerToken);
    var account = accounts.findById(claims.getSubject())
        .filter(candidate -> candidate.getStatus() == AccountStatus.ACTIVE)
        .filter(candidate -> AccountSecurityFingerprint.matches(
            claims.get(AccountSecurityFingerprint.CLAIM, String.class), candidate))
        .orElse(null);
    if (account != null) {
      SecurityContextHolder.getContext().setAuthentication(
          getAuthentication(account, bearerToken));
      chain.doFilter(request, response);
      return;
    }
  }
  if (cookieToken != null && browserSessions != null) {
    var resolved = browserSessions.authenticate(
        cookieToken,
        interactiveRequests != null && interactiveRequests.matches(request));
    if (resolved.isPresent()) {
      var session = resolved.get();
      SecurityContextHolder.getContext().setAuthentication(getAuthentication(session));
      if (browserCookies != null) {
        session.rotatedToken().ifPresent(token -> addCookies(
            response, browserCookies.authenticated(token)));
      }
      chain.doFilter(request, response);
      return;
    }
  }
  rejectCredential(publicRequest, response, chain, request, cookieToken != null);
} catch (Exception failure) {
  rejectCredential(publicRequest, response, chain, request, cookieToken != null);
}
```

Verification:
- `./gradlew.bat :website:test --tests '*JwtAuthenticationFilterTest'`

### Task 2 - Normalize login rejection and migrate password hashes (#1259, #1260)

Sequence / dependencies:
- Runs after Task 1 so a successful rehash automatically revokes credentials issued from the legacy hash state.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: unknown email, wrong password, malformed stored hash, and inactive account return the same 401 envelope; successful legacy login rewrites one current self-describing hash.
  - Invariants: verification is constant-time at the byte boundary; unknown accounts perform one current-work-factor derivation; malformed hashes reject without a 500; only successful authentication mutates the account.
  - Boundary/API: preserve legacy `generateSalt`, `hashPassword(password, salt)`, and `verifyPassword(password, salt, hash)` for compatible callers while adding current-format encode/rehash helpers.
  - Effects and failures: PBKDF2 is CPU work; account save occurs once for login timestamp plus optional rehash; crypto-provider failure retains its cause internally and maps to the public generic login rejection.
  - Tests and evidence: add parameterized RED tests comparing exception type/message for unknown, wrong, inactive, and malformed accounts plus password utility legacy/current/malformed/rehash cases.

#### Code Edit 2.1
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/security/PasswordUtil.java`
- Lines: 16-49
- Action: replace

Current:
```java
private static final int SALT_LENGTH = 16;
private static final int HASH_ITERATIONS = 65536;
private static final int HASH_KEY_LENGTH = 256;

public static String generateSalt() {
  SecureRandom secureRandom = new SecureRandom();
  byte[] salt = new byte[SALT_LENGTH];
  secureRandom.nextBytes(salt);
  return Base64.getEncoder().encodeToString(salt);
}

public static String hashPassword(String password, String salt)
    throws NoSuchAlgorithmException, InvalidKeySpecException {
  PBEKeySpec spec = new PBEKeySpec(
      password.toCharArray(), Base64.getDecoder().decode(salt), HASH_ITERATIONS, HASH_KEY_LENGTH);
  SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
  byte[] hash = factory.generateSecret(spec).getEncoded();
  return Base64.getEncoder().encodeToString(hash);
}

public static boolean verifyPassword(String password, String salt, String storedHash)
    throws NoSuchAlgorithmException, InvalidKeySpecException {
  String computedHash = hashPassword(password, salt);
  return computedHash.equals(storedHash);
}
```

Proposed:
```java
private static final String ALGORITHM = "PBKDF2WithHmacSHA256";
private static final String FORMAT = "pbkdf2-sha256";
private static final int SALT_LENGTH = 16;
private static final int LEGACY_ITERATIONS = 65_536;
private static final int CURRENT_ITERATIONS = 210_000;
private static final int HASH_KEY_LENGTH = 256;

public static String generateSalt() {
  var salt = new byte[SALT_LENGTH];
  new SecureRandom().nextBytes(salt);
  return Base64.getEncoder().encodeToString(salt);
}

public static String hashPassword(String password)
    throws NoSuchAlgorithmException, InvalidKeySpecException {
  var salt = generateSalt();
  return String.join("$", FORMAT, Integer.toString(CURRENT_ITERATIONS), salt,
      derive(password, salt, CURRENT_ITERATIONS));
}

public static String hashPassword(String password, String salt)
    throws NoSuchAlgorithmException, InvalidKeySpecException {
  return derive(password, salt, LEGACY_ITERATIONS);
}

public static boolean verifyPassword(String password, String legacySalt, String storedHash)
    throws NoSuchAlgorithmException, InvalidKeySpecException {
  try {
    var encoded = parse(storedHash);
    var expected = encoded == null
        ? derive(password, legacySalt, LEGACY_ITERATIONS)
        : derive(password, encoded.salt(), encoded.iterations());
    var actual = encoded == null ? storedHash : encoded.hash();
    return MessageDigest.isEqual(
        expected.getBytes(StandardCharsets.US_ASCII),
        actual.getBytes(StandardCharsets.US_ASCII));
  } catch (IllegalArgumentException | NullPointerException malformed) {
    return false;
  }
}

public static boolean needsRehash(String legacySalt, String storedHash) {
  var encoded = parse(storedHash);
  return encoded == null || encoded.iterations() != CURRENT_ITERATIONS || legacySalt != null;
}

private static String derive(String password, String salt, int iterations)
    throws NoSuchAlgorithmException, InvalidKeySpecException {
  var spec = new PBEKeySpec(password.toCharArray(), Base64.getDecoder().decode(salt),
      iterations, HASH_KEY_LENGTH);
  try {
    return Base64.getEncoder().encodeToString(
        SecretKeyFactory.getInstance(ALGORITHM).generateSecret(spec).getEncoded());
  } finally {
    spec.clearPassword();
  }
}
```

Verification:
- `./gradlew.bat :cbell-lib:test --tests '*PasswordUtilTest'`

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/account/auth/AccountAuthenticationService.java`
- Lines: 29-51
- Action: replace

Current:
```java
public String loginAccount(AccountLoginRequest accountLoginRequest)
    throws InvalidTokenException, ResourceNotFoundException {
  try {
    var sanitizedEmail = EmailSanitizer.sanitize(accountLoginRequest.email());
    var account = accountRepository
        .findByEmailIgnoreCase(sanitizedEmail)
        .orElseThrow(() -> new ResourceNotFoundException(
            String.format("Account with email %s not found.", sanitizedEmail)));

    if (!PermissionService.isAuthenticated(accountLoginRequest, account)) {
      throw new InvalidTokenException("Given Login information was not correct.");
    }
    if (!PermissionService.isAccountActive(account.getStatus())) {
      throw new AccountNotActiveException("Account is not active.");
    }

    account.setLastLoginOn(Instant.now());
    accountRepository.save(account);
    log.info("Successful login for account with id: {}", account.getId());
    return PermissionService.generateToken(account);
  } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
    throw new InvalidTokenException("Error validating password: " + e.getMessage(), e);
  }
}
```

Proposed:
```java
public String loginAccount(AccountLoginRequest request) throws InvalidTokenException {
  try {
    var email = EmailSanitizer.sanitize(request.email());
    var account = accountRepository.findByEmailIgnoreCase(email).orElse(null);
    var password = request.password();
    var verified = account == null
        ? PasswordUtil.verifyPassword(password, null, DUMMY_CURRENT_HASH)
        : PasswordUtil.verifyPassword(password, account.getPasswordSalt(), account.getPasswordHash());
    if (account == null || !verified || account.getStatus() != AccountStatus.ACTIVE) {
      log.info("Rejected account login category={}", rejectionCategory(account, verified));
      throw rejectedLogin();
    }
    if (PasswordUtil.needsRehash(account.getPasswordSalt(), account.getPasswordHash())) {
      account.setPasswordHash(PasswordUtil.hashPassword(password));
      account.setPasswordSalt(null);
    }
    account.setLastLoginOn(Instant.now());
    accountRepository.save(account);
    log.info("Successful login for account with id: {}", account.getId());
    return PermissionService.generateToken(account);
  } catch (NoSuchAlgorithmException | InvalidKeySpecException | IllegalArgumentException failure) {
    log.warn("Rejected account login because credential verification failed safely.");
    throw rejectedLogin(failure);
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests '*AccountServiceTest' --tests '*AccountAuthenticationRequestValidationTest'`

### Task 3 - Stabilize API errors and client-error logging (#1261)

Sequence / dependencies:
- Independent of Tasks 1-2, but runs before HTTP contract tests so all negative responses share final mapping.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: malformed JSON, invalid arguments, unsupported media, unacceptable response type, access denial, and unexpected failures return stable safe descriptions and appropriate statuses.
  - Invariants: raw framework/parser messages never cross the API boundary; expected 4xx outcomes do not log stack traces at ERROR; unexpected 500 and infrastructure failures retain full cause server-side.
  - Boundary/API: `ControllerExceptionHandler` remains the single response-envelope boundary.
  - Effects and failures: logging is the only effect; log category and level reflect caller-correctable versus operational failure.
  - Tests and evidence: add RED contract tests for malicious parser details and a captured-log test proving routine 4xx has no ERROR stack trace.

#### Code Edit 3.1
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`
- Lines: 46-59
- Action: replace

Current:
```java
@ExceptionHandler(Exception.class)
public ResponseEntity<Response<?>> handleGenericException(Exception e) {
  var frameworkStatus = statusForFrameworkException(e);
  if (frameworkStatus != null) {
    log.error(REQUEST_ERROR, e);
    return errorResponse(REQUEST_ERROR, e.getMessage(), frameworkStatus);
  }

  log.error(INTERNAL_SERVER_ERROR, e);
  return errorResponse(
      INTERNAL_SERVER_ERROR,
      "An unexpected error occurred. Please try again later.",
      HttpStatus.INTERNAL_SERVER_ERROR);
}
```

Proposed:
```java
@ExceptionHandler(Exception.class)
public ResponseEntity<Response<?>> handleGenericException(Exception failure) {
  var frameworkStatus = statusForFrameworkException(failure);
  if (frameworkStatus != null) {
    log.warn("{} status={} type={}", REQUEST_ERROR, frameworkStatus.value(),
        failure.getClass().getSimpleName());
    return errorResponse(REQUEST_ERROR, publicFrameworkDescription(frameworkStatus), frameworkStatus);
  }
  log.error(INTERNAL_SERVER_ERROR, failure);
  return errorResponse(INTERNAL_SERVER_ERROR,
      "An unexpected error occurred. Please try again later.",
      HttpStatus.INTERNAL_SERVER_ERROR);
}
```

Verification:
- `./gradlew.bat :cbell-lib:test --tests '*ControllerExceptionHandlerTest'`

### Task 4 - Validate and apply the production trusted-proxy chain (#1262)

Sequence / dependencies:
- Runs after error mapping so invalid startup configuration has clear diagnostic ownership and proxy tests use final request behavior.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: forwarding headers are ignored unless the immediate peer is trusted; trusted chains are walked right-to-left to the first untrusted client hop; malformed configured ranges fail bean creation.
  - Invariants: only IP literals/CIDRs are accepted; no DNS is performed; spoofed left-side header entries cannot override the nearest untrusted hop.
  - Boundary/API: retain `ClientIpProperties.trustedProxies` and `ClientIpResolver.resolveClientIp(HttpServletRequest)`.
  - Effects and failures: startup parses configuration once; request resolution is bounded by forwarded-hop count and performs no I/O.
  - Tests and evidence: add RED cases for invalid CIDR, IPv6 loopback, spoofed multihop input, untrusted remote, and the production default tunnel chain.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/configuration/ClientIpResolver.java`
- Lines: 10-79
- Action: replace

Current:
```java
@RequiredArgsConstructor
public class ClientIpResolver {
  private final ClientIpProperties properties;

  public String resolveClientIp(HttpServletRequest request) {
    var remoteAddress = request.getRemoteAddr();
    var forwardedFor = request.getHeader("X-Forwarded-For");
    if (!isTrustedProxy(remoteAddress) || forwardedFor == null || forwardedFor.isBlank()) {
      return remoteAddress;
    }
    var firstForwarded = forwardedFor.split(",")[0].trim();
    return firstForwarded.isBlank() ? remoteAddress : firstForwarded;
  }
}
```

Proposed:
```java
public class ClientIpResolver {
  private static final int MAX_FORWARDED_HOPS = 32;
  private final List<IpAddressMatcher> trustedProxies;

  public ClientIpResolver(ClientIpProperties properties) {
    this.trustedProxies = properties.getTrustedProxies().stream()
        .map(String::trim)
        .map(ClientIpResolver::validatedMatcher)
        .toList();
  }

  public String resolveClientIp(HttpServletRequest request) {
    var remote = request.getRemoteAddr();
    var forwarded = request.getHeader("X-Forwarded-For");
    if (!isTrusted(remote) || forwarded == null || forwarded.isBlank()) return remote;
    var hops = Arrays.stream(forwarded.split(",", MAX_FORWARDED_HOPS + 1))
        .map(String::trim).filter(value -> !value.isEmpty()).toList();
    if (hops.isEmpty() || hops.size() > MAX_FORWARDED_HOPS) return remote;
    for (int index = hops.size() - 1; index >= 0; index--) {
      var hop = hops.get(index);
      if (!isIpLiteral(hop)) return remote;
      if (!isTrusted(hop)) return hop;
    }
    return hops.getFirst();
  }

  private boolean isTrusted(String address) {
    return trustedProxies.stream().anyMatch(matcher -> matcher.matches(address));
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests '*ClientIpResolverTest' --tests '*CommandCenterActionServiceTest'`

#### Code Edit 4.2
- File: `website/src/main/resources/application-prod.yml`
- Lines: after 3
- Action: add

Proposed:
```yaml
client-ip:
  trusted-proxies: ${CLIENT_IP_TRUSTED_PROXIES:127.0.0.1/32,::1/128}
```

Verification:
- `./gradlew.bat :website:test --tests '*ProductionConfiguration*' --tests '*ClientIpResolverTest'`

### Task 5 - Make account status the only approval lifecycle (#1263)

Sequence / dependencies:
- Runs after credential revalidation so any status transition has immediate session consequences without consulting a second flag.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: signup creates active accounts; login and privileged feature access consult status; Back Office moderates status/role and has no separate pending-approval queue or action.
  - Invariants: one persisted lifecycle field controls access; old `isApproved`/`approvedBy` data is removed idempotently; no active account is denied due to stale legacy flags.
  - Boundary/API: remove approval-only endpoint and DTO fields; preserve status moderation and audit endpoints.
  - Effects and failures: migration `008` unsets two legacy fields across accounts and is safe to retry; UI requests no longer send `isApproved`.
  - Tests and evidence: first add RED tests showing active accounts with historical `isApproved=false` can access protected features and serialized details omit approval fields; add migration and UI regression tests.

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/account/model/Account.java`
- Lines: 44-63
- Action: replace

Current:
```java
@Id
private String id;
private String approvedBy;

@CreatedBy
private String createdBy;
// ...
private String firstName;
private Boolean isApproved;
private UUID inviteCode;
```

Proposed:
```java
@Id
private String id;

@CreatedBy
private String createdBy;
// ...
private String firstName;
private UUID inviteCode;
```

Verification:
- `./gradlew.bat :website:test --tests '*AccountServiceTest' --tests '*SharedFolderAccessServiceTest' --tests '*MusicAccessServiceTest' --tests '*CommandCenterAccessServiceTest'`

#### Code Edit 5.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V008RemoveAccountApprovalFields.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.mongo.migration;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Component;

/** Removes the retired approval flags after AccountStatus became authoritative. */
@Component
public final class V008RemoveAccountApprovalFields implements ApplicationMigration {
  @Override public String id() { return "008"; }
  @Override public String description() { return "Remove retired account approval fields"; }
  @Override public String checksum() { return "account-status-authoritative-v1"; }

  @Override
  public void apply(MongoTemplate mongo) {
    mongo.updateMulti(new Query(), new Update().unset("isApproved").unset("approvedBy"),
        "accounts");
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests '*V008RemoveAccountApprovalFieldsTest' --tests '*MongoMigrationRunnerTest'`

#### Code Edit 5.3
- File: `website/src/main/resources/static/js/back-office.js`
- Lines: 179-202
- Action: replace

Current:
```javascript
if (!account.isApproved) return 'queue-pending';
if (account.status === 'SUSPENDED') return 'queue-suspended';
return 'queue-active';
// ...
const pendingUsers = accounts.filter(account => !account.isApproved).length;
```

Proposed:
```javascript
if (account.status === 'SUSPENDED') return 'queue-suspended';
if (account.status === 'INACTIVE') return 'queue-inactive';
return 'queue-active';
// ...
const inactiveUsers = accounts.filter(account => account.status === 'INACTIVE').length;
```

Verification:
- `./gradlew.bat :website:jsTest`

### Task 6 - Correct account endpoint media and status contracts (#1264)

Sequence / dependencies:
- Runs last because the removed approval endpoint and final account DTO determine the controller contract under test.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: create returns 201 with a stable account resource location; synchronous update/delete return 200; DELETE routes accept requests without `Content-Type`; request-body endpoints retain JSON media validation.
  - Invariants: response envelopes and authorization remain unchanged; no bodyless mapping declares `consumes`; `Location` contains only the new public identifier.
  - Boundary/API: versioned `AccountController` mappings and owning README/Javadocs.
  - Effects and failures: no new effects; route matching must distinguish missing body media from unsupported response types.
  - Tests and evidence: change MockMvc expectations first, witness existing 200/202/415 failures, then make mapping/status edits and run the complete controller slice.

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/account/AccountController.java`
- Lines: 115-128
- Action: replace

Current:
```java
@PostMapping(
    value = V20241215 + "/create",
    consumes = MediaType.APPLICATION_JSON_VALUE,
    produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Response<AccountDetail>> createAccount(
    @Valid @RequestBody AccountCreateRequest accountCreateRequest) throws Exception {
  return new ResponseEntity<>(
      Response.<AccountDetail>builder()
          .payload(accountService.createAccount(accountCreateRequest))
          .success(true)
          .build(), HttpStatus.OK);
}
```

Proposed:
```java
@PostMapping(
    value = V20241215 + "/create",
    consumes = MediaType.APPLICATION_JSON_VALUE,
    produces = MediaType.APPLICATION_JSON_VALUE)
public ResponseEntity<Response<AccountDetail>> createAccount(
    @Valid @RequestBody AccountCreateRequest request) throws Exception {
  var created = accountService.createAccount(request);
  var body = Response.<AccountDetail>builder().payload(created).success(true).build();
  return ResponseEntity.created(URI.create(
      "/api/accounts" + V20241215 + "/" + created.getId())).body(body);
}
```

Verification:
- `./gradlew.bat :website:test --tests '*AccountControllerTest'`

#### Code Edit 6.2
- File: `website/src/main/java/dev/christopherbell/account/AccountController.java`
- Lines: 139-171
- Action: replace

Current:
```java
@DeleteMapping(
    value = V20250903 + "/{accountId}",
    consumes = MediaType.APPLICATION_JSON_VALUE,
    produces = MediaType.APPLICATION_JSON_VALUE)
// ...
@DeleteMapping(
    value = V20260726 + "/{accountId}",
    consumes = MediaType.APPLICATION_JSON_VALUE,
    produces = MediaType.APPLICATION_JSON_VALUE)
```

Proposed:
```java
@DeleteMapping(
    value = V20250903 + "/{accountId}",
    produces = MediaType.APPLICATION_JSON_VALUE)
// ...
@DeleteMapping(
    value = V20260726 + "/{accountId}",
    produces = MediaType.APPLICATION_JSON_VALUE)
```

Verification:
- `./gradlew.bat :website:test --tests '*AccountControllerTest'`

## Code Changes

- `account/auth`, `PermissionService`, JWT/browser filter wiring: shared current-account fingerprint and bearer revalidation.
- `PasswordUtil`, account creation/reset/authentication, command-center password verification: self-describing hash plus legacy upgrade.
- `ControllerExceptionHandler`: safe descriptions and severity-aware logging.
- `ClientIpResolver`, production YAML/environment example, configuration README/tests: validated right-to-left proxy chain.
- Account entity/DTO/update/moderation/access/UI/docs plus migration `008`: remove approval-only lifecycle state.
- `AccountController` and tests/docs: correct media/status/location contracts.

## Files and Modules

- `cbell-lib/src/main/java/dev/christopherbell/libs/security/PasswordUtil.java`
- `cbell-lib/src/main/java/dev/christopherbell/libs/api/controller/ControllerExceptionHandler.java`
- `website/src/main/java/dev/christopherbell/account/**`
- `website/src/main/java/dev/christopherbell/configuration/security/**`
- `website/src/main/java/dev/christopherbell/configuration/ClientIp*.java`
- `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V008*.java`
- `website/src/main/resources/application-prod.yml`, `ops/production/windows/config/app.env.example`
- `website/src/main/resources/static/js/back-office.js` and matching Java/JavaScript tests/readmes.

## Unit Testing

Run RED/GREEN cycles in task order with the focused commands above. Then run:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\all-open-issues-20260729\.gradle-user-home'
.\gradlew.bat :cbell-lib:test :website:test :website:jsTest
```

Required cases include bearer invalidation for every security-state transition, browser compatibility, indistinguishable login failures, current/legacy/malformed hashes, log-safe framework failures, invalid/spoofed proxy chains, status-only access, migration idempotency, and bodyless account deletes.

## Local Testing

After automated checks, package and run the app with the test/local profile on port 8093 and a disposable test Mongo database. Exercise:

- create account: JSON POST returns 201, `Location`, and no approval fields;
- wrong/unknown/inactive login: identical 401 envelopes;
- valid login followed by direct test-fixture role/status/permission/password mutation: old bearer receives 401;
- malformed JSON and unsupported media: stable safe 400/415 envelopes;
- DELETE without `Content-Type`: reaches authorization/domain handling rather than 415;
- trusted loopback plus `X-Forwarded-For`: audit/rate-limit-visible client address is the first untrusted hop; untrusted remote ignores the header.

Use a non-8080 listener only. Record exact commands, requests, response status/body/headers, and cleanup in the Builder test report.

## Validation

1. Focused RED/GREEN evidence exists for every semantic task.
2. `:cbell-lib:test`, `:website:test`, `:website:jsTest`, and final `:website:check` pass.
3. `node --check website/src/main/resources/static/js/back-office.js` passes.
4. `git diff --check` passes and final diff contains no line-ending-only `gradlew.bat` change.
5. Alternate-port HTTP acceptance proves #1258-#1264 contracts.
6. Independent diff review finds no blocker under the coding-standard rubric.
7. PR required CI, Dependency Review, and CodeQL gates pass before merge.
8. Native production deployment rotates to the merge and `/` plus affected public/auth boundaries pass without weakening ACLs.

## Rollback or Recovery

- Revert the batch PR and redeploy the prior release if authentication or account APIs regress.
- Migration `008` only removes redundant approval metadata; rollback does not require restoring it because pre-change active accounts already use status for login. If an emergency code rollback expects the fields, its null-safe access behavior must be verified before deployment.
- Existing legacy hashes remain readable until a successful login upgrades them; rollback retains the old hash only for accounts not yet upgraded. Because upgraded hashes are not readable by old code, production rollback after live logins requires retaining the new `PasswordUtil` compatibility commit or applying a forward fix rather than blindly deploying the old binary.
- Keep old bearer tokens rejected after rollback if security state is uncertain; forced login is preferable to accepting stale authorization.

## Risks

- Password format rollback is one-way after rehash; deployment must retain dual-read support in any emergency patch.
- Per-request account lookup adds database load for bearer clients; account ID is indexed and browser traffic continues using persisted session lookup already present.
- Removing approval fields changes Back Office payload shape; JS and API tests must land atomically in the same PR.
- Proxy-chain mistakes can collapse rate-limit/audit identity; negative spoof tests and production loopback defaults are mandatory.
- Immediate JWT revocation invalidates tokens issued before this release because they lack the fingerprint claim; this is an accepted secure failure requiring re-login.

## Completion Criteria

- All #1258-#1264 requirements are implemented or directly evidenced.
- Focused and full automated suites plus alternate-port runtime acceptance pass.
- A validated Builder test report and spoke review are committed and pushed.
- The implementation PR passes all required gates and is merged.
- Issues #1258-#1264 are closed with commit, PR, CI, runtime, and production evidence.
- Production serves the merged build safely and the campaign ledger is updated for Batch 2.
