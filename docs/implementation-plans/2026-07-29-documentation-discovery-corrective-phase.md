# Documentation Discovery Corrective Phase Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the residual archive-classification, interrupted-reader cleanup, and Javadoc findings so later documentation validators can safely depend on repository discovery.

**Architecture:** Retain the existing named exclusion policy and single-owner `GitProcessSession`. Extend archive matching with exact case-insensitive suffixes, and replace the reader cleanup early return with a monotonic-deadline loop that preserves interruption context while verifying termination or reporting a bounded failure.

**Tech Stack:** Java 25, JUnit Jupiter, Gradle Kotlin DSL, real Git fixtures, JDK concurrency primitives only.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729` on `codex/repository-documentation-coverage`.
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; do not edit, clean, stage, reset, switch, commit, or run builds there.
- Do not rebase, merge, pull, push, or open a pull request in this corrective phase.
- Use `A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage` as `GRADLE_USER_HOME`.
- Keep production dependencies JDK-only and add no npm dependency.
- Change only the four discovery production/test files named by the approved corrective specification.
- Do not add Java/non-Java documentation validation, README updates, Gradle `check` wiring, CI wiring, or documentation remediation.
- Every changed/new Java type, constructor, method, private method, field, parameter, return value, and thrown failure must retain useful accurate Javadocs.
- Use deterministic latches/deadlines for concurrency tests; do not use sleeps.

---

## Document Status

complete

## Objective

Produce one cohesive, independently reviewed correction commit on top of `e4784620bdfa072fb07415ea1d4e6fce688d0d27` that resolves every residual load-bearing discovery finding.

## Execution Record

Completed on 2026-07-29 through commits `bc91c576`, `010524e6`, `236503c2`, and `64476370`. The final scoped re-review returned `ALL_FINDINGS_ADDRESSED` with no introduced regression. Final verification reported 1,555 tests, 1,551 passed, 0 failures/errors, and 4 skipped.

## Goals

- Classify `.nar`, `.ear`, and `.tar.gz` archives without excluding owned near misses.
- Guarantee that interrupted reader cleanup continues to a bounded verified outcome.
- Preserve governing failures, cleanup failures, causes, suppressed failures, and caller interrupt status.
- Correct the null-input and bounded-cleanup Javadocs.
- Pass focused, module, private-Javadoc, full-build, and diff verification.

## Inputs

- Approved design: `docs/specs/2026-07-29-documentation-discovery-corrective-design.md`.
- Original discovery plan: `docs/implementation-plans/2026-07-29-repository-documentation-discovery-foundation.md`.
- Final scoped re-review verdict: residual `.nar`/`.ear`/`.tar.gz`, interrupted reader verification, and Javadoc findings.
- Current spoke head: `e4784620bdfa072fb07415ea1d4e6fce688d0d27`.

## Branch

- Continue `codex/repository-documentation-coverage` in the existing isolated worktree.
- Original base: `origin/main` at `5de2a8b02941ff7e95b6f2648b7bada9397f68b9`.
- Do not reconcile the branch's upstream drift until this corrective phase is independently review-clean.

## Non-Goals

- No application, library, operations, resource, workflow, README, or Gradle-wrapper edits.
- No broader archive-format invention beyond repository-native `.gitignore` package formats.
- No executor, future, structured-concurrency, or replacement process abstraction.
- No production publishing or integration.

## Assumptions

- Java 25 supports `Thread.join(Duration)` and virtual threads already used by the module.
- `InterruptedException` clears the current thread's interrupt status, permitting bounded cleanup to continue before `close()` restores it.
- The existing process fake and real-Git fixture remain the correct narrow test boundaries.
- The full build remains a non-runtime verification; no application launch is needed.

## Open Questions

None.

## Task Breakdown

### Task 1 - Correct archive scope and interrupted reader termination

Sequence / dependencies:

- Runs after the approved corrective specification and starts from clean commit `e4784620bdfa072fb07415ea1d4e6fce688d0d27`.
- This is one task because the residual policy, lifecycle, and Javadoc findings form one discovery-boundary acceptance gate and require one final independent review.

Implementation notes:

- Required skill: `write-chris-street-style-code` before any code edits; invoke it and `superpowers:test-driven-development`, then read the Java, design/API, and testing/review references.
- Before-Edit Brief:
  - Behavior: discovery excludes every repository-native archive package, and cleanup never claims success after an interrupted reader join unless the reader is verified stopped.
  - Invariants: exclusion reasons remain named and narrow; owned near misses remain discoverable; one session owns the process/streams/reader; every wait is bounded; primary failures and interrupt status are preserved.
  - Boundary/API: preserve `DocumentationPolicy.exclusionReason(Path)` and both `RepositoryDiscovery.discover(...)` signatures; change only their documented failures and internal behavior.
  - Effects and failures: one Git subprocess and one virtual reader may block; timeout, process, stream, reader, cleanup, null-input, and interruption failures retain causes and suppression order.
  - Tests and evidence: focused policy and cleanup tests must fail before production edits, then pass; module tests, private Javadocs, the root build, and diff checks must finish green.

- [ ] Add archive, near-miss, null-input, and interrupted-cleanup regression tests before production edits.
- [ ] Run the focused tests and record RED: missing archive classifications and missing nested cleanup-termination failure after interruption.
- [ ] Implement suffix classification, monotonic-deadline reader cleanup, and accurate Javadocs.
- [ ] Rerun the identical focused tests to GREEN.
- [ ] Run module tests, direct private Javadocs, the full root build, and `git diff --check`.
- [ ] Self-review the complete production/test diff and commit `Correct documentation discovery cleanup`.

#### Code Edit 1.1

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryTest.java`
- Lines: 55-67
- Action: replace

Current:

```java
        .tracked("artifacts/Compiled.class")
        .tracked("artifacts/package.zip")
        .tracked("artifacts/application.war")
        .tracked("artifacts/archive.rar")
        .tracked("images/logo.png")
        .tracked("images/vector.svg")
        .tracked("src/vendor/Owned.java")
        .tracked("src/building/Owned.java")
        .tracked("src/image.png.txt")
        .tracked("nested/gradle/wrapper/Owned.java")
        .tracked("nested/.superpowers/brainstorm/session/state/server.pid")
        .tracked(".superpowers/brainstorm/session/state/server.pid.txt")
        .tracked("src/Application.java")
```

Proposed:

```java
        .tracked("artifacts/Compiled.class")
        .tracked("artifacts/package.zip")
        .tracked("artifacts/application.war")
        .tracked("artifacts/archive.rar")
        .tracked("artifacts/native.nar")
        .tracked("nested/artifacts/application.ear")
        .tracked("artifacts/package.TAR.GZ")
        .tracked("images/logo.png")
        .tracked("images/vector.svg")
        .tracked("src/vendor/Owned.java")
        .tracked("src/building/Owned.java")
        .tracked("src/image.png.txt")
        .tracked("src/package.ear.txt")
        .tracked("src/package.tar.gz.txt")
        .tracked("src/package.tar.gzip")
        .tracked("nested/gradle/wrapper/Owned.java")
        .tracked("nested/.superpowers/brainstorm/session/state/server.pid")
        .tracked(".superpowers/brainstorm/session/state/server.pid.txt")
        .tracked("src/Application.java")
```

Verification:

- The real-Git test fails before the policy edit because the three new archives appear in discovered results.

#### Code Edit 1.2

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryTest.java`
- Lines: 70-79
- Action: replace

Current:

```java
    assertEquals(List.of(
        ".gitignore",
        ".superpowers/brainstorm/session/state/server.pid.txt",
        "nested/.superpowers/brainstorm/session/state/server.pid",
        "nested/gradle/wrapper/Owned.java",
        "src/Application.java",
        "src/building/Owned.java",
        "src/image.png.txt",
        "src/vendor/Owned.java"),
        files.stream().map(RepositoryFile::displayPath).toList());
```

Proposed:

```java
    assertEquals(List.of(
        ".gitignore",
        ".superpowers/brainstorm/session/state/server.pid.txt",
        "nested/.superpowers/brainstorm/session/state/server.pid",
        "nested/gradle/wrapper/Owned.java",
        "src/Application.java",
        "src/building/Owned.java",
        "src/image.png.txt",
        "src/package.ear.txt",
        "src/package.tar.gz.txt",
        "src/package.tar.gzip",
        "src/vendor/Owned.java"),
        files.stream().map(RepositoryFile::displayPath).toList());
```

Verification:

- The expected list retains every owned near miss while omitting the new archive packages.

#### Code Edit 1.3

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryTest.java`
- Lines: after 131
- Action: add

Proposed:

```java
  /** Rejects absent inputs at both discovery trust boundaries. */
  @Test
  void rejectsAbsentDiscoveryInputs() {
    assertThrows(NullPointerException.class, () -> RepositoryDiscovery.discover(null));
    assertThrows(NullPointerException.class, () -> DocumentationPolicy.exclusionReason(null));
  }
```

Verification:

- The test passes against existing runtime behavior and anchors the Javadoc failure contract without changing semantics.

#### Code Edit 1.4

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryTest.java`
- Lines: after 177
- Action: add

Proposed:

```java
        Arguments.of("archives/native.nar", DocumentationPolicy.ExclusionReason.ARCHIVE_FILE),
        Arguments.of("archives/application.ear",
            DocumentationPolicy.ExclusionReason.ARCHIVE_FILE),
        Arguments.of("archives/package.tar.gz",
            DocumentationPolicy.ExclusionReason.ARCHIVE_FILE),
        Arguments.of("archives/package.TAR.GZ",
            DocumentationPolicy.ExclusionReason.ARCHIVE_FILE),
```

Verification:

- The parameterized policy test fails for all four additions before the archive policy edit.

#### Code Edit 1.5

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryTest.java`
- Lines: before 199
- Action: add

Proposed:

```java
        Arguments.of("archives/package.ear.txt", null),
        Arguments.of("archives/package.tar.gz.txt", null),
        Arguments.of("archives/package.tar.gzip", null),
        Arguments.of("archives/native.narrow", null),
```

Verification:

- The same policy test proves suffix text and neighboring extensions remain owned.

#### Code Edit 1.6

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryProcessTest.java`
- Lines: 20-21
- Action: replace

Current:

```java
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
```

Proposed:

```java
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
```

Verification:

- The new deterministic cleanup test compiles with its cross-thread failure capture.

#### Code Edit 1.7

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryProcessTest.java`
- Lines: after 136
- Action: add

Proposed:

```java
  /**
   * Reports an unverified reader after cleanup interruption instead of returning early.
   *
   * @throws InterruptedException when deterministic test coordination is interrupted
   */
  @Test
  void cleanupInterruptionStillVerifiesReaderTermination() throws InterruptedException {
    var input = new InterruptIgnoringInputStream();
    var process = TestProcess.running(input);
    var observedFailure = new AtomicReference<IOException>();
    var interruptRestored = new AtomicBoolean();
    var worker = Thread.ofVirtual().start(() -> {
      try {
        RepositoryDiscovery.discover(
            repository, ignored -> process, Duration.ofNanos(1), Duration.ofMillis(50));
      } catch (IOException failure) {
        observedFailure.set(failure);
      } finally {
        interruptRestored.set(Thread.currentThread().isInterrupted());
      }
    });

    assertTrue(input.awaitClosed(TEST_TIMEOUT));
    worker.interrupt();
    assertTrue(input.awaitReaderInterruption(TEST_TIMEOUT));
    assertTrue(worker.join(TEST_TIMEOUT));

    var failure = assertInstanceOf(IOException.class, observedFailure.get());
    assertTrue(failure.getMessage().startsWith("Git file discovery timed out"));
    assertEquals(1, failure.getSuppressed().length);
    var cleanupFailure = assertInstanceOf(IOException.class, failure.getSuppressed()[0]);
    assertInstanceOf(InterruptedException.class, cleanupFailure.getCause());
    assertEquals(1, cleanupFailure.getSuppressed().length);
    assertTrue(cleanupFailure.getSuppressed()[0].getMessage()
        .contains("output reader did not terminate"));
    assertTrue(interruptRestored.get());

    input.releaseReader();
    assertTrue(input.awaitReaderStopped(TEST_TIMEOUT));
  }
```

Verification:

- RED against `e4784620`: the cleanup failure lacks the nested unverified-reader failure because interrupted `stopReader()` returns without its second bounded verification.

#### Code Edit 1.8

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/RepositoryDiscoveryProcessTest.java`
- Lines: before 150
- Action: add

Proposed:

```java
  /** Keeps a reader alive across closure and interruption until the test releases it. */
  private static final class InterruptIgnoringInputStream extends InputStream {
    /** Signals that lifecycle cleanup invoked stream closure. */
    private final CountDownLatch closed = new CountDownLatch(1);

    /** Signals that the output reader observed its cleanup interruption. */
    private final CountDownLatch readerInterrupted = new CountDownLatch(1);

    /** Releases the reader after cleanup has reported its bounded outcome. */
    private final CountDownLatch readerRelease = new CountDownLatch(1);

    /** Signals final output-reader termination so the test leaks no virtual thread. */
    private final CountDownLatch readerStopped = new CountDownLatch(1);

    /**
     * Waits for explicit release while recording and ignoring reader interruption.
     *
     * @return end-of-stream marker after release
     */
    @Override
    public int read() {
      try {
        while (true) {
          try {
            readerRelease.await();
            return -1;
          } catch (InterruptedException failure) {
            readerInterrupted.countDown();
          }
        }
      } finally {
        readerStopped.countDown();
      }
    }

    /** Records closure without releasing the deliberately stubborn reader. */
    @Override
    public void close() {
      closed.countDown();
    }

    /**
     * Waits for stream closure.
     *
     * @param timeout maximum coordination wait
     * @return whether closure occurred within the bound
     * @throws InterruptedException when test coordination is interrupted
     */
    boolean awaitClosed(Duration timeout) throws InterruptedException {
      return closed.await(timeout.toNanos(), TimeUnit.NANOSECONDS);
    }

    /**
     * Waits until the reader observes cleanup interruption.
     *
     * @param timeout maximum coordination wait
     * @return whether interruption occurred within the bound
     * @throws InterruptedException when test coordination is interrupted
     */
    boolean awaitReaderInterruption(Duration timeout) throws InterruptedException {
      return readerInterrupted.await(timeout.toNanos(), TimeUnit.NANOSECONDS);
    }

    /** Releases the deliberately stubborn reader after assertions capture cleanup outcome. */
    void releaseReader() {
      readerRelease.countDown();
    }

    /**
     * Waits for the released reader to terminate.
     *
     * @param timeout maximum coordination wait
     * @return whether the reader stopped within the bound
     * @throws InterruptedException when test coordination is interrupted
     */
    boolean awaitReaderStopped(Duration timeout) throws InterruptedException {
      return readerStopped.await(timeout.toNanos(), TimeUnit.NANOSECONDS);
    }
  }
```

Verification:

- The fixture coordinates solely through latches/deadlines and always releases the stubborn reader after assertions.

#### Code Edit 1.9

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationPolicy.java`
- Lines: 17-18
- Action: replace

Current:

```java
  /** Archive extensions whose contents are not owned source files at discovery time. */
  private static final Set<String> ARCHIVE_EXTENSIONS = Set.of(".jar", ".rar", ".war", ".zip");
```

Proposed:

```java
  /** Archive suffixes whose contents are not owned source files at discovery time. */
  private static final Set<String> ARCHIVE_SUFFIXES =
      Set.of(".ear", ".jar", ".nar", ".rar", ".tar.gz", ".war", ".zip");
```

Verification:

- The constant mirrors every package format in the repository `.gitignore`, including the compound suffix.

#### Code Edit 1.10

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationPolicy.java`
- Lines: 54-60
- Action: replace

Current:

```java
  /**
   * Classifies a path that is outside first-party documentation scope.
   *
   * @param path repository-relative path
   * @return named reason for an approved exclusion, or empty for first-party source
   */
  static Optional<ExclusionReason> exclusionReason(Path path) {
```

Proposed:

```java
  /**
   * Classifies a path that is outside first-party documentation scope.
   *
   * @param path repository-relative path
   * @return named reason for an approved exclusion, or empty for first-party source
   * @throws NullPointerException when the path is absent
   */
  static Optional<ExclusionReason> exclusionReason(Path path) {
```

Verification:

- Direct private Javadocs report no missing failure contract for the policy boundary.

#### Code Edit 1.11

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationPolicy.java`
- Lines: 82-84
- Action: replace

Current:

```java
    if (ARCHIVE_EXTENSIONS.contains(extension)) {
      return Optional.of(ExclusionReason.ARCHIVE_FILE);
    }
```

Proposed:

```java
    if (hasSuffix(normalized, ARCHIVE_SUFFIXES)) {
      return Optional.of(ExclusionReason.ARCHIVE_FILE);
    }
```

Verification:

- Named archive cases pass without altering binary or image classification.

#### Code Edit 1.12

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationPolicy.java`
- Lines: before 154
- Action: add

Proposed:

```java
  /**
   * Tests a case-insensitive filename against exact terminal suffixes.
   *
   * @param path normalized repository-relative path
   * @param suffixes lowercase terminal suffixes including their leading dots
   * @return whether the filename ends with one supplied suffix
   */
  private static boolean hasSuffix(Path path, Set<String> suffixes) {
    var name = path.getFileName().toString().toLowerCase(Locale.ROOT);
    return suffixes.stream().anyMatch(name::endsWith);
  }

```

Verification:

- `.tar.gz` and uppercase equivalents classify; `.tar.gz.txt`, `.tar.gzip`, and `.narrow` remain owned.

#### Code Edit 1.13

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/RepositoryDiscovery.java`
- Lines: 40-53
- Action: replace

Current:

```java
  /**
   * Discovers tracked and nonignored first-party files.
   *
   * <p>This method starts an external Git process and blocks for at most the Git timeout plus
   * bounded process and output-reader cleanup. If the caller is interrupted, cleanup runs first,
   * the interrupt flag is restored, and the checked failure retains the interruption cause.
   *
   * @param root Git worktree root
   * @return immutable files in stable path order
   * @throws IOException when Git cannot start, times out, produces unreadable output, exits
   *     nonzero, cannot be cleaned up, or discovery is interrupted
   */
  static List<RepositoryFile> discover(Path root) throws IOException {
    return discover(root, RepositoryDiscovery::startGit, GIT_TIMEOUT, CLEANUP_TIMEOUT);
  }
```

Proposed:

```java
  /**
   * Discovers tracked and nonignored first-party files.
   *
   * <p>This method starts an external Git process and blocks for at most the Git timeout plus
   * bounded process and output-reader cleanup. Cleanup verifies owned thread termination or reports
   * a checked failure. If the caller is interrupted, cleanup finishes first, the interrupt flag is
   * restored, and the checked failure retains the interruption cause.
   *
   * @param root Git worktree root
   * @return immutable files in stable path order
   * @throws NullPointerException when the root is absent
   * @throws IOException when Git cannot start, times out, produces unreadable output, exits
   *     nonzero, cannot be cleaned up, or discovery is interrupted
   */
  static List<RepositoryFile> discover(Path root) throws IOException {
    return discover(root, RepositoryDiscovery::startGit, GIT_TIMEOUT, CLEANUP_TIMEOUT);
  }
```

Verification:

- Direct private Javadocs exit clean and the null-root test passes.

#### Code Edit 1.14

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/RepositoryDiscovery.java`
- Lines: 357-378
- Action: replace

Current:

```java
    /**
     * Joins and verifies the output reader after its stream has been closed.
     *
     * @return cleanup failure, or {@code null} after verified reader termination
     */
    private IOException stopReader() {
      IOException failure = null;
      try {
        if (!join(outputReader, cleanupTimeout)) {
          outputReader.interrupt();
          if (!join(outputReader, cleanupTimeout)) {
            failure = new IOException(
                "Git output reader did not terminate within bounded cleanup");
          }
        }
      } catch (InterruptedException exception) {
        cleanupInterrupted = true;
        outputReader.interrupt();
        failure = new IOException("Interrupted while joining Git output reader", exception);
      }
      return failure;
    }
```

Proposed:

```java
    /**
     * Joins and verifies the output reader after its stream has been closed.
     *
     * <p>Interruptions are retained as cleanup failures while this method continues verification
     * within one monotonic deadline. The lifecycle owner restores the caller's interrupt flag only
     * after every owned resource has been handled.
     *
     * @return cleanup failure, or {@code null} after verified reader termination
     */
    private IOException stopReader() {
      long deadline = System.nanoTime() + cleanupTimeout.toNanos();
      IOException failure = null;
      while (outputReader.isAlive()) {
        long remainingNanos = deadline - System.nanoTime();
        if (remainingNanos <= 0) {
          outputReader.interrupt();
          return merge(failure,
              new IOException("Git output reader did not terminate within bounded cleanup"));
        }
        try {
          outputReader.join(Duration.ofNanos(remainingNanos));
        } catch (InterruptedException exception) {
          cleanupInterrupted = true;
          outputReader.interrupt();
          failure = merge(failure,
              new IOException("Interrupted while joining Git output reader", exception));
        }
      }
      return failure;
    }
```

Verification:

- The deterministic interruption test observes interruption as the cleanup primary failure and unverified termination as its suppressed failure, while the governing discovery timeout remains primary.
- Existing ordinary timeout, process interruption, large output, nonzero exit, start failure, output failure, and stubborn-process tests remain green.

## Code Changes

- `RepositoryDiscoveryTest.java`: add real-Git and policy cases for repository-native archives/near misses plus null-input contracts.
- `RepositoryDiscoveryProcessTest.java`: add one deterministic cleanup-interruption regression and its latch-controlled stream.
- `DocumentationPolicy.java`: add complete archive suffix matching and the null-input Javadoc contract.
- `RepositoryDiscovery.java`: continue bounded reader verification after interruption and correct the production boundary Javadocs.

## Files and Modules

Only `documentation-validator` changes. Expected tracked diff: four files, with no build configuration or runtime application changes.

## Unit Testing

RED command:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*RepositoryDiscoveryTest' --tests '*RepositoryDiscoveryProcessTest'
```

Expected RED: `.nar`, `.ear`, `.tar.gz`, and `.TAR.GZ` policy/real-Git assertions fail; the cleanup-interruption assertion lacks the nested unverified-reader failure.

GREEN commands:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*RepositoryDiscoveryTest' --tests '*RepositoryDiscoveryProcessTest'
.\gradlew.bat --no-daemon :documentation-validator:test
```

Require zero failures/errors; the Unix literal-backslash test may remain skipped on Windows.

## Local Testing

No application launch is required because runtime code is unchanged. Generate private-member Javadocs:

```powershell
$sourceFiles = Get-ChildItem -Recurse -Filter '*.java' 'documentation-validator\src\main\java'
& javadoc -private -quiet -d 'documentation-validator\build\reports\private-javadocs' $sourceFiles.FullName
```

Require exit 0 and no warnings. Then run the root build:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon build
```

## Validation

- Focused RED and identical-command GREEN are recorded.
- All validator tests pass with zero failures/errors.
- Direct `javadoc -private` exits 0 with no warnings.
- Root `build` passes with zero failures/errors.
- `git diff --check` passes.
- `git status --short` contains only the four planned files before commit and is clean afterward.
- Authoritative checkout status is read-only and unchanged during the task.
- Task review and final whole-phase review return no Critical/Important findings.

## Rollback or Recovery

Revert the single corrective commit in the isolated branch. Do not reset or clean either checkout. Preserve the worktree for investigation if any verification or review gate fails.

## Risks

- Compound suffix matching could hide near misses; exact terminal-suffix and real-Git tests prevent overmatching.
- Repeated cleanup interruption could exhaust the deadline; the loop records every interruption and reports unverified termination rather than claiming success.
- Nanosecond deadline arithmetic could be misunderstood; the task keeps one short positive duration and uses standard `System.nanoTime()` subtraction semantics.
- A stubborn test reader could leak; the fixture explicitly releases it and waits for its stopped latch after assertions.
- Upstream `main` has advanced; integration remains deferred until this branch is review-clean.

## Completion Criteria

- `.nar`, `.ear`, `.tar.gz`, and uppercase compound archives return `ARCHIVE_FILE`.
- Archive near misses remain discoverable.
- Interrupted reader cleanup either verifies termination or reports the missing verification within its deadline.
- Governing failure, interruption cause, cleanup suppression, and caller interrupt status are preserved.
- All affected Javadocs and tags are accurate and direct private Javadocs are warning-free.
- Focused/module/full verification and diff checks pass.
- One corrective commit is independently approved with no load-bearing residual findings.
