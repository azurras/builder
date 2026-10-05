# christopherbell.dev Shared Library Boundaries Implementation Plan

> **For agentic workers:** Execute this plan after the backend query/resource-bounds plan. Before editing production code, tests, build logic, or executable examples, invoke `chris-street-style` and `superpowers:test-driven-development`. Use a clean `codex/` worktree from refreshed `origin/main`; never edit the authoritative dirty checkout.

## Global Constraints

- Move code only when current production reuse or test-only ownership is demonstrated.
- Preserve public behavior and serialized Mongo document shapes; package relocation must not rename collections or fields.
- Do not create a generic dumping ground or move feature policy into `cbell-lib`.
- Keep dependencies in the narrowest consuming module.
- Complete package moves atomically in one commit so main never contains split ownership.
- The backend plan's JDK-only bounded response reader remains in `cbell-lib`; the Bucket4j store remains website-owned until a non-website consumer exists.

## Document Status

ready-for-execution

## Objective

Make `cbell-lib` a clearer shared foundation by moving stable cursor and Mongo lease primitives into it, exposing test utilities only through test fixtures, relocating website-only workflow code to WFL, and moving JWT dependencies to their sole production consumer.

## Goals

- Give pagination and Mongo lease primitives one shared Java owner.
- Remove test helpers from production artifacts.
- Remove JJWT from the library runtime/API surface.
- Move the workflow engine beside its sole WFL production consumer.
- Prove the resulting compile/runtime dependency graph and component discovery.

## Inputs

- Approved spec: `docs/specs/2026-07-29-christopherbell-dev-performance-scalability-library-optimization.md`
- Source baseline: `origin/main` at `f31535f29312d24573a6031b0162aa8ebc4b5318`
- Current reuse: pagination spans messages, notifications, federation, feeds, and discovery; leases span Canes, WFL, VIN, Music, migrations, and Shared Folder-related scheduling.
- Current single ownership: all production imports of `dev.christopherbell.libs.workflow` are in WFL.

## Branch

Create `codex/shared-library-boundaries` from the backend plan's merged commit, or stack it directly on that branch only when one combined PR is explicitly selected.

## Non-Goals

- No workflow-engine redesign.
- No new external library publication or semantic-versioning process.
- No Bucket4j dependency in `cbell-lib`.
- No generic abstraction for account/session feature policy.
- No behavioral changes to cursor encoding, lease renewal, or workflow retry rules.

## Assumptions

- `cbell-lib` remains an internal Gradle project dependency.
- Spring component scanning already includes `dev.christopherbell.libs` through application root scanning.
- The backend plan has added shared HTTP body-reading code before this plan begins.

## Open Questions

None. If a second non-WFL production workflow consumer exists at execution time, stop Task 5 and update the approved boundary rather than moving it.

## File Structure

- `cbell-lib/src/main/java/dev/christopherbell/libs/pagination/` — stable cursor API.
- `cbell-lib/src/main/java/dev/christopherbell/libs/mongo/lease/` — Mongo lease/coordinator API.
- `cbell-lib/src/testFixtures/java/dev/christopherbell/libs/test/TestUtil.java` — test-only JSON fixture helper.
- `website/src/main/java/dev/christopherbell/whatsforlunch/workflow/engine/` — WFL-owned workflow engine.

## Task Breakdown

### Task 1 - Move stable cursor primitives into cbell-lib

Sequence / dependencies:
- First task; independent of leases and dependency cleanup.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before tests, package moves, or import edits.
- Before-Edit Brief:
  - Behavior: cursor bytes, validation, exception types, and Spring injection remain identical.
  - Invariants: version prefix and timestamp/id ordering do not change.
  - Boundary/API: package becomes `dev.christopherbell.libs.pagination`.
  - Effects and failures: invalid cursor behavior remains fail-closed through `InvalidRequestException`.
  - Tests and evidence: move the codec tests first, then update all compile-time imports.

- [ ] Move tests to the library and run RED before moving production classes.
- [ ] Move both classes and rewrite every old-package import.
- [ ] Prove no `dev.christopherbell.pagination` references remain.

#### Code Edit 1.1
- File: `website/src/main/java/dev/christopherbell/pagination/{StableCursor,StableCursorCodec}.java`
- Lines: 1-57
- Action: move

Current:
```java
package dev.christopherbell.pagination;
```

Proposed:
```java
package dev.christopherbell.libs.pagination;
```

- Preserve every type member and codec byte format exactly. Delete the empty website package after all imports compile.

Verification:
- `./gradlew :cbell-lib:test :website:compileJava`
- `rg -n "dev\.christopherbell\.pagination" website cbell-lib` returns no matches.

#### Code Edit 1.2
- File: `website/src/{main,test}/java/**/*.java matching dev.christopherbell.pagination`
- Lines: 1-200
- Action: replace

Current:
```java
import dev.christopherbell.pagination.StableCursor;
import dev.christopherbell.pagination.StableCursorCodec;
```

Proposed:
```java
import dev.christopherbell.libs.pagination.StableCursor;
import dev.christopherbell.libs.pagination.StableCursorCodec;
```

Verification:
- `./gradlew :website:test --tests '*Cursor*' --tests '*ConversationQueryRepositoryTest' --tests '*NotificationQueryRepositoryTest' --tests '*PostFeedQueryRepositoryTest'`

#### Code Edit 1.3
- File: `website/src/test/java/dev/christopherbell/pagination/StableCursorCodecTest.java`
- Lines: 1-80
- Action: move

Current:
```java
package dev.christopherbell.pagination;
```

Proposed:
```java
package dev.christopherbell.libs.pagination;
```

Verification:
- `./gradlew :cbell-lib:test --tests dev.christopherbell.libs.pagination.StableCursorCodecTest`

### Task 2 - Move generic Mongo lease ownership into cbell-lib

Sequence / dependencies:
- Run after the backend plan so its new scheduler consumers are included in the import rewrite.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before tests, package moves, or import edits.
- Before-Edit Brief:
  - Behavior: acquisition, renewal, ownership loss, run status, and release remain unchanged.
  - Invariants: collection names, lease IDs, owner tokens, expiry fields, and run-status values remain byte-compatible.
  - Boundary/API: package becomes `dev.christopherbell.libs.mongo.lease`; feature-specific import guard remains WFL-owned.
  - Effects and failures: lease infrastructure still fails closed and status writes remain best-effort only where already specified.
  - Tests and evidence: move lease unit tests with code; run all feature scheduling tests after import rewrite.

- [ ] Move the eight generic lease classes and three lease tests.
- [ ] Rewrite imports in production/tests/migrations.
- [ ] Keep `RestaurantImportLeaseGuard` in WFL.
- [ ] Prove old package contains no lease implementation.

#### Code Edit 2.1
- File: `website/src/main/java/dev/christopherbell/configuration/mongo/lease/*.java`
- Lines: 1-85
- Action: move

Current:
```java
package dev.christopherbell.configuration.mongo.lease;
```

Proposed:
```java
package dev.christopherbell.libs.mongo.lease;
```

The exact moved set is `CollectorLeaseGuard`, `LeaseOwnershipLostException`, `MongoLeaseDocument`, `MongoLeaseService`, `RenewingMongoLease`, `ScheduledCollectorCoordinator`, `ScheduledCollectorRun`, and `ScheduledCollectorRunStatus`.

Verification:
- `./gradlew :cbell-lib:compileJava :website:compileJava`

#### Code Edit 2.2
- File: `website/src/{main,test}/java/**/*.java matching dev.christopherbell.configuration.mongo.lease`
- Lines: 1-300
- Action: replace

Current:
```java
import dev.christopherbell.configuration.mongo.lease.MongoLeaseService;
```

Proposed:
```java
import dev.christopherbell.libs.mongo.lease.MongoLeaseService;
```

- Apply the same literal prefix substitution for all eight types. Do not move WFL's `RestaurantImportLeaseGuard`.

Verification:
- `rg -n "dev\.christopherbell\.configuration\.mongo\.lease" website cbell-lib` returns no matches.

#### Code Edit 2.3
- File: `website/src/test/java/dev/christopherbell/configuration/mongo/lease/{MongoLeaseServiceTest,RenewingMongoLeaseTest,ScheduledCollectorCoordinatorTest}.java`
- Lines: 1-300
- Action: move

Current:
```java
package dev.christopherbell.configuration.mongo.lease;
```

Proposed:
```java
package dev.christopherbell.libs.mongo.lease;
```

Verification:
- `./gradlew :cbell-lib:test --tests 'dev.christopherbell.libs.mongo.lease.*'`
- `./gradlew :website:test --tests '*CanesBoxTrackerServiceTest' --tests '*RestaurantImportWorkflowServiceTest' --tests '*Vin*ServiceTest' --tests '*Music*Test'`

#### Code Edit 2.4
- File: `cbell-lib/build.gradle.kts`
- Lines: 27-29
- Action: replace

Current:
```kotlin
testImplementation("org.junit.jupiter:junit-jupiter")
testRuntimeOnly("org.junit.platform:junit-platform-launcher")
```

Proposed:
```kotlin
testImplementation("org.junit.jupiter:junit-jupiter")
testImplementation("org.assertj:assertj-core")
testImplementation("org.mockito:mockito-junit-jupiter")
testRuntimeOnly("org.junit.platform:junit-platform-launcher")
```

Verification:
- `./gradlew :cbell-lib:test --tests 'dev.christopherbell.libs.mongo.lease.*'`

### Task 3 - Publish TestUtil only as a Gradle test fixture

Sequence / dependencies:
- Independent of Tasks 1-2; land after their file moves to avoid build-file conflicts.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before build, fixture, or test edits.
- Before-Edit Brief:
  - Behavior: website tests read the same classpath JSON resources with the same failures.
  - Invariants: production compile/runtime classpaths cannot resolve `TestUtil`.
  - Boundary/API: website tests use `testFixtures(project(":cbell-lib"))`.
  - Effects and failures: missing/malformed fixtures retain current error categories.
  - Tests and evidence: fixture tests pass; dependency report proves absent from runtime elements.

- [ ] Enable `java-test-fixtures` and move TestUtil.
- [ ] Remove its Lombok-only annotation while preserving static API.
- [ ] Add website's test-fixture dependency and verify production isolation.

#### Code Edit 3.1
- File: `cbell-lib/build.gradle.kts`
- Lines: 1-33
- Action: replace

Current:
```kotlin
plugins {
    `java-library`
    id("io.spring.dependency-management")
}
```

Proposed:
```kotlin
plugins {
    `java-library`
    `java-test-fixtures`
    id("io.spring.dependency-management")
}
```

Add:
```kotlin
testFixturesImplementation("tools.jackson.core:jackson-databind")
```

Verification:
- `./gradlew :cbell-lib:compileTestFixturesJava`

#### Code Edit 3.2
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/test/TestUtil.java`
- Lines: 1-52
- Action: move

Current:
```java
import lombok.experimental.UtilityClass;

@UtilityClass
public final class TestUtil {
```

Proposed:
```java
public final class TestUtil {
  private TestUtil() {}
```

- Add `static` to `readJsonAsObject` and `readJsonAsString`; preserve method bodies and messages.

Verification:
- `./gradlew :cbell-lib:test --tests dev.christopherbell.libs.test.TestUtilTest`

#### Code Edit 3.3
- File: `website/build.gradle.kts`
- Lines: 61-72
- Action: replace

Current:
```kotlin
testImplementation("org.springframework.security:spring-security-test")
```

Proposed:
```kotlin
testImplementation(testFixtures(project(":cbell-lib")))
```

Verification:
- `./gradlew :website:test --tests '*ControllerTest'`
- `./gradlew :cbell-lib:outgoingVariants` confirms TestUtil is in test-fixtures output, not main runtime elements.

### Task 4 - Move JWT dependencies to website

Sequence / dependencies:
- Run after Task 3 build-file changes.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before build or test edits.
- Before-Edit Brief:
  - Behavior: token generation/validation does not change.
  - Invariants: versions stay BOM-managed/current; runtime implementation and Jackson adapter remain present for website.
  - Boundary/API: `cbell-lib` exposes no JJWT API.
  - Effects and failures: dependency-resolution failure is a build failure.
  - Tests and evidence: permission/security tests and dependency reports.

- [ ] Add direct website dependencies.
- [ ] Delete all three library declarations.
- [ ] Verify no library production source imports JJWT.

#### Code Edit 4.1
- File: `{cbell-lib,website}/build.gradle.kts`
- Lines: 17-72
- Action: move

Current:
```kotlin
api("io.jsonwebtoken:jjwt-api:0.13.0")
runtimeOnly("io.jsonwebtoken:jjwt-impl:0.13.0")
runtimeOnly("io.jsonwebtoken:jjwt-jackson:0.13.0")
```

Proposed:
```kotlin
implementation("io.jsonwebtoken:jjwt-api:0.13.0")
runtimeOnly("io.jsonwebtoken:jjwt-impl:0.13.0")
runtimeOnly("io.jsonwebtoken:jjwt-jackson:0.13.0")
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.permission.PermissionServiceTest --tests '*Jwt*Test'`
- `./gradlew :cbell-lib:dependencies --configuration runtimeClasspath` contains no `io.jsonwebtoken`.

### Task 5 - Move the single-consumer workflow engine into WFL

Sequence / dependencies:
- Run after confirming the production import inventory on the execution commit.

Implementation notes:
- Required skill: invoke `chris-street-style` and `superpowers:test-driven-development` before tests, package moves, or import edits.
- Before-Edit Brief:
  - Behavior: workflow execution, retry/stop behavior, result models, and logging stay unchanged.
  - Invariants: only package names and source-set owner change.
  - Boundary/API: new root is `dev.christopherbell.whatsforlunch.workflow.engine` with existing subpackages.
  - Effects and failures: Spring still discovers `WorkflowExecutor`; no duplicate bean remains.
  - Tests and evidence: move the full executor test and run WFL workflow/component-context tests.

- [ ] Re-run the production consumer search; stop if a non-WFL consumer exists.
- [ ] Move 14 production files and the executor test atomically.
- [ ] Rewrite WFL imports and prove the old package is absent.

#### Code Edit 5.1
- File: `cbell-lib/src/main/java/dev/christopherbell/libs/workflow/**/*.java`
- Lines: 1-193
- Action: move

Current:
```java
dev.christopherbell.libs.workflow
```

Proposed:
```java
dev.christopherbell.whatsforlunch.workflow.engine
```

- Preserve all types, annotations, visibility, and logic. `WorkflowExecutor` remains `@Service`.

Verification:
- `./gradlew :website:compileJava`
- `rg -n "dev\.christopherbell\.libs\.workflow" cbell-lib website` returns no matches.

#### Code Edit 5.2
- File: `website/src/{main,test}/java/dev/christopherbell/whatsforlunch/workflow/**/*.java`
- Lines: 1-300
- Action: replace

Current:
```java
import dev.christopherbell.libs.workflow.model.WorkflowContext;
```

Proposed:
```java
import dev.christopherbell.whatsforlunch.workflow.engine.model.WorkflowContext;
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.whatsforlunch.workflow.WhatsForLunchWorkflowTest`

#### Code Edit 5.3
- File: `cbell-lib/src/test/java/dev/christopherbell/libs/workflow/WorkflowExecutorTest.java`
- Lines: 1-240
- Action: move

Current:
```java
package dev.christopherbell.libs.workflow;
```

Proposed:
```java
package dev.christopherbell.whatsforlunch.workflow.engine;
```

Verification:
- `./gradlew :website:test --tests dev.christopherbell.whatsforlunch.workflow.engine.WorkflowExecutorTest`

### Task 6 - Verify module boundaries and runtime discovery

Sequence / dependencies:
- Final merge gate after Tasks 1-5.

- [ ] Run zero-reference searches for all retired package names.
- [ ] Run `:cbell-lib:check` and `:website:check`.
- [ ] Capture `dependencies`/`dependencyInsight` evidence for JJWT and test fixtures.
- [ ] Start the website on a non-8080 port and verify Spring creates cursor, lease coordinator, and workflow executor beans without collisions.
- [ ] Exercise login, one cursor-paginated route, one leased collector with scheduling disabled/manual test path, and WFL workflow.
- [ ] Save a Builder test report, then proceed through authorized PR/CI/merge/production-safe verification.

Verification:
- `./gradlew :cbell-lib:check :website:check`
- `./gradlew :cbell-lib:dependencies --configuration runtimeClasspath`
- `./gradlew :website:dependencyInsight --dependency jjwt --configuration runtimeClasspath`

## Code Changes

- Move stable cursor and generic Mongo lease packages to `cbell-lib`.
- Move `TestUtil` to the library test-fixtures variant.
- Move JJWT declarations to website.
- Move the workflow engine and tests beside WFL.

## Files and Modules

- `cbell-lib`: pagination, Mongo lease, HTTP reader from the preceding plan, test fixtures, build dependencies.
- `website`: import rewrites, WFL workflow engine, direct JJWT dependencies, feature tests.

## Unit Testing

- Cursor byte compatibility and invalid input.
- Lease acquisition/renewal/loss/release/status.
- Test fixture resource and JSON failures.
- JWT generation/validation.
- Workflow success/retry/stop/failure.

## Local Testing

Run on a non-8080 port with scheduling disabled. Verify application context startup and representative paths without touching production data or listeners.

## Validation

- No retired-package references.
- `:cbell-lib:check` and `:website:check` pass.
- Dependency reports demonstrate the intended scopes.
- Alternate-port context and representative runtime evidence are saved.

## Rollback or Recovery

Revert the atomic package-move PR. Because Mongo annotations and collection names do not change, rollback requires no data migration. If a component scan fails before merge, restore the old package/imports in the same branch rather than shipping duplicate types.

## Risks

- Package moves touch many imports and can conflict with concurrent work; execute after backend changes in an isolated branch.
- Moving Spring components can expose scan assumptions; context startup is mandatory.
- Gradle test-fixtures variants can be mis-scoped; outgoing variant and runtime dependency reports are mandatory.
- Workflow types may have hidden reflective name assumptions; search configuration/resources for old fully-qualified names before removal.

## Completion Criteria

- Pagination and leases compile/test from `cbell-lib` with no old-package references.
- `TestUtil` is unavailable to production main compilation and available to website tests.
- JJWT is absent from `cbell-lib` runtime and present in website runtime.
- Workflow production/test code is WFL-owned and behavior tests pass.
- Full checks, alternate-port smoke, authorized PR/CI/merge/production verification, documentation, and Builder closeout are complete.
