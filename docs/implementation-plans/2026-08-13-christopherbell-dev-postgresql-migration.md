# christopherbell.dev PostgreSQL Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Use `chris-street-style` before every production-code, test, migration, script, executable-configuration, or code-bearing-template edit. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace MongoDB as the website's authoritative persistence engine with native PostgreSQL, relational schemas, Flyway migrations, generated jOOQ types, verified data reconciliation, and pgAdmin 4 Desktop access.

**Architecture:** Keep existing domain persistence interfaces as application ports. Select exactly one backend at process startup while the transition is in progress, implement PostgreSQL adapters with jOOQ and explicit transactions, and make Flyway SQL the sole schema authority. A guarded offline-capable Java migration command maps every manifest kind into normalized relational tables, stages and reconciles deterministic batches, and publishes only complete kinds. Production uses a native loopback-only PostgreSQL service, separate least-privilege roles, pgAdmin connections without privileged credentials, stopped-writer authority transfer, and a time-bounded frozen-Mongo soak before retirement.

**Tech Stack:** Java 25, Spring Boot 4.1.0, PostgreSQL 18.4, Flyway, `flyway-database-postgresql`, jOOQ 3.21.5, PostgreSQL JDBC, JUnit 5, AssertJ, ArchUnit, Gradle, PowerShell 7, Windows PowerShell 5.1, Pester 5.9, pgAdmin 4 Desktop, native Windows services.

---

## Document Status

ready-for-execution

## Objective

Deliver the approved relational database, complete Mongo-to-PostgreSQL bridge, native Windows PostgreSQL and pgAdmin operating surface, automated and live verification, production cutover, 14-day Mongo freeze, 90-day final-archive retention, Mongo retirement, pull request/CI/merge, and Builder closeout.

## Goals

1. Replace all runtime Mongo persistence with relational PostgreSQL adapters behind unchanged domain ports.
2. Migrate and reconcile every one of the 52 source kinds without loss or semantic drift.
3. Make Flyway DDL and generated jOOQ types the reviewable, reproducible schema contract.
4. Operate native PostgreSQL safely on Windows with least-privilege roles, verified backups, and pgAdmin 4 Desktop access.
5. Transfer production authority within the approved window, prove a 14-day soak, retire Mongo, and retain the final archive for 90 days.

## Inputs

- Approved specification: `C:\Users\Christopher\Developer\builder\docs\specs\2026-08-13-christopherbell-dev-postgresql-migration.md`
- Work ledger: `C:\Users\Christopher\Developer\builder\docs\work\2026-08-13-christopherbell-dev-postgresql-migration.md`
- Spoke: `A:\Projects\christopherbell.dev`, remote `https://github.com/azurras/christopherbell.dev.git`
- Inspected base: refreshed `origin/main` at `e073823d14ffed0b4c113707d16c0ad0cfe1b7fa`
- Clean worktree: `A:\Projects\christopherbell.dev-worktrees\postgresql-migration`
- Feature branch: `codex/postgresql-migration`
- Private Gradle home: `A:\Projects\christopherbell.dev-gradle\postgresql-migration`
- Baseline: `BUILD SUCCESSFUL` with 2,002 tests, zero failures/errors, and 75 skips while explicitly connected only to Mongo database `test`.

## Global Constraints

- The finished website is PostgreSQL-only. The Mongo backend and transition bridge are temporary and must be deleted after the approved soak.
- Local development and every database-backed test use PostgreSQL database `test` only. Each automated test suite receives a disposable, uniquely named schema inside `test`; tests must refuse production-like database names.
- Flyway schema identifiers use one validated `${schema_prefix}` placeholder: production supplies the empty string and test/code-generation runs supply a unique `cbtest_<run>_` prefix. Thus `identity` becomes `cbtest_<run>_identity` in tests; jOOQ maps prefixed input schemas back to canonical generated schema names.
- Flyway versioned SQL is the only schema source. Never edit an applied migration; add a forward migration.
- jOOQ-generated sources are reproducible build output and are never hand-edited. jOOQ 3.21.5 stays aligned with Spring Boot 4.1.0 dependency management.
- Domain services, controllers, and frontend code retain persistence-neutral ports and cannot import `DSLContext`, generated jOOQ packages, JDBC, Mongo APIs, or PostgreSQL driver types.
- All 52 manifest kinds are mapped explicitly. Unknown kinds, fields, identifier forms, enum values, or unmapped relationships fail before publication.
- No application dual-write. While the bridge exists, startup selects exactly one of `mongodb` or `postgresql`, and production rejects a missing or ambiguous selection.
- A kind is readable from PostgreSQL only after its complete staged data is transactionally published and reconciled.
- Candidate runtime validation uses a non-8080 port before any production listener or authority change.
- Production cutover holds the existing protected deployment lock, disables service recovery, stops all Mongo writers, takes and dry-restores a final backup, refreshes PostgreSQL from the frozen source, reconciles, starts PostgreSQL authority, and verifies exact runtime behavior.
- Before PostgreSQL authority, rollback may return to untouched Mongo. After any accepted PostgreSQL write, never return to stale Mongo.
- MongoDB is stopped/frozen for 14 days after successful PostgreSQL authority. Its final verified archive is retained for 90 days. Retirement never weakens production ACLs.
- Native PostgreSQL listens only on loopback. The website role cannot migrate schemas; the pgAdmin viewer role is database-enforced read-only; privileged credentials are not saved in pgAdmin.
- All secret-bearing values come from protected production environment/configuration and are redacted from command output, logs, reports, and errors.

## Branch

- Base: `origin/main` at `e073823d14ffed0b4c113707d16c0ad0cfe1b7fa`
- Feature branch: `codex/postgresql-migration`
- Worktree: `A:\Projects\christopherbell.dev-worktrees\postgresql-migration`
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`.

## Non-Goals

- No public route, visual design, feature, authentication-policy, or frontend-state redesign.
- No JSONB envelope lift of Mongo documents. JSONB is permitted only for catalog-justified opaque values that are not relationally queried or constrained.
- No H2, SQLite, embedded PostgreSQL, unbounded offset pagination, or generic ORM repository layer.
- No cloud database, Docker database, or remote pgAdmin server in production.
- No deletion of Mongo data or archives before the soak and retention gates.

## Assumptions

- A maintenance window of up to 30 minutes is available for final authority transfer.
- The native host can run a supported 64-bit PostgreSQL 18 service and pgAdmin 4 Desktop.
- CI can provision PostgreSQL database `test`; developer verification uses either the loopback native service or the pinned Compose service.
- Current application ports are the behavioral contract; port changes require explicit review and are not implied by this migration.

## Open Questions

None. If a source kind cannot be represented relationally without an unapproved semantic change, stop that task and return to design review before creating or publishing its target tables.

## Target Schema and Source Ownership

| PostgreSQL schema | Tables / source kinds owned by the slice |
|---|---|
| `identity` | `account`, `account_follow`, `account_trust_relationship`, `account_deletion_job`, `browser_session`, `conversation_archive_state` |
| `social` | `post`, `post_like`, `post_report`, `hidden_post_thread`, `post_link_preview_cache` |
| `communication` | `message`, `notification`, `notification_preference`, `notification_delivery_guard`, `notification_rate_limit` |
| `federation` | `federation_scan_state`, `federation_delivery_job` |
| `music` | `music_track`, `music_playlist`, playlist membership, `music_metadata_edit`, `music_runtime_state`, `music_radio_history`, `music_access_attempt` |
| `shared_folder` | `audit_event`, `maintenance_lease`, `media_job`, `mutation_recovery`, `radio_state`, `recycle_item`, `upload_session` |
| `mobility` | `vehicle`, `vin_decode_cache`, `nhtsa_import_state`, `random_vin_import_state`, `zip_coordinate`, `zip_import_state` |
| `lunch` | `restaurant`, `vote`, `favorite`, `preference`, `session`, session membership, `daily_picks`, daily-pick membership, `import_state`, `import_preview` |
| `canes` | `price_snapshot` |
| `platform` | `admin_activity`, `pending_action`, `application_lease`, `scheduled_collector_run`, migration run/batch/source ledger/reconciliation/publication records |

## Code Changes

- Add the PostgreSQL/Flyway/jOOQ build and configuration foundation while retaining a strictly conditional Mongo bridge.
- Add ten normalized PostgreSQL schemas, 52-kind catalog mappings, generated jOOQ records, and one PostgreSQL adapter per persistence port.
- Add the deterministic, resumable, reconciliation-gated migration engine and native Windows PostgreSQL/pgAdmin operations.
- Rehearse and execute the authority cutover, then delete all bridge/Mongo runtime code and configuration after the soak gate.

## Files and Modules

- `website/src/main/resources/db/migration/V1__create_roles_and_schemas.sql` through versioned slice migrations — canonical PostgreSQL DDL.
- `website/src/main/resources/db/migration/postgresql-migration-catalog.yml` — all 52 source-kind transformations and reconciliation rules.
- `website/src/main/java/dev/christopherbell/configuration/persistence/*` — backend selection and persistence health.
- `website/src/main/java/dev/christopherbell/configuration/postgresql/*` — jOOQ support, transaction helpers, cleanup scheduling, and adapter annotations.
- `website/src/main/java/dev/christopherbell/**/Postgres*.java` — domain-port implementations beside existing ports.
- `website/src/main/java/dev/christopherbell/configuration/postgresql/migration/*` — guarded migration CLI, catalog validation, transformers, staging, reconciliation, and publication.
- `website/src/test/java/dev/christopherbell/configuration/postgresql/*` — schema, isolation, architecture, migration, and contract tests.
- `ops/production/windows/modules/Production.PostgreSql.psm1` — installation, role/database/bootstrap, backup/restore, status, pgAdmin, and retirement operations.
- `ops/production/windows/modules/Production.PostgreSqlMigration.psm1` — shadow, cutover, rollback-before-authority, soak, and archive gates.
- `docs/operations/postgresql.md` — native PostgreSQL, test database, pgAdmin, backup/restore, monitoring, cutover, and incident runbook.

## Task Breakdown

### Task 1 - Establish the PostgreSQL build, profiles, backend boundary, and test guard

Sequence / dependencies:
- First implementation task. Every later slice depends on this backend-selection and schema-isolation contract.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: provide Flyway, jOOQ, JDBC, PostgreSQL, a pinned local PostgreSQL service, and exact `mongodb`/`postgresql` startup selection.
  - Invariants: one backend active; local and test use database `test`; production credentials have no defaults; tests use unique schemas and reject any other database.
  - Boundary/API: `app.persistence.backend` is the only application backend selector; domain code never reads it directly.
  - Effects and failures: startup performs a redacted database identity check and fails before context readiness on a wrong database, ambiguous adapter set, or unavailable schema.
  - Tests and evidence: configuration parsing, bean-selection tests, database-identity rejection, concurrent unique-schema isolation, JDBC connectivity, and Compose loopback checks.

- [ ] **Step 1: Add failing profile, dependency, backend-selection, and database-guard tests.**
- [ ] **Step 2: Run the focused tests and confirm failures because PostgreSQL configuration and selectors do not exist.**
- [ ] **Step 3: Add dependencies, pinned Compose PostgreSQL, profiles, conditional adapter annotations, and identity guard.**
- [ ] **Step 4: Connect only to database `test`, create two guarded disposable schemas, and prove the two connections cannot see each other's fixtures.**
- [ ] **Step 5: Run focused tests and `:website:compileJava`, then commit `feat: establish PostgreSQL persistence foundation`.**

#### Code Edit 1.2
- File: `website/build.gradle.kts`
- Lines: 16-85
- Action: replace

Current:
```kotlin
plugins {
    id("org.springframework.boot")
    id("io.spring.dependency-management")
    java
}

dependencies {
    implementation(project(":cbell-lib"))
    implementation("org.springframework.boot:spring-boot-starter-data-mongodb")
    // existing application and test dependencies
}
```

Proposed:
```kotlin
plugins {
    id("org.springframework.boot")
    id("io.spring.dependency-management")
    java
}

dependencies {
    implementation(project(":cbell-lib"))
    implementation("org.springframework.boot:spring-boot-starter-data-mongodb") // transition only
    implementation("org.springframework.boot:spring-boot-starter-flyway")
    implementation("org.springframework.boot:spring-boot-starter-jooq")
    runtimeOnly("org.flywaydb:flyway-database-postgresql")
    runtimeOnly("org.postgresql:postgresql")
    // retain all existing non-persistence and test dependencies unchanged
}
```

Verification:
- `$env:SPRING_PROFILES_ACTIVE='test'; $env:SPRING_DATASOURCE_URL='jdbc:postgresql://127.0.0.1:5432/test'; ./gradlew.bat :website:compileJava --console=plain` succeeds without requiring generated tables that do not exist yet.

#### Code Edit 1.3
- File: `compose.yaml`
- Lines: 1-18
- Action: replace

Current:
```yaml
services:
  mongodb:
    image: mongo:8.3.2
    ports:
      - "127.0.0.1:27017:27017"
volumes:
  christopherbell_mongo_data: {}
```

Proposed:
```yaml
services:
  mongodb:
    image: mongo:8.3.2
    restart: unless-stopped
    ports: ["127.0.0.1:27017:27017"]
    volumes: ["christopherbell_mongo_data:/data/db"]
  postgresql:
    image: postgres:18.4
    restart: unless-stopped
    environment:
      POSTGRES_DB: test
      POSTGRES_USER: christopherbell_test
      POSTGRES_PASSWORD: ${POSTGRES_TEST_PASSWORD:?set POSTGRES_TEST_PASSWORD}
    ports: ["127.0.0.1:5432:5432"]
    volumes: ["christopherbell_postgresql_data:/var/lib/postgresql"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U christopherbell_test -d test"]
      interval: 5s
      timeout: 5s
      retries: 12
      start_period: 10s
volumes:
  christopherbell_mongo_data: {}
  christopherbell_postgresql_data: {}
```

Verification:
- `docker compose config` contains database `test`, loopback port 5432, a pinned image, and no literal password.

#### Code Edit 1.4
- File: `website/src/main/resources/application-local.yml`
- Lines: 20-26
- Action: replace

Current:
```yaml
spring:
  mongodb:
    database: christopherbell
    uri: mongodb://localhost:27017
  data:
    mongodb:
      auto-index-creation: true
```

Proposed:
```yaml
app:
  persistence:
    backend: postgresql
spring:
  datasource:
    url: ${SPRING_DATASOURCE_URL:jdbc:postgresql://127.0.0.1:5432/test}
    username: ${SPRING_DATASOURCE_USERNAME:christopherbell_test}
    password: ${SPRING_DATASOURCE_PASSWORD:}
  flyway:
    enabled: true
    default-schema: ${APP_TEST_SCHEMA:public}
    schemas: ${APP_TEST_SCHEMA:public}
  jooq:
    sql-dialect: POSTGRES
```

Verification:
- Profile test proves the default JDBC URL ends in `/test` and contains no production database fallback.

#### Code Edit 1.5
- File: `website/src/main/resources/application-prod.yml`
- Lines: 6-25
- Action: replace

Current:
```yaml
spring:
  mongodb:
    database: ${SPRING_MONGODB_DATABASE:christopherbell}
    uri: ${SPRING_MONGODB_URI:}
  data:
    mongodb:
      auto-index-creation: true
```

Proposed:
```yaml
spring:
  datasource:
    url: ${SPRING_DATASOURCE_URL:}
    username: ${SPRING_DATASOURCE_USERNAME:}
    password: ${SPRING_DATASOURCE_PASSWORD:}
  flyway:
    enabled: false
  jooq:
    sql-dialect: POSTGRES
app:
  persistence:
    backend: ${APP_PERSISTENCE_BACKEND:}
```

The transition-only Mongo properties move under a separately imported bridge profile and are removed in Task 10.

Verification:
- Production configuration test proves backend and JDBC credentials have no fallback and Flyway cannot run as the website role.

#### Code Edit 1.6
- File: `website/src/main/resources/application-test.yml`
- Lines: 1-4
- Action: replace

Current:
```yaml
app:
  shared-folder:
    root: build/shared-folder/test/shared
    system-root: build/shared-folder/test/system
```

Proposed:
```yaml
app:
  persistence:
    backend: postgresql
  database-guard:
    required-database: test
    schema-prefix: cbtest_
  shared-folder:
    root: build/shared-folder/test/shared
    system-root: build/shared-folder/test/system
spring:
  datasource:
    url: ${SPRING_DATASOURCE_URL:jdbc:postgresql://127.0.0.1:5432/test}
    username: ${SPRING_DATASOURCE_USERNAME:christopherbell_test}
    password: ${SPRING_DATASOURCE_PASSWORD:}
  flyway:
    default-schema: ${APP_TEST_SCHEMA:}
    schemas: ${APP_TEST_SCHEMA:}
```

Verification:
- `PostgresqlTestDatabaseGuardTest` refuses an empty schema, a schema without `cbtest_`, and every database name other than `test`.

#### Code Edit 1.7
- File: `website/src/main/java/dev/christopherbell/configuration/persistence/PersistenceBackend.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.persistence;

public enum PersistenceBackend {
  MONGODB,
  POSTGRESQL
}
```

Verification:
- Enum parsing accepts only the two transition values and reports invalid configuration without echoing secrets.

#### Code Edit 1.8
- File: `website/src/main/java/dev/christopherbell/configuration/persistence/PostgresPersistence.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.persistence;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Repository;

@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Repository
@ConditionalOnProperty(prefix = "app.persistence", name = "backend", havingValue = "postgresql")
public @interface PostgresPersistence {}
```

Add the symmetric transition-only `MongoPersistence` annotation with `havingValue = "mongodb"`; apply it to every Mongo repository, query service, store, migration runner, and Mongo configuration component found by `MongoPersistenceBoundaryRules`.

Verification:
- `PersistenceBackendSelectionTest` proves exactly one implementation of every migrated port is active under each transition backend.

#### Code Edit 1.9
- File: `website/src/test/java/dev/christopherbell/configuration/PersistenceProfileConfigurationTest.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import org.junit.jupiter.api.Test;
import org.springframework.boot.env.YamlPropertySourceLoader;
import org.springframework.core.io.ClassPathResource;

class PersistenceProfileConfigurationTest {
  @Test
  void localAndTestProfilesUseOnlyPostgresqlDatabaseTest() throws IOException {
    for (String name : java.util.List.of("application-local.yml", "application-test.yml")) {
      var source = new YamlPropertySourceLoader()
          .load(name, new ClassPathResource(name)).getFirst();
      assertThat(source.getProperty("app.persistence.backend")).isEqualTo("postgresql");
      assertThat(source.getProperty("spring.datasource.url").toString()).endsWith("/test}");
    }
  }
}
```

Verification:
- `./gradlew.bat :website:test --tests '*PersistenceProfileConfigurationTest' --tests '*PostgresqlTestDatabaseGuardTest' --console=plain`

Delete `MongoProfileConfigurationTest.java` lines 1-51 only after this replacement test passes.

### Task 2 - Create canonical relational DDL, catalog validation, and reproducible jOOQ generation

Sequence / dependencies:
- Depends on Task 1. Complete all schema/catalog work before implementing domain adapters.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: create an empty database solely from immutable Flyway migrations and produce typed jOOQ sources for every table/key/index.
  - Invariants: ten bounded-context schemas; explicit PK/FK/delete behavior; UTC timestamps; deterministic identifiers; no undocumented JSONB; every manifest kind appears once in the migration catalog.
  - Boundary/API: the catalog is consumed by migration transformers and tests, while runtime adapters consume generated jOOQ types.
  - Effects and failures: DDL is transactional where PostgreSQL permits; catalog validation reports only kind/path metadata and stops on unknown or duplicate mappings.
  - Tests and evidence: empty-schema migration, schema snapshot, constraint/index assertions, generated-source clean rebuild, and exact 52-kind coverage.

- [ ] **Step 1: Add failing schema/catalog tests that compare `DomainCollectionManifest` with the target catalog.**
- [ ] **Step 2: Add role/schema/ledger DDL, then slice DDL in FK dependency order.**
- [ ] **Step 3: Write all 52 catalog entries with source field mappings, hashes, load order, and reconciliation rules.**
- [ ] **Step 4: Generate jOOQ twice from clean unique schemas and prove byte-identical generated sources.**
- [ ] **Step 5: Run schema/catalog tests and commit `feat: define canonical PostgreSQL schema`.**

#### Code Edit 2.0
- File: `build.gradle.kts`
- Lines: 1-5
- Action: replace

Current:
```kotlin
plugins {
    id("org.springframework.boot") version "4.1.0" apply false
    id("io.spring.dependency-management") version "1.1.7" apply false
    java
}
```

Proposed:
```kotlin
plugins {
    id("org.springframework.boot") version "4.1.0" apply false
    id("io.spring.dependency-management") version "1.1.7" apply false
    id("org.jooq.jooq-codegen-gradle") version "3.21.5" apply false
    java
}
```

Apply the plugin in `website/build.gradle.kts`, add the PostgreSQL driver to the `jooqCodegen` configuration, configure the generator from `JOOQ_CODEGEN_JDBC_URL`, `JOOQ_CODEGEN_USERNAME`, `JOOQ_CODEGEN_PASSWORD`, and `JOOQ_CODEGEN_SCHEMA_PREFIX`, restrict generation to the ten approved prefixed input schemas, map them to canonical output schemas, target `build/generated-src/jooq/main`, and make `compileJava` depend on `jooqCodegen` only after the Task 2 Flyway schema-preparation task. `JOOQ_CODEGEN_SCHEMA_PREFIX` is the exact approved public key because it supplies the shared `cbtest_<run>_` prefix, not one schema name; the obsolete singular `JOOQ_CODEGEN_SCHEMA` key is unsupported and fails closed.

Verification:
- Apply Task 2 Flyway migrations to a unique `cbtest_*` schema, then `./gradlew.bat :website:jooqCodegen :website:compileJava --console=plain` succeeds and contains no credential in task output.

#### Code Edit 2.1
- File: `website/src/main/resources/db/migration/V1__create_schemas_and_migration_ledger.sql`
- Lines: before 1
- Action: add

Proposed:
```sql
CREATE SCHEMA ${schema_prefix}identity;
CREATE SCHEMA ${schema_prefix}social;
CREATE SCHEMA ${schema_prefix}communication;
CREATE SCHEMA ${schema_prefix}federation;
CREATE SCHEMA ${schema_prefix}music;
CREATE SCHEMA ${schema_prefix}shared_folder;
CREATE SCHEMA ${schema_prefix}mobility;
CREATE SCHEMA ${schema_prefix}lunch;
CREATE SCHEMA ${schema_prefix}canes;
CREATE SCHEMA ${schema_prefix}platform;

CREATE TABLE ${schema_prefix}platform.persistence_migration_run (
  run_id uuid PRIMARY KEY,
  catalog_version varchar(64) NOT NULL,
  source_database varchar(128) NOT NULL,
  target_database varchar(128) NOT NULL,
  source_frozen boolean NOT NULL,
  status varchar(32) NOT NULL CHECK (status IN ('STAGING','RECONCILING','READY','PUBLISHED','FAILED')),
  started_at timestamptz NOT NULL DEFAULT transaction_timestamp(),
  completed_at timestamptz
);

CREATE TABLE ${schema_prefix}platform.persistence_migration_source (
  run_id uuid NOT NULL REFERENCES ${schema_prefix}platform.persistence_migration_run(run_id) ON DELETE RESTRICT,
  source_kind varchar(96) NOT NULL,
  source_id varchar(512) NOT NULL,
  transformer_version integer NOT NULL CHECK (transformer_version > 0),
  source_hash char(64) NOT NULL,
  target_hash char(64),
  status varchar(24) NOT NULL CHECK (status IN ('STAGED','VERIFIED','PUBLISHED','FAILED')),
  PRIMARY KEY (run_id, source_kind, source_id)
);

CREATE INDEX persistence_migration_source_status_idx
  ON ${schema_prefix}platform.persistence_migration_source (run_id, source_kind, status);
```

The first schema statement is likewise `CREATE SCHEMA ${schema_prefix}identity;`; every schema-qualified identifier in all Task 2 migrations uses the same validated placeholder. Production accepts only an empty prefix; test/code-generation accepts only a generated `cbtest_<run>_` prefix and drops exactly those owned schemas after verification. jOOQ config enumerates the ten prefixed input schemas and assigns canonical output schema names (`identity`, `social`, and so on), so random run prefixes never enter generated Java.

Verification:
- Apply all Flyway migrations to a new `cbtest_schema_*` schema and query `pg_catalog` for exactly ten owned schemas and the declared constraints.

#### Code Edit 2.2
- File: `website/src/main/resources/db/migration/V2__create_identity_social_communication_federation.sql`
- Lines: before 1
- Action: add

Proposed:
```sql
CREATE TABLE ${schema_prefix}identity.account (
  account_id varchar(128) PRIMARY KEY,
  email varchar(320) NOT NULL,
  normalized_email varchar(320) NOT NULL UNIQUE,
  display_name varchar(160) NOT NULL,
  password_hash varchar(512),
  version bigint NOT NULL DEFAULT 0 CHECK (version >= 0),
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL,
  deleted_at timestamptz
);

CREATE TABLE ${schema_prefix}social.post (
  post_id varchar(128) PRIMARY KEY,
  author_account_id varchar(128) NOT NULL REFERENCES ${schema_prefix}identity.account(account_id) ON DELETE RESTRICT,
  body text NOT NULL,
  visibility varchar(32) NOT NULL,
  version bigint NOT NULL DEFAULT 0 CHECK (version >= 0),
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL,
  expires_at timestamptz
);
CREATE INDEX post_author_created_idx ON ${schema_prefix}social.post (author_account_id, created_at DESC, post_id DESC);
CREATE INDEX post_expiration_idx ON ${schema_prefix}social.post (expires_at) WHERE expires_at IS NOT NULL;

CREATE TABLE ${schema_prefix}communication.message (
  message_id varchar(128) PRIMARY KEY,
  sender_account_id varchar(128) NOT NULL REFERENCES ${schema_prefix}identity.account(account_id) ON DELETE RESTRICT,
  recipient_account_id varchar(128) NOT NULL REFERENCES ${schema_prefix}identity.account(account_id) ON DELETE RESTRICT,
  body text NOT NULL,
  sent_at timestamptz NOT NULL,
  read_at timestamptz
);
CREATE INDEX message_conversation_idx
  ON ${schema_prefix}communication.message (sender_account_id, recipient_account_id, sent_at DESC, message_id DESC);

CREATE TABLE ${schema_prefix}federation.delivery_job (
  delivery_job_id varchar(128) PRIMARY KEY,
  actor_account_id varchar(128) REFERENCES ${schema_prefix}identity.account(account_id) ON DELETE SET NULL,
  destination_uri text NOT NULL,
  state varchar(32) NOT NULL,
  attempt_count integer NOT NULL DEFAULT 0 CHECK (attempt_count >= 0),
  next_attempt_at timestamptz,
  created_at timestamptz NOT NULL
);
CREATE INDEX federation_delivery_claim_idx
  ON ${schema_prefix}federation.delivery_job (state, next_attempt_at, delivery_job_id);
```

The same migration contains the remaining identity/social/communication/federation tables named in the ownership table. Each current Mongo uniqueness, TTL, cursor, and partial-index rule is represented by an explicit constraint or partial index and asserted by `PostgresqlSchemaContractTest`.

Verification:
- `./gradlew.bat :website:test --tests '*PostgresqlSchemaContractTest' --tests '*PostgresqlMigrationCatalogTest' --console=plain`

#### Code Edit 2.3
- File: `website/src/main/resources/db/migration/V3__create_music_shared_folder.sql`
- Lines: before 1
- Action: add

Proposed:
```sql
CREATE TABLE ${schema_prefix}music.track (
  track_id varchar(512) PRIMARY KEY,
  relative_path text NOT NULL UNIQUE,
  title text NOT NULL,
  artist text,
  album text,
  duration_millis bigint CHECK (duration_millis IS NULL OR duration_millis >= 0),
  version bigint NOT NULL DEFAULT 0 CHECK (version >= 0),
  discovered_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);

CREATE TABLE ${schema_prefix}music.playlist (
  playlist_id varchar(128) PRIMARY KEY,
  owner_account_id varchar(128) REFERENCES ${schema_prefix}identity.account(account_id) ON DELETE SET NULL,
  name varchar(256) NOT NULL,
  version bigint NOT NULL DEFAULT 0 CHECK (version >= 0),
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);
CREATE TABLE ${schema_prefix}music.playlist_track (
  playlist_id varchar(128) NOT NULL REFERENCES ${schema_prefix}music.playlist(playlist_id) ON DELETE CASCADE,
  ordinal integer NOT NULL CHECK (ordinal >= 0),
  track_id varchar(512) NOT NULL REFERENCES ${schema_prefix}music.track(track_id) ON DELETE RESTRICT,
  PRIMARY KEY (playlist_id, ordinal),
  UNIQUE (playlist_id, track_id)
);

CREATE TABLE ${schema_prefix}shared_folder.maintenance_lease (
  lease_name varchar(128) PRIMARY KEY,
  owner_id varchar(256) NOT NULL,
  fence_token bigint NOT NULL CHECK (fence_token > 0),
  expires_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT transaction_timestamp()
);
CREATE INDEX shared_folder_lease_expiration_idx
  ON ${schema_prefix}shared_folder.maintenance_lease (expires_at);
```

Verification:
- Contract tests prove playlist ordering/uniqueness and atomic lease claim/renew/release using database time.

#### Code Edit 2.4
- File: `website/src/main/resources/db/migration/V4__create_mobility_lunch_canes_platform.sql`
- Lines: before 1
- Action: add

Proposed:
```sql
CREATE TABLE ${schema_prefix}mobility.vehicle (
  vehicle_id varchar(128) PRIMARY KEY,
  vin char(17) NOT NULL UNIQUE,
  owner_account_id varchar(128) REFERENCES ${schema_prefix}identity.account(account_id) ON DELETE SET NULL,
  model_year integer CHECK (model_year BETWEEN 1886 AND 9999),
  make text,
  model text,
  version bigint NOT NULL DEFAULT 0 CHECK (version >= 0),
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL
);

CREATE TABLE ${schema_prefix}lunch.restaurant (
  restaurant_id varchar(128) PRIMARY KEY,
  normalized_name varchar(512) NOT NULL UNIQUE,
  display_name text NOT NULL,
  latitude numeric(9,6),
  longitude numeric(9,6),
  locality text,
  region text,
  country_code char(2),
  version bigint NOT NULL DEFAULT 0 CHECK (version >= 0),
  created_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL,
  CHECK ((latitude IS NULL) = (longitude IS NULL))
);

CREATE TABLE ${schema_prefix}canes.price_snapshot (
  snapshot_id varchar(128) PRIMARY KEY,
  location_key varchar(256) NOT NULL,
  amount numeric(12,2) NOT NULL CHECK (amount >= 0),
  currency char(3) NOT NULL,
  captured_at timestamptz NOT NULL,
  UNIQUE (location_key, captured_at)
);

CREATE TABLE ${schema_prefix}platform.application_lease (
  lease_name varchar(128) PRIMARY KEY,
  owner_id varchar(256) NOT NULL,
  fence_token bigint NOT NULL CHECK (fence_token > 0),
  expires_at timestamptz NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT transaction_timestamp()
);
```

Verification:
- Schema tests prove coordinate pairing, VIN uniqueness, monetary scale, lease fencing, and every declared index.

#### Code Edit 2.5
- File: `website/src/main/resources/db/migration/postgresql-migration-catalog.yml`
- Lines: before 1
- Action: add

Proposed:
```yaml
version: 1
kinds:
  - sourceCollection: accounts
    sourceKind: account
    sourceSchemaVersion: 1
    transformerVersion: 1
    identifierType: string
    targetSchema: identity
    targetTables: [account]
    loadOrder: 100
    canonicalHash: sha256-rfc8785-v1
    reconciliation: [row-count, canonical-record-hash, normalized-email-uniqueness]
  - sourceCollection: content
    sourceKind: post
    sourceSchemaVersion: 1
    transformerVersion: 1
    identifierType: string
    targetSchema: social
    targetTables: [post]
    loadOrder: 200
    canonicalHash: sha256-rfc8785-v1
    reconciliation: [row-count, canonical-record-hash, author-foreign-key, feed-order]
```

Add one complete entry for each of the 52 manifest kinds listed in the approved specification. Each entry declares every source field and target column/child row, null/missing rules, enum/timestamp/numeric conversion, dependency/load order, key preservation, delete behavior, version/expiry semantics, canonical hash, port queries, and transformer class. `PostgresqlMigrationCatalogTest` compares the exact set with `DomainCollectionManifest` and rejects YAML aliases, duplicate keys, unknown properties, undeclared JSONB, or source wildcards.

Verification:
- `./gradlew.bat :website:test --tests '*PostgresqlMigrationCatalogTest' --tests '*JooqGenerationReproducibilityTest' --console=plain`

### Task 3 - Implement identity, social, communication, and federation PostgreSQL adapters

Sequence / dependencies:
- Depends on Tasks 1-2. This is the first port-parity slice and establishes the shared adapter contract harness.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: implement existing ports and Mongo-backed query services with typed jOOQ queries and explicit transactions.
  - Invariants: public/service behavior, stable cursor order, atomic optimistic updates, uniqueness, privacy filters, and foreign-key semantics match Mongo.
  - Boundary/API: ports remain unchanged; adapters are activated only by `@PostgresPersistence`.
  - Effects and failures: map unique/FK/serialization conflicts to existing domain exceptions without leaking SQL or credentials.
  - Tests and evidence: run one shared port contract suite against Mongo and PostgreSQL, plus PostgreSQL concurrency/query-plan tests.

- [ ] **Step 1: Extract persistence-neutral contract fixtures from existing Mongo tests and make PostgreSQL cases fail.**
- [ ] **Step 2: Implement account/session/follow/trust/deletion adapters and transactional account deletion.**
- [ ] **Step 3: Implement posts/likes/reports/hides/previews and all discovery/feed/report query services.**
- [ ] **Step 4: Implement messages/archive, notifications/preferences/guards/rate limits, federation scans/delivery, and queries.**
- [ ] **Step 5: Run contract, concurrency, architecture, and query-plan tests; commit `feat: migrate core social persistence to PostgreSQL`.**

#### Code Edit 3.1
- File: `website/src/test/java/dev/christopherbell/configuration/postgresql/PersistencePortContract.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.postgresql;

public interface PersistencePortContract<T> {
  T createFixture();
  T save(T value);
  java.util.Optional<T> findById(String id);
  void deleteById(String id);

  default void verifyCrudRoundTrip() {
    T expected = createFixture();
    T saved = save(expected);
    org.assertj.core.api.Assertions.assertThat(findById(identityOf(saved))).contains(saved);
    deleteById(identityOf(saved));
    org.assertj.core.api.Assertions.assertThat(findById(identityOf(saved))).isEmpty();
  }

  String identityOf(T value);
}
```

Domain-specific contracts add pagination, optimistic-lock, lifecycle, aggregation, and atomic-operation scenarios; Mongo and PostgreSQL adapters must pass the same assertions until Mongo retirement.

Verification:
- `./gradlew.bat :website:test --tests '*PortContract*' --console=plain`

#### Code Edit 3.2
- File: `website/src/main/java/dev/christopherbell/account/PostgresAccountRepository.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.account;

import static dev.christopherbell.jooq.identity.tables.Account.ACCOUNT;

import dev.christopherbell.account.model.Account;
import dev.christopherbell.configuration.persistence.PostgresPersistence;
import java.util.Optional;
import org.jooq.DSLContext;

@PostgresPersistence
public final class PostgresAccountRepository implements AccountRepository {
  private final DSLContext database;
  private final PostgresAccountMapper mapper;

  public PostgresAccountRepository(DSLContext database, PostgresAccountMapper mapper) {
    this.database = database;
    this.mapper = mapper;
  }

  @Override
  public Optional<Account> findById(String accountId) {
    return database.selectFrom(ACCOUNT)
        .where(ACCOUNT.ACCOUNT_ID.eq(accountId))
        .fetchOptional(mapper::fromRecord);
  }
}
```

Implement all methods of the unchanged `AccountRepository`; updates use `WHERE account_id = ? AND version = ?`, increment version once, and require exactly one affected row.

Verification:
- `PostgresAccountRepositoryContractTest` and two-writer optimistic-lock tests pass in a unique PostgreSQL test schema.

#### Code Edit 3.3
- File: `website/src/main/java/dev/christopherbell/post/feed/PostFeedQueryRepository.java`
- Lines: 1-161
- Action: replace

Current:
```java
@Repository
public class PostFeedQueryRepository {
  private final DomainMongoOperationsFactory operationsFactory;
  // Mongo aggregation implementation
}
```

Proposed:
```java
public interface PostFeedQueryRepository {
  PostFeedPage findFeed(PostFeedQuery query);
}
```

Move the current body unchanged in behavior to `MongoPostFeedQueryRepository` with `@MongoPersistence`; add `PostgresPostFeedQueryRepository` with a jOOQ keyset query ordered by `(created_at DESC, post_id DESC)`, explicit relationship/privacy joins, and the same cursor encoding.

Verification:
- Shared fixtures produce identical ordered IDs, cursors, visibility filtering, and expiration behavior on both backends; PostgreSQL `EXPLAIN (FORMAT JSON)` uses the declared feed indexes.

#### Code Edit 3.4
- File: `website/src/test/java/dev/christopherbell/architecture/PostgresqlPersistenceBoundaryRules.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

final class PostgresqlPersistenceBoundaryRules {
  static final com.tngtech.archunit.lang.ArchRule DOMAIN_CODE_DOES_NOT_DEPEND_ON_JOOQ =
      noClasses().that().resideOutsideOfPackage("..configuration.postgresql..")
          .and().haveSimpleNameNotStartingWith("Postgres")
          .should().dependOnClassesThat().resideInAnyPackage("org.jooq..", "java.sql..",
              "org.postgresql..");

  private PostgresqlPersistenceBoundaryRules() {}
}
```

Verification:
- Architecture tests additionally require all `Postgres*` adapters to implement an existing port and carry `@PostgresPersistence`.

#### Adapter inventory for Task 3

- Identity: `AccountRepository`, `AccountLoginStore`, `AccountFollowStore`, `AccountTrustRepository`, `AccountDeletionJobRepository`, `AccountDeletionOperations`, browser session repository/activity/authentication stores, and conversation archive state.
- Social: `PostRepository`, `PostLikeStore`, `ReportRepository`, hidden-thread and link-preview repositories; feed/engagement/void/people/report query services; post expiration cleanup.
- Communication: `MessageRepository`, conversation query repository, notification repository/preference/query, fanout guard, and rate-limit bucket store.
- Federation: outbox query, scan state, and delivery store/repository.

### Task 4 - Implement music and shared-folder PostgreSQL adapters

Sequence / dependencies:
- Depends on Tasks 1-3 for shared adapter contracts and transaction/error mapping.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: preserve music catalog/playlist/runtime/audit behavior and all shared-folder durable work/lease/recovery flows.
  - Invariants: filesystem remains the content authority; database paths are normalized relative paths; playlists preserve order; leases use database time and fencing; recovery/job claims are atomic and idempotent.
  - Boundary/API: existing music and shared-folder ports stay stable.
  - Effects and failures: transactions never hold across filesystem or media-process calls; claimed work records durable intent before external effects and records completion afterward.
  - Tests and evidence: shared port parity, contention, crash/retry, ordered membership, and alternate-port UI/API smoke flows.

- [ ] **Step 1: Add failing PostgreSQL contract cases for every music and shared-folder port.**
- [ ] **Step 2: Implement music catalog, playlist, metadata, runtime, radio history, and access audit adapters.**
- [ ] **Step 3: Implement shared audit, maintenance, media, recovery, radio, recycle, and upload adapters.**
- [ ] **Step 4: Prove atomic claims and lease fencing under concurrent connections and crash/retry simulations.**
- [ ] **Step 5: Run focused and architecture tests; commit `feat: migrate media persistence to PostgreSQL`.**

#### Code Edit 4.1
- File: `website/src/main/java/dev/christopherbell/music/library/PostgresMusicPlaylistRepository.java`
- Lines: before 1
- Action: add

Proposed:
```java
@PostgresPersistence
public final class PostgresMusicPlaylistRepository implements MusicPlaylistRepository {
  private final org.jooq.DSLContext database;
  private final PostgresMusicPlaylistMapper mapper;

  @Override
  public MusicPlaylist save(MusicPlaylist playlist) {
    return database.transactionResult(configuration -> {
      var transaction = org.jooq.impl.DSL.using(configuration);
      mapper.upsertPlaylist(transaction, playlist);
      transaction.deleteFrom(PLAYLIST_TRACK)
          .where(PLAYLIST_TRACK.PLAYLIST_ID.eq(playlist.getId())).execute();
      mapper.insertTracksInOrder(transaction, playlist);
      return mapper.requirePlaylist(transaction, playlist.getId());
    });
  }
}
```

Verification:
- Contract tests prove duplicate/order semantics and transaction rollback leaves the prior playlist unchanged.

#### Code Edit 4.2
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/mongo/lease/MongoLeaseStore.java`
- Lines: 1-12
- Action: replace

Current:
```java
package dev.christopherbell.libs.mongo.lease;
// Mongo-specific lease interface and document contract
```

Proposed:
```java
package dev.christopherbell.libs.lease;

import java.time.Duration;
import java.util.Optional;

public interface LeaseStore {
  Optional<LeaseGrant> tryAcquire(String leaseName, String ownerId, Duration duration);
  Optional<LeaseGrant> renew(LeaseGrant grant, Duration duration);
  boolean release(LeaseGrant grant);
}
```

`LeaseGrant` carries lease name, owner, monotonic fence token, and database-issued expiration. Update consumers to the neutral port; keep `MongoLeaseStoreAdapter` only for transition parity.

Verification:
- Both adapters pass the same acquisition, expiration, renewal, stale-fence, and release contract.

#### Code Edit 4.3
- File: `website/src/main/java/dev/christopherbell/sharedfolder/maintenance/PostgresSharedFolderMaintenanceLeaseStore.java`
- Lines: before 1
- Action: add

Proposed:
```java
@PostgresPersistence
final class PostgresSharedFolderMaintenanceLeaseStore
    implements SharedFolderMaintenanceLeaseStore {
  private final org.jooq.DSLContext database;

  @Override
  public boolean tryAcquire(String leaseName, String ownerId, java.time.Duration duration) {
    return database.insertInto(MAINTENANCE_LEASE)
        .set(MAINTENANCE_LEASE.LEASE_NAME, leaseName)
        .set(MAINTENANCE_LEASE.OWNER_ID, ownerId)
        .set(MAINTENANCE_LEASE.FENCE_TOKEN, 1L)
        .set(MAINTENANCE_LEASE.EXPIRES_AT,
            org.jooq.impl.DSL.currentOffsetDateTime().add(duration.toSeconds()))
        .onConflict(MAINTENANCE_LEASE.LEASE_NAME)
        .doUpdate()
        .set(MAINTENANCE_LEASE.OWNER_ID, ownerId)
        .set(MAINTENANCE_LEASE.FENCE_TOKEN, MAINTENANCE_LEASE.FENCE_TOKEN.plus(1L))
        .where(MAINTENANCE_LEASE.EXPIRES_AT.lt(org.jooq.impl.DSL.currentOffsetDateTime()))
        .execute() == 1;
  }
}
```

Use a dialect-safe jOOQ interval expression verified against PostgreSQL rather than application time.

Verification:
- A two-connection test proves only one owner can hold a live lease and every takeover increases the fence token.

#### Adapter inventory for Task 4

- Music: track, playlist, metadata edit, radio history, runtime state, access-attempt recorder/query, catalog/query configuration.
- Shared folder: audit repository/sink/query, maintenance lease, media job, mutation recovery, radio state, recycle item, and upload session.

### Task 5 - Implement mobility, lunch, canes, admin, and platform PostgreSQL adapters

Sequence / dependencies:
- Depends on Tasks 1-4 and completes PostgreSQL coverage of all runtime ports.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: implement remaining domain adapters and platform stores without changing service behavior.
  - Invariants: VIN and restaurant normalized-name uniqueness, real location integrity, stable session/vote/pick ordering, money precision, scheduled-run atomicity, and admin audit immutability.
  - Boundary/API: existing domain ports remain stable; shared library types become engine-neutral.
  - Effects and failures: unique conflicts preserve current winner/progress semantics; scheduled claims and leases use database time; batch imports preserve later-candidate progress.
  - Tests and evidence: shared parity, unique-race, import-resume, location-integrity, lease, scheduler, and query-plan cases.

- [ ] **Step 1: Add failing contracts for every remaining port and direct Mongo query service.**
- [ ] **Step 2: Implement vehicle/VIN/ZIP and Canes adapters.**
- [ ] **Step 3: Implement restaurants, votes, favorites, preferences, sessions, picks, and import adapters.**
- [ ] **Step 4: Implement admin activity, pending actions, application leases, scheduled runs, and direct metrics queries.**
- [ ] **Step 5: Run focused tests and full adapter coverage audit; commit `feat: complete PostgreSQL domain adapters`.**

#### Code Edit 5.1
- File: `website/src/main/java/dev/christopherbell/whatsforlunch/restaurant/PostgresRestaurantRepository.java`
- Lines: before 1
- Action: add

Proposed:
```java
@PostgresPersistence
public final class PostgresRestaurantRepository implements RestaurantRepository {
  private final org.jooq.DSLContext database;
  private final PostgresRestaurantMapper mapper;

  @Override
  public Restaurant save(Restaurant candidate) {
    return database.transactionResult(configuration -> {
      var transaction = org.jooq.impl.DSL.using(configuration);
      var owner = transaction.selectFrom(RESTAURANT)
          .where(RESTAURANT.NORMALIZED_NAME.eq(candidate.getNormalizedName()))
          .forUpdate()
          .fetchOne();
      return mapper.saveAgainstResolvedOwner(transaction, candidate, owner);
    });
  }
}
```

The mapper preserves the current ID-first ownership rules and real locality/state/country/coordinate requirements. It never invents `Imported Metro, TX` or another placeholder.

Verification:
- Parallel normalized-name collision tests preserve one owner and continue later candidates; location-integrity tests reject fabricated or incomplete locality.

#### Code Edit 5.2
- File: `website/src/main/java/dev/christopherbell/configuration/postgresql/runtime/PostgresApplicationLeaseStore.java`
- Lines: before 1
- Action: add

Proposed:
```java
@PostgresPersistence
public final class PostgresApplicationLeaseStore implements LeaseStore {
  private final org.jooq.DSLContext database;

  @Override
  public Optional<LeaseGrant> tryAcquire(String leaseName, String ownerId, Duration duration) {
    return database.transactionResult(configuration ->
        PostgresLeaseStatements.tryAcquire(
            org.jooq.impl.DSL.using(configuration), leaseName, ownerId, duration));
  }
}
```

Verification:
- Scheduler tests prove expired-work takeover, stale-token rejection, and no duplicate collector run.

#### Code Edit 5.3
- File: `website/src/test/java/dev/christopherbell/architecture/PostgresqlAdapterCoverageTest.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Test
void everyMongoRuntimePortHasExactlyOnePostgresqlImplementation() {
  assertThat(PostgresqlAdapterCatalog.actualPorts())
      .containsExactlyInAnyOrderElementsOf(PostgresqlAdapterCatalog.requiredPorts());
  assertThat(PostgresqlAdapterCatalog.duplicates()).isEmpty();
  assertThat(PostgresqlAdapterCatalog.missing()).isEmpty();
}
```

The required list covers all named Mongo adapters and direct `DomainMongoOperationsFactory`, `KindScopedMongoOperations`, `MongoTemplate`, `MongoOperations`, and `MongoRepository` consumers discovered from production sources.

Verification:
- `rg -l 'DomainMongoOperationsFactory|KindScopedMongoOperations|MongoTemplate|MongoOperations|MongoRepository' website/src/main/java cbell-lib/src/main/java` is fully classified as transition adapter, migration reader, or retirement deletion.

#### Adapter inventory for Task 5

- Mobility: vehicle repository, VIN decode cache, NHTSA import state, random-VIN import state, ZIP coordinate repository/import state.
- Lunch: restaurant, daily picks, import state/preview, favorites, preferences, sessions/mutation, votes, inventory/duplicate/vote query repositories.
- Canes: price snapshot repository.
- Platform/admin: admin activity repository/query, pending action store, command-center metrics, application lease, scheduled collector run.

### Task 6 - Build the guarded, resumable Mongo-to-PostgreSQL migration and reconciliation engine

Sequence / dependencies:
- Depends on complete DDL, catalog, and PostgreSQL adapters in Tasks 1-5.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: read each approved kind from Mongo, deterministically transform into staging tables, checkpoint committed batches, reconcile, and transactionally publish complete kinds.
  - Invariants: Mongo is read-only; unknown input fails closed; no incomplete kind is visible; reruns are idempotent; exact-source deletion is allowed only when source-frozen evidence is valid.
  - Boundary/API: a non-web Java command accepts `shadow`, `finalize`, `reconcile`, and `status`; ordinary website role and HTTP routes cannot invoke it.
  - Effects and failures: bounded transactions persist checkpoints; errors redact payloads/credentials; interruption resumes from durable ledgers without guessing.
  - Tests and evidence: malformed/unknown inputs, all 52 transformers, batch interruption/resume, hash mismatch, FK mismatch, idempotence, frozen-source deletion guard, and end-to-end disposable database migration.

- [ ] **Step 1: Add failing catalog-transformer completeness and canonical-hash tests.**
- [ ] **Step 2: Implement validated command options, protected role/identity checks, staging schema lifecycle, and ledger.**
- [ ] **Step 3: Implement transformers in catalog load order and batch checkpoint/resume.**
- [ ] **Step 4: Implement count/hash/relationship/query reconciliation and transactional publication.**
- [ ] **Step 5: Run full disposable Mongo-to-PostgreSQL migration twice plus interruption matrix; commit `feat: add Mongo to PostgreSQL migration engine`.**

#### Code Edit 6.1
- File: `website/src/main/java/dev/christopherbell/configuration/postgresql/migration/PostgresqlMigrationCommand.java`
- Lines: before 1
- Action: add

Proposed:
```java
package dev.christopherbell.configuration.postgresql.migration;

public enum PostgresqlMigrationCommand {
  SHADOW,
  FINALIZE,
  RECONCILE,
  STATUS
}
```

Verification:
- Command parsing accepts only `shadow`, `finalize`, `reconcile`, and `status`, with `finalize` requiring frozen-source evidence.

#### Code Edit 6.2
- File: `website/src/main/java/dev/christopherbell/configuration/postgresql/migration/PostgresqlMigrationRunner.java`
- Lines: before 1
- Action: add

Proposed:
```java
public final class PostgresqlMigrationRunner {
  private final MigrationPreflight preflight;
  private final MigrationCatalog catalog;
  private final KindMigrationEngine engine;
  private final MigrationReconciler reconciler;

  public MigrationResult run(MigrationRequest request) {
    ValidatedMigrationContext context = preflight.validate(request);
    for (MigrationKind kind : catalog.inLoadOrder()) {
      engine.stageAndCheckpoint(context, kind);
      reconciler.requireStagedKindEquivalent(context, kind);
      engine.publishKind(context, kind);
    }
    return reconciler.requireCompleteRunEquivalent(context);
  }
}
```

`MigrationPreflight` verifies exact source/target database names, loopback endpoints, non-website migration role, catalog checksum, release, mode, protected lock evidence, and `sourceFrozen` proof for finalization.

Verification:
- Unit tests prove every invalid identity/mode/role/lock combination fails before reading a source document or writing a target row.

#### Code Edit 6.3
- File: `website/src/main/java/dev/christopherbell/configuration/postgresql/migration/KindMigrationEngine.java`
- Lines: before 1
- Action: add

Proposed:
```java
public final class KindMigrationEngine {
  public void stageAndCheckpoint(ValidatedMigrationContext context, MigrationKind kind) {
    MigrationCheckpoint checkpoint = context.ledger().checkpoint(kind);
    while (!checkpoint.complete()) {
      SourceBatch batch = context.source().readAfter(kind, checkpoint.cursor(), kind.batchSize());
      if (batch.isEmpty()) {
        context.ledger().markStagingComplete(kind, checkpoint);
        return;
      }
      checkpoint = context.target().transaction(transaction -> {
        StagedBatch transformed = kind.transformer().transform(batch);
        transaction.stage(kind, transformed);
        transaction.recordSourceHashes(kind, transformed);
        return transaction.advanceCheckpoint(kind, batch.lastCursor());
      });
    }
  }
}
```

Verification:
- Kill after source read, staging write, ledger write, reconciliation, and publication; every restart converges to the same counts and canonical hashes.

#### Code Edit 6.4
- File: `website/src/test/java/dev/christopherbell/configuration/postgresql/migration/MongoToPostgresqlMigrationAcceptanceTest.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Test
void migratesEveryManifestKindTwiceWithoutChangingTheResult() {
  FixtureInventory source = fixtures.insertAllKindsWithBoundaryValues();
  MigrationResult first = runner.run(shadowRequest());
  MigrationResult second = runner.run(shadowRequest());

  assertThat(first.sourceKinds()).containsExactlyInAnyOrderElementsOf(source.kinds());
  assertThat(first.reconciliationFailures()).isEmpty();
  assertThat(second.targetDigest()).isEqualTo(first.targetDigest());
  assertThat(mongoFixture.digest()).isEqualTo(source.digest());
}
```

Verification:
- Acceptance fixtures include missing/null distinction, Unicode, extreme timestamps/numerics, array order/duplicates, all enum values, relationship edges, TTL-eligible and ineligible records, and ID shapes from production inventory.

### Task 7 - Add native Windows PostgreSQL, pgAdmin, backup/restore, status, and access controls

Sequence / dependencies:
- Can begin after Task 2 but must be complete before any production shadow run.

Implementation notes:
- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: install/configure native PostgreSQL 18, create least-privilege roles/databases, install pgAdmin 4 Desktop, manage backups/restores, and expose guarded status commands.
  - Invariants: loopback-only listener; SCRAM authentication; app cannot migrate; viewer cannot write; migration role unavailable to normal service; no privileged pgAdmin credential; protected ACLs remain intact.
  - Boundary/API: `prod.ps1` provides explicit idempotent commands; all mutations support `-WhatIf`, exact identity checks, and protected lock where applicable.
  - Effects and failures: installers validate signatures/versions; partial bootstrap is safely resumable; secrets never cross stdout; backups are checksummed and dry-restored.
  - Tests and evidence: Pester unit/integration tests, native service/listener checks, role capability probes, pgAdmin connection tests, backup/dry-restore evidence.

- [ ] **Step 1: Add failing Pester tests for config, commands, role SQL, pgAdmin registrations, backup, restore, and status.**
- [ ] **Step 2: Implement native PostgreSQL install and loopback/SCRAM bootstrap.**
- [ ] **Step 3: Create owner, migrator, app, bridge, viewer, and backup roles plus production and `test` databases.**
- [ ] **Step 4: Install pgAdmin 4 Desktop and register RW `christopherbell-test` plus RO `christopherbell-production-viewer` without storing privileged secrets.**
- [ ] **Step 5: Implement checksummed custom-format backup, isolated dry restore, status/monitoring, and docs; commit `feat: add native PostgreSQL operations`.**

#### Code Edit 7.1
- File: `ops/production/windows/prod.ps1`
- Lines: 1-79
- Action: replace

Current:
```powershell
[ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup',
  'mongo-inventory','mongo-consolidation-preview','mongo-consolidate',
  'mongo-consolidation-rollback','verify-startup','uninstall')]
```

Proposed:
```powershell
[ValidateSet('help','install','deploy','status','logs','restart','releases','rollback','backup',
  'postgres-install','postgres-bootstrap','postgres-status','postgres-backup',
  'postgres-restore-check','postgres-pgadmin','postgres-shadow','postgres-reconcile',
  'postgres-cutover','postgres-soak-status','postgres-retire-mongo',
  'mongo-inventory','verify-startup','uninstall')]
```

Import `Production.PostgreSql.psm1` and `Production.PostgreSqlMigration.psm1`. Cutover and retirement handlers require separate explicit switches, reject `-WhatIf` bypass, and delegate to protected functions rather than embedding SQL.

Verification:
- `Production.Command.Tests.ps1` proves every validate-set entry has one handler and destructive commands require their exact confirmation switch.

#### Code Edit 7.2
- File: `ops/production/windows/config/deploy.example.json`
- Lines: 1-24
- Action: replace

Current:
```json
"mongoToolsPath": "C:\\Program Files\\MongoDB\\Tools\\100\\bin",
"mongoShellExe": "C:\\Program Files\\MongoDB\\mongosh\\current\\bin\\mongosh.exe",
"backupRoot": "A:\\Projects\\christopherbell.dev-backups"
```

Proposed:
```json
"postgresqlVersion": "18.4",
"postgresqlBinPath": "C:\\Program Files\\PostgreSQL\\18\\bin",
"postgresqlServiceName": "postgresql-x64-18",
"pgAdminExe": "C:\\Program Files\\pgAdmin 4\\runtime\\pgAdmin4.exe",
"postgresqlBackupRoot": "A:\\Projects\\christopherbell.dev-postgresql-backups",
"mongoToolsPath": "C:\\Program Files\\MongoDB\\Tools\\100\\bin",
"mongoShellExe": "C:\\Program Files\\MongoDB\\mongosh\\current\\bin\\mongosh.exe"
```

Mongo tools remain transition-only until Task 10.

Verification:
- Config validation requires resolved absolute executable/root paths under expected locations and exact supported major version.

#### Code Edit 7.3
- File: `ops/production/windows/config/app.env.example`
- Lines: 1-7
- Action: replace

Current:
```dotenv
SPRING_MONGODB_URI=mongodb://127.0.0.1:27017
```

Proposed:
```dotenv
APP_PERSISTENCE_BACKEND=postgresql
SPRING_DATASOURCE_URL=jdbc:postgresql://127.0.0.1:5432/christopherbell
SPRING_DATASOURCE_USERNAME=christopherbell_app
SPRING_DATASOURCE_PASSWORD=replace-with-protected-app-role-secret
```

The migration bridge uses a separate protected environment file and role; it is never merged into the website service environment.

Verification:
- Environment validation rejects missing backend/JDBC values, non-loopback production URLs, app username mismatch, and Mongo authority after retirement marker publication.

#### Code Edit 7.4
- File: `ops/production/windows/modules/Production.PostgreSql.psm1`
- Lines: before 1
- Action: add

Proposed:
```powershell
function New-ProductionPostgreSqlBackup {
    [CmdletBinding()]
    param([Parameter(Mandatory)][pscustomobject]$Config)

    $identity = Assert-ProductionPostgreSqlIdentity -Config $Config -ExpectedDatabase 'christopherbell'
    $archive = New-ValidatedPostgreSqlBackupPath -Config $Config -Database $identity.Database
    Invoke-CheckedProcess -FilePath (Join-Path $Config.postgresqlBinPath 'pg_dump.exe') `
        -ArgumentList @('--format=custom','--no-owner','--no-privileges',
            '--file', $archive, '--dbname', $identity.RedactedConnectionName)
    $digest = Get-FileHash -LiteralPath $archive -Algorithm SHA256
    Test-ProductionPostgreSqlRestore -Config $Config -Archive $archive -ExpectedDigest $digest.Hash
}
```

The module also implements version/signature checks, installer/bootstrap, `listen_addresses='localhost'`, SCRAM `pg_hba.conf`, role grants/default privileges, database identity, schema migration under the migrator, viewer transaction read-only enforcement, status, and pgAdmin registration.

Verification:
- `Invoke-Pester ops/production/windows/tests/Production.PostgreSql.Tests.ps1 -Output Detailed`

#### Code Edit 7.5
- File: `ops/production/windows/service/ChristopherBellDev.xml`
- Lines: 1-19
- Action: replace

Current:
```xml
<depend>MongoDB</depend>
```

Proposed:
```xml
<depend>postgresql-x64-18</depend>
```

Verification:
- Installed service dependency readback contains PostgreSQL and does not contain MongoDB after cutover-ready deployment.

#### Code Edit 7.6
- File: `docs/operations/postgresql.md`
- Lines: before 1
- Action: add

Proposed:
```markdown
# PostgreSQL Operations

Production PostgreSQL is a loopback-only native Windows service. The website connects as
`christopherbell_app`; Flyway runs only as `christopherbell_migrator`; pgAdmin production
inspection uses `christopherbell_viewer` with database-enforced read-only transactions.

pgAdmin registers `christopherbell-test` for read/write development and
`christopherbell-production-viewer` for production inspection. Never save owner,
migrator, bridge, or backup credentials in pgAdmin.
```

Add exact install, connection, role, backup, dry-restore, monitoring, shadow, cutover, soak, retirement, and incident procedures with redacted command examples.

Verification:
- Documentation tests match command names, role names, database names, ports, and retention gates in code.

### Task 8 - Rehearse shadow migration and validate a PostgreSQL candidate runtime

Sequence / dependencies:
- Depends on Tasks 1-7. This task produces evidence; it does not transfer production authority.

Implementation notes:
- Required skill: `chris-street-style` before any needed test/tool correction.
- Before-Edit Brief:
  - Behavior: repeatedly refresh a non-authoritative PostgreSQL shadow, reconcile it, and run the candidate website against that shadow on a non-8080 port.
  - Invariants: Mongo remains authoritative and unchanged; no production listener, service dependency, or backend marker changes; candidate uses only PostgreSQL after startup.
  - Boundary/API: guarded PowerShell orchestration invokes the migration CLI and existing alternate-port verifier.
  - Effects and failures: a failed rehearsal drops only the exact run-owned staging/shadow schemas after identity checks; it never changes production authority.
  - Tests and evidence: restored-clone plus live-source shadow, all-kind counts/hashes/relationships, representative API/UI flows, health backend detail, scheduled work, and performance budgets.

- [ ] **Step 1: Run a complete migration from a dry-restored Mongo archive into an isolated PostgreSQL database/schema.**
- [ ] **Step 2: Run two live-source shadows and prove idempotence plus reconciliation of all 52 kinds.**
- [ ] **Step 3: Start the candidate on an approved non-8080 port with PostgreSQL backend and mutation sources disabled.**
- [ ] **Step 4: Exercise authentication, account, posts, messages, notifications, music, shared folder, vehicles, lunch, admin, health, and scheduled-job flows with exact request/response evidence.**
- [ ] **Step 5: Record query plans and latency/capacity checks, save the Builder test report, and commit any evidence-only docs as required.**

#### Code Edit 8.1
- File: `ops/production/windows/modules/Production.PostgreSqlMigration.psm1`
- Lines: before 1
- Action: add

Proposed:
```powershell
function Invoke-ProductionPostgreSqlShadow {
    [CmdletBinding(SupportsShouldProcess)]
    param([Parameter(Mandatory)][pscustomobject]$Config)

    $state = Assert-PostgreSqlMigrationPreflight -Config $Config -Mode Shadow
    if ($PSCmdlet.ShouldProcess($state.RedactedTarget, 'refresh PostgreSQL shadow')) {
        Invoke-PostgreSqlMigrationJar -State $state -Mode shadow
        Assert-PostgreSqlReconciliation -State $state -RequireAllKinds
    }
}
```

Verification:
- Pester proves mode and identity checks precede process invocation and `-WhatIf` performs no write.

#### Code Edit 8.2
- File: `website/src/main/java/dev/christopherbell/configuration/persistence/PersistenceHealthIndicator.java`
- Lines: before 1
- Action: add

Proposed:
```java
@Component
public final class PersistenceHealthIndicator implements HealthIndicator {
  private final PersistenceBackend backend;
  private final PersistenceIdentityProbe probe;

  @Override
  public Health health() {
    PersistenceIdentity identity = probe.requireIdentity();
    return Health.up()
        .withDetail("backend", backend.name().toLowerCase(java.util.Locale.ROOT))
        .withDetail("database", identity.redactedDatabaseName())
        .withDetail("schemaVersion", identity.schemaVersion())
        .build();
  }
}
```

Verification:
- Candidate `/actuator/health` reports `backend=postgresql`, expected redacted database identity, and Flyway schema version without credentials.

### Task 9 - Execute the guarded production authority cutover

Sequence / dependencies:
- Depends on a passing Task 8 test report, merged code, green CI, verified final backup/restore tooling, and an approved maintenance window.

Implementation notes:
- Required skill: `chris-street-style` before any required correction; do not improvise unreviewed production mutations.
- Before-Edit Brief:
  - Behavior: transfer authority once from frozen Mongo to fully reconciled PostgreSQL and restore public service within 30 minutes.
  - Invariants: one protected lock; all writers stopped; final archive dry-restored; frozen-source evidence binds catalog/release/digests; candidate passes before listener rotation; no post-authority Mongo fallback.
  - Boundary/API: `prod.ps1 postgres-cutover -ConfirmPostgreSqlCutover`; no lower-level function is directly exposed.
  - Effects and failures: before authority marker, restore untouched Mongo service; after marker and accepted PG write, recover PostgreSQL forward from backup/WAL and keep Mongo frozen.
  - Tests and evidence: timestamped state transitions, final hashes, service/listener identity, exact request/status/body, write/read round trips, jobs/leases, pgAdmin viewer denial, backup, and rollback-boundary proof.

- [ ] **Step 1: Acquire lock, disable website recovery, stop website/media/scheduled writers, and prove no Mongo sessions can write.**
- [ ] **Step 2: Create and dry-restore the final checksummed Mongo archive.**
- [ ] **Step 3: Finalize PostgreSQL from frozen Mongo, reconcile every kind/relationship/hash, and create a PostgreSQL backup.**
- [ ] **Step 4: Start the PostgreSQL candidate on the alternate port, verify, publish the authority marker, rotate the production listener/service dependency, and re-enable recovery.**
- [ ] **Step 5: Verify public reads/writes/jobs/viewer role/backup and record production test evidence; enter the 14-day soak.**

#### Code Edit 9.1
- File: `ops/production/windows/modules/Production.PostgreSqlMigration.psm1`
- Lines: after 1
- Action: add

Proposed:
```powershell
function Invoke-ProductionPostgreSqlCutover {
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory)][pscustomobject]$Config,
        [Parameter(Mandatory)][switch]$Confirm
    )
    if (-not $Confirm) { throw 'PostgreSQL authority cutover requires explicit confirmation.' }
    Use-ProductionDeploymentLock -Config $Config -Operation {
        $state = Stop-AndAssertAllMongoWriters -Config $Config
        $state = Add-FinalMongoBackupEvidence -State $state
        $state = Invoke-FrozenSourcePostgreSqlFinalize -State $state
        $state = Assert-PostgreSqlReconciliation -State $state -RequireAllKinds
        $state = Test-PostgreSqlCandidate -State $state -Port $Config.candidatePort
        $state = Publish-PostgreSqlAuthorityMarker -State $state
        Set-WebsitePostgreSqlAuthority -State $state
        Assert-ProductionPostgreSqlAcceptance -State $state
        Enter-MongoFrozenSoak -State $state -Days 14 -ArchiveRetentionDays 90
    }
}
```

Every transition is durably journaled with prior/next state, release, database identities, catalog digest, reconciliation digest, archive digest, and timestamp. Resume dispatches only from a recognized fully evidenced state.

Verification:
- Pester transition matrix rejects missing, stale, reordered, cross-release, cross-database, or tampered evidence and proves rollback is available only before the authority marker.

### Task 10 - Complete the soak, retire Mongo, and close delivery

Sequence / dependencies:
- Begins after Task 9. Mongo retirement requires 14 full days of passing PostgreSQL production evidence and a valid 90-day archive-retention marker.

Implementation notes:
- Required skill: `chris-street-style` before code/config deletions.
- Before-Edit Brief:
  - Behavior: prove PostgreSQL stability, remove Mongo runtime/code/tooling/dependencies/service, retain the final archive for 90 days, and finish repository/Builder delivery.
  - Invariants: no Mongo client dependency or source remains; app has one PostgreSQL adapter per port; production service depends only on PostgreSQL; archive deletion remains separately time-gated.
  - Boundary/API: remove transition selector and make PostgreSQL unconditional; preserve domain ports and public APIs.
  - Effects and failures: retirement stops on any soak gap, reconciliation drift, backup failure, unresolved alert, Mongo use, or archive-retention mismatch.
  - Tests and evidence: 14 daily status/backup/restore samples, final architecture scan, clean build/test, alternate-port and production verification, dependency/service/config readback, and archive existence/checksum.

- [ ] **Step 1: Collect 14 days of health, error, latency, connection, job, reconciliation, backup, and restore evidence; resolve any critical/blocking issue before proceeding.**
- [ ] **Step 2: Run the retirement preflight and preserve the exact final Mongo archive/checksum/retention marker.**
- [ ] **Step 3: Delete Mongo adapters, query implementations, migration/domain-envelope code, Spring Data Mongo dependency, Mongo Compose service, and Mongo production commands/config/service dependencies.**
- [ ] **Step 4: Make PostgreSQL unconditional, run all unit/integration/architecture/Pester/build checks, verify alternate-port then production, and merge the retirement change.**
- [ ] **Step 5: Save final test report/session memory, close source issue/work ledger/hub work, refresh indexes, validate Builder, and commit/push Builder main.**

#### Code Edit 10.1
- File: `website/build.gradle.kts`
- Lines: 32-85
- Action: replace

Current:
```kotlin
implementation("org.springframework.boot:spring-boot-starter-data-mongodb") // transition only
implementation("org.springframework.boot:spring-boot-starter-flyway")
implementation("org.springframework.boot:spring-boot-starter-jooq")
```

Proposed:
```kotlin
implementation("org.springframework.boot:spring-boot-starter-flyway")
implementation("org.springframework.boot:spring-boot-starter-jooq")
runtimeOnly("org.flywaydb:flyway-database-postgresql")
runtimeOnly("org.postgresql:postgresql")
```

Delete the Mongo dependency from `cbell-lib/build.gradle.kts` after its lease types are persistence-neutral.

Verification:
- `./gradlew.bat dependencyInsight --dependency mongodb --configuration runtimeClasspath` reports no Mongo driver/starter.

#### Code Edit 10.2
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/domain/DomainCollectionManifest.java`
- Lines: 1-683
- Action: delete

Current:
```java
package dev.christopherbell.configuration.mongo;
// domain envelope, kind-scoped operations, startup preflight, and Mongo migrations V001-V015
```

Proposed:
```text
Directory absent. Flyway and PostgreSQL migration ledgers are the only active schema history.
```

Also delete every `Mongo*.java` adapter and transition-only `Mongo*QueryRepository` implementation. Keep persistence-neutral domain ports, models, and contract tests.

Verification:
- `rg -n 'Mongo|mongodb|mongosh|mongodump|mongorestore' website/src/main cbell-lib/src/main` returns no runtime persistence dependency; reviewed documentation/history allowlist is explicit.

#### Code Edit 10.3
- File: `compose.yaml`
- Lines: 1-18
- Action: replace

Current:
```yaml
services:
  mongodb:
    image: mongo:8.3.2
  postgresql:
    image: postgres:18.4
volumes:
  christopherbell_mongo_data: {}
  christopherbell_postgresql_data: {}
```

Proposed:
```yaml
services:
  postgresql:
    image: postgres:18.4
    restart: unless-stopped
    environment:
      POSTGRES_DB: test
      POSTGRES_USER: christopherbell_test
      POSTGRES_PASSWORD: ${POSTGRES_TEST_PASSWORD:?set POSTGRES_TEST_PASSWORD}
    ports: ["127.0.0.1:5432:5432"]
    volumes: ["christopherbell_postgresql_data:/var/lib/postgresql"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U christopherbell_test -d test"]
volumes:
  christopherbell_postgresql_data: {}
```

Verification:
- Compose configuration contains no Mongo service/volume and still binds PostgreSQL only to loopback.

#### Code Edit 10.4
- File: `ops/production/windows/modules/Production.DomainCollections.psm1`
- Lines: 1-1947
- Action: delete

Current:
```powershell
# Mongo domain-collection preview, cutover, rollback, and inventory orchestration
```

Proposed:
```text
File absent. PostgreSQL operations and retained archive metadata replace runtime Mongo operations.
```

Delete Mongo consolidation scripts/tests and remove Mongo command handlers, config requirements, environment values, install behavior, backup calls, writer-start preflights, and service dependency. Retain one read-only archive-retention status command that does not require the Mongo service.

Verification:
- Pester proves production install/deploy/status/backup/rollback/worker-start paths require PostgreSQL and do not invoke Mongo executables.

#### Code Edit 10.5
- File: `README.md`
- Lines: 11-505
- Action: replace

Current:
```markdown
- MongoDB 8.3.2
Local MongoDB database: christopherbell
MongoDB-backed tests use database test.
```

Proposed:
```markdown
- PostgreSQL 18.4 with Flyway and generated jOOQ types
- pgAdmin 4 Desktop for visual database inspection

Local development and every database-backed test use PostgreSQL database `test` only.
Automated tests create disposable `cbtest_*` schemas and must refuse every other database.
Use pgAdmin connection `christopherbell-test` for local read/write inspection and
`christopherbell-production-viewer` for database-enforced read-only production inspection.
```

Verification:
- Documentation references match exact profiles, roles, commands, service names, backup format, pgAdmin registrations, soak, and archive retention behavior.

## Unit Testing

- Run mapper, transformer, catalog, backend-selection, canonical-hash, exception-translation, lease, cursor, and cleanup unit tests first for each task.
- Run each shared persistence-port contract against both transition backends until retirement, then retain the PostgreSQL contract cases.
- Use a unique `cbtest_*` schema in database `test` for every database-backed suite; verify and record `current_database()` and `current_schema()` before fixtures are written.

## Local Testing

- Start the PostgreSQL candidate on a non-8080 port with Mongo mutation sources disabled and `backend=postgresql` visible in health.
- Send representative authenticated and anonymous requests through account, posts, messages, notifications, music, shared-folder, vehicle, lunch, Canes, admin, health, and scheduled-work flows.
- Record URL/port, request or UI input, response status/body or UI state, and database readback in the Builder test report.
- Validate pgAdmin connection `christopherbell-test` can perform a disposable read/write transaction and `christopherbell-production-viewer` is denied writes by the database.

## Validation

| Layer | Required evidence |
|---|---|
| Unit | transformers, canonical hashes, mappers, error translation, catalog validation, identity guard |
| Database contract | every port on PostgreSQL; transition parity on Mongo; concurrency, cursor, TTL cleanup, leases, transactions |
| Schema | empty Flyway build, constraints/indexes/FKs, exact ten schemas, reproducible jOOQ generation |
| Migration | all 52 kinds, boundary values, interruption/resume, idempotence, count/hash/relationship/query reconciliation |
| Architecture | domain code isolated from jOOQ/JDBC/PostgreSQL/Mongo; exactly one adapter per port; no Mongo after retirement |
| Operations | Pester command/config/install/backup/restore/role/pgAdmin/cutover/soak/retirement transition matrix |
| Candidate runtime | non-8080 URL/port, exact request input, status/body, backend health detail, read/write/jobs |
| Production | listener/service identity, public endpoints, persistence round trips, viewer denial, backup/dry restore, 14-day soak |

## Required Verification Commands

Run with private `GRADLE_USER_HOME=A:\Projects\christopherbell.dev-gradle\postgresql-migration` and explicit database `test` configuration:

```powershell
$env:SPRING_PROFILES_ACTIVE = 'test'
$env:SPRING_DATASOURCE_URL = 'jdbc:postgresql://127.0.0.1:5432/test'
$env:SPRING_DATASOURCE_USERNAME = 'christopherbell_test'
$env:APP_TEST_SCHEMA = 'cbtest_plan_verification'
.\gradlew.bat clean check --no-daemon --stacktrace
Invoke-Pester ops/production/windows/tests -Output Detailed
```

Before any database-backed test, query `current_database()` and `current_schema()` and save evidence that they equal `test` and an owned disposable `cbtest_*` schema. Never run tests against local-development, staging, production, or any other database.

## Rollback or Recovery

- Before the PostgreSQL authority marker, stop the candidate and restart the untouched Mongo-backed release using the recorded service/recovery state.
- After the authority marker and any accepted PostgreSQL write, never return to stale Mongo. Restore PostgreSQL forward from the verified backup/WAL and reconcile against the PostgreSQL authority ledger.
- Interrupted shadow or staging runs resume from committed ledgers or delete only their exact run-owned staging schemas after database/run identity validation.
- Mongo remains stopped/frozen for the 14-day soak and its final checksummed archive remains recoverable for 90 days.

## Risks

- Relational transformation drift: block the kind through exact catalog/transformer/adapter/reconciliation completeness checks.
- Query semantic or performance drift: shared port contracts plus `EXPLAIN (FORMAT JSON)` assertions for high-volume paths.
- Native host conflict: validate installation, listener, roles, and candidate on non-production ports before dependency/listener changes.
- Cutover exceeds 30 minutes: abort before authority marker and restore untouched Mongo; after marker, recover PostgreSQL forward.
- Migration interruption: resume from committed batch/publication ledger; never infer state from partial tables.
- Credential exposure: separate roles/files, redacted process wrapper, no passwords in commands/reports/pgAdmin, protected ACLs.
- Viewer privilege drift: database-enforced `default_transaction_read_only`, revoked writes, and direct denial tests.
- Soak regression: keep Mongo frozen and archive intact, fix PostgreSQL forward, and postpone retirement.

## Completion Criteria

- PostgreSQL is the sole production persistence authority and the website passes exact public/runtime acceptance.
- Flyway creates the full schema from empty state and jOOQ generation is reproducible.
- Every former Mongo port/query has one passing PostgreSQL adapter and all 52 kinds reconcile exactly.
- Local development and every DB-backed test use only PostgreSQL database `test` with disposable unique schemas.
- Native PostgreSQL is loopback-only, backed up and dry-restored; least-privilege roles pass direct capability probes.
- pgAdmin 4 Desktop is installed with `christopherbell-test` RW and `christopherbell-production-viewer` RO connections and no privileged stored credential.
- Fourteen days of PostgreSQL soak evidence pass, Mongo runtime/code/service/tool dependencies are removed, and the final Mongo archive remains checksummed under a 90-day retention gate.
- Full Gradle and Pester suites, CI, merge, production verification, source issue closure, test report, session memory, indexes, Builder validation, and hub closure are complete.
