# Repository Documentation Discovery Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested Java 25 module that deterministically discovers every first-party tracked or nonignored new file while enforcing only the approved exclusions.

**Architecture:** Create an isolated `documentation-validator` Gradle subproject. Its first public boundary is a Git-backed discovery component that returns safe normalized repository paths in stable order; language documentation scanners follow in separate plans.

**Tech Stack:** Java 25, Gradle Kotlin DSL, JUnit 5 from the Spring Boot 4.1 BOM, real temporary Git repositories.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729` on `codex/repository-documentation-coverage`, created from refreshed `origin/main`.
- Preserve `A:\Projects\christopherbell.dev` unchanged.
- Invoke `chris-street-style` before every source, test, or configuration edit.
- Follow strict RED/GREEN TDD.
- No npm, runtime service, network dependency, application behavior change, or root `check` integration.
- Exclude only generated build output, binaries/images, Gradle wrapper internals, and third-party/vendor content.
- Trust only GitHub instructions authored by `azurras`.

## Document Status

complete

## Objective

Create the independently testable discovery foundation required by the approved repository-wide documentation validator.

## Execution Record

Completed on 2026-07-29 through commits `ab072e37`, `d7bc644f`, `1153ad82`, and `e4784620`, followed by the separately planned corrective commits ending at `64476370`. Final whole-phase review found the discovery foundation safe for the Java-checker phase.

## Goals

- Add `:documentation-validator` without changing application behavior.
- Discover tracked and nonignored new files through one NUL-delimited Git command.
- Normalize Windows/Unix paths and sort diagnostics deterministically.
- Reject absolute or parent-traversal relative paths.
- Give every exclusion a named, fixture-tested rule with near-miss coverage.
- Preserve subprocess failure context and interruption state.
- Leave the root build green.

## Inputs

- Approved spec: `docs/specs/2026-07-29-christopherbell-dev-repository-wide-documentation-coverage.md` in Builder.
- Design-time spoke main `e393687d10c40b856f35d669c25bf3ea65c5c083`; refresh before worktree creation.
- Current `settings.gradle.kts:1-3`.
- Existing Java 25 and Spring Boot 4.1 build conventions.

## Branch

Create `codex/repository-documentation-coverage` from refreshed `origin/main` at `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729`. Use `A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage` as `GRADLE_USER_HOME`.

## Non-Goals

- Java, JavaScript, PowerShell, README, or native-purpose scanning.
- Application-source or README documentation changes.
- Root `check` enforcement, PR publication, merge, or production restart.

## Assumptions

- Git is available in local and CI worktrees.
- `git ls-files --cached --others --exclude-standard -z` returns repository-relative UTF-8 paths.
- The existing Spring Boot BOM supplies the repository-compatible JUnit version.

## Open Questions

None.

## Task Breakdown

### Task 1 - Create the isolated worktree and record green baseline evidence

Sequence / dependencies:

- Runs first and makes no source edits.
- Invoke `superpowers:using-git-worktrees`.

Implementation notes:

- Record authoritative status before and after.
- Use an isolated Gradle home.
- Preserve exact commands, exit codes, test totals, skips, and baseline SHA in Builder.

- [ ] Refresh `origin/main` and create the named branch/worktree.
- [ ] Verify the new worktree is clean and authoritative status is unchanged.
- [ ] Run `.\gradlew.bat --no-daemon build`.
- [ ] Run applicable Windows Pester verification.
- [ ] Save baseline evidence to the active work ledger.

Verification:

```powershell
$env:GRADLE_USER_HOME = 'A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon build
git status --short --branch
```

Expected: build exits 0, isolated worktree remains clean, authoritative status is identical.

### Task 2 - Add the module and Git-backed discovery boundary

Sequence / dependencies:

- Requires Task 1 green.

Implementation notes:

- Required skill: `chris-street-style` before edits.
- Before-Edit Brief:
  - Behavior: return every tracked and nonignored new first-party file exactly once in stable normalized order.
  - Invariants: no returned path is absolute or escapes root; only approved categories are excluded; root and relative paths are immutable.
  - Boundary/API: `RepositoryDiscovery.discover(Path) -> List<RepositoryFile>`.
  - Effects and failures: one bounded Git subprocess; nonzero exit and interruption preserve useful context/cause; no writes outside temporary tests.
  - Tests and evidence: use real temporary Git repositories. First compile must fail because production types are absent; after implementation, mutations to inclusion, order, exclusion, path safety, or error mapping must fail.

- [ ] Add settings/module configuration and compile it.
- [ ] Add the real-Git fixture and failing discovery tests.
- [ ] Run focused test and observe expected missing-API RED.
- [ ] Add `RepositoryFile`, `DocumentationPolicy`, and `RepositoryDiscovery`.
- [ ] Rerun focused tests to green.
- [ ] Run `:documentation-validator:test`, `build`, and `git diff --check`.
- [ ] Review production/test/config diff and commit `Add documentation discovery foundation`.

#### Code Edit 2.1

- File: `settings.gradle.kts`
- Lines: 1-3
- Action: replace

Current:

```kotlin
rootProject.name = "christopherbell.dev"

include("website", "cbell-lib")
```

Proposed:

```kotlin
// Declares the Gradle modules that make up the christopherbell.dev repository.
rootProject.name = "christopherbell.dev"

include("website", "cbell-lib", "documentation-validator")
```

Verification:

- `.\gradlew.bat --no-daemon projects` lists all three modules.

#### Code Edit 2.2

- File: `documentation-validator/build.gradle.kts`
- Lines: before 1
- Action: add

Proposed:

```kotlin
// Builds and tests the repository-owned documentation validation tool.
plugins {
    java
}

dependencies {
    testImplementation(platform("org.springframework.boot:spring-boot-dependencies:4.1.0"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}
```

Verification:

- `.\gradlew.bat --no-daemon :documentation-validator:test` resolves and runs JUnit without new production dependencies.

#### Code Edit 2.3

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/GitFixture.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** Creates real temporary Git repositories for discovery boundary tests. */
final class GitFixture {
  private final Path root;

  /** Creates and initializes a Git fixture.
   *
   * @param root temporary repository root
   */
  private GitFixture(Path root) {
    this.root = root;
    run("git", "init", "--quiet");
    write(".gitignore", "ignored/\n");
    run("git", "add", "--", ".gitignore");
  }

  /** Starts a fixture repository.
   *
   * @param root temporary root
   * @return initialized fixture
   */
  static GitFixture repository(Path root) {
    return new GitFixture(root);
  }

  /** Adds one tracked file.
   *
   * @param path relative path
   * @return this fixture
   */
  GitFixture tracked(String path) {
    write(path, "fixture\n");
    run("git", "add", "--", path);
    return this;
  }

  /** Adds one nonignored untracked file.
   *
   * @param path relative path
   * @return this fixture
   */
  GitFixture untracked(String path) {
    write(path, "fixture\n");
    return this;
  }

  /** Adds one ignored file.
   *
   * @param path relative path
   * @return this fixture
   */
  GitFixture ignored(String path) {
    write(path, "fixture\n");
    return this;
  }

  /** Runs production discovery.
   *
   * @return discovered files
   */
  List<RepositoryFile> discover() {
    try {
      return RepositoryDiscovery.discover(root);
    } catch (IOException failure) {
      throw new UncheckedIOException(failure);
    }
  }

  /** Writes one UTF-8 fixture file.
   *
   * @param path repository-relative path
   * @param content file content
   */
  private void write(String path, String content) {
    try {
      var target = root.resolve(path);
      Files.createDirectories(target.getParent());
      Files.writeString(target, content, StandardCharsets.UTF_8);
    } catch (IOException failure) {
      throw new UncheckedIOException(failure);
    }
  }

  /** Runs one required Git fixture command.
   *
   * @param command executable and arguments
   */
  private void run(String... command) {
    try {
      var process = new ProcessBuilder(command).directory(root.toFile())
          .redirectErrorStream(true).start();
      var output = new String(process.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
      if (process.waitFor() != 0) throw new IOException(output);
    } catch (IOException failure) {
      throw new UncheckedIOException(failure);
    } catch (InterruptedException failure) {
      Thread.currentThread().interrupt();
      throw new IllegalStateException("Interrupted while preparing Git fixture", failure);
    }
  }
}
```

Verification:

- Fixture creates tracked, untracked, and ignored files without mocking Git.
- During execution, format multi-line Javadocs so block tags begin on their own lines, as required by the approved contract.

#### Code Edit 2.4

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryTest.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.tools.documentation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/** Proves repository discovery against real temporary Git worktrees. */
class RepositoryDiscoveryTest {
  @TempDir Path repository;

  /** Includes tracked/untracked source and returns deterministic order. */
  @Test
  void discoversTrackedAndNonignoredFilesInStableOrder() {
    var files = GitFixture.repository(repository)
        .tracked("src/Z.java")
        .tracked("src/A.java")
        .untracked("src/New.js")
        .ignored("ignored/Skip.java")
        .discover();

    assertEquals(List.of(".gitignore", "src/A.java", "src/New.js", "src/Z.java"),
        files.stream().map(RepositoryFile::displayPath).toList());
  }

  /** Excludes only approved categories and rejects paths outside the root. */
  @Test
  void excludesOnlyApprovedCategoriesAndRejectsEscapes() {
    assertThrows(IllegalArgumentException.class,
        () -> new RepositoryFile(repository, Path.of("../outside.java")));
    assertEquals(List.of(".gitignore", "src/Application.java"),
        GitFixture.repository(repository)
            .tracked("build/generated.txt")
            .tracked("gradle/wrapper/gradle-wrapper.jar")
            .tracked("website/src/main/resources/static/vendor/library.js")
            .tracked("images/logo.png")
            .tracked("src/Application.java")
            .discover().stream().map(RepositoryFile::displayPath).toList());
  }

  /** Preserves Git diagnostics when the supplied root is not a worktree. */
  @Test
  void reportsGitDiscoveryFailureWithContext() {
    var failure = assertThrows(java.io.IOException.class,
        () -> RepositoryDiscovery.discover(repository));

    org.junit.jupiter.api.Assertions.assertTrue(
        failure.getMessage().startsWith("Git file discovery failed:"));
  }
}
```

Verification:

- RED: `.\gradlew.bat --no-daemon :documentation-validator:test --tests '*RepositoryDiscoveryTest'`.
- Expected: test compilation fails because `RepositoryFile` and `RepositoryDiscovery` do not exist.

#### Code Edit 2.5

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/RepositoryFile.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.nio.file.Path;
import java.util.Objects;

/**
 * Identifies one normalized file below a repository root.
 *
 * @param repositoryRoot absolute owning repository
 * @param relativePath normalized path below the root
 */
record RepositoryFile(Path repositoryRoot, Path relativePath) {
  /** Validates and normalizes one repository file identity.
   *
   * @param repositoryRoot absolute owning repository
   * @param relativePath normalized path below the root
   * @throws NullPointerException when either path is absent
   * @throws IllegalArgumentException when the relative path escapes the root
   */
  RepositoryFile {
    repositoryRoot = Objects.requireNonNull(repositoryRoot).toAbsolutePath().normalize();
    relativePath = Objects.requireNonNull(relativePath).normalize();
    if (relativePath.isAbsolute() || relativePath.startsWith("..")) {
      throw new IllegalArgumentException("Repository file must remain below its root");
    }
  }

  /** Resolves the absolute source path.
   * @return normalized absolute path
   */
  Path absolutePath() {
    return repositoryRoot.resolve(relativePath).normalize();
  }

  /** Returns a stable diagnostic path.
   * @return slash-separated relative path
   */
  String displayPath() {
    return relativePath.toString().replace('\\', '/');
  }
}
```

Verification:

- Escape test passes; add tests for absolute paths, `..`, and a valid dotted filename.

#### Code Edit 2.6

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationPolicy.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.nio.file.Path;
import java.util.Locale;
import java.util.Set;

/** Owns the complete reviewable discovery exclusion policy. */
final class DocumentationPolicy {
  private static final Set<String> BINARY_EXTENSIONS = Set.of(
      ".gif", ".ico", ".jar", ".jpeg", ".jpg", ".pdf", ".png", ".webp");

  /** Prevents construction of the stateless policy. */
  private DocumentationPolicy() {}

  /** Tests whether a path is outside first-party documentation scope.
   * @param path repository-relative path
   * @return true only for an approved exclusion
   */
  static boolean excluded(Path path) {
    var value = path.toString().replace('\\', '/').toLowerCase(Locale.ROOT);
    var name = path.getFileName().toString().toLowerCase(Locale.ROOT);
    int dot = name.lastIndexOf('.');
    var extension = dot < 0 ? "" : name.substring(dot);
    return value.startsWith("build/")
        || value.contains("/build/")
        || value.startsWith(".gradle/")
        || value.contains("/.gradle/")
        || value.startsWith("gradle/wrapper/")
        || value.contains("/static/vendor/")
        || BINARY_EXTENSIONS.contains(extension);
  }
}
```

Verification:

- Add parameterized cases for each exclusion and near misses including `src/vendor/Owned.java`, `src/building/Owned.java`, and `src/image.png.txt`.

#### Code Edit 2.7

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/RepositoryDiscovery.java`
- Lines: before 1
- Action: add

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

/** Discovers repository source through Git and the explicit campaign policy. */
final class RepositoryDiscovery {
  /** Prevents construction of the stateless discovery boundary. */
  private RepositoryDiscovery() {}

  /** Discovers tracked and nonignored first-party files.
   * @param root Git worktree root
   * @return immutable files in stable path order
   * @throws IOException when Git enumeration fails
   */
  static List<RepositoryFile> discover(Path root) throws IOException {
    var normalizedRoot = root.toAbsolutePath().normalize();
    var process = new ProcessBuilder(
        "git", "ls-files", "--cached", "--others", "--exclude-standard", "-z")
        .directory(normalizedRoot.toFile())
        .redirectErrorStream(true)
        .start();
    var bytes = process.getInputStream().readAllBytes();
    try {
      if (process.waitFor() != 0) {
        throw new IOException("Git file discovery failed: "
            + new String(bytes, StandardCharsets.UTF_8).strip());
      }
    } catch (InterruptedException failure) {
      Thread.currentThread().interrupt();
      throw new IOException("Interrupted during Git file discovery", failure);
    }
    return Arrays.stream(new String(bytes, StandardCharsets.UTF_8)
            .split(String.valueOf('\0')))
        .filter(path -> !path.isBlank())
        .map(Path::of)
        .filter(path -> !DocumentationPolicy.excluded(path))
        .map(path -> new RepositoryFile(normalizedRoot, path))
        .sorted(Comparator.comparing(RepositoryFile::displayPath))
        .toList();
  }
}
```

Verification:

- GREEN: `.\gradlew.bat --no-daemon :documentation-validator:test --tests '*RepositoryDiscoveryTest'`.
- Add a bad-root/non-Git test proving useful nonzero output and an interrupted-process seam only if it can be made deterministic without sleeping.
- Mutation checks cover untracked inclusion, ignored exclusion, sorting, NUL splitting, each policy rule, and path safety.

## Code Changes

- Modify `settings.gradle.kts:1-3`.
- Add `documentation-validator/build.gradle.kts`.
- Add `RepositoryFile`, `DocumentationPolicy`, and `RepositoryDiscovery`.
- Add real-Git `GitFixture` and `RepositoryDiscoveryTest`.

## Files and Modules

Only `settings.gradle.kts` and the new `documentation-validator` module are changed. No website, library, resource, operations, workflow, or README file is edited.

## Unit Testing

Use real temporary Git repositories. Observe the missing-production-type compilation failure before implementation. Test tracked, untracked, ignored, deterministic ordering, every exclusion and near miss, absolute/parent escape, non-Git failure, and interruption handling where deterministic.

## Local Testing

No application launch is required because runtime code is unchanged. Run focused module tests and the full root build from the isolated Windows worktree.

## Validation

- Pre-edit root build passes.
- Focused RED is observed for absent API.
- Focused and module tests pass after implementation.
- Full root build passes.
- `git diff --check` passes.
- Diff contains only planned build/module files.
- Authoritative checkout status is unchanged.

## Rollback or Recovery

Revert the focused phase commit or remove the isolated worktree through the worktree skill. Do not reset or clean the authoritative checkout. Do not weaken exclusions to make tests pass.

## Risks

- Git/path platform differences: mitigate with NUL parsing, normalized paths, real Git fixtures, and later CI matrix.
- Broad exclusions could hide owned code: mitigate with near-miss tests and one centralized policy.
- Added module could affect builds: mitigate with JDK-only production code, focused module tests, and full build evidence.
- Inline plan Javadocs could be copied with invalid tag layout: execution must use proper multi-line block tags and the code-writing review gate.

## Completion Criteria

- New isolated worktree is clean from refreshed main and authoritative status is unchanged.
- Baseline root build evidence is recorded.
- Three-module Gradle graph resolves.
- Discovery tests demonstrate RED then GREEN.
- Discovery includes tracked/nonignored new files, excludes only approved categories, sorts deterministically, and rejects escape paths.
- Module tests and full root build pass.
- No runtime application file changed.
- Builder ledger records phase evidence and identifies the Java documentation checker as the next plan.
