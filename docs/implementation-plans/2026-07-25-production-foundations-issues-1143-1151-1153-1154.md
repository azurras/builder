# Production Foundations Issues 1143, 1151, 1153, and 1154 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` inline. Do not dispatch subagents.

**Goal:** Finish the remaining production/configuration foundations by making production settings fail fast, providing a reproducible local MongoDB service, and adding a versioned leased Mongo migration runner.

**Architecture:** A registered `ApplicationContextInitializer` validates the fully prepared production environment before Spring refreshes Mongo, mail, or web beans and emits one redacted configuration report. Mail delivery binds through an explicit typed switch. Local MongoDB uses the official pinned `mongo:8.3.2` image, a named volume, loopback-only port publishing, and a health check. A repository-native migration runner stores immutable migration identity/checksum/status records, serializes execution through an atomic Mongo lease, rejects incomplete or mutated migrations, and ships an idempotent infrastructure-index migration.

**Tech Stack:** Java 25, Spring Boot 4.1, Spring Data MongoDB, MongoDB 8.3.2, Docker Compose specification, PowerShell 7/Pester, Gradle, JUnit 5, Mockito, AssertJ.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\production-foundations-1143-1154` on `codex/production-foundations-1143-1154`.
- Preserve the dirty authoritative checkout and never stage the checkout-only CRLF difference in `gradlew.bat`.
- Production configuration errors must list setting names without printing secret values, URIs with credentials, or mail credentials.
- `SPRING_MONGODB_URI` must be explicitly supplied for `prod`; a value may point to the native loopback service, but no production fallback may do so.
- Mail defaults to disabled outside production. Production defaults the explicit switch to enabled; setting `APP_MAIL_ENABLED=false` intentionally makes Resend and sender settings optional.
- Migrations are append-only, ordered, idempotent, and fail closed on checksum drift or incomplete state. Rollback never silently reverses data.
- Use a dedicated temporary Mongo database for runtime acceptance. Never run new migration tests against the production `christopherbell` database.
- Verify the application on a non-8080 port. Production port `8080` and the live Windows service remain untouched before merge.
- Only comments by `azurras` may change scope; issues #1143, #1151, #1153, and #1154 have no comments or attachments.

---

## Document Status

complete

## Objective

Complete `azurras/christopherbell.dev#1143`, `#1151`, `#1153`, and `#1154` in one production-foundations PR with witnessed RED/GREEN evidence, safe temporary-database acceptance, CI, merge, production verification, and closure.

## Goals

- Remove the hard-coded production Mongo URI and require `SPRING_MONGODB_URI`.
- Produce one early, clear, redacted production configuration report covering Mongo, JWT, and explicitly enabled mail.
- Make mail enablement intentional and testable instead of depending on blank auto-configuration.
- Add a pinned loopback-only local Mongo Compose service with persistence, health, and reset documentation.
- Add a durable versioned migration state machine and atomic lease that future index/data migrations can reuse.
- Document migration authoring, interruption recovery, backup, and rollback boundaries.

## Inputs

- Approved campaign spec: `docs/specs/2026-07-25-complete-all-open-christopherbell-dev-issues.md`, remaining Batch 1 foundations.
- Issues: <https://github.com/azurras/christopherbell.dev/issues/1143>, <https://github.com/azurras/christopherbell.dev/issues/1151>, <https://github.com/azurras/christopherbell.dev/issues/1153>, and <https://github.com/azurras/christopherbell.dev/issues/1154>.
- Base: `origin/main` at `4b82116a0ed489c74eed144a478f1b3a3944ada2`.
- Baseline: 1,002 of 1,003 Java tests passed on the first clean run; unrelated `CommandCenterMetricsServiceTest.timedOutInterruptIgnoringProviderIsNotResubmittedUntilItsInvocationCompletes` missed a timing handoff once, then its complete 12-test class passed on immediate isolated rerun. Record this as a pre-edit characterization, not a batch regression.
- Runtime MongoDB: native server `8.3.2`; official `mongo:8.3.2` image tag verified on Docker Hub.

## Branch

- `codex/production-foundations-1143-1154` from `origin/main`
- `A:\Projects\christopherbell.dev-worktrees\production-foundations-1143-1154`

## Non-Goals

- Migrating or replacing the native production MongoDB service.
- Adding production database authentication, Atlas, replica sets, or Kubernetes.
- Rewriting existing feature repositories or converting every current annotation index in this batch.
- Automatically retrying an incomplete migration without operator review.
- Implementing later account, notification, report, WFL, VIN, or scheduler migrations.

## Assumptions

- The production `app.env` already supplies real values; configuration-key additions preserve existing secrets and require only the explicit mail switch default.
- Spring's config data has loaded before registered application-context initializers run.
- Mongo `findAndModify` with a fixed `_id`, owner token, and expiry is the atomic lease boundary.
- The first migration owns only migration infrastructure indexes; future feature migrations append new immutable IDs.
- Docker is optional on this host because native MongoDB is installed, so the Compose contract is always tested structurally and `docker compose config` runs when the CLI is available.

## Open Questions

None. The campaign spec already prefers a repository-native migration/lease implementation unless compatibility evidence favors a maintained library. Current Spring Boot 4.1 code already uses `MongoTemplate` and an atomic fixed-key lease pattern, so the repository-native option is the smaller and more reusable boundary.

## Task Breakdown

### Task 1 - Add RED contracts for production settings, Compose, mail, lease, and migration behavior

Sequence / dependencies:
- First task. Do not edit production code/configuration before capturing the focused failures.

Implementation notes:
- Required skill: `chris-street-style` before test or production edits.
- Before-Edit Brief:
  - Behavior: production settings aggregate failures, mail disablement is explicit, Compose is bounded, leases serialize, and migrations persist/skip/fail closed.
  - Invariants: no secret values in errors; no live database mutation; applied IDs/checksums are immutable; incomplete records block startup.
  - Boundary/API: `SPRING_MONGODB_URI`, `APP_JWT_SECRET`, `APP_MAIL_ENABLED`, `APP_MAIL_FROM`, `RESEND_API_KEY`, `application_migrations`, and `application_leases` are named contracts.
  - Effects and failures: configuration failure precedes context refresh; migration failure records safe state and releases ownership; contention never executes a migration twice.
  - Tests and evidence: focused JUnit and Pester commands below must fail for missing classes/configuration, not harness errors.

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/configuration/MongoProfileConfigurationTest.java`
- Lines: 15-25
- Action: replace

Current:
```java
@ParameterizedTest
@ValueSource(strings = {"application-local.yml", "application-prod.yml"})
void profileUsesSpringBootFourMongoConnectionProperties(String resourceName) throws IOException {
  var source = load(resourceName);
  assertThat(source.getProperty("spring.mongodb.database")).isEqualTo("christopherbell");
  assertThat(source.getProperty("spring.mongodb.uri")).isEqualTo("mongodb://localhost:27017");
  assertThat(source.getProperty("spring.data.mongodb.auto-index-creation")).isEqualTo(true);
}
```

Proposed:
```java
@Test
void localProfileKeepsLoopbackMongoDefault() throws IOException {
  assertThat(load("application-local.yml").getProperty("spring.mongodb.uri"))
      .isEqualTo("mongodb://localhost:27017");
}

@Test
void productionProfileRequiresEnvironmentMongoUriAndExplicitMailSwitch() throws IOException {
  var source = load("application-prod.yml");
  assertThat(source.getProperty("spring.mongodb.uri")).isEqualTo("${SPRING_MONGODB_URI:}");
  assertThat(source.getProperty("app.mail.enabled")).isEqualTo("${APP_MAIL_ENABLED:true}");
  assertThat(source.getProperty("spring.mail.password")).isEqualTo("${RESEND_API_KEY:}");
}
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.MongoProfileConfigurationTest`
- Expected RED: production still hard-codes `mongodb://localhost:27017` and has no explicit mail switch.

#### Code Edit 1.2
- File: `website/src/test/java/dev/christopherbell/configuration/ProductionSettingsApplicationContextInitializerTest.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
class ProductionSettingsApplicationContextInitializerTest {
  @Test
  void productionAggregatesMissingSettingsWithoutLeakingValues() {
    var context = context("prod", Map.of(
        "APP_JWT_SECRET", "short-secret-value",
        "APP_MAIL_ENABLED", "true"));

    assertThatThrownBy(() -> new ProductionSettingsApplicationContextInitializer()
        .initialize(context))
        .hasMessageContaining("Invalid production configuration")
        .hasMessageContaining("SPRING_MONGODB_URI", "APP_JWT_SECRET",
            "APP_MAIL_FROM", "RESEND_API_KEY")
        .hasMessageNotContaining("short-secret-value");
  }

  @Test
  void explicitMailDisableMakesMailCredentialsOptional() {
    var context = validProductionContext(Map.of("APP_MAIL_ENABLED", "false"));
    assertThatCode(() -> initializer().initialize(context)).doesNotThrowAnyException();
  }

  @Test
  void nonProductionProfilesAreNotSubjectToProductionRequirements() {
    assertThatCode(() -> initializer().initialize(context("local", Map.of())))
        .doesNotThrowAnyException();
  }
}
```

Verification:
- Expected RED: initializer does not exist.

#### Code Edit 1.3
- File: `website/src/test/java/dev/christopherbell/account/PasswordResetNotificationServiceTest.java`
- Lines: 23-63
- Action: replace

Current:
```java
var service = new PasswordResetNotificationService(mailSenderProvider);
```

Proposed:
```java
@Test
void disabledMailDoesNotResolveOrInvokeSender(CapturedOutput output) {
  var service = new PasswordResetNotificationService(
      mailSenderProvider, new MailProperties(false, "noreply@example.com"));

  service.sendPasswordReset(account(), "https://example.com/reset?token=secret");

  verifyNoInteractions(mailSenderProvider, mailSender);
  assertThat(output).contains("disabled").doesNotContain("token=secret");
}

@Test
void enabledMailUsesConfiguredSender() {
  var service = new PasswordResetNotificationService(
      mailSenderProvider, new MailProperties(true, "noreply@example.com"));
  when(mailSenderProvider.getIfAvailable()).thenReturn(mailSender);
  service.sendPasswordReset(account(), "https://example.com/reset?token=secret");
  verify(mailSender).send(messageCaptor.capture());
  assertThat(messageCaptor.getValue().getFrom()).isEqualTo("noreply@example.com");
}
```

Verification:
- Expected RED: no typed mail properties or explicit disable branch exists.

#### Code Edit 1.4
- File: `website/src/test/java/dev/christopherbell/configuration/LocalMongoComposeConfigurationTest.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
class LocalMongoComposeConfigurationTest {
  @Test
  void composePinsMongoPersistsDataAndPublishesOnlyLoopback() throws IOException {
    JsonNode compose = readRepositoryYaml("compose.yaml");
    JsonNode mongo = compose.at("/services/mongodb");
    assertThat(mongo.path("image").asText()).isEqualTo("mongo:8.3.2");
    assertThat(textValues(mongo.path("ports"))).containsExactly("127.0.0.1:27017:27017");
    assertThat(textValues(mongo.path("volumes"))).contains("christopherbell_mongo_data:/data/db");
    assertThat(mongo.at("/healthcheck/test").toString()).contains("db.adminCommand('ping')");
    assertThat(compose.at("/volumes/christopherbell_mongo_data").isObject()).isTrue();
  }
}
```

Verification:
- Expected RED: `compose.yaml` does not exist.

#### Code Edit 1.5
- File: `website/src/test/java/dev/christopherbell/configuration/mongo/lease/MongoLeaseServiceTest.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
class MongoLeaseServiceTest {
  @Test
  void acquireUsesFixedNameOwnerAndExpiredLeaseBoundary() {
    when(mongo.findAndModify(any(), any(), any(), eq(MongoLeaseDocument.class)))
        .thenReturn(lease("application-migrations", "owner-1"));
    assertThat(service.tryAcquire("application-migrations", "owner-1", now, expiresAt)).isTrue();
    assertThat(capturedQuery()).contains("_id", "ownerToken", "expiresAt");
  }

  @Test
  void duplicateKeyContentionReturnsFalseWithoutLeakingDatabaseDetails() {
    when(mongo.findAndModify(any(), any(), any(), eq(MongoLeaseDocument.class)))
        .thenThrow(new DuplicateKeyException("host details"));
    assertThat(service.tryAcquire("application-migrations", "owner-2", now, expiresAt)).isFalse();
  }

  @Test
  void onlyTheCurrentOwnerCanRelease() {
    when(mongo.updateFirst(any(), any(), eq(MongoLeaseDocument.class)))
        .thenReturn(UpdateResult.acknowledged(1, 1L, null));
    assertThat(service.release("application-migrations", "owner-1")).isTrue();
  }
}
```

Verification:
- Expected RED: generic lease classes do not exist.

#### Code Edit 1.6
- File: `website/src/test/java/dev/christopherbell/configuration/mongo/migration/MongoMigrationRunnerTest.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
class MongoMigrationRunnerTest {
  @Test
  void appliesMissingMigrationsInStableIdOrderAndRecordsCompletion() {
    runner(migration("002"), migration("001")).afterPropertiesSet();
    assertThat(executedIds).containsExactly("001", "002");
    verify(state).start("001", CHECKSUM_001, OWNER);
    verify(state).complete(eq("001"), any(Instant.class));
  }

  @Test
  void appliedMigrationWithMatchingChecksumIsSkipped() {
    when(state.find("001")).thenReturn(applied("001", CHECKSUM_001));
    runner(migration("001")).afterPropertiesSet();
    assertThat(executedIds).isEmpty();
  }

  @Test
  void checksumDriftOrIncompleteRecordFailsStartup() {
    when(state.find("001")).thenReturn(applied("001", "old-checksum"));
    assertThatThrownBy(() -> runner(migration("001")).afterPropertiesSet())
        .hasMessageContaining("001", "checksum");
    when(state.find("001")).thenReturn(running("001"));
    assertThatThrownBy(() -> runner(migration("001")).afterPropertiesSet())
        .hasMessageContaining("incomplete");
  }

  @Test
  void migrationFailureRecordsSafeFailureAndReleasesLease() {
    assertThatThrownBy(() -> runner(failingMigration("001")).afterPropertiesSet())
        .hasMessageContaining("001").hasMessageNotContaining("database-secret");
    verify(state).fail(eq("001"), any(Instant.class), eq("MIGRATION_FAILED"));
    verify(leases).release(MigrationProperties.LEASE_NAME, OWNER);
  }
}
```

Verification:
- Expected RED: runner/state abstractions do not exist.

#### Code Edit 1.7
- File: `ops/production/windows/tests/Production.Common.Tests.ps1`
- Lines: 112-142
- Action: replace

Current:
```powershell
$required = @('APP_JWT_SECRET','RESEND_API_KEY','APP_MAIL_FROM','SPRING_MONGODB_URI')
```

Proposed:
```powershell
It 'allows mail credentials to be absent only when mail is explicitly disabled' {
    @('APP_JWT_SECRET=abcdefghijklmnopqrstuvwxyz123456',
      'SPRING_MONGODB_URI=mongodb://127.0.0.1:27017',
      'APP_MAIL_ENABLED=false') | Set-Content $path
    { Read-ProductionEnvironment $path } | Should -Not -Throw
}

It 'requires mail credentials when mail is enabled or omitted' {
    @('APP_JWT_SECRET=abcdefghijklmnopqrstuvwxyz123456',
      'SPRING_MONGODB_URI=mongodb://127.0.0.1:27017',
      'APP_MAIL_ENABLED=true') | Set-Content $path
    { Read-ProductionEnvironment $path } | Should -Throw '*RESEND_API_KEY*APP_MAIL_FROM*'
}
```

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.Common.Tests.ps1`
- Expected RED: `APP_MAIL_ENABLED` is unsupported and mail is always required.

### Task 2 - Implement early production validation and explicit mail configuration

Sequence / dependencies:
- After Task 1 RED evidence.

Implementation notes:
- Required skill: `chris-street-style`; invoke it before production or test edits.
- Before-Edit Brief:
  - Behavior: production startup validates all required settings in one pre-refresh pass and mail delivery follows an explicit switch.
  - Invariants: values remain redacted, non-prod defaults remain usable, production mail remains enabled unless explicitly disabled, and JWT defense in depth remains.
  - Boundary/API: profile selection plus the five named environment variables and `app.mail` typed properties define the interface.
  - Effects and failures: invalid production settings abort before Mongo/mail/web bean creation; disabled mail never resolves or invokes a sender.
  - Tests and evidence: initializer profile/validation partitions, password-reset mail partitions, Pester environment parsing, and packaged startup failure prove the boundary.
- Register the initializer through `META-INF/spring.factories` so packaged `SpringApplication.run` and tests share the same startup gate.
- Read names only in the report; never interpolate values.
- Validate: nonblank explicit Mongo URI, JWT at least 32 UTF-8 bytes and not the known development/example secret, Boolean mail switch, and when enabled a non-placeholder sender plus Resend key.
- Keep `PermissionService` key-length validation as defense in depth.

#### Code Edit 2.1
- File: `website/src/main/resources/application-prod.yml`
- Lines: 4-30
- Action: replace

Current:
```yaml
spring:
  mongodb:
    database: christopherbell
    uri: mongodb://localhost:27017
  mail:
    password: ${RESEND_API_KEY}
app:
  jwt:
    secret: ${APP_JWT_SECRET:}
  mail:
    from: ${APP_MAIL_FROM:noreply@christopherbell.dev}
```

Proposed:
```yaml
spring:
  mongodb:
    database: ${SPRING_MONGODB_DATABASE:christopherbell}
    uri: ${SPRING_MONGODB_URI:}
  mail:
    host: smtp.resend.com
    port: 587
    username: resend
    password: ${RESEND_API_KEY:}
app:
  jwt:
    secret: ${APP_JWT_SECRET:}
  mail:
    enabled: ${APP_MAIL_ENABLED:true}
    from: ${APP_MAIL_FROM:}
  migrations:
    lease-duration: 2m
```

Verification:
- Focused Mongo/profile and initializer tests pass.

#### Code Edit 2.2
- File: `website/src/main/resources/application.yml`
- Lines: 65-72
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
  jwt:
    secret: ${APP_JWT_SECRET:local-development-jwt-secret-change-me-at-least-32-bytes}
  mail:
    enabled: ${APP_MAIL_ENABLED:false}
    from: ${APP_MAIL_FROM:noreply@christopherbell.dev}
  migrations:
    lease-duration: 2m
```

Verification:
- Bind the default configuration and assert mail is disabled and the bounded migration lease duration is present.

#### Code Edit 2.3
- File: `website/src/main/java/dev/christopherbell/configuration/mail/MailProperties.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
@ConfigurationProperties("app.mail")
public record MailProperties(boolean enabled, String from) {
  public MailProperties {
    from = from == null ? "" : from.trim();
  }
}
```

Verification:
- `PasswordResetNotificationServiceTest` compiles with the typed record and covers enabled/disabled partitions.

#### Code Edit 2.4
- File: `website/src/main/java/dev/christopherbell/configuration/mail/MailConfiguration.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
@Configuration(proxyBeanMethods = false)
@EnableConfigurationProperties(MailProperties.class)
public class MailConfiguration {}
```

Verification:
- A focused context runner binds exactly one `MailProperties` bean without loading MongoDB.

#### Code Edit 2.5
- File: `website/src/main/java/dev/christopherbell/account/passwordreset/PasswordResetNotificationService.java`
- Lines: 16-49
- Action: replace

Current:
```java
private final ObjectProvider<JavaMailSender> mailSenderProvider;

@Value("${app.mail.from:noreply@christopherbell.dev}")
private String fromAddress;
```

Proposed:
```java
private final ObjectProvider<JavaMailSender> mailSenderProvider;
private final MailProperties mailProperties;

public void sendPasswordReset(Account account, String resetUrl) {
  if (!mailProperties.enabled()) {
    log.info("Password reset email for account {} was not sent because mail is disabled.",
        account.getId());
    return;
  }
  JavaMailSender mailSender = mailSenderProvider.getIfAvailable();
  if (mailSender == null) {
    log.error("Password reset email for account {} was not sent because mail is unavailable.",
        account.getId());
    return;
  }
  SimpleMailMessage message = passwordResetMessage(account, resetUrl, mailProperties.from());
  // Existing bounded send/error handling remains.
}
```

Verification:
- Focused password-reset notification tests prove disabled no-op, configured sender, unavailable sender, and redacted send failure.

#### Code Edit 2.6
- File: `website/src/main/java/dev/christopherbell/configuration/ProductionSettingsApplicationContextInitializer.java`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```java
public final class ProductionSettingsApplicationContextInitializer
    implements ApplicationContextInitializer<ConfigurableApplicationContext> {
  private static final String DEVELOPMENT_JWT_SECRET =
      "local-development-jwt-secret-change-me-at-least-32-bytes";

  @Override
  public void initialize(ConfigurableApplicationContext context) {
    Environment environment = context.getEnvironment();
    if (!environment.acceptsProfiles(Profiles.of("prod"))) {
      return;
    }
    List<String> errors = new ArrayList<>();
    validateMongoUri(environment.getProperty("SPRING_MONGODB_URI"), errors);
    validateJwt(environment.getProperty("APP_JWT_SECRET"), errors);
    boolean mailEnabled = parseBoolean(environment.getProperty("APP_MAIL_ENABLED", "true"),
        "APP_MAIL_ENABLED", errors);
    if (mailEnabled) {
      validateMailFrom(environment.getProperty("APP_MAIL_FROM"), errors);
      requireNonPlaceholder(environment, "RESEND_API_KEY", errors);
    }
    if (!errors.isEmpty()) {
      throw new ApplicationContextException(
          "Invalid production configuration:\n- " + String.join("\n- ", errors));
    }
  }
}
```

Verification:
- Focused initializer tests cover prod/non-prod, aggregate errors, malformed/credential-bearing Mongo URI redaction, weak JWT, invalid sender email, mail disabled, and redaction.

#### Code Edit 2.7
- File: `website/src/main/resources/META-INF/spring.factories`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```properties
org.springframework.context.ApplicationContextInitializer=\
dev.christopherbell.configuration.ProductionSettingsApplicationContextInitializer
```

Verification:
- Inspect the processed boot JAR resources and run the packaged missing-settings startup probe.

#### Code Edit 2.8
- File: `ops/production/windows/config/app.env.example`
- Lines: 1-5
- Action: replace

Current:
```text
APP_JWT_SECRET=replace-with-at-least-32-random-characters
RESEND_API_KEY=re_your_resend_api_key
APP_MAIL_FROM=noreply@your-verified-domain.com
SPRING_MONGODB_URI=mongodb://127.0.0.1:27017
```

Proposed:
```text
APP_JWT_SECRET=replace-with-at-least-32-random-characters
SPRING_MONGODB_URI=mongodb://127.0.0.1:27017
APP_MAIL_ENABLED=true
RESEND_API_KEY=re_your_resend_api_key
APP_MAIL_FROM=noreply@your-verified-domain.com
APP_SHARED_FOLDER_ENABLED=false
```

Verification:
- Pester parses the example-key set and rejects example placeholders without echoing values.

#### Code Edit 2.9
- File: `ops/production/windows/service/Start-ChristopherBellDev.ps1`
- Lines: 13-27
- Action: replace

Current:
```powershell
$allowed = @('APP_JWT_SECRET','RESEND_API_KEY','APP_MAIL_FROM',
    'SPRING_MONGODB_URI','APP_SHARED_FOLDER_ENABLED')
```

Proposed:
```powershell
$allowed = @('APP_JWT_SECRET','SPRING_MONGODB_URI','APP_MAIL_ENABLED',
    'RESEND_API_KEY','APP_MAIL_FROM','APP_SHARED_FOLDER_ENABLED')
$booleanKeys = @('APP_MAIL_ENABLED','APP_SHARED_FOLDER_ENABLED')
# Reject non-Boolean values before setting the process environment.
```

Verification:
- Production command tests prove the launcher allowlists and validates `APP_MAIL_ENABLED`.

#### Code Edit 2.10
- File: `ops/production/windows/modules/Production.Common.psm1`
- Lines: 384-413
- Action: replace

Current:
```powershell
$required = @('APP_JWT_SECRET','RESEND_API_KEY','APP_MAIL_FROM','SPRING_MONGODB_URI')
$optional = @('APP_SHARED_FOLDER_ENABLED')
```

Proposed:
```powershell
$alwaysRequired = @('APP_JWT_SECRET','SPRING_MONGODB_URI')
$optional = @('APP_MAIL_ENABLED','RESEND_API_KEY','APP_MAIL_FROM','APP_SHARED_FOLDER_ENABLED')
# Default APP_MAIL_ENABLED to true when omitted for compatibility.
# Aggregate missing/invalid key names into one redacted error.
# Require RESEND_API_KEY and APP_MAIL_FROM only when mail is true.
```

Verification:
- Focused JUnit and Pester tests pass.
- Inspect thrown messages to prove no test secret or URI value appears.

### Task 3 - Add the pinned local MongoDB Compose contract and contributor documentation

Sequence / dependencies:
- May follow Task 1 independently; complete before runtime acceptance.

Implementation notes:
- Required skill: `chris-street-style`; invoke it before editing executable Compose configuration or copy-ready commands.
- Before-Edit Brief:
  - Behavior: one command starts a persistent healthy local MongoDB matching the host's server version.
  - Invariants: port publishing is loopback-only, no production secret is embedded, stop preserves data, and reset names its destructive scope.
  - Boundary/API: Compose service `mongodb`, port 27017, named volume, health check, and contributor commands are stable.
  - Effects and failures: unhealthy Mongo remains visible through Compose health; reset removes only the project named volume.
  - Tests and evidence: YAML structural assertions and optional `docker compose config` validate the contract.

#### Code Edit 3.1
- File: `compose.yaml`
- Lines: before 1
- Action: add

Current:
```text
File does not exist.
```

Proposed:
```yaml
services:
  mongodb:
    image: mongo:8.3.2
    restart: unless-stopped
    ports:
      - "127.0.0.1:27017:27017"
    volumes:
      - christopherbell_mongo_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--quiet", "--eval", "quit(db.adminCommand('ping').ok ? 0 : 1)"]
      interval: 5s
      timeout: 5s
      retries: 12
      start_period: 10s
    stop_grace_period: 30s

volumes:
  christopherbell_mongo_data: {}
```

Verification:
- `LocalMongoComposeConfigurationTest` proves image, port, volume, and health-check values.

#### Code Edit 3.2
- File: `.env.example`
- Lines: 1-6
- Action: replace

Current:
```text
RESEND_API_KEY=re_your_resend_api_key
APP_MAIL_FROM=noreply@your-verified-domain.com
APP_JWT_SECRET=replace-with-at-least-32-random-characters
```

Verification:
- Static review proves local defaults contain no real credential and mail is explicitly disabled.

Proposed:
```text
SPRING_MONGODB_URI=mongodb://localhost:27017
APP_MAIL_ENABLED=false
# Add RESEND_API_KEY and APP_MAIL_FROM only when testing mail locally.
APP_JWT_SECRET=replace-with-at-least-32-random-characters
```

#### Code Edit 3.3
- File: `README.md`
- Lines: 68-125
- Action: replace

Current:
```markdown
Requirements:

- MongoDB

Run Locally:

Start MongoDB first. Then run commands from the repository root:
`./gradlew :website:bootRun`
```

Proposed:
```markdown
### Local MongoDB with Docker Compose

`docker compose up -d mongodb` starts the pinned MongoDB 8.3.2 service on
`mongodb://localhost:27017`. `docker compose ps` must report it healthy.
`docker compose stop mongodb` preserves the named volume.

Reset is destructive to local Compose data only:
`docker compose down --volumes`. Confirm the project and volume names first.

Database shape changes must be appended through the versioned migration runner;
never edit an applied migration ID or checksum. See the migration runbook.
```

Verification:
- Structural Compose test passes.
- If `docker` is available: `docker compose config` succeeds.

### Task 4 - Implement reusable Mongo leases and the versioned migration state machine

Sequence / dependencies:
- After Task 1 RED evidence and Task 2 configuration defaults.

Implementation notes:
- Required skill: `chris-street-style`; invoke it before migration/lease source or tests.
- Before-Edit Brief:
  - Behavior: one owner applies each immutable migration once, records durable state, and safely skips an identical applied migration.
  - Invariants: fixed bounded IDs, checksum immutability, atomic owner/expiry lease, applied-only skip, and release in `finally`.
  - Boundary/API: `ApplicationMigration`, migration properties, `application_migrations`, and `application_leases` are the reusable interface.
  - Effects and failures: lease contention fails startup without executing work; incomplete/checksum-drift/failure abort startup and preserve a safe durable category.
  - Tests and evidence: mocked atomic query/update tests plus a real disposable-database first-run/restart prove semantics.
- Use fixed collection names `application_leases` and `application_migrations`.
- Store `_id` as lease name or migration ID; never rely on unbounded generated IDs.
- Migration status is `RUNNING`, `APPLIED`, or `FAILED` with bounded timestamps, checksum, description, owner token, and safe failure category.
- A matching `APPLIED` record skips execution; checksum drift and any non-applied record fail startup.
- A failure is recorded as `FAILED`, the lease is released in `finally`, and the thrown message names only the migration ID/category.
- V001 creates only idempotent infrastructure indexes, avoiding broad production collection churn.

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/lease/MongoLeaseDocument.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Data
@NoArgsConstructor
@Document(MongoLeaseService.COLLECTION)
final class MongoLeaseDocument {
  @Id private String id;
  private String ownerToken;
  private Instant acquiredAt;
  private Instant expiresAt;
}
```

Verification:
- Compile plus lease tests prove the fixed collection and bounded fields.

#### Code Edit 4.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/lease/MongoLeaseService.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Repository
public final class MongoLeaseService {
  public static final String COLLECTION = "application_leases";

  public boolean tryAcquire(String name, String ownerToken, Instant now, Instant expiresAt) {
    Query query = Query.query(Criteria.where("_id").is(name).orOperator(
        Criteria.where("ownerToken").is(ownerToken), Criteria.where("expiresAt").lte(now)));
    Update update = new Update().set("ownerToken", ownerToken)
        .set("acquiredAt", now).set("expiresAt", expiresAt);
    try {
      MongoLeaseDocument lease = mongo.findAndModify(query, update,
          FindAndModifyOptions.options().upsert(true).returnNew(true), MongoLeaseDocument.class);
      return lease != null && ownerToken.equals(lease.getOwnerToken());
    } catch (DuplicateKeyException contention) {
      return false;
    }
  }

  public boolean release(String name, String ownerToken) {
    // Match both fixed name and owner; unset ownership and expire immediately.
  }
}
```

Verification:
- Focused lease tests cover acquire, expired takeover, contention, renewal, and owner-only release.

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/ApplicationMigration.java`
- Lines: before 1
- Action: add

Proposed:
```java
public interface ApplicationMigration {
  String id();
  String checksum();
  String description();
  void apply(MongoTemplate mongoTemplate);
}
```

Verification:
- Runner tests compile synthetic success/failure migrations against the interface.

#### Code Edit 4.4
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/MigrationProperties.java`
- Lines: before 1
- Action: add

Proposed:
```java
@ConfigurationProperties("app.migrations")
@Validated
public record MigrationProperties(
    @NotNull @DurationMin(seconds = 30) Duration leaseDuration) {
  public static final String LEASE_NAME = "application-migrations";
}
```

Verification:
- Properties binding tests reject short/zero durations and accept repository defaults.

#### Code Edit 4.5
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/MigrationStatus.java`
- Lines: before 1
- Action: add

Proposed:
```java
enum MigrationStatus {
  RUNNING,
  APPLIED,
  FAILED
}
```

Verification:
- State-store/runner tests cover every status transition and reject non-`APPLIED` startup state.

#### Code Edit 4.6
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/MigrationRecord.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Data
@NoArgsConstructor
@Document(MigrationRecord.COLLECTION)
final class MigrationRecord {
  static final String COLLECTION = "application_migrations";
  @Id private String id;
  private String checksum;
  private String description;
  private MigrationStatus status;
  private String ownerToken;
  private Instant startedAt;
  private Instant completedAt;
  private String failureCategory;

  static MigrationRecord running(
      ApplicationMigration migration, String ownerToken, Instant startedAt) {
    MigrationRecord record = new MigrationRecord();
    record.id = migration.id();
    record.checksum = migration.checksum();
    record.description = migration.description();
    record.status = MigrationStatus.RUNNING;
    record.ownerToken = ownerToken;
    record.startedAt = startedAt;
    return record;
  }
}
```

Verification:
- Serialization test proves bounded fields and fixed `_id` migration identity.

#### Code Edit 4.7
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/MigrationStateStore.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Repository
final class MigrationStateStore {
  Optional<MigrationRecord> find(String id) {
    return Optional.ofNullable(mongo.findById(id, MigrationRecord.class));
  }

  void start(ApplicationMigration migration, String owner, Instant now) {
    mongo.insert(MigrationRecord.running(migration, owner, now));
  }

  void complete(String id, String owner, Instant now) {
    Update update = new Update().set("status", MigrationStatus.APPLIED)
        .set("completedAt", now).unset("failureCategory");
    requireMatched(mongo.updateFirst(ownedRunning(id, owner), update, MigrationRecord.class), id);
  }

  void fail(String id, String owner, Instant now, String category) {
    Update update = new Update().set("status", MigrationStatus.FAILED)
        .set("completedAt", now).set("failureCategory", category);
    requireMatched(mongo.updateFirst(ownedRunning(id, owner), update, MigrationRecord.class), id);
  }

  private Query ownedRunning(String id, String owner) {
    return Query.query(Criteria.where("_id").is(id)
        .and("ownerToken").is(owner).and("status").is(MigrationStatus.RUNNING));
  }
}
```

Verification:
- State-store tests require owner plus `RUNNING` status for completion/failure and reject unmatched updates.

#### Code Edit 4.8
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/MongoMigrationRunner.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Component
@EnableConfigurationProperties(MigrationProperties.class)
public final class MongoMigrationRunner implements InitializingBean {
  @Override
  public void afterPropertiesSet() {
    List<ApplicationMigration> ordered = validatedOrder(migrations);
    String owner = UUID.randomUUID().toString();
    if (!leases.tryAcquire(MigrationProperties.LEASE_NAME, owner, clock.instant(),
        clock.instant().plus(properties.leaseDuration()))) {
      throw new IllegalStateException("Required migrations are already running.");
    }
    try {
      for (ApplicationMigration migration : ordered) applyOrSkip(migration, owner);
    } finally {
      leases.release(MigrationProperties.LEASE_NAME, owner);
    }
  }

  private void applyOrSkip(ApplicationMigration migration, String owner) {
    Optional<MigrationRecord> existing = state.find(migration.id());
    if (existing.isPresent()) {
      verifyAppliedIdentity(existing.orElseThrow(), migration);
      return;
    }
    state.start(migration, owner, clock.instant());
    try {
      migration.apply(mongo);
      state.complete(migration.id(), owner, clock.instant());
    } catch (RuntimeException failure) {
      state.fail(migration.id(), owner, clock.instant(), "MIGRATION_FAILED");
      throw new IllegalStateException("Required migration failed: " + migration.id(), failure);
    }
  }
}
```

Verification:
- Runner tests cover ordering, duplicate IDs, locking, skip, drift, incomplete state, success, failure, and release.

#### Code Edit 4.9
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/migration/V001EnsureMigrationInfrastructure.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Component
final class V001EnsureMigrationInfrastructure implements ApplicationMigration {
  public String id() { return "001-ensure-migration-infrastructure"; }
  public String checksum() {
    return "aec77e3e8cf68bf8d67f239ee0e842fbdad26ea9766ab04cbc3d74dd9ad93876";
  }
  public String description() { return "Ensure migration status and lease expiry indexes"; }

  public void apply(MongoTemplate mongo) {
    mongo.indexOps(MigrationRecord.COLLECTION).ensureIndex(new Index()
        .on("status", Sort.Direction.ASC).on("completedAt", Sort.Direction.DESC)
        .named("migration_status_completed"));
    mongo.indexOps(MongoLeaseService.COLLECTION).ensureIndex(new Index()
        .on("expiresAt", Sort.Direction.ASC).named("lease_expiry"));
  }
}
```

Verification:
- Focused lease/runner/V001 tests pass.
- Add a duplicate-ID test, lease-contention test, state-update matched-count test, and bounded-properties binding test.
- Recompute SHA-256 from the reviewed canonical descriptor `001-ensure-migration-infrastructure|v1|migration_status_completed:status,completedAt|lease_expiry:expiresAt` and assert the exact constant.

### Task 5 - Document authoring, recovery, production, and operator contracts

Sequence / dependencies:
- After the final configuration and migration interfaces are stable.

Implementation notes:
- Required skill: `chris-street-style` before copy-ready migration/operations examples.
- Before-Edit Brief:
  - Behavior: contributors and operators can start local Mongo, author immutable migrations, and recover interrupted production starts safely.
  - Invariants: backup first, exact record/lease scope, no silent data rollback, and destructive commands identify their target.
  - Boundary/API: environment keys, Compose commands, collections, statuses, and deployment sequence are named.
  - Effects and failures: incomplete migrations halt startup; recovery requires root-cause correction and an explicit bounded operator action.
  - Tests and evidence: doc review cross-checks commands against implemented names and runtime acceptance output.

#### Code Edit 5.1
- File: `docs/operations/mongodb-migrations.md`
- Lines: before 1
- Action: add

Proposed:
```markdown
# MongoDB Application Migrations

- Back up production before a migration release.
- Add a new ordered migration ID; never edit an applied ID/checksum.
- Keep migrations additive and idempotent, and preserve compatibility with the previous app release.
- `RUNNING` or `FAILED` records block startup. Inspect the safe failure category and application logs,
  correct the cause, verify no deployment owns `application-migrations`, and restore from backup if the
  data change was not safely idempotent. Only then may an operator remove the single incomplete record
  and restart; record that recovery in the deployment report.
- Application rollback does not reverse Mongo data. A compensating migration is a new reviewed ID.
```

Verification:
- Review all collection/status/command names against implementation and test the non-destructive inspection commands.

#### Code Edit 5.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/README.md`
- Lines: 1-10
- Action: replace

Current:
```markdown
# Configuration Mongo

Owns MongoDB infrastructure configuration.

What Lives Here:

- `MongoAuditingConfig` enables Spring Data Mongo auditing and provides auditor and timestamp sources.
```

Proposed:
```markdown
This package owns Mongo auditing, reusable fixed-name leases, and versioned application migrations.
Feature models remain in their owning package. Migration IDs/checksums are immutable after merge.
```

Verification:
- Package documentation names the exact lease/migration ownership boundary.

#### Code Edit 5.3
- File: `website/src/main/java/dev/christopherbell/configuration/README.md`
- Lines: 46-51
- Action: replace

Current:
```markdown
- MongoDB auditing configuration under `mongo`.
- Shared configuration properties that do not yet need a subpackage.
```

Proposed:
```markdown
- Production settings validation runs before context refresh and reports only setting names.
- Explicit `app.mail.enabled` controls password-reset delivery.
- Mongo auditing, fixed-name leases, and immutable versioned migrations live under `configuration.mongo`.
```

Verification:
- Configuration README matches class/property names and does not include secrets.

#### Code Edit 5.4
- File: `docs/operations/windows-production.md`
- Lines: 99-109
- Action: replace

Current:
```markdown
Use absolute native Windows paths. Set `cloudflaredExe` to the signed
machine-wide executable, `publicUrl` to
`https://www.christopherbell.dev/`, a real smoke-account email, a stable JWT
secret of at least 32 characters, and
`SPRING_MONGODB_URI=mongodb://127.0.0.1:27017`.
```

Proposed:
```markdown
Configure `APP_JWT_SECRET` and an explicit `SPRING_MONGODB_URI` with no production fallback.
Set `APP_MAIL_ENABLED=true` with `RESEND_API_KEY` and `APP_MAIL_FROM`, or set it to `false`
to intentionally disable mail. Deployment runs immutable Mongo migrations before readiness;
see the MongoDB migration runbook for failed/incomplete recovery.
```

Verification:
- Windows runbook keys match the protected environment parser and link the migration recovery document.

#### Code Edit 5.5
- File: `README.md`
- Lines: 357-441
- Action: replace

Current:
```markdown
Production runs natively on Windows through the `MongoDB`,
`ChristopherBellDev`, and `cloudflared` Windows services.

### MongoDB Backups and Restores

Use the Windows production runbook and MongoDB backup and restore runbook.
```

Proposed:
```markdown
Production requires an explicit `SPRING_MONGODB_URI`. Startup validates production settings
before service readiness and applies immutable leased Mongo migrations. Back up before migration
releases; application rollback does not reverse data. See `docs/operations/mongodb-migrations.md`.
```

Verification:
- Documentation names exact environment keys, collections, commands, backup boundary, and destructive recovery scope.

### Task 6 - Focused GREEN, safe temporary-database runtime acceptance, and full regression

Sequence / dependencies:
- After Tasks 2-5.

Focused automated verification:
- `./gradlew :website:test --tests dev.christopherbell.configuration.MongoProfileConfigurationTest --tests dev.christopherbell.configuration.ProductionSettingsApplicationContextInitializerTest --tests dev.christopherbell.account.PasswordResetNotificationServiceTest --tests dev.christopherbell.configuration.LocalMongoComposeConfigurationTest --tests 'dev.christopherbell.configuration.mongo.*' --no-daemon --no-watch-fs --max-workers=1`
- `Invoke-Pester ops/production/windows/tests/Production.Common.Tests.ps1,ops/production/windows/tests/Production.Command.Tests.ps1`
- If Docker exists: `docker compose config`.

Production-failure acceptance:
- Build the boot JAR.
- Start it with `prod,deploy-smoke`, port `8090`, and all production settings intentionally absent.
- Expected: nonzero exit before the port binds; one `Invalid production configuration` report names every missing setting and contains no configured values.
- Repeat with mail disabled, a synthetic 32+ byte JWT, and a dedicated temporary Mongo URI/database; expected configuration validation passes.

Migration runtime acceptance:
- Resolve an exact disposable database name such as `christopherbell_foundations_test_<timestamp>` and verify it differs from `christopherbell` and all configured production database names.
- Start the branch only on port `8090` with `prod,deploy-smoke`, `APP_MAIL_ENABLED=false`, a synthetic JWT, `SPRING_MONGODB_URI=mongodb://127.0.0.1:27017`, and `SPRING_MONGODB_DATABASE=<disposable>`.
- Verify `/` and readiness return expected status, `application_migrations` contains exactly applied V001 with the reviewed checksum, the two indexes exist, and the lease is unowned/expired.
- Restart against the same disposable database and prove V001 remains one record and is skipped.
- Stop port `8090`, verify the live `8080` PID and `/` remained healthy, re-resolve the exact disposable database name, then drop only that disposable database and prove it no longer exists.

Full verification:
- `./gradlew :website:cleanTest :website:check --no-daemon --no-watch-fs --max-workers=1 --console=plain`
- Full Windows production Pester suite with environment-only integration skips recorded honestly.
- `git diff --check`.
- Inspect the final committed diff for secret values, localhost production fallback, mutable migration IDs, and accidental `gradlew.bat` staging.

### Task 7 - Builder evidence, review, PR, CI, merge, production, and closure

Sequence / dependencies:
- After authoritative local GREEN.

Steps:
1. Save and validate `docs/test-reports/2026-07-25-production-foundations-issues-1143-1151-1153-1154.md` with exact missing-setting output shape, temporary database name, Mongo records/indexes, cleanup proof, Pester/Gradle counts, and live-8080 continuity.
2. Commit/push the Builder test-report checkpoint.
3. Save an independent spoke review; resolve every Blocker/Warning and rerun affected verification.
4. Commit only intended spoke files, push `codex/production-foundations-1143-1154`, and open one PR with `Closes #1143`, `Closes #1151`, `Closes #1153`, and `Closes #1154`.
5. Wait for Ubuntu, macOS, Windows, Dependency Review, and all CodeQL checks; fix root causes rather than rerunning blindly.
6. Squash-merge only when review and all checks are green; verify all four issues close.
7. Monitor guarded automatic deployment. Confirm the Java PID/release changes, `/` stays `200`, readiness is healthy, mail configuration intent is preserved, and production migration V001 is `APPLIED` exactly once without exposing secrets.
8. Update the test report, spoke update/review, campaign ledger (34 to 30 remaining), indexes, and session memory; validate, commit, and push Builder checkpoints.

## Risks and Mitigations

- Early validation order could occur after Mongo auto-configuration. Mitigation: register an application-context initializer and prove missing settings fail before port bind or Mongo connection output.
- Blank URI binding could obscure the combined report. Mitigation: initializer reads `SPRING_MONGODB_URI` directly before refresh; test the actual packaged JAR.
- Mail disablement could silently change production behavior. Mitigation: production defaults `APP_MAIL_ENABLED=true`; protected config remains compatible, and disabling is explicit/tested.
- A migration crash can leave `RUNNING`. Mitigation: fail closed, durable owner/timestamps, bounded lease expiry, backup-first documented recovery, no automatic record deletion.
- Index changes can conflict with existing definitions. Mitigation: V001 creates only named indexes on new infrastructure collections; feature indexes remain for later reviewed migrations.
- Runtime acceptance could touch production data. Mitigation: exact disposable database name, preflight inequality checks, explicit override, bounded cleanup, and production-port continuity evidence.
- Baseline command-center timing test can flake. Mitigation: retain first-failure evidence, rerun the isolated class, and require an authoritative clean single-worker suite before publication.

## Unit Testing

- Production initializer: profile partition, all-missing aggregate, weak/example JWT, malformed mail switch, enabled-mail requirements, disabled-mail success, and redaction.
- Mail service: disabled no-op, enabled configured sender, missing sender safe failure, authentication failure redaction.
- Compose: pinned official image, loopback port, named volume, health check, and no secrets.
- Lease: first acquire, same-owner renewal, expired takeover, contention, current-owner release, and query boundaries.
- Runner: ordering, duplicate IDs, applied skip, checksum drift, incomplete state, lease contention, success record, failure record, release in `finally`, and safe error messages.
- V001: exact index names/fields and idempotent `ensureIndex` calls.
- PowerShell: allowlist, Boolean switches, mail enabled/disabled partitions, placeholder rejection, and aggregated missing names.

## Local Testing

- Missing production settings fail the packaged application before bind with one redacted report.
- Explicit mail disable permits safe startup without Resend credentials.
- Disposable Mongo database receives one V001 applied record and expected indexes; restart skips it.
- Port `8090` is stopped and freed; production `8080` remains healthy throughout.
- Disposable database cleanup is verified after exact-name guard checks.

## Expected Outcome

- Production has no built-in Mongo URI and fails fast with one actionable, redacted settings report.
- Mail operation is explicitly enabled/disabled and cannot accidentally appear configured from blank values.
- Contributors can start a pinned persistent MongoDB locally with one Compose command.
- The application owns an append-only, leased, observable Mongo migration mechanism suitable for later issue batches.
- Issues #1143, #1151, #1153, and #1154 close after CI, merge, production migration verification, and Builder closeout.

## Code Changes

- Replace the production Mongo fallback and mail ambiguity in `application-prod.yml` with explicit environment-driven values and an intentional mail switch.
- Add an early registered production-settings initializer and typed mail configuration; update password-reset notification delivery and Windows environment parsing accordingly.
- Add the root Compose contract and its structural regression.
- Add reusable Mongo lease infrastructure, immutable migration metadata/state, the startup runner, and V001 infrastructure indexes.
- Add focused Java/Pester tests and update repository/package/operations documentation.

## Files and Modules

- Configuration: `website/src/main/java/dev/christopherbell/configuration/`, `application.yml`, `application-prod.yml`, and `META-INF/spring.factories`.
- Mail consumer: `website/src/main/java/dev/christopherbell/account/passwordreset/PasswordResetNotificationService.java`.
- Mongo infrastructure: new `configuration/mongo/lease` and `configuration/mongo/migration` packages.
- Local development: `compose.yaml`, `.env.example`, and `README.md`.
- Windows production: `ops/production/windows/config/app.env.example`, launcher, common environment parser/tests, and production runbook.
- Evidence: focused configuration/mail/migration/Compose tests plus Builder plan, test report, review, spoke update, ledger, and memory.

## Validation

- Witness focused RED failures before semantic edits.
- Run the named focused JUnit and Pester commands after each owning task.
- Validate Compose structurally and with `docker compose config` when available.
- Exercise missing production settings against the packaged JAR and prove one redacted pre-bind failure.
- Run first-start/restart migration acceptance against an exact disposable Mongo database on port `8090`, then verify bounded cleanup and live `8080` continuity.
- Require the authoritative clean single-worker Gradle check, full relevant Pester suite, `git diff --check`, independent review, and all GitHub CI/CodeQL/dependency gates.

## Rollback or Recovery

- Before merge, remove only the isolated branch/worktree changes if implementation is abandoned; never touch the dirty authoritative checkout.
- Candidate deployment failure leaves the current release on port `8080`; use the existing guarded Windows rollback workflow if post-switch verification fails.
- Application rollback does not reverse applied Mongo changes. V001 is additive and idempotent; later corrections are new migrations.
- A `RUNNING` or `FAILED` record blocks startup. Back up, inspect the exact migration and fixed lease, correct the cause, confirm no current owner, and remove only the reviewed incomplete record when the migration is proven safe to retry. Restore from backup when idempotence cannot be proven.
- Drop only the preflight-validated disposable acceptance database after stopping the alternate-port app; never use a computed or production database name as a destructive target.

## Risks

- Initializer ordering, blank URI auto-binding, and the packaged-resource registration are validated against the real boot JAR.
- Production mail behavior is preserved by a true default and can change only through the explicit switch.
- Mongo concurrency/crash behavior is fail-closed with fixed IDs, owner tokens, expiry, durable state, and no automatic incomplete retry.
- V001 is limited to new infrastructure collections to avoid existing-index conflicts.
- Baseline command-center timing flakiness is recorded separately and the final authoritative suite must pass from a clean, non-overlapping invocation.

## Completion Criteria

- The implementation-plan validator and readiness review report no blockers.
- Every issue acceptance item maps to committed code/configuration/documentation and witnessed evidence.
- Focused tests, packaged failure probes, disposable-database first-run/restart, full Gradle/Pester verification, and production-port continuity pass.
- The final diff contains no secret values, no production Mongo fallback, no mutable applied migration, and no staged `gradlew.bat` noise.
- PR checks pass on Ubuntu, macOS, Windows, Dependency Review, and all CodeQL analyses; the PR merges and closes all four issues.
- Automatic production deployment succeeds, V001 is applied exactly once, the live site/readiness remain healthy, and Builder closure artifacts are validated, committed, and pushed.
