# ChristopherBell.dev ActivityPub Discovery Foundation Plan

## Document Status

complete

## Objective

Ship the first guarded ActivityPub rollout gate: explicit account consent, encrypted local actor identity, WebFinger, NodeInfo, local actor discovery, and read-only collections, while inbound mutations and outbound delivery remain disabled.

## Goals

- Existing accounts remain unfederated until an authenticated explicit opt-in.
- Browser signup shows the approved disclosure and a default-on choice when federation enrollment is configured; a safely disabled deployment shows the choice as unavailable, and API clients that omit the field remain opted out.
- Enabled active accounts have a stable ActivityPub actor URI and RSA public key while private key material is AES-GCM encrypted at rest.
- Anonymous WebFinger, NodeInfo, actor, outbox, followers, and following reads are bounded, no-store, and Mastodon-compatible enough for controlled discovery testing.
- Independent discovery, inbound, and outbound flags fail closed; this gate enables no inbox mutation, remote fetch, delivery, or lifespan change.

## Inputs

- Program spec: `docs/specs/2026-07-28-void-public-growth-program.md`.
- Release 2 production baseline: `f77c5f5bb644cc75cf98b27e722efdc00cd036f1`.
- Existing account creation, profile settings, active-account, post-expiration, security, stable-cursor, and browser public-base-url boundaries.
- User direction: continue autonomously, commit and push completed tasks, favor working software and security evidence over repeated process pauses.

## Branch

- Branch: `codex/activitypub-federation`.
- Base: `origin/main` at `f77c5f5bb644cc75cf98b27e722efdc00cd036f1`.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\activitypub-federation`.

## Non-Goals

- No outbound remote delivery, durable delivery queue, remote actor/key fetch, HTTP request signing, or controlled-peer delivery in this gate.
- No inbound Follow, Like, Undo, Create, Update, or Delete mutation.
- No remote account/post persistence, remote relationship projection, or local lifespan extension.
- No claim that disabling federation retracts remote history.
- No ActivityPub exposure for Messages, Music, Shared Folder, reports, or administrative data.

## Assumptions

- The canonical production ActivityPub origin is the existing validated `app.browser-security.public-base-url` (`https://www.christopherbell.dev`); apex requests may redirect, and federation cannot configure a competing origin.
- Username lookup remains case-insensitive through the existing account repository and only ACTIVE, consented accounts are discoverable.
- Existing null consent/identity fields mean disabled, so no historical account migration or key backfill is required.
- RSA 2048 with SHA-256 remains compatible with the first Mastodon-controlled discovery target; later signature work can deliberately rotate keys.
- A separate 32-byte base64 federation encryption secret is required only when discovery is enabled; disabled environments start without it.

## Open Questions

None for this gate. Remote delivery and inbound protocol choices stay in later approved rollout gates.

## Task Breakdown

### Task 1 - Persist explicit consent and atomic local identity

Sequence / dependencies:
- First task. Public protocol routes must never infer consent or synthesize unstable actor identities.

Expected files or modules:
- Account entity/create/update DTOs, mapper tests, federation consent/identity package, signup/profile behavior, migration/index, and account documentation.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: browser signup may explicitly request federation when server enrollment is available; existing users may enable or disable it; an enabled account owns one stable actor identity and keypair.
  - Invariants: omitted API consent is false; old null fields are false; identity generation and account enablement persist in one account write; disabling retains identity for stable re-enable; suspended/inactive accounts are never discoverable.
  - Boundary/API: `FederationConsentService.setEnabled(accountId, enabled)` is the only post-create toggle boundary; `AccountCreateRequest.federatePublicVoidPosts` is nullable for backward compatibility.
  - Effects and failures: key generation/encryption happens before the account save; failed cryptography or persistence never produces an enabled account without usable identity; private material never enters DTOs or logs.
  - Tests and evidence: first fail account-create/toggle tests for omitted, enabled, disabled, re-enabled, crypto failure, and persistence failure; finish with focused account/federation identity tests.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/account/model/dto/AccountCreateRequest.java`
- Lines: 33-37
- Action: replace

Current:
```java
    @NotBlank
    @Size(min = 3, max = 50)
    @Pattern(regexp = "^[A-Za-z0-9._-]+$")
    String username
) {}
```

Proposed:
```java
    @NotBlank
    @Size(min = 3, max = 50)
    @Pattern(regexp = "^[A-Za-z0-9._-]+$")
    String username,
    Boolean federatePublicVoidPosts
) {
  public boolean federationRequested() {
    return Boolean.TRUE.equals(federatePublicVoidPosts);
  }
}
```

Additional changes:
- Add nullable/false-by-default consent metadata and `@JsonIgnore` encrypted identity material to `Account`; extend explicit self/admin DTOs only with the consent boolean.
- Add `FederationIdentity` as a validated value object containing actor ID, key ID, PEM public key, AES-GCM nonce/ciphertext, key version, and creation time; reject raw private-key storage.
- Add `FederationConsentService` and a versioned authenticated consent endpoint. Generate identity before the single account save on first enable; disable without deleting identity.
- Add migration V006 index for active consented username lookup; do not backfill or enable existing accounts.
- Update account and federation package documentation.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-activitypub'; .\gradlew.bat :website:test --tests "*FederationConsent*" --tests "*AccountServiceTest*" --tests "*AccountControllerTest*" --no-daemon --console=plain`

### Task 2 - Encrypt and validate signing identity material

Sequence / dependencies:
- Runs with Task 1 before public actor projection; no actor may publish a key that cannot later be used by the configured signer.

Expected files or modules:
- Federation properties/configuration, identity cryptography service, PEM codec, production-settings validation, configuration examples, and negative tests.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: enabling federation creates one RSA keypair, publishes only the public key, encrypts PKCS#8 private bytes using AES-256-GCM, and can decrypt them only through the identity service.
  - Invariants: encryption uses a fresh 96-bit nonce and authenticated context binding account ID, actor ID, key ID, and key version; key/config values never appear in errors or logs; disabled discovery does not require a secret.
  - Boundary/API: `FederationIdentityCryptography` accepts typed plaintext key bytes and returns a validated encrypted value; callers cannot select algorithms or nonce.
  - Effects and failures: invalid/missing production secret fails startup only when discovery is enabled; corrupt ciphertext fails closed without returning partial key bytes.
  - Tests and evidence: first fail round-trip, nonce uniqueness, wrong-account AAD, wrong-secret, corrupt-ciphertext, secret validation, and disabled-mode tests.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/federation/identity/FederationIdentityCryptography.java`
- Lines: after 0
- Action: add

Proposed:
```java
public final class FederationIdentityCryptography {
  public EncryptedPrivateKey encrypt(
      String accountId, String actorId, String keyId, int keyVersion, byte[] pkcs8) {
    // Generate an internal 96-bit nonce and seal with AES/GCM/NoPadding using
    // canonical length-prefixed associated data for account, actor, key, and version.
  }

  public byte[] decrypt(String accountId, FederationIdentity identity) {
    // Rebuild the exact associated data and fail closed on any mismatch.
  }
}
```

Additional changes:
- Add validated `FederationProperties` under `app.federation` with `discovery-enabled`, `inbound-enabled`, `outbound-enabled`, software metadata, and base64 key-encryption secret; derive every actor/object origin from `BrowserSecurityProperties.publicBaseUrl()`.
- Reject inbound/outbound enablement when discovery is disabled; reject a missing/short/malformed secret when any federation surface is enabled.
- Add PEM encoding without a third-party crypto dependency and clear temporary private-key byte arrays where practical.
- Extend production configuration examples and startup validation without weakening existing JWT/mail/Mongo validation.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-activitypub'; .\gradlew.bat :website:test --tests "*FederationIdentityCryptography*" --tests "*FederationProperties*" --tests "*ProductionSettingsApplicationContextInitializerTest*" --no-daemon --console=plain`

### Task 3 - Expose bounded read-only ActivityPub discovery

Sequence / dependencies:
- Runs after Tasks 1-2 so protocol responses project only validated, stable, consented identities.

Expected files or modules:
- Federation discovery controller/service/models, account/post query projection, security public routes, no-store response helpers, and protocol tests.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: WebFinger resolves exact local acct resources; NodeInfo describes the site; enabled actors and bounded read-only collections serialize canonical ActivityStreams JSON.
  - Invariants: only ACTIVE consented accounts with valid identity are visible; actor IDs, object IDs, links, and key IDs derive from the configured canonical origin; expired/private/missing posts never appear; inbox mutation remains unavailable.
  - Boundary/API: exact GET routes are `/.well-known/webfinger`, `/.well-known/nodeinfo`, `/nodeinfo/2.1`, `/ap/users/{username}`, and bounded actor collections; content types are explicit and responses are no-store.
  - Effects and failures: malformed resource/username/cursor returns bounded 400/404; disabled discovery returns 404 without account existence disclosure; serialization performs no remote calls or writes.
  - Tests and evidence: first fail exact resource/host/case, inactive/disabled/missing identity, content type, JSON-LD shape, escaping, expiration, page bounds, cursor, no-store, and mutation-denial tests.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/configuration/security/SecurityConfig.java`
- Lines: 73-89
- Action: replace

Current:
```java
  private static final String[] PUBLIC_URLS = {
      "/",
      "GET:/robots.txt",
      "GET:/sitemap.xml",
      "GET:/actuator/health/liveness",
      "GET:/actuator/health/readiness",
      "/shared",
      "/music",
      "GET:/shared-folder-auth-sw.js",
      "GET:/api/music" + APIVersion.V20260728 + "/access",
      "/api/accounts" + APIVersion.V20241215 + "/login",
      "/api/accounts" + APIVersion.V20241215 + "/logout",
      "/api/accounts" + APIVersion.V20241215 + "/create",
      "/api/accounts" + APIVersion.V20241215 + "/password-reset/request",
      "/api/accounts" + APIVersion.V20241215 + "/password-reset/confirm",
      "GET:/api/accounts" + APIVersion.V20250914 + "/profile/**",
      "/favicon.ico",
```

Proposed:
```java
  private static final String[] PUBLIC_URLS = {
      "/",
      "GET:/robots.txt",
      "GET:/sitemap.xml",
      "GET:/actuator/health/liveness",
      "GET:/actuator/health/readiness",
      "GET:/.well-known/webfinger",
      "GET:/.well-known/nodeinfo",
      "GET:/nodeinfo/2.1",
      "GET:/ap/users/**",
      "/shared",
      "/music",
      "GET:/shared-folder-auth-sw.js",
      "GET:/api/music" + APIVersion.V20260728 + "/access",
      "/api/accounts" + APIVersion.V20241215 + "/login",
      "/api/accounts" + APIVersion.V20241215 + "/logout",
      "/api/accounts" + APIVersion.V20241215 + "/create",
      "/api/accounts" + APIVersion.V20241215 + "/password-reset/request",
      "/api/accounts" + APIVersion.V20241215 + "/password-reset/confirm",
      "GET:/api/accounts" + APIVersion.V20250914 + "/profile/**",
      "/favicon.ico",
```

Additional changes:
- Use dedicated protocol response records/maps with allowlisted fields; never serialize Account/Post entities.
- Return actor `inbox`, `outbox`, `followers`, `following`, `publicKey`, and Mastodon-compatible `url`; expose shared inbox only as a URI while POST routes remain denied in this gate.
- Outbox reads only active local public posts/replies owned by that actor, maps them to Note objects, and caps page size at 20 with opaque stable cursors.
- Followers/following return bounded local-only consented relationships; totals are protocol metadata and never enter ranking.
- Add explicit no-store and content-type tests plus public security coverage.

Verification:
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-activitypub'; .\gradlew.bat :website:test --tests "*FederationDiscovery*" --tests "*WebFinger*" --tests "*NodeInfo*" --tests "*SecurityConfigTest*" --no-daemon --console=plain`

### Task 4 - Add consent UI and controlled discovery verification

Sequence / dependencies:
- Runs after Tasks 1-3. It exposes the approved human choice and validates the full gate without enabling later federation effects.

Expected files or modules:
- Signup/profile templates and JavaScript, CSS/accessibility tests, frontend docs, federation operations docs, and local/runtime evidence.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: signup presents a checked federation choice when enrollment is available, or the same disabled choice with unavailable copy when the safe rollout flag is off; current users can opt in/out from profile settings; UI reflects server-confirmed state.
  - Invariants: unchecked, disabled, or omitted means false; disclosure is never hidden behind a tooltip; disabling does not promise remote deletion; no browser secret or key material exists.
  - Boundary/API: the server-rendered signup model owns the non-secret enrollment-available boolean; signup sends one consent boolean; profile toggle calls only the authenticated consent endpoint and renders bounded server errors as text.
  - Effects and failures: submit is gated against duplicate clicks; failed consent update restores authoritative state; normal account creation/login redirects remain unchanged.
  - Tests and evidence: first fail payload/default/disclosure/toggle rollback/accessibility tests; finish with browser signup/profile and protocol discovery checks.

#### Code Edit 4.1
- File: `website/src/main/resources/templates/signup.html`
- Lines: 42-46
- Action: replace

Current:
```html
              <div class="mb-3 mt-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢" required />
              </div>
              <div class="d-grid gap-2">
```

Proposed:
```html
              <div class="mb-3 mt-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢" required />
              </div>
              <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="federatePublicVoidPosts"
                       th:checked="${federationEnrollmentAvailable}"
                       th:disabled="${!federationEnrollmentAvailable}" />
                <label class="form-check-label" for="federatePublicVoidPosts">Federate my public Void posts</label>
              </div>
              <p class="form-text mb-3">Federated posts and interactions go to independent servers. Void sends deletion notices when content expires, but remote servers may retain cached or copied content.</p>
              <p class="form-text mb-3" th:if="${!federationEnrollmentAvailable}">Federation enrollment is temporarily unavailable.</p>
              <div class="d-grid gap-2">
```

Additional changes:
- Extend the account view controller with the non-secret enrollment-availability model value; extend `signupPayload` and form field collection with `checked && !disabled`; update JSDoc and browser tests.
- Add equivalent authenticated profile setting with the same disclosure, server-confirmed state, and text-only failure rendering.
- Update frontend/account/federation docs and production configuration runbook for generating and installing the separate protected secret.
- Validate locally with discovery enabled but inbound/outbound false; do not edit production protected config until the code, CI, and controlled discovery evidence pass.

Verification:
- `node --test website/src/test/js/signup-auth.test.js website/src/test/js/federation-consent.test.js website/src/test/js/a11y-markup.test.js`
- `$env:GRADLE_USER_HOME='A:\Temp\gradle-activitypub'; .\gradlew.bat :website:test --tests "*Federation*" --tests "*AccountControllerTest*" --no-daemon --console=plain`

### Task 5 - Full gate validation, one PR, and guarded deployment

Sequence / dependencies:
- Runs after Tasks 1-4. No merge occurs until all protocol, crypto, consent, and disabled-effect evidence is green.

Expected files or modules:
- No production code unless a witnessed regression requires a focused test-first correction; Builder test report, plan/spec status, and session memory are updated after runtime evidence.

Implementation notes:
- Verify the final diff contains no remote HTTP client, inbox mutation handler, delivery scheduler, plaintext private key, raw entity serialization, or popularity ranking.
- Run the full check, then start the app on port 8081 with explicit isolated Mongo URI/database, discovery enabled, inbound/outbound disabled, a test-only random secret, and controlled accounts/posts.
- Exercise WebFinger, NodeInfo, actor, collections, signup consent, existing-account toggle, disabled/malformed paths, content types, no-store, and service restart identity stability.
- Open one PR for this discovery-foundation gate, wait for Windows/macOS/Linux CI, Dependency Review, and CodeQL, merge, and let automatic deployment validate the disabled-by-default production artifact.
- Enabling production discovery is a separate protected configuration action after a real secret is installed; inbound/outbound remain false.

## Code Changes

- `AccountCreateRequest`, `Account`, account mapping/service/controller, V006: add explicit consent and stable atomic identity ownership.
- `federation/configuration` and `federation/identity`: validate flags/origin/secret and own RSA/AES-GCM material.
- `federation/discovery`: WebFinger, NodeInfo, actors, Notes, and bounded local collections.
- `SecurityConfig`: expose only exact read-only protocol routes.
- Signup/profile templates and JavaScript: approved choice, disclosure, and authoritative toggle state.
- Tests/docs/config examples: cryptographic, protocol, consent, security, accessibility, and operations evidence.

## Files and Modules

- `website/src/main/java/dev/christopherbell/federation/{configuration,identity,discovery}/**`
- `website/src/main/java/dev/christopherbell/account/**`
- `website/src/main/java/dev/christopherbell/configuration/{security,mongo/migration}/**`
- `website/src/main/resources/{application*.yml,templates,static/js,static/css}/**`
- `website/src/test/java/dev/christopherbell/{federation,account,configuration}/**`
- `website/src/test/js/{signup-auth,federation-consent,a11y-markup}.test.js`
- `docs/operations/windows-production.md` and feature READMEs.

## Unit Testing

- Consent partitions: omitted, false, true, discovery-disabled enrollment rejection, existing null, disable, re-enable, suspended/missing, duplicate request, persistence failure.
- Cryptography: RSA identity shape, PEM, AES-GCM round trip, nonce uniqueness, AAD mismatch, secret mismatch, corruption, invalid config, and disabled config.
- WebFinger: exact acct scheme, canonical host, Unicode/punctuation, case, blank/oversized resource, disabled/inactive/missing account, and safe link shape.
- NodeInfo: exact schema/content type, stable software metadata, bounded usage counts, and disabled state.
- Actor/collections: exact context/type/IDs, public key, no secret fields, active-only posts, expiration boundary, replies, cursors, size caps, local-only relationship filtering, and no-store.
- Security: anonymous GET allowlist only; POST inbox/shared-inbox and unsupported methods perform no service mutation.
- Browser: configured default-checked disclosure, disabled-rollout presentation and false payload, explicit false/true payload, profile authoritative rollback, escaping, focus, labels, and mobile markup.

## Local Testing

- Use `A:\Projects\christopherbell.dev-worktrees\activitypub-federation`, port 8081, and database `christopherbell_activitypub_discovery_test`.
- Set both `SPRING_MONGODB_URI=mongodb://127.0.0.1:27017` and `SPRING_MONGODB_DATABASE=christopherbell_activitypub_discovery_test`; use the existing browser-security public origin for actor IDs.
- Generate a test-only 32-byte base64 secret in memory; set discovery true and inbound/outbound false. Never copy it into docs, logs, Git, or production.
- Seed one consented active account, one unconsented active account, one suspended account, active/expired posts, and local relationships.
- Check `curl`/browser responses, content types, headers, pagination, negative routes, and restart-stable actor/key IDs.
- Confirm production fixture IDs remain zero before/after; drop only the exact isolated database; stop only the port-8081 process.

## Validation

- Narrow RED-to-GREEN tests precede each production edit.
- Full `:website:check` succeeds.
- Read-only diff audit proves no inbound/outbound side effect path exists.
- Controlled local discovery works across app restart with exact content types and no-store.
- One PR passes all required checks and automatically deploys the default-disabled artifact.
- Exact production merge SHA serves existing Void/login/Music/Messages/admin smoke routes with no behavior regression.

## Rollback or Recovery

- All fields and collections are additive; old binaries ignore consent/identity metadata.
- Discovery, inbound, and outbound flags default false. Turning discovery off immediately returns protocol discovery to generic not-found behavior without deleting identity evidence.
- Retain encrypted identity on disable and rollback so actor/key IDs remain stable on deliberate re-enable.
- Use the existing production release rollback if deployment smoke fails; do not weaken startup validation or ACLs.

## Risks

- Private-key disclosure: encrypt with AES-GCM, bind AAD to identity, exclude from DTOs/logs, and negative-test serialization.
- Consent ambiguity: browser default is explicit and visible; omitted API field remains false; existing null accounts remain disabled.
- Actor instability: generate once, persist atomically with enablement, and test across disable/re-enable and restart.
- Account enumeration: disabled/inactive/missing actors share the same bounded 404 behavior.
- Protocol injection: canonicalize host/resource/username, construct IDs from configured origin, and serialize allowlisted records only.
- Accidental federation effects: no remote client, POST inbox mutation, delivery scheduler, or signer is included; inbound/outbound flags remain false.
- Secret installation requires protected production configuration authority. Merge/deploy remains safe with discovery false; production enablement waits for a separately generated secret and exact config verification.

## Completion Criteria

- Consent and encrypted identity semantics are explicit and fully tested.
- WebFinger, NodeInfo, local actors, and bounded local collections interoperate in controlled discovery checks.
- No remote network request or federation mutation exists in this gate.
- Full automated/local/browser/security evidence is recorded.
- The gate merges through one green PR, deploys automatically, and production remains healthy with federation default-disabled.
