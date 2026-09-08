# christopherbell.dev Modular Monolith Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the build-time module model, deterministic no-regression dependency ratchet, and reviewable architecture documentation that every later `christopherbell.dev` module migration will use.

**Architecture:** Keep `website` as the single Spring Boot deployable and use Spring Modulith 2.1 only on the test classpath. Explicitly annotated discovery lets capability migrations opt into closed-module enforcement one at a time; focused ArchUnit conditions and a version-controlled frozen store reject new legacy cross-area access until every baseline violation is removed.

**Tech Stack:** Java 25, Spring Boot 4.1.0, Spring Modulith 2.1.0, ArchUnit through `spring-modulith-starter-test`, JUnit Jupiter, AssertJ, Gradle Kotlin DSL, MongoDB, native Windows/PowerShell verification.

## Global Constraints

- Preserve one `website` boot JAR, one process, and the current production deployment topology.
- Preserve `settings.gradle.kts` with only `website` and `cbell-lib`; do not create a Gradle project per capability.
- Keep Spring Modulith build/test-only: no runtime verifier, actuator endpoint, event registry, MongoDB event starter, outbox, broker, or observability starter.
- Use `spring.modulith.detection-strategy: explicitly-annotated`; unmigrated packages must not be presented as closed modules.
- Preserve public HTTP contracts, MongoDB collection names, indexes, and document shapes.
- Keep templates, JavaScript, CSS, and other browser assets out of this foundation change.
- Promote code to `cbell-lib` only after two demonstrated consumers need a domain-neutral contract; this plan adds nothing to `cbell-lib`.
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; execute from a clean sibling worktree created from refreshed `origin/main`.
- Before editing production source, tests, reusable scripts, code-bearing configuration, or copy-ready implementation examples, invoke `write-jane-street-style-code` and complete its Before-Edit Brief.
- Use a task-specific private `GRADLE_USER_HOME`; do not impose short outer timeouts on Gradle, Java tests, Pester, or application startup.
- Verify runtime candidates on an unused non-8080 port before any production action.

---

## Document Status

complete

## Objective

Deliver Phase 1 of [the approved modular-monolith specification](../session-memory/2026-08-04-christopherbell-dev.md#source-docs-specs-2026-08-04-christopherbell-dev-modular-monolith-md): a test-only Spring Modulith model, explicit discovery configuration, normalized ArchUnit dependency conditions, a checked-in legacy violation store, generated module documentation, and contributor commands. The deliverable prevents architecture debt from increasing without forcing existing capability packages to close in one branch.

## Goals

1. Resolve and verify Spring Modulith 2.1.0 without adding it to the packaged runtime.
2. Make `ApplicationModules.verify()` part of `:website:test` and therefore the existing root `build` CI jobs.
3. Treat `permission` as account-owned when measuring legacy package access.
4. Fail CI when a new top-level website package is not assigned to the architecture catalog; `libs` is the only explicit external area.
5. Allow cross-area access only through a target package named `api` while separately ratcheting forbidden business-to-`admin`, business-to-`configuration`, and business-to-`view` directions.
6. Store normalized, line-number-free legacy violations in version control so unrelated line movement does not churn the baseline.
7. Require explicit Gradle properties to create or reduce the frozen store; ordinary local and CI runs must be read-only.
8. Generate PlantUML and module canvas build artifacts from the same `ApplicationModules` model used by verification.

## Inputs

- Approved Builder spec: `docs/specs/2026-08-04-christopherbell-dev-modular-monolith.md`.
- Authoritative spoke: `A:\Projects\christopherbell.dev`.
- Inspected source baseline: remote and local `origin/main` at `9c587103cb7f7df2ab52ed3e232f1ca67660fd6e` on 2026-08-04.
- Current build: Java 25, Spring Boot 4.1.0, Gradle Kotlin DSL, `website` plus `cbell-lib`.
- Current CI: Linux, macOS, and Windows jobs run the root `build` task, so a `website` JUnit test is already a required gate.
- Official framework contracts: Spring Modulith 2.1.0 `ApplicationModules`, `ApplicationModuleDetectionStrategy.explicitlyAnnotated()`, `Documenter`, named interfaces, and module verification; ArchUnit `FreezingArchRule` with a plain-text violation store.

## Branch

- Create `codex/modular-monolith-foundation` from freshly fetched `origin/main` in a clean sibling worktree.
- Before creating the worktree, invoke `superpowers:using-git-worktrees` and verify the resolved worktree path with `Test-Path` and `git rev-parse --show-toplevel`.
- If refreshed `origin/main` is not `9c587103cb7f7df2ab52ed3e232f1ca67660fd6e`, compare every inspected line range and current block in this plan against the new base. Update and revalidate the Builder plan before editing when a block has drifted.

## Non-Goals

- Do not annotate or close a production business module in this foundation plan.
- Do not move `permission` code into `account`; only normalize those packages to one ownership area in the ratchet.
- Do not split `configuration`, introduce module APIs, reroute consumers, or move repositories/entities.
- Do not change any controller, service, repository, Mongo document, route, security decision, browser asset, production script, or service definition.
- Do not commit generated PlantUML/canvas output under `website/build/`.
- Do not deploy this plan independently of the normal PR, CI, merge, and protected Windows release workflow.

## Assumptions

- Spring Modulith 2.1.0 remains the stable Boot 4.1-compatible line when execution begins; dependency resolution must confirm this before code review.
- `spring-modulith-starter-test` supplies the ArchUnit and documentation APIs used by test sources.
- Spring Modulith's configuration lookup reads the packaged `application.yml`, so the explicit detection property applies consistently to verification and documentation without a global system-property mutation.
- The current root `build` CI tasks execute `:website:test`; no workflow edit is required.
- The Gradle dependency-verification file and ArchUnit frozen store are generated review artifacts. Their exact hashes and store identifiers must come from the documented commands, not handwritten values.
- MongoDB is locally available for the final alternate-port smoke check; the test must use a uniquely named disposable database.

## Open Questions

None. The user approved the architecture and migration design on 2026-08-04.

## Task Breakdown

### Task 1 - Add explicit Spring Modulith verification

Sequence / dependencies:
- Runs first because all later architecture sources compile against the test-only Modulith and ArchUnit APIs established here.
- Create the isolated worktree and private Gradle cache before Step 1.

Files:
- Create: `website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java`
- Modify: `website/build.gradle.kts:22-27`
- Modify: `website/build.gradle.kts:72-80`
- Modify: `website/build.gradle.kts:after 81`
- Modify: `website/src/main/resources/application.yml:1-2`
- Generate: `gradle/verification-metadata.xml` entries for the resolved Spring Modulith/ArchUnit test graph.

Interfaces:
- Consumes: `dev.christopherbell.Application`; Spring Modulith `ApplicationModules.of(Class<?>)` and `ApplicationModules.verify()`.
- Produces: one central `ModularMonolithArchitectureTest` and the repository-wide `spring.modulith.detection-strategy=explicitly-annotated` contract used by Tasks 3 and 4 and every later module plan.

Implementation notes:
- Required skill: `write-jane-street-style-code` before any code edits. Invoke it before Step 1.
- Before-Edit Brief:
  - Behavior: `:website:test` discovers only packages explicitly marked as modules and fails when declared modules contain cycles, internal access, or undeclared dependencies.
  - Invariants: the production runtime classpath and boot JAR contain no Spring Modulith artifact; `website` remains the only boot application; no business package is declared a module yet.
  - Boundary/API: this task introduces a test boundary only; `Application`, HTTP APIs, MongoDB, and deployed configuration behavior remain unchanged.
  - Effects and failures: dependency resolution may fail until verification metadata is generated; the first test run must fail at compilation before dependencies are added; an incorrect detection setting would cause legacy top-level packages such as `configuration` to appear as modules.
  - Tests and evidence: RED is the missing Modulith import; GREEN is the focused architecture test plus proof that `configuration` is not detected and `MODULES.verify()` succeeds.

- [x] **Step 1: Create the failing central module verification test.**

#### Code Edit 1.1
- File: `website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java`
- Lines: 1-17
- Action: add

Proposed:
```java
package dev.christopherbell.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import dev.christopherbell.Application;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ModularMonolithArchitectureTest {
  private static final ApplicationModules MODULES = ApplicationModules.of(Application.class);

  @Test
  void explicitBusinessModulesObeyDeclaredBoundaries() {
    assertThat(MODULES.getModuleByName("configuration")).isEmpty();
    MODULES.verify();
  }
}
```

Verification:
- Run `\.\gradlew.bat :website:test --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest --stacktrace` with the task-specific private `GRADLE_USER_HOME`.
- Expected RED: Java compilation fails because `org.springframework.modulith.core.ApplicationModules` is not on the test compile classpath.

- [x] **Step 2: Import the Spring Modulith 2.1.0 BOM.**

#### Code Edit 1.2
- File: `website/build.gradle.kts`
- Lines: 22-27
- Action: replace

Current:
```kotlin
dependencyManagement {
    dependencies {
        dependency("net.bytebuddy:byte-buddy:1.18.11")
        dependency("net.bytebuddy:byte-buddy-agent:1.18.11")
    }
}
```

Proposed:
```kotlin
dependencyManagement {
    imports {
        mavenBom("org.springframework.modulith:spring-modulith-bom:2.1.0")
    }
    dependencies {
        dependency("net.bytebuddy:byte-buddy:1.18.11")
        dependency("net.bytebuddy:byte-buddy-agent:1.18.11")
    }
}
```

Verification:
- Run `\.\gradlew.bat :website:dependencyManagement --stacktrace`.
- Expected: the task succeeds and reports the imported Spring Modulith BOM without adding a runtime dependency.

- [x] **Step 3: Add the test-only Spring Modulith starter.**

#### Code Edit 1.3
- File: `website/build.gradle.kts`
- Lines: 72-80
- Action: replace

Current:
```kotlin
    // Testing
    testImplementation("com.fasterxml.jackson.dataformat:jackson-dataformat-yaml")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.boot:spring-boot-starter-webmvc-test")
    testImplementation("org.springframework.security:spring-security-test")
    testImplementation(testFixtures(project(":cbell-lib")))
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
    testAnnotationProcessor("org.projectlombok:lombok:1.18.46")
    testCompileOnly("org.projectlombok:lombok:1.18.46")
```

Proposed:
```kotlin
    // Testing
    testImplementation("com.fasterxml.jackson.dataformat:jackson-dataformat-yaml")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.boot:spring-boot-starter-webmvc-test")
    testImplementation("org.springframework.security:spring-security-test")
    testImplementation("org.springframework.modulith:spring-modulith-starter-test")
    testImplementation(testFixtures(project(":cbell-lib")))
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
    testAnnotationProcessor("org.projectlombok:lombok:1.18.46")
    testCompileOnly("org.projectlombok:lombok:1.18.46")
```

Verification:
- Run `\.\gradlew.bat :website:dependencies --configuration testRuntimeClasspath --stacktrace`.
- Expected: Spring Modulith 2.1.0 resolves on `testRuntimeClasspath`.
- Run `\.\gradlew.bat :website:dependencies --configuration runtimeClasspath --stacktrace`.
- Expected: no `org.springframework.modulith` artifact appears on `runtimeClasspath`.

- [x] **Step 4: Select explicit module discovery.**

#### Code Edit 1.4
- File: `website/src/main/resources/application.yml`
- Lines: 1-2
- Action: replace

Current:
```yaml
spring:
  web:
```

Proposed:
```yaml
spring:
  modulith:
    detection-strategy: explicitly-annotated
  web:
```

Verification:
- Run the focused test after verification metadata is generated.
- Expected: `configuration` is absent from the module model and `MODULES.verify()` passes with no explicitly declared production modules.

- [x] **Step 5: Forward approved ArchUnit flags to forked test workers.**

#### Code Edit 1.5
- File: `website/build.gradle.kts`
- Lines: after 81
- Action: add

Proposed:
```kotlin
val forwardedArchitectureTestSystemProperties = listOf(
    "archunit.freeze.store.default.allowStoreCreation",
    "archunit.freeze.store.default.allowStoreUpdate")

tasks.withType<Test>().configureEach {
    forwardedArchitectureTestSystemProperties.forEach { propertyName ->
        providers.systemProperty(propertyName).orNull?.let { value ->
            systemProperty(propertyName, value)
        }
    }
}
```

Verification:
- Run `\.\gradlew.bat :website:properties -Darchunit.freeze.store.default.allowStoreCreation=true`.
- Expected: Gradle configures successfully; only the two named ArchUnit flags are eligible for propagation to test workers, and `archunit.freeze.refreeze` is not forwarded.

- [x] **Step 6: Generate and review dependency-verification metadata.**

Run from the isolated worktree:

```powershell
$env:GRADLE_USER_HOME = Join-Path $env:TEMP 'christopherbell-dev-modular-monolith-foundation-gradle'
.\gradlew.bat --write-verification-metadata sha256 :website:test --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest --stacktrace
git diff -- gradle/verification-metadata.xml
```

Expected:
- The focused test passes.
- `gradle/verification-metadata.xml` adds only the BOM, POM, module, and JAR hashes required by the resolved Spring Modulith/ArchUnit test graph.
- Existing verification entries remain intact.
- A second focused test run without `--write-verification-metadata` passes.

- [x] **Step 7: Commit Task 1.**

```powershell
git add website/build.gradle.kts website/src/main/resources/application.yml website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java gradle/verification-metadata.xml
git commit -m "test: add Spring Modulith verification harness"
```

Task-level verification:
- `\.\gradlew.bat :website:test --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest --stacktrace`
- `\.\gradlew.bat :website:dependencies --configuration runtimeClasspath --stacktrace` with no `org.springframework.modulith` result.

### Task 2 - Define normalized legacy dependency rules

Sequence / dependencies:
- Runs after Task 1 because it compiles against ArchUnit delivered transitively by `spring-modulith-starter-test`.
- Does not freeze production violations yet; first prove the rule semantics with isolated fixtures.

Files:
- Create: `website/src/test/java/dev/christopherbell/architecture/LegacyModuleDependencyRules.java`
- Create: `website/src/test/java/dev/christopherbell/architecture/LegacyModuleDependencyRulesTest.java`
- Create: `website/src/test/java/dev/christopherbell/architecture/fixture/alpha/AlphaConsumer.java`
- Create: `website/src/test/java/dev/christopherbell/architecture/fixture/beta/api/BetaApiContract.java`
- Create: `website/src/test/java/dev/christopherbell/architecture/fixture/beta/internal/BetaInternalDependency.java`
- Create: `website/src/test/java/dev/christopherbell/architecture/fixture/ops/OrchestrationDependency.java`

Interfaces:
- Consumes: ArchUnit `JavaClasses`, `Dependency`, `ArchCondition`, `ArchRule`, and `FreezingArchRule`.
- Produces:
  - `LegacyModuleDependencyRules.production()`.
  - `JavaClasses importProductionClasses()`.
  - `ArchRule crossAreaAccessRule()` and `frozenCrossAreaAccessRule()`.
  - `ArchRule orchestrationDirectionRule()` and `frozenOrchestrationDirectionRule()`.
  - `Optional<String> areaOf(String packageName)` for ownership normalization tests.
  - `Set<String> unknownAreas(JavaClasses classes)` for complete top-level package catalog enforcement.

Implementation notes:
- Required skill: `write-jane-street-style-code` before any code edits. Invoke it again and produce the task-specific brief before Step 1.
- Before-Edit Brief:
  - Behavior: inspect compiled production dependencies, normalize the top-level `permission` package to account ownership, ignore external/unknown packages, permit another area's `.api` package, and emit deterministic violations for every other cross-area access.
  - Invariants: a rule never reads source text, never includes source line numbers, never imports test classes for the production baseline, and never treats `dev.christopherbell.libs` as a website business area.
  - Boundary/API: the helper is package-private test code; only the central architecture test consumes it.
  - Effects and failures: classpath import is read-only; an unrecognized first-party package fails the catalog assertion; duplicate bytecode dependency kinds collapse to one source-class/target-class violation.
  - Tests and evidence: fixture tests must prove internal access fails, `.api` access passes, business-to-orchestration access fails even if API-shaped later, `permission` normalizes to `account`, and an uncatalogued top-level area is reported.

- [x] **Step 1: Add rule fixtures that distinguish API and internal access.**

#### Code Edit 2.1
- File: `website/src/test/java/dev/christopherbell/architecture/fixture/beta/api/BetaApiContract.java`
- Lines: 1-3
- Action: add

Proposed:
```java
package dev.christopherbell.architecture.fixture.beta.api;

public interface BetaApiContract {}
```

Verification:
- Compiles as a target package that the generic cross-area rule must permit.

#### Code Edit 2.2
- File: `website/src/test/java/dev/christopherbell/architecture/fixture/beta/internal/BetaInternalDependency.java`
- Lines: 1-3
- Action: add

Proposed:
```java
package dev.christopherbell.architecture.fixture.beta.internal;

public final class BetaInternalDependency {}
```

Verification:
- Compiles as a target package that the generic cross-area rule must reject.

#### Code Edit 2.3
- File: `website/src/test/java/dev/christopherbell/architecture/fixture/ops/OrchestrationDependency.java`
- Lines: 1-3
- Action: add

Proposed:
```java
package dev.christopherbell.architecture.fixture.ops;

public final class OrchestrationDependency {}
```

Verification:
- Compiles as the orchestration-area target used by the forbidden-direction rule.

#### Code Edit 2.4
- File: `website/src/test/java/dev/christopherbell/architecture/fixture/alpha/AlphaConsumer.java`
- Lines: 1-20
- Action: add

Proposed:
```java
package dev.christopherbell.architecture.fixture.alpha;

import dev.christopherbell.architecture.fixture.beta.api.BetaApiContract;
import dev.christopherbell.architecture.fixture.beta.internal.BetaInternalDependency;
import dev.christopherbell.architecture.fixture.ops.OrchestrationDependency;

public final class AlphaConsumer {
  private final BetaApiContract apiContract;
  private final BetaInternalDependency internalDependency;
  private final OrchestrationDependency orchestrationDependency;

  public AlphaConsumer(
      BetaApiContract apiContract,
      BetaInternalDependency internalDependency,
      OrchestrationDependency orchestrationDependency) {
    this.apiContract = apiContract;
    this.internalDependency = internalDependency;
    this.orchestrationDependency = orchestrationDependency;
  }
}
```

Verification:
- Compiles with one permitted cross-area target and two forbidden targets.

- [x] **Step 2: Write the failing rule contract tests.**

#### Code Edit 2.5
- File: `website/src/test/java/dev/christopherbell/architecture/LegacyModuleDependencyRulesTest.java`
- Lines: 1-54
- Action: add

Proposed:
```java
package dev.christopherbell.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import java.util.Set;
import org.junit.jupiter.api.Test;

class LegacyModuleDependencyRulesTest {
  private static final String FIXTURE_ROOT = "dev.christopherbell.architecture.fixture";
  private static final LegacyModuleDependencyRules RULES =
      new LegacyModuleDependencyRules(
          FIXTURE_ROOT, Set.of("alpha", "beta", "ops"), Set.of("ops"));
  private static final JavaClasses FIXTURES =
      new ClassFileImporter().importPackages(FIXTURE_ROOT);

  @Test
  void rejectsInternalCrossAreaAccessButAllowsPublishedApis() {
    var details = RULES.crossAreaAccessRule().evaluate(FIXTURES).getFailureReport().getDetails();

    assertThat(details)
        .anyMatch(detail -> detail.contains("alpha -> beta")
            && detail.contains("BetaInternalDependency"))
        .noneMatch(detail -> detail.contains("BetaApiContract"));
  }

  @Test
  void rejectsBusinessDependenciesOnOrchestrationAreas() {
    var details =
        RULES.orchestrationDirectionRule().evaluate(FIXTURES).getFailureReport().getDetails();

    assertThat(details)
        .anyMatch(detail -> detail.contains("alpha -> ops")
            && detail.contains("OrchestrationDependency"));
  }

  @Test
  void treatsPermissionAsAccountOwnership() {
    var rules = new LegacyModuleDependencyRules(
        "dev.christopherbell", Set.of("account", "permission"), Set.of());

    assertThat(rules.areaOf("dev.christopherbell.permission.jwt"))
        .contains("account");
  }

  @Test
  void reportsUncataloguedTopLevelAreas() {
    var rules = new LegacyModuleDependencyRules(
        FIXTURE_ROOT, Set.of("alpha", "beta"), Set.of());

    assertThat(rules.unknownAreas(FIXTURES)).containsExactly("ops");
  }
}
```

Verification:
- Run `\.\gradlew.bat :website:test --tests dev.christopherbell.architecture.LegacyModuleDependencyRulesTest --stacktrace`.
- Expected RED: compilation fails because `LegacyModuleDependencyRules` does not exist.

- [x] **Step 3: Implement normalized, deterministic dependency conditions.**

#### Code Edit 2.6
- File: `website/src/test/java/dev/christopherbell/architecture/LegacyModuleDependencyRules.java`
- Lines: 1-206
- Action: add

Proposed:
```java
package dev.christopherbell.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;

import com.tngtech.archunit.core.domain.Dependency;
import com.tngtech.archunit.core.domain.JavaClass;
import com.tngtech.archunit.core.domain.JavaClasses;
import com.tngtech.archunit.core.importer.ClassFileImporter;
import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.lang.ArchCondition;
import com.tngtech.archunit.lang.ArchRule;
import com.tngtech.archunit.lang.ConditionEvents;
import com.tngtech.archunit.lang.SimpleConditionEvent;
import com.tngtech.archunit.library.freeze.FreezingArchRule;
import java.util.Optional;
import java.util.Set;
import java.util.TreeSet;

final class LegacyModuleDependencyRules {
  private static final String APPLICATION_ROOT = "dev.christopherbell";
  private static final Set<String> APPLICATION_AREAS = Set.of(
      "account",
      "admin",
      "blog",
      "canesboxtracker",
      "configuration",
      "federation",
      "location",
      "message",
      "music",
      "notification",
      "permission",
      "photo",
      "post",
      "report",
      "sharedfolder",
      "vehicle",
      "view",
      "whatsforlunch");
  private static final Set<String> ORCHESTRATION_AREAS =
      Set.of("admin", "configuration", "view");

  private final String rootPackage;
  private final Set<String> applicationAreas;
  private final Set<String> orchestrationAreas;
  private final Set<String> externalAreas;

  LegacyModuleDependencyRules(
      String rootPackage,
      Set<String> applicationAreas,
      Set<String> orchestrationAreas) {
    this(rootPackage, applicationAreas, orchestrationAreas, Set.of());
  }

  private LegacyModuleDependencyRules(
      String rootPackage,
      Set<String> applicationAreas,
      Set<String> orchestrationAreas,
      Set<String> externalAreas) {
    this.rootPackage = rootPackage;
    this.applicationAreas = Set.copyOf(applicationAreas);
    this.orchestrationAreas = Set.copyOf(orchestrationAreas);
    this.externalAreas = Set.copyOf(externalAreas);
  }

  static LegacyModuleDependencyRules production() {
    return new LegacyModuleDependencyRules(
        APPLICATION_ROOT, APPLICATION_AREAS, ORCHESTRATION_AREAS, Set.of("libs"));
  }

  JavaClasses importProductionClasses() {
    return new ClassFileImporter()
        .withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
        .importPackages(rootPackage);
  }

  Set<String> unknownAreas(JavaClasses classes) {
    var unknown = new TreeSet<String>();
    classes.stream()
        .map(JavaClass::getPackageName)
        .map(this::firstAreaOf)
        .flatMap(Optional::stream)
        .filter(area -> !applicationAreas.contains(area))
        .filter(area -> !externalAreas.contains(area))
        .forEach(unknown::add);
    return Set.copyOf(unknown);
  }

  ArchRule crossAreaAccessRule() {
    return classes()
        .that().resideInAPackage(rootPackage + "..")
        .should(new CrossAreaAccessCondition(ViolationKind.INTERNAL_ACCESS));
  }

  ArchRule frozenCrossAreaAccessRule() {
    return FreezingArchRule.freeze(crossAreaAccessRule());
  }

  ArchRule orchestrationDirectionRule() {
    return classes()
        .that().resideInAPackage(rootPackage + "..")
        .should(new CrossAreaAccessCondition(ViolationKind.ORCHESTRATION_DIRECTION));
  }

  ArchRule frozenOrchestrationDirectionRule() {
    return FreezingArchRule.freeze(orchestrationDirectionRule());
  }

  Optional<String> areaOf(String packageName) {
    return physicalAreaOf(packageName).map(area -> area.equals("permission") ? "account" : area);
  }

  private Optional<String> physicalAreaOf(String packageName) {
    return firstAreaOf(packageName).filter(applicationAreas::contains);
  }

  private Optional<String> firstAreaOf(String packageName) {
    var prefix = rootPackage + ".";
    if (!packageName.startsWith(prefix)) {
      return Optional.empty();
    }

    var remainder = packageName.substring(prefix.length());
    var separator = remainder.indexOf('.');
    var area = separator < 0 ? remainder : remainder.substring(0, separator);
    return Optional.of(area);
  }

  private boolean isPublishedApi(String packageName) {
    var physicalArea = physicalAreaOf(packageName);
    if (physicalArea.isEmpty() || physicalArea.get().equals("permission")) {
      return false;
    }

    var apiPackage = rootPackage + "." + physicalArea.get() + ".api";
    return packageName.equals(apiPackage) || packageName.startsWith(apiPackage + ".");
  }

  private Optional<AccessViolation> violation(Dependency dependency, ViolationKind kind) {
    var source = dependency.getOriginClass();
    var target = dependency.getTargetClass();
    var sourceArea = areaOf(source.getPackageName());
    var targetArea = areaOf(target.getPackageName());

    if (sourceArea.isEmpty() || targetArea.isEmpty() || sourceArea.equals(targetArea)) {
      return Optional.empty();
    }

    if (kind == ViolationKind.INTERNAL_ACCESS && isPublishedApi(target.getPackageName())) {
      return Optional.empty();
    }

    if (kind == ViolationKind.ORCHESTRATION_DIRECTION
        && (orchestrationAreas.contains(sourceArea.get())
            || !orchestrationAreas.contains(targetArea.get()))) {
      return Optional.empty();
    }

    return Optional.of(new AccessViolation(
        sourceArea.get(), targetArea.get(), source.getName(), target.getName()));
  }

  private enum ViolationKind {
    INTERNAL_ACCESS,
    ORCHESTRATION_DIRECTION
  }

  private record AccessViolation(
      String sourceArea,
      String targetArea,
      String sourceClass,
      String targetClass) implements Comparable<AccessViolation> {

    String description() {
      return "%s -> %s | %s -> %s"
          .formatted(sourceArea, targetArea, sourceClass, targetClass);
    }

    @Override
    public int compareTo(AccessViolation other) {
      return description().compareTo(other.description());
    }
  }

  private final class CrossAreaAccessCondition extends ArchCondition<JavaClass> {
    private final ViolationKind kind;

    private CrossAreaAccessCondition(ViolationKind kind) {
      super(kind == ViolationKind.INTERNAL_ACCESS
          ? "access only its own area or another area's published api"
          : "not depend on an orchestration area from a business area");
      this.kind = kind;
    }

    @Override
    public void check(JavaClass source, ConditionEvents events) {
      source.getDirectDependenciesFromSelf().stream()
          .map(dependency -> violation(dependency, kind))
          .flatMap(Optional::stream)
          .distinct()
          .sorted()
          .forEach(violation -> events.add(
              SimpleConditionEvent.violated(source, violation.description())));
    }
  }
}
```

Verification:
- Run `\.\gradlew.bat :website:test --tests dev.christopherbell.architecture.LegacyModuleDependencyRulesTest --stacktrace`.
- Expected GREEN: all three fixture tests pass.
- Run the same test twice and compare output; violation descriptions must be stable and contain no source line numbers.

- [x] **Step 4: Commit Task 2.**

```powershell
git add website/src/test/java/dev/christopherbell/architecture
git commit -m "test: define legacy module dependency rules"
```

Task-level verification:
- `\.\gradlew.bat :website:test --tests dev.christopherbell.architecture.LegacyModuleDependencyRulesTest --stacktrace`

### Task 3 - Freeze the production dependency baseline

Sequence / dependencies:
- Runs after Task 2 because the frozen store must be created from already-tested, normalized violation messages.
- Store creation is enabled for exactly one explicit command; the committed default remains read-only.

Files:
- Modify: `website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java:1-17` from Task 1.
- Create: `website/src/test/resources/archunit.properties`.
- Generate: `website/src/test/resources/architecture-baseline/**` plain-text ArchUnit store files.

Interfaces:
- Consumes: all Task 2 `LegacyModuleDependencyRules` production methods.
- Produces: two frozen CI gates: legacy internal cross-area access and forbidden business-to-orchestration direction.

Implementation notes:
- Required skill: `write-jane-street-style-code` before any code edits. Invoke it before Step 1.
- Before-Edit Brief:
  - Behavior: ordinary test runs compare production dependencies with the checked-in baseline and fail on any new normalized violation; explicit maintenance runs may only update a reviewed store.
  - Invariants: store creation/update are disabled by default; baseline messages contain source area, target area, source class, and target class but no source line; test classes and `cbell-lib` are outside the production import set.
  - Boundary/API: the central architecture test owns baseline enforcement; no production code consumes the store.
  - Effects and failures: the first ordinary run fails because the store is absent; creation writes test resources; CI fails if a rule key or violation changes without a committed update.
  - Tests and evidence: prove missing-store failure, explicit creation success, read-only repeatability, new-fixture rule behavior from Task 2, and a clean baseline diff after a second read-only run.

- [x] **Step 1: Make the baseline store read-only by default.**

#### Code Edit 3.1
- File: `website/src/test/resources/archunit.properties`
- Lines: 1-3
- Action: add

Proposed:
```properties
freeze.store.default.path=src/test/resources/architecture-baseline
freeze.store.default.allowStoreCreation=false
freeze.store.default.allowStoreUpdate=false
```

Verification:
- Run the central architecture test before creating the store.
- Expected RED: ArchUnit reports that store creation is disabled or that no stored rule exists.

- [x] **Step 2: Wire both frozen rules into the central test.**

#### Code Edit 3.2
- File: `website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java`
- Lines: 1-17
- Action: replace

Current:
```java
package dev.christopherbell.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import dev.christopherbell.Application;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ModularMonolithArchitectureTest {
  private static final ApplicationModules MODULES = ApplicationModules.of(Application.class);

  @Test
  void explicitBusinessModulesObeyDeclaredBoundaries() {
    assertThat(MODULES.getModuleByName("configuration")).isEmpty();
    MODULES.verify();
  }
}
```

Proposed:
```java
package dev.christopherbell.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import com.tngtech.archunit.core.domain.JavaClasses;
import dev.christopherbell.Application;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ModularMonolithArchitectureTest {
  private static final ApplicationModules MODULES = ApplicationModules.of(Application.class);
  private static final LegacyModuleDependencyRules LEGACY_RULES =
      LegacyModuleDependencyRules.production();
  private static final JavaClasses PRODUCTION_CLASSES =
      LEGACY_RULES.importProductionClasses();

  @Test
  void explicitBusinessModulesObeyDeclaredBoundaries() {
    assertThat(MODULES.getModuleByName("configuration")).isEmpty();
    MODULES.verify();
  }

  @Test
  void everyProductionAreaIsCataloged() {
    assertThat(LEGACY_RULES.unknownAreas(PRODUCTION_CLASSES)).isEmpty();
  }

  @Test
  void legacyInternalCrossAreaAccessDoesNotGrow() {
    LEGACY_RULES.frozenCrossAreaAccessRule().check(PRODUCTION_CLASSES);
  }

  @Test
  void businessDependenciesOnOrchestrationAreasDoNotGrow() {
    LEGACY_RULES.frozenOrchestrationDirectionRule().check(PRODUCTION_CLASSES);
  }
}
```

Verification:
- Run the focused central test with the default configuration.
- Expected RED: the absent baseline cannot be created because creation is disabled.

- [x] **Step 3: Create the initial store with explicit one-time authority.**

```powershell
.\gradlew.bat :website:test `
  --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest `
  -Darchunit.freeze.store.default.allowStoreCreation=true `
  -Darchunit.freeze.store.default.allowStoreUpdate=true `
  --stacktrace
git status --short website/src/test/resources/architecture-baseline
git diff -- website/src/test/resources/architecture-baseline
```

Expected:
- The test succeeds and creates plain-text files under `website/src/test/resources/architecture-baseline/`.
- Stored messages are sorted, normalized as `source -> target | source class -> target class`, and contain no `:<line>` suffix.
- `permission` and `account` never appear as a cross-area pair.
- `dev.christopherbell.libs` never appears as a website area.

- [x] **Step 4: Prove the committed defaults are repeatable and read-only.**

```powershell
.\gradlew.bat :website:test --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest --stacktrace
git diff --exit-code -- website/src/test/resources/architecture-baseline
```

Expected: the test passes and the second run makes no store change.

- [x] **Step 5: Document the only allowed baseline-reduction command in the commit body.**

For later module slices, the explicit maintenance command is:

```powershell
.\gradlew.bat :website:test `
  --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest `
  -Darchunit.freeze.store.default.allowStoreUpdate=true `
  --stacktrace
git diff -- website/src/test/resources/architecture-baseline
```

The implementer must reject any diff that adds a violation. A baseline update is accepted only when all added lines are absent and removed lines correspond to reviewed boundary repairs.

- [x] **Step 6: Commit Task 3.**

```powershell
git add website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java website/src/test/resources/archunit.properties website/src/test/resources/architecture-baseline
git commit -m "test: freeze modular monolith dependency baseline"
```

Task-level verification:
- `\.\gradlew.bat :website:test --tests 'dev.christopherbell.architecture.*' --stacktrace`
- `git diff --exit-code -- website/src/test/resources/architecture-baseline` after the read-only run.

### Task 4 - Generate module documentation and publish contributor workflow

Sequence / dependencies:
- Runs after Task 3 so documentation and contributor guidance refer to the same verified module model and frozen store.
- Ends with full build, package, alternate-port runtime, and runtime-classpath evidence.

Files:
- Modify: `website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java:1-37` from Task 3.
- Modify: `README.md:203-219`.
- Generate but do not commit: `website/build/spring-modulith-docs/**`.

Interfaces:
- Consumes: Task 1 `MODULES`; Spring Modulith `Documenter`.
- Produces: PlantUML overview and per-module canvas build output plus contributor commands for normal verification and explicit baseline reduction.

Implementation notes:
- Required skill: `write-jane-street-style-code` before any code edits. Invoke it before Step 1.
- Before-Edit Brief:
  - Behavior: the architecture test emits reviewable module documentation under the build directory, and README instructions tell contributors how to run checks and reduce debt safely.
  - Invariants: generated documentation is not committed; frontend guidance remains unchanged; the normal architecture command cannot create or update the frozen store.
  - Boundary/API: documentation derives from `MODULES`, not a separate handwritten graph.
  - Effects and failures: the test writes only beneath `website/build`; documentation generation failure fails the test; README commands must work in both normal CI and the Windows development host.
  - Tests and evidence: focused architecture tests generate the files, the full build passes, the boot JAR has no Modulith runtime artifact, and the candidate serves readiness/liveness and `/` from a non-8080 port.

- [x] **Step 1: Generate documentation from the verified module model.**

#### Code Edit 4.1
- File: `website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java`
- Lines: 1-37
- Action: replace

Current:
```java
package dev.christopherbell.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import com.tngtech.archunit.core.domain.JavaClasses;
import dev.christopherbell.Application;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;

class ModularMonolithArchitectureTest {
  private static final ApplicationModules MODULES = ApplicationModules.of(Application.class);
  private static final LegacyModuleDependencyRules LEGACY_RULES =
      LegacyModuleDependencyRules.production();
  private static final JavaClasses PRODUCTION_CLASSES =
      LEGACY_RULES.importProductionClasses();

  @Test
  void explicitBusinessModulesObeyDeclaredBoundaries() {
    assertThat(MODULES.getModuleByName("configuration")).isEmpty();
    MODULES.verify();
  }

  @Test
  void everyProductionAreaIsCataloged() {
    assertThat(LEGACY_RULES.unknownAreas(PRODUCTION_CLASSES)).isEmpty();
  }

  @Test
  void legacyInternalCrossAreaAccessDoesNotGrow() {
    LEGACY_RULES.frozenCrossAreaAccessRule().check(PRODUCTION_CLASSES);
  }

  @Test
  void businessDependenciesOnOrchestrationAreasDoNotGrow() {
    LEGACY_RULES.frozenOrchestrationDirectionRule().check(PRODUCTION_CLASSES);
  }
}
```

Proposed:
```java
package dev.christopherbell.architecture;

import static org.assertj.core.api.Assertions.assertThat;

import com.tngtech.archunit.core.domain.JavaClasses;
import dev.christopherbell.Application;
import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.docs.Documenter;

class ModularMonolithArchitectureTest {
  private static final ApplicationModules MODULES = ApplicationModules.of(Application.class);
  private static final LegacyModuleDependencyRules LEGACY_RULES =
      LegacyModuleDependencyRules.production();
  private static final JavaClasses PRODUCTION_CLASSES =
      LEGACY_RULES.importProductionClasses();

  @Test
  void explicitBusinessModulesObeyDeclaredBoundaries() {
    assertThat(MODULES.getModuleByName("configuration")).isEmpty();
    MODULES.verify();
  }

  @Test
  void everyProductionAreaIsCataloged() {
    assertThat(LEGACY_RULES.unknownAreas(PRODUCTION_CLASSES)).isEmpty();
  }

  @Test
  void legacyInternalCrossAreaAccessDoesNotGrow() {
    LEGACY_RULES.frozenCrossAreaAccessRule().check(PRODUCTION_CLASSES);
  }

  @Test
  void businessDependenciesOnOrchestrationAreasDoNotGrow() {
    LEGACY_RULES.frozenOrchestrationDirectionRule().check(PRODUCTION_CLASSES);
  }

  @Test
  void writesReviewableModuleDocumentation() {
    new Documenter(MODULES)
        .writeModulesAsPlantUml()
        .writeModuleCanvases();
  }
}
```

Verification:
- Run the focused architecture test.
- Expected: `website/build/spring-modulith-docs/` contains PlantUML/module-canvas output and the test passes.
- Run `git status --short`; expected: no generated documentation is tracked.

- [x] **Step 2: Replace the descriptive backend section with enforceable conventions.**

#### Code Edit 4.2
- File: `README.md`
- Lines: 205-219
- Action: replace

Current:
```markdown
Backend code is organized by feature, not by technical layer. For example,
`post`, `account`, `vehicle`, and `whatsforlunch` each own their controller,
service, repository, mapper, models, and package docs.

Common pattern inside a feature:

- `*Controller` defines HTTP endpoints.
- `*Service` owns business rules.
- `*Repository` owns MongoDB access.
- `*Mapper` converts between persistence models and API DTOs.
- `model/` contains entities, request DTOs, response DTOs, and enums.
- `README.md` explains the feature's technical behavior.

Cross-cutting web infrastructure lives in `configuration`. Server-rendered page
routes live in `view`.
```

Proposed:
```markdown
`website` is one Spring Boot deployable organized as a modular monolith. Business
capabilities own their controllers, application/domain behavior, repositories,
persistence documents, and package documentation. `cbell-lib` contains only
domain-neutral behavior with multiple demonstrated consumers.

Capabilities migrate to closed Spring Modulith modules incrementally. A migrated
module exposes cross-module commands, queries, identifiers, result DTOs, semantic
failures, and non-critical events only through a named `api` package. Repositories,
Mongo documents, implementation services, mappers, and internal DTOs are never
module APIs. `permission` is account-owned. `view`, `admin`, and Spring bootstrap
may orchestrate module APIs; business modules may not depend on those layers.

Run the architecture gates with:

~~~shell
./gradlew :website:test --tests 'dev.christopherbell.architecture.*'
~~~

The checked-in ArchUnit store freezes legacy cross-area accesses. Normal test and
CI runs cannot create or update it. After a reviewed boundary repair, reduce the
store explicitly and inspect the diff before committing:

~~~shell
./gradlew :website:test \
  --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest \
  -Darchunit.freeze.store.default.allowStoreUpdate=true
git diff -- website/src/test/resources/architecture-baseline
~~~

Accept only removed violations. Module diagrams and canvases are generated under
`website/build/spring-modulith-docs/` and are review artifacts, not tracked files.
```

Verification:
- Read the rendered README section and run both commands on the development host using the `.\gradlew.bat` equivalent.
- Expected: the normal command is read-only; the update command makes no change when the code has not reduced a violation.

- [x] **Step 3: Run focused and aggregate automated verification.**

```powershell
.\gradlew.bat :website:test --tests 'dev.christopherbell.architecture.*' --stacktrace
.\gradlew.bat :website:check --stacktrace
```

Expected:
- Rule fixture, module verification, frozen baseline, and documentation tests pass.
- Existing Java, JavaScript, Pester, packaged-JAR, sensor, and production-context checks pass.
- No baseline file changes after the read-only run.

- [x] **Step 4: Prove Modulith remains absent from the runtime artifact.**

```powershell
.\gradlew.bat :website:bootJar --stacktrace
$candidateJar = Get-ChildItem website\build\libs\*.jar |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
jar tf $candidateJar.FullName | Select-String 'spring-modulith'
```

Expected: `bootJar` succeeds and the final command returns no matches.

- [x] **Step 5: Verify the packaged candidate on an alternate port.**

Invoke `verify-local-spring-app` before this runtime action. Resolve an unused port, preferring `8096`, and create a uniquely named disposable MongoDB database. Start the packaged candidate with `local,deploy-smoke`, the alternate port, and the disposable database.

```powershell
$candidatePort = 8096
if (Get-NetTCPConnection -LocalPort $candidatePort -State Listen -ErrorAction SilentlyContinue) {
  throw "Candidate port $candidatePort is already in use."
}
$candidateJar = Get-ChildItem website\build\libs\*.jar |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
$candidateDatabase = 'christopherbell_modular_monolith_foundation_' +
  [DateTimeOffset]::UtcNow.ToString('yyyyMMddHHmmss')
$candidateStdout = Join-Path $PWD 'website\build\modular-monolith-foundation.stdout.log'
$candidateStderr = Join-Path $PWD 'website\build\modular-monolith-foundation.stderr.log'
$candidateArguments = @(
  '-jar',
  $candidateJar.FullName,
  '--spring.profiles.active=local,deploy-smoke',
  "--server.port=$candidatePort",
  "--spring.mongodb.database=$candidateDatabase")
$candidateProcess = Start-Process `
  -FilePath 'java' `
  -ArgumentList $candidateArguments `
  -PassThru `
  -WindowStyle Hidden `
  -RedirectStandardOutput $candidateStdout `
  -RedirectStandardError $candidateStderr

$deadline = [DateTimeOffset]::UtcNow.AddMinutes(2)
do {
  try {
    $readiness = Invoke-WebRequest `
      "http://localhost:$candidatePort/actuator/health/readiness" `
      -UseBasicParsing
  } catch {
    if ([DateTimeOffset]::UtcNow -ge $deadline) { throw }
    Start-Sleep -Seconds 2
  }
} until ($readiness.StatusCode -eq 200)

$readiness = Invoke-WebRequest 'http://localhost:8096/actuator/health/readiness' -UseBasicParsing
$liveness = Invoke-WebRequest 'http://localhost:8096/actuator/health/liveness' -UseBasicParsing
$home = Invoke-WebRequest 'http://localhost:8096/' -UseBasicParsing
$readiness.StatusCode
$readiness.Content
$liveness.StatusCode
$liveness.Content
$home.StatusCode
```

Expected:
- Readiness URL `http://localhost:8096/actuator/health/readiness`: HTTP 200 with body status `UP` and MongoDB ready.
- Liveness URL `http://localhost:8096/actuator/health/liveness`: HTTP 200 with body status `UP`.
- Home URL `http://localhost:8096/`: HTTP 200.
- Production port 8080 and the `ChristopherBellDev` service are untouched.
- Save `$candidateProcess.Id`, `$candidateDatabase`, both log paths, request URLs, statuses, and bodies in the Builder test report.
- Stop and clean only the owned candidate targets after evidence is saved:

```powershell
if (!$candidateProcess.HasExited) {
  Stop-Process -Id $candidateProcess.Id
  $candidateProcess.WaitForExit()
}
mongosh --quiet --eval "db.getSiblingDB('$candidateDatabase').dropDatabase()"
```

- [x] **Step 6: Commit Task 4.**

```powershell
git add README.md website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java
git commit -m "docs: publish modular monolith architecture workflow"
```

Task-level verification:
- Focused architecture suite, `:website:check`, boot-JAR inspection, and alternate-port runtime evidence all pass.

## Follow-On Plan Portfolio

This foundation plan is intentionally the only ready-for-execution plan in the portfolio. Each entry below requires a separate inspected, line-level Builder plan before code changes:

1. **Account and authorization boundary:** absorb `permission` into account ownership, define account commands/queries/IDs/results, replace security and consumer repository/entity access, annotate account as the first closed module, and reduce the baseline.
2. **Bootstrap and configuration boundary:** classify every `configuration` type as feature-owned, platform-neutral, or bootstrap-only; move feature wiring; prohibit business-to-bootstrap access.
3. **Lower-coupled modules:** one plan each for blog, location, Canes tracker, vehicle, and What's for Lunch; close each module before beginning the next.
4. **Social core:** separate plans in dependency order for post, message, notification, report, and federation; use in-process events only for already non-critical follow-up behavior.
5. **Host-heavy modules:** separate plans for music, shared folder, and admin that preserve filesystem, lease, native process, sensor, and Windows service boundaries.
6. **Final closure:** migrate photo and remaining ownership, remove compatibility facades, delete the frozen store, require zero undeclared cross-module access, and publish the final module graph.

Every follow-on plan must use the same isolated-worktree, RED/GREEN, focused-test, full-check, alternate-port, PR/CI, merge, and production-verification workflow.

## Code Changes

### `website/build.gradle.kts`

- Code Edit 1.2: import the Spring Modulith 2.1.0 BOM in dependency management.
- Code Edit 1.3: add `spring-modulith-starter-test` to test dependencies only.
- Code Edit 1.5: forward only the approved ArchUnit store-creation and store-update flags to forked test workers.

### `website/src/main/resources/application.yml`

- Code Edit 1.4: select explicitly annotated module detection.

### `website/src/test/java/dev/christopherbell/architecture/ModularMonolithArchitectureTest.java`

- Code Edit 1.1: create central Modulith verification.
- Code Edit 3.2: add both frozen production dependency gates.
- Code Edit 4.1: generate module documentation from the verified model.

### `website/src/test/java/dev/christopherbell/architecture/LegacyModuleDependencyRules.java`

- Code Edit 2.6: implement deterministic area ownership, API allowance, orchestration direction, production import, and frozen-rule factories.

### Rule contract tests and fixtures

- Code Edits 2.1-2.5: create API, internal, orchestration, and consumer fixtures plus contract tests.

### `website/src/test/resources/archunit.properties`

- Code Edit 3.1: make the version-controlled store read-only by default.

### Generated review artifacts

- `gradle/verification-metadata.xml`: Gradle-generated hashes for the resolved test graph.
- `website/src/test/resources/architecture-baseline/**`: ArchUnit-generated frozen-rule index and violation files.
- `website/build/spring-modulith-docs/**`: untracked generated diagrams and canvases.

### `README.md`

- Code Edit 4.2: publish module ownership and safe baseline commands.

## Files and Modules

- Build ownership: `website/build.gradle.kts`, `gradle/verification-metadata.xml`.
- Discovery configuration: `website/src/main/resources/application.yml`.
- Architecture test ownership: `website/src/test/java/dev/christopherbell/architecture/**`.
- Baseline ownership: `website/src/test/resources/archunit.properties` and `website/src/test/resources/architecture-baseline/**`.
- Contributor contract: `README.md`.
- No production business module, `cbell-lib` source, frontend asset, MongoDB schema, or operations script changes.

## Unit Testing

- RED Task 1: central test cannot compile without Spring Modulith.
- GREEN Task 1: explicit discovery excludes unannotated `configuration`; `ApplicationModules.verify()` passes.
- RED Task 2: contract tests cannot compile without the dependency-rule helper.
- GREEN Task 2: internal beta access and alpha-to-ops access violate; beta API access does not; permission maps to account.
- RED Task 3: central test cannot create an absent store under read-only defaults.
- GREEN Task 3: explicit creation succeeds; ordinary repeat runs pass without store changes.
- GREEN Task 4: documentation generation succeeds and the entire architecture package passes as a focused suite.

Commands:

```powershell
.\gradlew.bat :website:test --tests dev.christopherbell.architecture.LegacyModuleDependencyRulesTest --stacktrace
.\gradlew.bat :website:test --tests dev.christopherbell.architecture.ModularMonolithArchitectureTest --stacktrace
.\gradlew.bat :website:test --tests 'dev.christopherbell.architecture.*' --stacktrace
```

## Local Testing

1. Use a private `GRADLE_USER_HOME` and run `:website:check --stacktrace` without a short outer timeout.
2. Confirm dependency verification succeeds without write mode after metadata generation.
3. Confirm a read-only architecture run produces no baseline diff.
4. Build the boot JAR and prove it contains no `spring-modulith` nested artifact.
5. Invoke `verify-local-spring-app`, start the packaged candidate on unused port 8096 or another verified non-8080 port, and use a disposable MongoDB database.
6. Record URL, request, HTTP status, and response body for readiness, liveness, and home.
7. Stop only the candidate process and clean only its disposable data.

## Validation

- `git diff --check` passes.
- `git status --short` contains only intended branch changes before each commit.
- Focused rule and module tests pass.
- The frozen store is stable under a normal run and contains no line-number churn.
- `:website:check` passes all applicable Java, JavaScript, Pester, packaged-JAR, sensor, and deployment-context checks.
- `runtimeClasspath` and the boot JAR contain no Spring Modulith runtime artifact.
- Alternate-port readiness and liveness return HTTP 200/`UP`; `/` returns HTTP 200.
- Existing Linux, macOS, Windows, Dependency Review, and CodeQL PR checks pass.
- After merge and protected deployment, verify listener rotation, readiness/liveness, exact release SHA, public/local HTTP 200, security headers, service state, and absence of new architecture-related runtime errors.

## Rollback or Recovery

- Before merge, revert the focused task commit or close the branch; no production data is involved.
- After merge, revert the foundation commits and regenerate dependency-verification metadata for the reverted graph. The boot JAR and MongoDB schemas are unchanged, so no data rollback is required.
- If the frozen store is corrupted, do not enable creation in CI. Delete only the branch's generated store, recreate it locally with the explicit creation command against the reviewed production classes, and compare the complete diff before recommitting.
- If a runtime artifact unexpectedly includes Spring Modulith, stop delivery, remove the runtime dependency path, regenerate verification metadata, and rerun boot-JAR inspection before any deployment.
- Never recover by editing generated store identifiers or dependency hashes by hand.

## Risks

- **Empty module model appears successful:** explicit discovery initially finds no closed production modules. Mitigation: permanently assert that unannotated `configuration` is excluded, retain `ApplicationModules.verify()`, and require the account follow-on plan to add the first explicit module.
- **Baseline normalizes too much:** mapping or API detection could hide forbidden access. Mitigation: fixture-test internal/API/orchestration cases, map only `permission` to account, and keep orchestration direction as a separate rule that does not exempt `.api`.
- **ArchUnit violation churn:** default dependency descriptions include line details. Mitigation: emit custom source-area/target-area and source-class/target-class messages, distinct and sorted.
- **Baseline grows silently:** permissive store settings could bless debt. Mitigation: creation and update are false in committed configuration; explicit update must be paired with an inspected diff that contains removals only.
- **Test dependency leaks into production:** an incorrect Gradle scope could enlarge the boot JAR or activate runtime features. Mitigation: `testImplementation`, runtime-classpath inspection, and exact boot-JAR entry inspection.
- **Dependency verification damage:** bulk regeneration could rewrite unrelated hashes. Mitigation: generate from the focused task, inspect the metadata diff, and reject unrelated removals or substitutions.
- **Dirty checkout loss:** the authoritative checkout contains unrelated work. Mitigation: use a verified sibling worktree from refreshed `origin/main` and never clean/reset the authoritative path.
- **Foundation branch becomes a migration branch:** adding capability refactors would undermine reviewability. Mitigation: enforce this plan's non-goals and create the account boundary as the next separate plan/PR.

## Completion Criteria

- Spring Modulith 2.1.0 is resolved only on the website test classpath and is absent from runtime classpath and the boot JAR.
- Explicitly annotated detection is configured and verified.
- `ApplicationModules.verify()` runs in `:website:test` and existing root CI builds.
- Rule fixtures prove internal/API/orchestration/permission semantics.
- The production baseline is generated, committed, deterministic, and read-only by default.
- Ordinary focused and aggregate test runs do not modify the store.
- Generated PlantUML/module-canvas output comes from the verified `ApplicationModules` model and remains untracked.
- README contributor commands are accurate.
- Focused tests, `:website:check`, dependency verification, boot-JAR inspection, alternate-port runtime checks, PR CI, Dependency Review, and CodeQL pass.
- The foundation merges and deploys without changing HTTP behavior, MongoDB data, frontend behavior, or the single-service production topology.
- A separate account/authorization implementation plan is the next migration artifact; no business module closure is implied by completing this foundation plan.
