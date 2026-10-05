# ChristopherBell.dev ActivityPub Controlled Outbound Delivery Plan

## Document Status

complete

## Objective

Ship the second ActivityPub rollout gate: asynchronously deliver only newly-created, explicitly eligible public Void posts to operator-configured controlled peer inboxes with durable idempotent jobs, interoperable RSA-SHA256 HTTP signatures, strict SSRF/redirect controls, bounded retries, and a fail-closed outbound kill switch. Production remains disabled.

## Goals

- A post is outbound-eligible only when its author is ACTIVE and federation-enabled and the server outbound flag is true at creation time; enabling outbound never backfills historical posts.
- Delivery uses the exact bytes whose SHA-256 digest is signed, a stable activity ID, the actor's encrypted-at-rest key, and Mastodon-compatible `(request-target) host date digest` RSA-SHA256 headers.
- Network connections go only to trusted configured peers, use a prevalidated pinned address, preserve TLS SNI/hostname verification, never follow redirects, discard response bodies, and enforce connect/request timeouts.
- A Mongo queue survives restarts, claims work atomically, retries only transient outcomes with bounded exponential backoff, and treats stable activity IDs as the receiver-side idempotency key.
- Turning outbound off prevents every new remote call without deleting jobs or identities.
- The controlled-peer gate is testable locally, but production configuration remains discovery/inbound/outbound false with no peer endpoints.

## Inputs

- Program spec: `docs/specs/2026-07-28-void-public-growth-program.md`.
- Discovery foundation plan and production merge `6cd9e397e4ec2c3175ae5c31a95f633b7a7c7c95`.
- Discovery runtime report: `docs/test-reports/2026-07-28-christopherbell-dev-activitypub-discovery-foundation-test-report.md`.
- W3C ActivityPub sections 7/7.1: remote inbox POST, asynchronous delivery, retry, stable activity/object bodies, and shared-inbox behavior.
- W3C security considerations B.3-B.7: localhost/URI restrictions, recursion limits, federation DoS controls, and exponential backoff.
- Mastodon security interoperability contract: RSA-SHA256 over `(request-target) host date digest`; POST body SHA-256 `Digest` header.
- Reactor Netty client boundary: pinned remote address, explicit SNI, hostname-verification configurer, redirect opt-in (therefore keep disabled), and bounded timeouts.
- User direction: continue autonomously, use one coherent PR, commit/push completed tasks, and prioritize working behavior plus security.

## Branch

- Branch: `codex/activitypub-outbound-delivery`.
- Base: `origin/main` at `6cd9e397e4ec2c3175ae5c31a95f633b7a7c7c95`.
- Worktree: `A:\Projects\christopherbell.dev-worktrees\activitypub-outbound-delivery`.

## Non-Goals

- No production outbound activation or production peer secret/config installation.
- No remote Follow acceptance, inbound mutation, remote actor persistence, or remote follower graph.
- No broad public/follower fanout; only explicitly configured controlled peers receive this gate's Create activities.
- No Update/Delete delivery yet. The next outbound-production gate must add lifecycle propagation before broad enablement.
- No redirects, proxy use, arbitrary user-supplied peer URL, WebFinger/actor crawling, collection recursion, LD signatures, or RFC 9421 fallback in this gate.
- No effect on local post lifespan, likes, replies, Messages, Music, Shared Folder, reports, or administrative data.

## Assumptions

- Controlled peer configuration is trusted operator input, never browser/API input.
- Mastodon-compatible draft HTTP Signatures remain the broadest controlled-peer interoperability baseline; stable body bytes and RSA-SHA256 are sufficient for this gate.
- A receiver may accept a delivery and the sender may crash before recording success. Stable activity IDs and a unique local job key make retries safely recognizable as duplicates.
- Local development may use HTTP loopback only when the app's canonical public origin is also HTTP loopback and an explicit development switch is true. An HTTPS production origin can never enable that exception.
- Reactor Netty runtime dependencies are already present; no new third-party library is needed.

## Open Questions

None for this gate. Broader peer discovery, RFC 9421 negotiation, Update/Delete propagation, and production activation remain explicit later gates.

## Task Breakdown

### Task 1 - Define fail-closed peers and a pinned outbound network boundary

Sequence / dependencies:
- Runs first because no signing, queue, or scheduler may own a generic unrestricted HTTP client.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: outbound startup requires at least one valid controlled peer; every request connects only to a currently public resolved address for that exact configured HTTPS host.
  - Invariants: discovery is required before outbound; disabled deployments require no peer; redirects/proxies/private addresses remain unavailable; production never accepts the loopback test exception.
  - Boundary/API: extend `app.federation` with bounded nested outbound settings and expose a package-local client that accepts only a validated peer plus immutable request bytes/headers.
  - Effects and failures: DNS/config/TLS/timeout failures become typed transient or permanent delivery outcomes; no response body is retained or logged.
  - Tests and evidence: first fail properties/address/client tests for missing peers, unsafe schemes/ports/hosts, mixed DNS answers, rebinding-resistant pinned connect address, redirects, timeout, and response classification.
- Resolve all A/AAAA answers immediately before each attempt, reject the entire result if any address is loopback, private/site-local, link-local, multicast, unspecified, IPv4-mapped private IPv6, or otherwise non-global, then select deterministically and pass that exact `InetSocketAddress` to Reactor Netty `remoteAddress`.
- Set the original host in `Host` and TLS SNI and apply `HttpClientSecurityUtils.HOSTNAME_VERIFICATION_CONFIGURER`; never call `followRedirect(true)`.
- Disable Reactor Netty's implicit aborted-request retry so only the durable job policy retries.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/federation/configuration/FederationProperties.java`
- Lines: 8-91
- Action: replace

Current:
```java
public final class FederationProperties {
  private final boolean discoveryEnabled;
  private final boolean inboundEnabled;
  private final boolean outboundEnabled;
  // software metadata and encryption secret only
}
```

Proposed:
```java
public final class FederationProperties {
  private final boolean discoveryEnabled;
  private final boolean inboundEnabled;
  private final boolean outboundEnabled;
  private final FederationOutboundProperties outbound;

  // Validate bounded peers, timing, attempts, batch size, and development-loopback rules.
  // outboundEnabled requires discovery, a key, a nonempty peer list, and notBefore.
  public FederationOutboundProperties outbound() { return outbound; }
}
```

Verification:
- `gradlew.bat :website:test --tests dev.christopherbell.federation.configuration.FederationPropertiesTest --tests dev.christopherbell.federation.outbound.FederationPeerAddressPolicyTest`

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/federation/outbound/FederationPeerAddressPolicy.java`
- Lines: 1-220
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Resolves and pins one configured peer address while rejecting SSRF destinations. */
final class FederationPeerAddressPolicy {
  ValidatedPeerTarget validateAndResolve(ControlledPeer peer, URI publicOrigin) {
    // Require exact scheme/authority/path rules, resolve all addresses, reject unsafe sets,
    // and return the original TLS host plus one exact global InetSocketAddress.
  }
}
```

Verification:
- Unit tests cover IPv4/IPv6 public addresses, private/mapped addresses, userinfo, fragments, query limits, non-443 production ports, mixed safe/unsafe DNS sets, and loopback only under the local-origin development contract.

#### Code Edit 1.3
- File: `website/src/main/java/dev/christopherbell/federation/outbound/FederationOutboundHttpClient.java`
- Lines: 1-240
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Sends one bounded signed activity to one already-validated controlled inbox. */
final class FederationOutboundHttpClient {
  FederationDeliveryResult post(ValidatedPeerTarget target, SignedFederationRequest request) {
    // Pin remoteAddress, set original Host/SNI, enable hostname verification,
    // disable redirects/implicit retry, send exact bytes, discard body, classify status.
  }
}
```

Verification:
- A local controlled TLS/HTTP fixture proves exact target, headers, no redirect following, timeout behavior, and body discard; address-policy tests prove unsafe targets fail before socket creation.

#### Code Edit 1.4
- File: `website/src/main/resources/application.yml`
- Lines: 83-90
- Action: replace

Current:
```yaml
  federation:
    discovery-enabled: false
    inbound-enabled: false
    outbound-enabled: false
    software-name: christopherbell.dev
    software-version: ${GIT_COMMIT:development}
    key-encryption-secret: ""
```

Proposed:
```yaml
  federation:
    discovery-enabled: false
    inbound-enabled: false
    outbound-enabled: false
    software-name: christopherbell.dev
    software-version: ${GIT_COMMIT:development}
    key-encryption-secret: ""
    outbound:
      not-before:
      peers: []
      connect-timeout: 3s
      request-timeout: 10s
      initial-backoff: 30s
      max-backoff: 6h
      max-attempts: 6
      batch-size: 10
      development-loopback-enabled: false
```

Verification:
- Default app starts with no peer; outbound-enabled validation fails without an explicit safe peer/not-before boundary.

### Task 2 - Produce one canonical activity and sign its exact bytes

Sequence / dependencies:
- Runs after Task 1 so the signer output has a single bounded network consumer.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: outbox JSON and delivered Create activity share one factory; the delivery signer emits Date, Digest, and Signature headers for the exact serialized bytes.
  - Invariants: stable post-derived activity/object IDs, public/followers addressing, escaped content, encrypted-at-rest keys, and zero private material in logs/DTOs remain unchanged.
  - Boundary/API: move activity construction into `FederationActivityFactory`; encapsulate key decryption/signing in the identity package and return only headers plus body bytes.
  - Effects and failures: malformed identity/key/ciphertext fails the job without exposing key bytes; decrypted PKCS#8 byte arrays are zeroed in `finally`.
  - Tests and evidence: first fail byte-for-byte digest/base-string/signature verification tests using a known RSA key and fixed Clock.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/federation/discovery/FederationCollectionService.java`
- Lines: 150-178
- Action: replace

Current:
```java
  private ActivityPubCreate createActivity(String actorId, Post post) {
    String objectId = publicOrigin + "/void/" + post.getId();
    // Build the Note and Create directly in the collection service.
  }
```

Proposed:
```java
  // Inject FederationActivityFactory and map each loaded post with
  // activities.create(actorId, post); remove this duplicate private builder.
```

Verification:
- Existing collection tests stay green and a new factory test proves outbox/delivery objects are identical.

#### Code Edit 2.2
- File: `website/src/main/java/dev/christopherbell/federation/outbound/FederationActivityFactory.java`
- Lines: 1-150
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Owns stable public Create/Note construction for outbox reads and delivery. */
public final class FederationActivityFactory {
  public ActivityPubCreate create(String actorId, Post post) {
    // Preserve stable object/activity IDs, timestamps, reply link, escaping, to/cc.
  }
}
```

Verification:
- `FederationActivityFactoryTest` covers root/reply content, escaping, addressing, and stable IDs.

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/federation/identity/FederationRequestSigner.java`
- Lines: 1-220
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Signs the exact outbound bytes using the actor's encrypted local RSA key. */
public final class FederationRequestSigner {
  public SignedFederationRequest sign(Account account, URI inbox, byte[] body) {
    // Date RFC 1123; Digest SHA-256 base64; canonical lowercase request-target/host/date/digest;
    // SHA256withRSA; clear decrypted PKCS#8 bytes in finally; return immutable copies.
  }
}
```

Verification:
- A fixed-key test independently verifies Digest and RSA signature, query-bearing request-target, IPv6/port Host formatting, immutable body copies, and byte clearing on success/failure.

### Task 3 - Add durable eligibility, reconciliation, claim, retry, and kill-switch semantics

Sequence / dependencies:
- Runs after Tasks 1-2 because the queue owns validated peers and signed delivery artifacts.

Implementation notes:
- Required skill: `chris-street-style` before any code edits.
- Before-Edit Brief:
  - Behavior: only posts marked eligible at creation are reconciled into unique per-peer jobs; one worker claims due jobs, rechecks current consent/flags/post activity, signs/sends, and records success/retry/dead/cancelled.
  - Invariants: no historical backfill, no remote call when outbound is off, no delivery for disabled/suspended authors or expired/deleted posts, stable activity ID across retry, and at-most-one active claim per job.
  - Boundary/API: add one nullable-safe post eligibility field, queue/scan collections, atomic Mongo repository operations, and scheduled beans conditional on outbound enabled.
  - Effects and failures: queue persistence is durable; crash-after-remote-success may retry the stable ID; transient network/408/425/429/5xx retries exponentially; other 4xx and exhausted attempts become dead; bounded metadata only.
  - Tests and evidence: first fail post eligibility, unique enqueue, cursor recovery, expired claim, kill switch, retry schedule, Retry-After bound, and no-delivery tests.
- Scanner uses ascending `(createdOn,_id)` cursor and commits the cursor only after idempotent job upserts for the batch. Reprocessing after a crash is safe through the unique key.
- Dispatcher claims one exact due job with `findAndModify`; a lease expiration makes abandoned work recoverable.

#### Code Edit 3.1
- File: `website/src/main/java/dev/christopherbell/post/model/Post.java`
- Lines: 87-103
- Action: add

Current:
```java
  private Instant expiresOn;

  /** Most recent confirmed interaction that extended this root post's lifespan. */
  private Instant lastExtendedOn;
```

Proposed:
```java
  private Instant expiresOn;

  /** True only when this post was explicitly eligible for outbound federation at creation. */
  private Boolean federationOutboundEligible;

  public boolean isFederationOutboundEligible() {
    return Boolean.TRUE.equals(federationOutboundEligible);
  }

  /** Most recent confirmed interaction that extended this root post's lifespan. */
  private Instant lastExtendedOn;
```

Verification:
- Serialization/backward-compatibility tests prove missing/null is false.

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/post/creation/PostCreationService.java`
- Lines: 35-108
- Action: replace

Current:
```java
  private final PostTopicExtractor postTopicExtractor;
  private final Clock clock;
  // ...
  var post = Post.builder()
      .id(newId)
      .accountId(account.getId())
      .text(text)
      // ...
      .build();
```

Proposed:
```java
  private final PostTopicExtractor postTopicExtractor;
  private final FederationPublicationPolicy federationPublicationPolicy;
  private final Clock clock;
  // ...
  var post = Post.builder()
      .id(newId)
      .accountId(account.getId())
      .text(text)
      .federationOutboundEligible(federationPublicationPolicy.eligibleAtCreation(account, now))
      // ...
      .build();
```

Verification:
- `PostCreationServiceTest` proves disabled/opted-out/suspended posts are false, and only active opted-in authors under enabled outbound are true.

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/federation/outbound/FederationDeliveryJob.java`
- Lines: 1-180
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
@Document("federation_delivery_jobs")
final class FederationDeliveryJob {
  // Stable job key, post/account/peer IDs, state, attempts, due/claim timestamps,
  // bounded outcome category/status, and created/updated timestamps. No body, key, or response text.
}
```

Verification:
- Repository tests prove unique post/peer Create jobs, atomic due claim, exact-owner completion, expired-claim recovery, and bounded fields.

#### Code Edit 3.4
- File: `website/src/main/java/dev/christopherbell/federation/outbound/FederationDeliveryJobRepository.java`
- Lines: 1-260
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Owns idempotent enqueue, durable scan cursor, due claim, and exact-owner transitions. */
final class FederationDeliveryJobRepository {
  void enqueueIfAbsent(Post post, ControlledPeer peer) { /* upsert unique stable job key */ }
  Optional<FederationDeliveryJob> claimDue(String owner, Instant now, Instant leaseUntil) { /* findAndModify */ }
  boolean succeed(String jobId, String owner, Instant now) { /* exact state/owner CAS */ }
  boolean retryOrDead(String jobId, String owner, DeliveryDecision decision) { /* bounded CAS */ }
}
```

Verification:
- Mongo tests exercise real indexes/queries for unique enqueue, cursor replay, due ordering, claim ownership, expired claim recovery, and every terminal transition.

#### Code Edit 3.5
- File: `website/src/main/java/dev/christopherbell/federation/outbound/FederationOutboundCoordinator.java`
- Lines: 1-320
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Reconciles eligible posts and dispatches one bounded controlled-peer job at a time. */
final class FederationOutboundCoordinator {
  @Scheduled(fixedDelayString = "${app.federation.outbound.scan-delay:2s}")
  void reconcile() { /* cursor batch -> idempotent peer jobs */ }

  @Scheduled(fixedDelayString = "${app.federation.outbound.delivery-delay:2s}")
  void deliver() { /* flag/consent/activity checks -> sign -> send -> durable outcome */ }
}
```

Verification:
- Coordinator tests cover cursor replay, current consent revocation, flag-off kill switch, expired post cancellation, success, transient retry/backoff, permanent failure, max attempts, and crash-safe stable activity IDs.

#### Code Edit 3.6
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V007EnsureFederationOutboundIndexes.java`
- Lines: 1-100
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Creates named post-scan, unique job, due-job, and expired-claim indexes. */
@Component
public final class V007EnsureFederationOutboundIndexes implements ApplicationMigration {
  public void apply(MongoTemplate mongo) { /* four deterministic named indexes */ }
}
```

Verification:
- Migration test asserts exact collection, field order, uniqueness, names, and immutable checksum.

### Task 4 - Prove controlled delivery and preserve disabled production defaults

Sequence / dependencies:
- Runs after Tasks 1-3 and blocks PR creation until both enabled and disabled runtime passes are complete.

Implementation notes:
- Required skill: `chris-street-style` before edits to executable acceptance fixtures or configuration.
- Before-Edit Brief:
  - Behavior: a local controlled peer receives one valid signed Create, scripts one transient failure then success, observes stable activity ID on retry, and receives nothing after the kill switch.
  - Invariants: production flags and peer list remain empty/false; no real third party receives test traffic; temporary keys/databases/logs are removed.
  - Boundary/API: local-only controlled peer fixture plus production/example configuration and federation operations documentation.
  - Effects and failures: tests may bind only alternate local ports and isolated Mongo; never touch the production listener/database or weaken ACLs.
  - Tests and evidence: complete automated check, enabled/disabled candidate startup, peer signature verification, restart recovery, retry, and cleanup evidence.

#### Code Edit 4.1
- File: `website/src/main/resources/application-prod.yml`
- Lines: 29-36
- Action: replace

Current:
```yaml
  federation:
    discovery-enabled: ${APP_FEDERATION_DISCOVERY_ENABLED:false}
    inbound-enabled: ${APP_FEDERATION_INBOUND_ENABLED:false}
    outbound-enabled: ${APP_FEDERATION_OUTBOUND_ENABLED:false}
    software-name: christopherbell.dev
    software-version: ${GIT_COMMIT:unknown}
    key-encryption-secret: ${APP_FEDERATION_KEY_ENCRYPTION_SECRET:}
```

Proposed:
```yaml
  federation:
    discovery-enabled: ${APP_FEDERATION_DISCOVERY_ENABLED:false}
    inbound-enabled: ${APP_FEDERATION_INBOUND_ENABLED:false}
    outbound-enabled: ${APP_FEDERATION_OUTBOUND_ENABLED:false}
    software-name: christopherbell.dev
    software-version: ${GIT_COMMIT:unknown}
    key-encryption-secret: ${APP_FEDERATION_KEY_ENCRYPTION_SECRET:}
    outbound:
      not-before: ${APP_FEDERATION_OUTBOUND_NOT_BEFORE:}
      peers: []
      development-loopback-enabled: false
```

Verification:
- Prod-profile configuration test proves defaults start without peer/key and enabling outbound without protected required values fails closed.

#### Code Edit 4.2
- File: `website/src/test/java/dev/christopherbell/federation/outbound/ControlledPeerDeliveryIntegrationTest.java`
- Lines: 1-260
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
/** Runs a loopback controlled inbox and independently verifies digest/signature/retry semantics. */
class ControlledPeerDeliveryIntegrationTest {
  // Receive exact bytes, verify actor public key signature, return 503 then 202,
  // assert stable activity ID and no request after kill-switch/consent disable.
}
```

Verification:
- Run the integration test alone, then `gradlew.bat :website:check --no-daemon`.

## Code Changes

- `FederationProperties` and application YAML: nested controlled-peer, timing, retry, batch, not-before, and development safety settings.
- `federation/outbound` new package: peer policy, pinned client, activity factory, signer request model, job/state/repositories, publication policy, reconciler, dispatcher, and typed outcomes.
- `FederationCollectionService`: consume the shared activity factory.
- `FederationIdentityCryptography`: keep decryption encapsulated for the signer and clear temporary bytes.
- `Post` and `PostCreationService`: persist explicit creation-time outbound eligibility.
- `PostRepository`: bounded ascending eligibility scan query.
- V007 migration: deterministic scan/job/claim indexes.
- Tests: property, address, HTTP client, factory, signer, model, post creation, Mongo repository, coordinator, migration, and controlled-peer integration coverage.
- Operations/config docs: exact flags, peer format, key/not-before requirements, kill switch, metrics/log categories, and safe activation/rollback.

## Files and Modules

- `website/src/main/java/dev/christopherbell/federation/{configuration,identity,discovery,outbound}/**`
- `website/src/main/java/dev/christopherbell/post/{model,creation,PostRepository}.java`
- `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V007EnsureFederationOutboundIndexes.java`
- `website/src/main/resources/application*.yml`
- `website/src/test/java/dev/christopherbell/federation/**`
- `website/src/test/java/dev/christopherbell/post/**`
- `docs/operations/windows-production.md` or the existing federation operations section.

## Unit Testing

- Red/green focused commands per task using `:website:test --tests ...`.
- Cryptographic tests independently verify the Digest and signature rather than reusing production signer logic.
- Network tests prove address rejection before connect, pinned address use, SNI/Host preservation, redirect refusal, timeout, no implicit retry, and response classification.
- Mongo/coordinator tests prove unique enqueue, cursor replay, lease recovery, kill-switch behavior, bounded retries, and no historical/post-expiry delivery.
- Full `gradlew.bat :website:check --no-daemon` with isolated `GRADLE_USER_HOME=A:\Temp\gradle-activitypub-outbound`.

## Local Testing

- Use port 8081 for the app, a separate loopback port for the controlled inbox, and database `christopherbell_activitypub_outbound_test`.
- Start with discovery/outbound true, inbound false, one test peer, explicit not-before, a test-only encryption key, and the local-origin loopback development switch.
- Create an opted-in account and new post through real CSRF/browser-cookie APIs.
- Verify the controlled inbox receives exact ActivityStreams content, valid digest/signature/date, stable actor/activity/object IDs, and no private material.
- Script 503 then 202, restart the app between attempts, and prove the durable job retries with the same ID and reaches success.
- Turn outbound off and create another post; prove no socket request occurs.
- Run disabled-default candidate with no peer/key and prove site 200/outbound absent.
- Stop only test processes, drop only the isolated database, remove temporary keys/logs, and confirm port 8081 is closed.

## Validation

- All focused and full automated checks pass.
- One controlled peer accepts a valid signed Create after a durable retry and restart.
- Unsafe URI/address/redirect/timeout cases never reach an unvalidated destination.
- Only creation-time eligible posts produce jobs; historical, opted-out, suspended, expired, and post-kill-switch work makes no remote call.
- PR checks pass on Ubuntu, macOS, Windows, dependency review, and CodeQL.
- Automatic production deployment remains noninteractive; production root stays 200 and federation outbound remains disabled with no delivery jobs or identities created for existing accounts.

## Rollback or Recovery

- Immediate operational rollback is `APP_FEDERATION_OUTBOUND_ENABLED=false`; the conditional scheduler/client beans stop remote calls while retaining jobs for inspection.
- Application rollback uses the existing immutable Windows release rollback. New nullable post fields and queue collections are backward-compatible and ignored by the prior release.
- Do not delete delivery jobs during incident response. Preserve them as bounded evidence; fix configuration/code and resume or explicitly mark dead through a later reviewed operation.
- A failed candidate never replaces production because automatic deployment validates on the alternate port before switching.

## Risks

- SSRF/DNS rebinding: only operator-configured peers, validate all answers, pin the exact connection address, preserve SNI/hostname verification, and never redirect.
- Duplicate remote delivery after crash: stable activity IDs and unique local job keys; test retry-after-acceptance behavior.
- Accidental historical blast: persist false-by-default eligibility at post creation; scanner never infers eligibility from current flags alone.
- Secret exposure: signer owns decrypt/use/clear; jobs/logs store no body, signature, key, peer response body, or raw exception chain.
- Remote overload: single bounded batch, no client implicit retry, exponential backoff, Retry-After cap, max attempts, and kill switch.
- Incomplete lifecycle: this gate is controlled-peer Create only and cannot be broadly activated until Update/Delete propagation is implemented and proven.
- Cross-platform TLS/network behavior: run platform CI and an independent signature verifier; avoid OS-specific socket assumptions.

## Completion Criteria

- Tasks 1-4 are implemented with tests-first evidence and task commits pushed.
- Full local check and controlled-peer runtime report pass with complete cleanup.
- One green PR merges; automatic deployment completes; production remains healthy and outbound-disabled.
- Builder test report, plan status, program status, closure, and session memory are committed/pushed.
- No production peer receives traffic and no existing production account/post is marked or queued for outbound delivery.
