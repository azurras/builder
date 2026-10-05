# ChristopherBell.dev ActivityPub Production Discovery Activation Plan

## Document Status

complete

## Objective

Enable production read-only ActivityPub discovery with one stable protected secret and mandatory deployment smoke proof, while inbound and outbound stay disabled.

## Goals

- Atomically create or reuse a 32-byte production federation secret.
- Default only production discovery on.
- Require both NodeInfo routes during candidate and public deployment checks.
- Merge one PR and verify automatic production deployment.

## Inputs

The approved activation spec, spoke `origin/main` at `6c1501070ff518bc040583c4576c2df201dcd3ed`, the protected SYSTEM/Administrators production config directory, and the user's authorization to continue without routine approvals.

## Branch

`codex/activitypub-production-activation` from `origin/main`, in `A:\Projects\christopherbell.dev-worktrees\activitypub-production-activation`.

## Non-Goals

No inbound mutations, outbound activation, arbitrary peer, historical federation, manual UAC step, external secret service, or consent change.

## Assumptions

Production candidate and service processes run as SYSTEM. Spring initializers execute before configuration-properties binding. The protected config parent exists and must not be created by the application.

## Open Questions

None.

## Task Breakdown

### Task 1 - Create the stable secret and activate discovery

Sequence / dependencies:
- First; discovery cannot bind safely without the key.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Invoke `superpowers:test-driven-development` and witness focused RED failures first.
- Before-Edit Brief:
  - Behavior: prod plus discovery creates/reuses a secret and injects its base64 value; explicit override wins; disabled/non-prod performs no file I/O.
  - Invariants: never replace/truncate; accept only a real regular 32-byte file; never expose bytes; inbound/outbound false.
  - Boundary/API: Spring initializer supplies the existing federation secret placeholder before `FederationProperties` binds.
  - Effects and failures: secure randomness and atomic file I/O; missing parent, symbolic/non-regular/wrong-size/inaccessible storage fails startup with redacted context.
  - Tests and evidence: RED is missing initializer behavior and old false discovery default; GREEN is focused initializer and YAML coverage.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/configuration/FederationSecretApplicationContextInitializerTest.java`
- Lines: 1
- Action: add

Proposed:
```java
class FederationSecretApplicationContextInitializerTest {
  @Test void enabledProdCreatesAndReusesOneThirtyTwoByteSecret() { }
  @Test void explicitOverrideAndDisabledContextsDoNotTouchDisk() { }
  @Test void unsafeOrMalformedStorageFailsClosedWithoutLeakingBytes() { }
}
```

Verification:
- Focused Gradle test fails before implementation and passes afterward.

#### Code Edit 1.2
- File: `website/src/main/java/dev/christopherbell/configuration/FederationSecretApplicationContextInitializer.java`
- Lines: 1
- Action: add

Proposed:
```java
public final class FederationSecretApplicationContextInitializer
    implements ApplicationContextInitializer<ConfigurableApplicationContext>, Ordered {
  @Override public void initialize(ConfigurableApplicationContext context) {
    // prod + discovery + no override only; require existing real parent;
    // read valid existing bytes or CREATE_NEW SecureRandom bytes atomically;
    // recover a concurrent-create winner and inject one redacted property.
  }
}
```

Verification:
- Focused initializer tests pass and error messages contain no secret values.

#### Code Edit 1.3
- File: `website/src/main/resources/META-INF/spring.factories`
- Lines: 1-2
- Action: replace

Current:
```properties
org.springframework.context.ApplicationContextInitializer=\
dev.christopherbell.configuration.ProductionSettingsApplicationContextInitializer
```

Proposed:
```properties
org.springframework.context.ApplicationContextInitializer=\
dev.christopherbell.configuration.FederationSecretApplicationContextInitializer,\
dev.christopherbell.configuration.ProductionSettingsApplicationContextInitializer
```

Verification:
- Production-profile context binding receives the injected secret.

#### Code Edit 1.4
- File: `website/src/main/resources/application-prod.yml`
- Lines: 29-39
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
    outbound:
      not-before: ${APP_FEDERATION_OUTBOUND_NOT_BEFORE:}
      peers: []
      development-loopback-enabled: false
```

Proposed:
```yaml
  federation:
    discovery-enabled: ${APP_FEDERATION_DISCOVERY_ENABLED:true}
    inbound-enabled: ${APP_FEDERATION_INBOUND_ENABLED:false}
    outbound-enabled: ${APP_FEDERATION_OUTBOUND_ENABLED:false}
    software-name: christopherbell.dev
    software-version: ${GIT_COMMIT:unknown}
    key-encryption-secret: ${APP_FEDERATION_KEY_ENCRYPTION_SECRET:}
    key-encryption-secret-file: ${APP_FEDERATION_KEY_ENCRYPTION_SECRET_FILE:C:/ProgramData/christopherbell.dev/config/federation-key-encryption-secret.bin}
    outbound:
      not-before: ${APP_FEDERATION_OUTBOUND_NOT_BEFORE:}
      peers: []
      development-loopback-enabled: false
```

Verification:
- Updated `PublicDeliveryConfigurationTest` proves discovery true, inbound/outbound false, protected path, empty peers, and loopback false.

### Task 2 - Gate deployment on NodeInfo and finish delivery

Sequence / dependencies:
- After Task 1, because these endpoints must be live before becoming gates.

Implementation notes:
- Required skill: `write-chris-street-style-code` before any code edits.
- Update Pester expected paths/counts first and witness RED before production edit.
- Before-Edit Brief:
  - Behavior: candidate/local production and both public hosts must return 200 for both NodeInfo routes.
  - Invariants: preserve existing routes/timeouts; no consented username assumption; existing rollback owns failures.
  - Boundary/API: `$script:ProductionSmokePaths` feeds local/public verifiers.
  - Effects and failures: two bounded GETs per host; timeout/non-200 aborts candidate or triggers rollback.
  - Tests and evidence: RED is 11-vs-9 and 22-vs-18 Pester failure; GREEN is Pester, full check, alternate-port runtime, CI, and production.

#### Code Edit 2.1
- File: `ops/production/windows/tests/Production.Deploy.Tests.ps1`
- Lines: 215-260
- Action: replace

Current:
```powershell
$expectedPaths = @(
    '/', '/blog', '/wfl', '/canes-box-tracker', '/robots.txt', '/sitemap.xml',
    '/favicon.ico', '/actuator/health/liveness', '/actuator/health/readiness'
)
# Public matrix expects 18 checks.
```

Proposed:
```powershell
$expectedPaths = @(
    '/', '/blog', '/wfl', '/canes-box-tracker', '/robots.txt', '/sitemap.xml',
    '/favicon.ico', '/actuator/health/liveness', '/actuator/health/readiness',
    '/.well-known/nodeinfo', '/nodeinfo/2.1'
)
# Preserve host/status/timeout assertions and expect 22 checks.
```

Verification:
- Pester 5.9.0 fails before and passes after the production edit.

#### Code Edit 2.2
- File: `ops/production/windows/modules/Production.Deploy.psm1`
- Lines: 3-13
- Action: replace

Current:
```powershell
$script:ProductionSmokePaths = @(
    '/', '/blog', '/wfl', '/canes-box-tracker', '/robots.txt', '/sitemap.xml',
    '/favicon.ico', '/actuator/health/liveness', '/actuator/health/readiness'
)
```

Proposed:
```powershell
$script:ProductionSmokePaths = @(
    '/', '/blog', '/wfl', '/canes-box-tracker', '/robots.txt', '/sitemap.xml',
    '/favicon.ico', '/actuator/health/liveness', '/actuator/health/readiness',
    '/.well-known/nodeinfo', '/nodeinfo/2.1'
)
```

Verification:
- Pester 5.9.0 deployment suite passes.

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/federation/README.md`
- Lines: 3-20
- Action: replace

Current:
```text
Discovery, inbound, and outbound switches default to off. Production keeps outbound disabled and peers empty.
```

Proposed:
```text
Production enables read-only discovery with a dedicated protected persistent key. Inbound and outbound remain independently disabled and peerless. The discovery environment switch is the immediate kill switch.
```

Verification:
- Documentation matches tested defaults and contains no secret.

#### Code Edit 2.4
- File: `docs/operations/windows-production.md`
- Lines: after 302
- Action: add

Proposed:
```text
ActivityPub discovery operations: production creates/reuses the protected 32-byte key; never print, replace, or delete it. APP_FEDERATION_DISCOVERY_ENABLED=false is the emergency kill switch. Inbound/outbound remain false. Verify both NodeInfo routes locally and publicly.
```

Verification:
- Runbook names persistence, kill switch, loss consequence, and checks without exposing a value.

## Code Changes

Add/register/test the initializer; activate only discovery; add/test NodeInfo deployment gates; document operations and rollback.

## Files and Modules

Website configuration/federation files and tests, Windows deployment module/tests, and Windows operations documentation listed above.

## Unit Testing

Initializer create/reuse/override/no-op/fail-closed; production YAML safety; Pester path and host-matrix counts.

## Local Testing

Use isolated Gradle state. Run focused tests, Pester 5.9.0, full `:website:check`, and a non-8080 `prod,deploy-smoke` runtime with isolated Mongo and secret-file path. Verify NodeInfo 200, foreign WebFinger 404, inbox POST denied, no outbound jobs/requests, and unchanged secret hash after restart.

## Validation

One PR; focused/full/CI/CodeQL green; automatic deploy; root and NodeInfo healthy locally/publicly; inbound/outbound no effects.

## Rollback or Recovery

Set protected discovery switch false and restart; use existing atomic release rollback; preserve the key. If lost, keep discovery disabled and restore from secured host backup before serving existing actors.

## Risks

Missing/malformed storage blocks startup, discovery increases bounded visibility, NodeInfo adds bounded deployment checks, and no real peer leaves outbound off. Candidate checks, consent filtering, timeouts, rollback, and fail-closed defaults mitigate these risks.

## Completion Criteria

One PR merged and deployed without prompts; tests and runtime proof pass; production root/NodeInfo return 200; inbound/outbound inactive; Builder evidence is committed and pushed.
