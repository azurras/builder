# Java Documentation Checker Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested, parse-only Java documentation checker that reports every undocumented source-declared type, constructor, method, and enum constant plus incomplete parameter, return, and throws tags without compiling application dependencies.

**Architecture:** Consume the corrected `RepositoryFile` discovery boundary, parse all discovered Java files in one Java 25 compiler task, traverse syntax trees with `TreePathScanner`, read structured Javadocs through `DocTrees`, and return validated, deterministically sorted violations. Keep the checker JDK-only and package-private so the later aggregate CLI can compose it without introducing a premature public API.

**Tech Stack:** Java 25 compiler/tree/documentation APIs, JUnit Jupiter, Gradle Kotlin DSL, no application parser dependency, no npm.

## Global Constraints

- Work only in `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729` on `codex/repository-documentation-coverage`.
- Preserve the dirty authoritative checkout at `A:\Projects\christopherbell.dev`; do not edit, clean, stage, reset, switch, commit, or run builds there.
- Do not rebase, merge, pull, push, open a pull request, wire Gradle `check`, wire CI, add non-Java scanners, update READMEs, or remediate application documentation in this phase.
- Use `A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage` as `GRADLE_USER_HOME`.
- Keep production dependencies JDK-only and do not call `JavacTask.analyze()` or `generate()`.
- Use the existing `RepositoryFile.absolutePath()` for input and `RepositoryFile.displayPath()` for diagnostics; do not rediscover Git state or rebuild paths from strings.
- Inspect source-declared named classes, interfaces, records, annotation types, enums, local types, constructors, compact constructors, methods at every visibility including tests/private/anonymous-class methods, annotation members, and enum constants. Skip only anonymous `ClassTree` documentation because the anonymous type has no declared name; still traverse and check its declared methods and nested named types.
- Do not report compiler-synthesized record constructors/accessors. Require `@param` tags for record components on the record declaration and for the synthesized component parameter list on an explicitly source-declared compact constructor.
- Require a nonblank descriptive body. A sole `{@inheritDoc}` is structurally accepted only on a method annotated `@Override`, and its local tag requirements are inherited; the later documentation-remediation review must prove that the inherited contract is complete and that no implementation-specific constraint or failure needs local text. A sole inherited-doc marker on a type, constructor, annotation member, enum constant, or method without `@Override` is a `JAVA_INHERIT_DOC` violation.
- Require exactly one documented tag for every formal parameter and type parameter, exactly one `@return` for non-`void` methods, no `@return` for constructors or `void` methods, and at least one matching `@throws`/`@exception` tag for every syntactically declared thrown type. Reject duplicate and unknown `@param` tags and blank required-tag descriptions. Additional nonblank throws tags may document undeclared runtime failures.
- Collect parse errors and documentation violations across all inputs. Return immutable output sorted by display path, line, rule identifier, and message.
- Every new Java type, record component, constructor, method, private method, field, enum constant, parameter, return value, and thrown failure in this validator phase must have accurate Javadocs.
- Apply test-driven development: add the fixture test first, run the focused command and retain expected RED evidence, then add the minimum production implementation and run the identical command GREEN.

---

## Document Status

complete

## Objective

Produce one independently reviewed Java-checker commit on top of `644763701d5438062ee93594ae9a5695b1659715` that exposes the campaign's current Java documentation gaps through stable structured violations while leaving application behavior and build lifecycle wiring unchanged.

## Goals

- Parse every discovered Java source through supported Java 25 compiler and documentation APIs without compiling application dependencies.
- Detect missing or structurally incomplete Javadocs for every source declaration required by the approved campaign.
- Return stable, validated, immutable, aggregate diagnostics that the later repository command can render and count.
- Prove repository-native declaration shapes and edge cases with test-first fixtures.

## Inputs

- Approved specification: `docs/specs/2026-07-29-christopherbell-dev-repository-wide-documentation-coverage.md`.
- Corrected discovery implementation at spoke commit `644763701d5438062ee93594ae9a5695b1659715`.
- Read-only inventory: 837 Java files; repository-native records/compact constructors, nested/package-private/sealed types, enums with fields/constructors, generic types/methods, checked throws, private/test methods, and anonymous test classes.
- JDK 25 probes confirming enum constants are enum-owned `VariableTree` nodes with `NewClassTree` initializers and compact constructors are source `MethodTree` nodes named `<init>` with component parameters.

## Branch

- Repository: `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729`.
- Branch: `codex/repository-documentation-coverage`.
- Phase base: `644763701d5438062ee93594ae9a5695b1659715`.

## Non-Goals

- No semantic natural-language quality scoring. The checker enforces structural completeness and nonblank descriptions; subsystem review remains responsible for factual and non-boilerplate quality.
- No inherited-member resolution, application classpath analysis, annotation processing, bytecode generation, or dependency compilation. This structural phase permits sole `{@inheritDoc}` only with source `@Override`; the later manual documentation review owns the specification's semantic completeness condition.
- No field Javadoc rule except enum constants and record-component tags owned by the record declaration.
- No package/module documentation rule in this phase because the refreshed repository contains no `package-info.java` or `module-info.java`; the later file-purpose scanner must classify any future introduction explicitly.
- No aggregate command, totals, exit code, Gradle task, CI change, private-Javadoc task, JavaScript/PowerShell/native scanner, README diagram rule, or application documentation remediation.

## Assumptions

- Java 25 is available because the repository build already requires it.
- Parse-only compiler diagnostics are limited to source syntax failures; unresolved application dependencies are not analyzed.
- An enum constant is a direct child `VariableTree` of an enum whose flags contain `PUBLIC`, `STATIC`, and `FINAL`, whose declared type text equals the enclosing enum simple name, and whose `NewClassTree` initializer identifier equals that same enum name. A negative fixture with an ordinary enum field initialized by `new Object()` must remain outside the rule.
- Direct non-static record-owned `VariableTree` members are record components; Java records cannot declare other instance fields.
- A declared throws tag matches either the exact syntactic type text or its terminal simple name so fully qualified documentation and source spellings interoperate without type resolution.

## Open Questions

None. The broad specification and user approvals fix the JDK syntax-tree architecture, complete tag policy, private/test scope, enum-constant rule, and continuous subagent-driven execution choice.

## Before-Edit Brief

- **Behavior:** Given discovered Java files, return every parser/documentation defect with stable rule, path, source line, and actionable message; valid fixture declarations return an empty immutable list.
- **Invariants:** Inputs are nonnull discovered `.java` files; violation rule/path/line/message are valid; all named source declarations and all source methods are checked exactly once; synthesized members and anonymous type identities never become findings; one malformed file cannot hide findings in other files.
- **Boundary/API:** Add package-private `DocumentationRule`, `DocumentationViolation`, and `JavaDocumentationChecker.check(List<RepositoryFile>)`; preserve the existing package-private discovery boundary and defer public/CLI exposure.
- **Effects and failures:** The checker reads files and opens a JDK file manager but performs no writes, class loading, annotation processing, dependency analysis, network access, or application compilation. Invalid API inputs fail fast; source syntax errors become violations; file I/O remains a contextual checked `IOException`.
- **Tests and evidence:** RED is the missing checker API/behavior in `JavaDocumentationCheckerTest`; GREEN covers clean and defective declaration matrices, tag validation, parse-error aggregation, line/path ordering, records, enum constant bodies, anonymous methods, and immutable results, followed by module tests, private Javadocs, root build, and diff review.

---

## Task Breakdown

### Task 1: Add the parse-only Java documentation checker

**Required skill:** Invoke `write-chris-street-style-code` in implementation mode and follow `superpowers:test-driven-development`.

**Before-Edit Brief:** Use the phase brief above verbatim. If implementation investigation disproves an AST assumption, stop before production edits and update the plan rather than adding source-text heuristics.

**Files:**

- Create: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationRule.java`
- Create: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationViolation.java`
- Create: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaDocumentationChecker.java`
- Create: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaDocumentationCheckerTest.java`

- [ ] **Step 1: Write the complete failing fixture suite**

#### Code Edit 1.1

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaDocumentationCheckerTest.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base 644763701d5438062ee93594ae9a5695b1659715.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

/** Proves Java documentation rules against source-only JDK parser fixtures. */
class JavaDocumentationCheckerTest {
  /** Complete declarations, tags, constant body, and inherited method contract. */
  private static final String COMPLETE_SOURCE = """
      package example;
      /**
       * Complete type.
       * @param <T> stored value type
       */
      class Complete<T> {
        /**
         * Creates a value.
         * @param value initial value
         */
        Complete(T value) {}
        /**
         * Copies a value.
         * @param value source value
         * @return copied value
         */
        private T copy(T value) { return value; }
        /** Exercises the fixture. */
        @org.junit.jupiter.api.Test void testMethod() {}
        /** Nested operation. */
        interface Nested { /** Runs the operation. */ void run(); }
        /** Marker metadata. */
        @interface Marker {
          /**
           * Returns its label.
           * @return label
           */
          String value();
        }
        /**
         * Pair value.
         * @param <U> value type
         * @param value stored value
         */
        record Pair<U>(U value) {
          /**
           * Creates a pair.
           * @param value stored value
           */
          Pair {}
        }
        /** Processing state. */
        enum State {
          /** Ready for work. */ READY,
          /** Actively working. */ ACTIVE {
            /**
             * Applies the state.
             * @return state code
             */
            int apply() { return 1; }
          };
          static final Object SUPPORT = new Object();
        }
        /**
         * Converts a value.
         * @param <U> result type
         * @param value input value
         * @return converted value
         * @throws java.io.IOException when conversion fails
         */
        <U> U convert(U value) throws java.io.IOException { return value; }
        /** Parent operation. */
        interface Parent { /** Performs inherited work. */ void inherited(); }
        /** Parent implementation. */
        class Child implements Parent {
          /** {@inheritDoc} */ @Override public void inherited() {}
        }
      }
      """;

  /** Missing named declarations and source methods at representative visibilities. */
  private static final String MISSING_DECLARATIONS_SOURCE = """
      package example;
      class Missing {
        Missing() {}
        private void privateMethod() {}
        @org.junit.jupiter.api.Test
        void testMethod() {}

        interface Nested {}
        enum State { READY }
        Runnable callback = new Runnable() {
          public void run() {}
        };
      }
      """;

  /** Malformed parameter, return, throws, constructor, and inherited-doc contracts. */
  private static final String MALFORMED_TAGS_SOURCE = """
      package example;
      /**
       * Tags.
       * @param T documented with the wrong parameter kind
       */
      class Tags<T> {
        /** Calculates.
         * @param <value> ordinary parameter documented as a type parameter
         * @param value
         * @param value duplicate
         * @param U type parameter documented as an ordinary parameter
         * @param extra unknown parameter
         * @return
         * @return duplicate
         * @throws IllegalStateException
         */
        <U> String calculate(String value)
            throws java.io.IOException, IllegalStateException { return value; }
        /**
         * Runs.
         * @return invalid return
         */
        void run() {}
        /**
         * Creates.
         * @return invalid return
         */
        Tags() {}
        /** Returns a value without its result contract. */
        String missingReturn() { return "value"; }
        /** */ void emptyDescription() {}
        /** {@inheritDoc} */ void inheritedWithoutOverride() {}
      }
      """;

  /** Record component and explicit compact-constructor tag gaps. */
  private static final String RECORD_SOURCE = """
      package example;
      /**
       * Record value.
       * @param count item count
       */
      record RecordCase(String name, int count) {
        /**
         * Creates a value.
         * @param name item name
         */
        RecordCase {}
      }
      """;

  /** Constant-specific and anonymous methods plus an ordinary enum field. */
  private static final String ANONYMOUS_SOURCE = """
      package example;
      /** Processing mode. */
      enum AnonymousCase {
        /** First mode. */ FIRST { int apply() { return 1; } };
        static final Object SUPPORT = new Object();
        /**
         * Creates a callback.
         * @return callback
         */
        Runnable callback() {
          return new Runnable() { public void run() {} };
        }
      }
      """;

  /** Temporary repository root that owns each source fixture. */
  @TempDir Path repository;

  /**
   * Accepts every repository-native declaration shape when its contract is complete.
   *
   * @throws IOException when fixture source cannot be written or read
   */
  @Test
  void acceptsCompleteDocumentationAcrossDeclarationShapes() throws IOException {
    var violations = JavaDocumentationChecker.check(List.of(source(
        "src/main/java/example/Complete.java",
        COMPLETE_SOURCE)));

    assertEquals(List.of(), violations);
  }

  /**
   * Reports named and callable declarations regardless of visibility or test annotations.
   *
   * @throws IOException when fixture source cannot be written or read
   */
  @Test
  void reportsEveryUndocumentedNamedDeclarationAndSourceMethod() throws IOException {
    var violations = JavaDocumentationChecker.check(List.of(source(
        "src/test/java/example/Missing.java",
        MISSING_DECLARATIONS_SOURCE)));

    assertEquals(List.of(
        "class Missing", "constructor Missing", "method privateMethod", "method testMethod",
        "interface Nested", "enum State", "enum constant READY", "method run"),
        messages(violations));
  }

  /**
   * Reports missing, duplicate, unknown, unexpected, and blank contract tags.
   *
   * @throws IOException when fixture source cannot be written or read
   */
  @Test
  void reportsIncompleteAndMalformedContractTags() throws IOException {
    var violations = JavaDocumentationChecker.check(List.of(source(
        "src/main/java/example/Tags.java",
        MALFORMED_TAGS_SOURCE)));

    assertTrue(messages(violations).containsAll(List.of(
        "missing @param <T>",
        "type parameter T documented as an ordinary parameter",
        "ordinary parameter value documented as a type parameter",
        "missing @param <U>",
        "type parameter U documented as an ordinary parameter",
        "duplicate @param value",
        "unknown @param extra",
        "blank @param value description",
        "duplicate @return",
        "blank @return description",
        "missing @return",
        "missing @throws IOException",
        "blank @throws IllegalStateException description",
        "unexpected @return on void method",
        "unexpected @return on constructor",
        "method emptyDescription has no descriptive body",
        "method inheritedWithoutOverride uses {@inheritDoc} without @Override")));
  }

  /**
   * Requires record-component tags without inventing synthesized accessor findings.
   *
   * @throws IOException when fixture source cannot be written or read
   */
  @Test
  void checksRecordComponentsAndExplicitCompactConstructorOnly() throws IOException {
    var violations = JavaDocumentationChecker.check(List.of(source(
        "src/main/java/example/RecordCase.java",
        RECORD_SOURCE)));

    assertEquals(List.of("missing @param name", "missing @param count"), messages(violations));
  }

  /**
   * Checks a constant-specific method while ignoring only the anonymous type identity.
   *
   * @throws IOException when fixture source cannot be written or read
   */
  @Test
  void checksEnumConstantAndAnonymousClassMethodsWithoutAnonymousTypeFinding() throws IOException {
    var violations = JavaDocumentationChecker.check(List.of(source(
        "src/main/java/example/AnonymousCase.java",
        ANONYMOUS_SOURCE)));

    assertEquals(List.of("method apply", "method run"), messages(violations));
  }

  /**
   * Aggregates parser and declaration findings in deterministic path and line order.
   *
   * @throws IOException when fixture source cannot be written or read
   */
  @Test
  void aggregatesParserErrorsWithStableUnicodePathsAndLines() throws IOException {
    var violations = JavaDocumentationChecker.check(List.of(
        source("src/\u2003 Broken.java", "package example;\nclass Broken {\n"),
        source("src/A.java", "package example;\nclass A {}\n")));

    assertEquals(List.of("src/A.java", "src/\u2003 Broken.java"),
        violations.stream().map(v -> v.file().displayPath()).distinct().toList());
    assertTrue(violations.stream().anyMatch(v -> v.rule() == DocumentationRule.JAVA_PARSE_ERROR));
    assertTrue(violations.stream().allMatch(v -> v.line() >= 1));
    assertEquals(2, violations.stream()
        .filter(v -> v.file().displayPath().equals("src/A.java"))
        .findFirst().orElseThrow().line());
  }

  /**
   * Rejects invalid API inputs and exposes immutable results.
   *
   * @throws IOException when fixture source cannot be written or read
   */
  @Test
  void rejectsInvalidInputsAndReturnsImmutableResults() throws IOException {
    assertThrows(NullPointerException.class, () -> JavaDocumentationChecker.check(null));
    assertThrows(NullPointerException.class,
        () -> JavaDocumentationChecker.check(java.util.Arrays.asList((RepositoryFile) null)));
    assertThrows(IllegalArgumentException.class,
        () -> JavaDocumentationChecker.check(List.of(source("src/not-java.txt", "text"))));
    var violations = JavaDocumentationChecker.check(List.of(source(
        "src/Undocumented.java", "class Undocumented {}")));
    assertThrows(UnsupportedOperationException.class,
        () -> violations.add(violations.getFirst()));
  }

  /** Rejects incomplete violation values at their construction boundary. */
  @Test
  void rejectsInvalidViolationState() {
    var file = new RepositoryFile(repository, Path.of("src/A.java"));
    assertThrows(NullPointerException.class,
        () -> new DocumentationViolation(null, file, 1, "message"));
    assertThrows(NullPointerException.class,
        () -> new DocumentationViolation(DocumentationRule.JAVA_PARSE_ERROR, null, 1, "message"));
    assertThrows(IllegalArgumentException.class,
        () -> new DocumentationViolation(DocumentationRule.JAVA_PARSE_ERROR, file, 0, "message"));
    assertThrows(IllegalArgumentException.class,
        () -> new DocumentationViolation(DocumentationRule.JAVA_PARSE_ERROR, file, 1, " "));
  }

  /**
   * Writes one UTF-8 source fixture below the temporary repository.
   *
   * @param path repository-relative source path
   * @param contents complete Java source
   * @return discovered source identity
   * @throws IOException when the fixture cannot be written
   */
  private RepositoryFile source(String path, String contents) throws IOException {
    var relativePath = Path.of(path);
    var absolutePath = repository.resolve(relativePath);
    Files.createDirectories(absolutePath.getParent());
    Files.writeString(absolutePath, contents, StandardCharsets.UTF_8);
    return new RepositoryFile(repository, relativePath);
  }

  /**
   * Extracts actionable messages in checker order.
   *
   * @param violations checker findings
   * @return immutable ordered messages
   */
  private static List<String> messages(List<DocumentationViolation> violations) {
    return violations.stream().map(DocumentationViolation::message).toList();
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaDocumentationCheckerTest'
```

Expected RED: test compilation fails because `JavaDocumentationChecker`, `DocumentationRule`, and `DocumentationViolation` do not exist. Preserve the output in the task report before production edits.

- [ ] **Step 2: Add validated rule and violation domain types**

#### Code Edit 1.2

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationRule.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base 644763701d5438062ee93594ae9a5695b1659715.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

/** Identifies one stable Java documentation policy category. */
enum DocumentationRule {
  /** Java source could not be parsed completely. */
  JAVA_PARSE_ERROR,

  /** A required source declaration has no associated Javadoc. */
  JAVA_MISSING_JAVADOC,

  /** A Javadoc exists but has no locally descriptive body. */
  JAVA_EMPTY_DESCRIPTION,

  /** An inherited-doc marker is attached to a declaration that cannot inherit a contract. */
  JAVA_INHERIT_DOC,

  /** A formal, type, or record-component parameter tag is incomplete or malformed. */
  JAVA_PARAM_TAG,

  /** A return tag is missing, duplicated, malformed, or inapplicable. */
  JAVA_RETURN_TAG,

  /** A declared thrown type lacks a complete matching failure contract. */
  JAVA_THROWS_TAG
}
```

Verification:

- The enum compiles as the only source of stable Java rule identifiers and every constant has semantic documentation.

#### Code Edit 1.3

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationViolation.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base 644763701d5438062ee93594ae9a5695b1659715.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.Objects;

/**
 * Identifies one actionable source documentation defect.
 *
 * @param rule stable policy category
 * @param file discovered repository file that owns the defect
 * @param line one-based source line
 * @param message nonblank corrective guidance
 */
record DocumentationViolation(
    DocumentationRule rule, RepositoryFile file, long line, String message) {
  /**
   * Rejects incomplete diagnostics before aggregation.
   *
   * @param rule stable policy category
   * @param file discovered repository file that owns the defect
   * @param line one-based source line
   * @param message nonblank corrective guidance
   * @throws NullPointerException when the rule, file, or message is absent
   * @throws IllegalArgumentException when the line is not positive or the message is blank
   */
  DocumentationViolation {
    Objects.requireNonNull(rule);
    Objects.requireNonNull(file);
    Objects.requireNonNull(message);
    if (line < 1) {
      throw new IllegalArgumentException("Documentation violation line must be positive");
    }
    if (message.isBlank()) {
      throw new IllegalArgumentException("Documentation violation message must not be blank");
    }
  }
}
```

Verification: rerun the focused test; RED advances to the absent checker boundary rather than fixture setup failure.

- [ ] **Step 3: Implement parse-only aggregation and declaration traversal**

#### Code Edit 1.4

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaDocumentationChecker.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base 644763701d5438062ee93594ae9a5695b1659715.
```

Proposed:

Create one stateless package-private final class with a private documented constructor and this boundary:

```java
  /**
   * Checks every supplied Java source in one parse-only compiler task.
   *
   * @param files discovered Java files
   * @return immutable violations in stable path, line, rule, and message order
   * @throws NullPointerException when the list or one element is absent
   * @throws IllegalArgumentException when an input is not a Java source
   * @throws IOException when a source file or compiler file manager cannot be read or closed
   * @throws IllegalStateException when the running JDK has no system Java compiler
   */
  static List<DocumentationViolation> check(List<RepositoryFile> files) throws IOException
```

Implementation requirements:

1. Copy and validate the input once. Reject filenames whose lowercase terminal extension is not `.java`; do not silently filter a caller mistake.
2. Return `List.of()` for an empty list.
3. Obtain `ToolProvider.getSystemJavaCompiler()` and fail with `IllegalStateException("Java documentation checking requires a full JDK")` when absent.
4. Create a `DiagnosticCollector<JavaFileObject>` and `StandardJavaFileManager` in try-with-resources. Convert the normalized absolute input paths with `getJavaFileObjectsFromPaths` and invoke `compiler.getTask(null, fileManager, diagnostics, List.of("-proc:none"), null, units)`.
5. Cast to `JavacTask`, call only `parse()`, then create `DocTrees` and source positions. Build an absolute normalized `Path -> RepositoryFile` map before parsing; never derive a display path from a diagnostic string.
6. Convert every `Diagnostic.Kind.ERROR` to `JAVA_PARSE_ERROR`, using its normalized source URI mapping, positive diagnostic line or line 1 fallback, and a single-line locale-root message. If a compiler-level diagnostic has no source, attach it deterministically to the first sorted input file; continue processing other compilation units.
7. Scan each parsed compilation unit with a private documented `DeclarationScanner extends TreePathScanner<Void, Void>` that owns its `CompilationUnitTree`, `RepositoryFile`, `DocTrees`, `SourcePositions`, and mutable violation sink.
8. Override `visitClass`, `visitMethod`, and `visitVariable`. Require docs for every nonempty `ClassTree.getSimpleName()`. Skip the anonymous class's type finding only, then call `super` so its methods and nested named types remain checked. Require docs for every source `MethodTree`, rendering `<init>` as `constructor <enclosing simple name>`. Treat a variable as an enum constant only when its direct parent is an enum, its flags contain `PUBLIC`, `STATIC`, and `FINAL`, its declared type text equals the enclosing enum simple name, and its `NewClassTree` initializer identifier equals that enum name; render `enum constant NAME`. The `SUPPORT = new Object()` fixture must produce no finding.
9. A missing comment emits `JAVA_MISSING_JAVADOC` at the declaration start line. A present comment whose full body has no content after rendering and trimming all nodes emits `JAVA_EMPTY_DESCRIPTION`; inline code/link/value nodes count as content. Detect a body consisting only of `InheritDocTree`: accept it only for a `MethodTree` whose modifiers include an annotation named exactly `Override` or `java.lang.Override`, skip local tag requirements for that inherited contract, and otherwise emit `JAVA_INHERIT_DOC`. Continue independent tag checks on every other present comment.
10. For type declarations, expected ordinary parameters are direct non-static `VariableTree` members of a record; expected type parameters come from `ClassTree.getTypeParameters()`. For methods, expected ordinary and type parameters and declared throws come from `MethodTree`; require return only when `getReturnType()` is nonnull and not primitive `void`.
11. Read `ParamTree`, `ReturnTree`, and `ThrowsTree` from `DocCommentTree.getBlockTags()`. Require exact parameter-name sets, report one defect per missing/unknown/duplicate tag, and require every required tag description to contain non-whitespace content. Permit extra nonblank throws tags for runtime failures. Match declared throws by exact tree text or terminal simple name; accept both `@throws` and `@exception` because both surface as `ThrowsTree`.
12. Use source positions and the compilation unit line map, falling back to line 1 only when the compiler returns `Diagnostic.NOPOS`. Never use a regex to locate declarations or comments.
13. Return `violations.stream().sorted(comparing display path, then line, then `rule().name()`, then message).toList()`.

The class may use small private records for expected tags or scan context only when they enforce the stated invariant. Every field, nested type, enum constant, constructor, and method must be documented. Do not add interfaces, dependency injection, application classpath settings, or source-text fallback parsing.

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaDocumentationCheckerTest'
```

Expected GREEN: all checker fixtures pass with zero failures/errors and no compiler diagnostics printed to standard output/error.

- [ ] **Step 4: Run phase verification and commit**

Run:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test
$sourceFiles = Get-ChildItem -Recurse -Filter '*.java' 'documentation-validator\src\main\java'
& javadoc -private -quiet -d 'documentation-validator\build\reports\private-javadocs-java-checker' $sourceFiles.FullName
.\gradlew.bat --no-daemon build
git diff --check
git status --short
```

Require all validator tests and the root build to pass with zero failures/errors; allow only established platform skips. Require private Javadocs exit 0 with no warnings, `git diff --check` exit 0, and only the four planned files in the diff. Inspect the complete diff against the Jane Street review rubric and verify the authoritative checkout status hash is unchanged across the task. Commit with:

```powershell
git add -- documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationRule.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/DocumentationViolation.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaDocumentationChecker.java documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaDocumentationCheckerTest.java
git commit -m "Add Java documentation checker"
```

## Code Changes

- Add stable validated Java documentation rule/violation domain values.
- Add one parse-only, aggregate, deterministic JDK syntax-tree checker behind the discovery boundary.
- Add fixture coverage for complete and incomplete declarations, private/test/anonymous methods, nested/sealed-compatible type shapes, records/compact constructors, enum constants and constant bodies, annotation members, generics, tags, parse errors, Unicode paths, line numbers, invalid inputs, and immutable output.

## Files and Modules

Only `documentation-validator` changes. Expected tracked diff: four new Java files. Existing discovery, Gradle, application, workflow, README, configuration, and CI files remain unchanged.

## Unit Testing

RED and GREEN use the identical focused command:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaDocumentationCheckerTest'
```

Then run the complete validator suite:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test
```

## Local Testing

No application launch is required because runtime code and Gradle lifecycle wiring are unchanged. Generate private-member Javadocs and run the root build as specified in Step 4.

## Validation

- Focused test compilation fails first for the absent checker types, then passes after production implementation.
- Complete fixture returns no violations; each defective declaration/tag family returns stable path/line/rule/message output.
- Parse errors aggregate without hiding other files.
- Anonymous type identities and synthesized record members are not reported; source-declared anonymous methods and compact constructors are checked.
- Results are immutable and deterministically sorted.
- Validator module tests, direct private Javadocs, root build, and `git diff --check` pass.
- Task-scoped spec/quality review and final phase review report no Critical/Important findings.
- Authoritative checkout is read-only and unchanged.

## Execution Evidence

- Implementation commits: `459ed2612aaffbe92078e54062a1a854fc64462e` (checker foundation), `ce47fba455987bcced491d51ba7ff23f24cacad5` (blank throws-tag validation and exact identities), and `d4a77e2e2a58906b968f61972ea964cdc10a8833` (same-name parameter namespaces, inapplicable return tags, and diagnostic ownership).
- Initial RED: focused test compilation exited 1 with 20 expected missing-symbol errors before any production checker existed.
- Task-review RED: the exact mixed-diagnostic assertion failed because the unmatched blank runtime `@throws` finding was absent.
- Final-review RED: the legal same-name type/value parameter fixture and inapplicable type/enum-constant return fixture failed; the diagnostic-ownership seam did not yet exist.
- Controller-owned final verification on `d4a77e2e2a58906b968f61972ea964cdc10a8833`: 72 validator tests, 0 failures, 0 errors, 1 established Windows skip; 1,566 total Java tests, 0 failures, 0 errors, 4 skips.
- Direct private-member Javadocs exited 0 with no warnings; root `build` exited 0; `git diff --check` exited 0; the isolated worktree was clean.
- Authoritative checkout status hash remained `C706E834EA40C9F523941C350570B68C5663FA4F3200528FA54D870A816E0CEB` before and after the phase.
- Task fix-round re-review returned `ALL_FINDINGS_ADDRESSED`; final whole-phase fix-wave re-review returned `ALL_FINDINGS_ADDRESSED` with no new Critical or Important breakage.

## Rollback or Recovery

Revert the single Java-checker commit in the isolated branch. Do not reset or clean either checkout. Preserve the SDD workspace and report files for diagnosis if a validation or review gate fails.

## Risks

- **Compiler AST drift:** tests pin Java 25 shapes for enum constants, compact constructors, record components, and anonymous bodies.
- **Inherited-doc completeness is semantic:** the checker accepts a sole marker only on source `@Override`; the later documentation-remediation review must prove the inherited contract is complete and add local constraints/failures where required by the approved specification.
- **False record findings:** scan parse trees only and never analyze, preventing generated accessors/canonical constructors from entering the tree.
- **Exception name ambiguity:** exact/suffix matching is deliberately syntactic; fixtures cover qualified/simple forms and semantic documentation remains review-owned.
- **No semantic prose scoring:** nonblank structural enforcement is explicit and final human subsystem review rejects restatements or inaccurate comments.
- **Large repository input:** parse all files in one compiler task to amortize setup while returning only immutable diagnostics; no analyze/generate phase is permitted.

## Completion Criteria

- Every required Java declaration shape is recognized without regex parsing or dependency compilation.
- Every enum constant and every source method at any visibility, including private/test/anonymous-class methods, is covered.
- Record component and compact-constructor contracts are enforced without synthesized-member false positives.
- Missing/empty Javadocs and malformed/missing parameter, return, and throws contracts aggregate with stable rule/path/line/messages.
- Parse failures fail closed as violations; invalid API inputs fail fast with typed exceptions.
- Focused/module/full verification and private Javadocs pass.
- One cohesive commit is independently approved with no load-bearing residual findings.
