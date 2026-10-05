# JavaScript Lexical Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. Each task must also invoke `write-chris-street-style-code` and `superpowers:test-driven-development` before editing production or test code.

**Goal:** Add a pure, JDK-only JavaScript tokenizer that safely separates code from comments, strings, regular-expression bodies, and template raw text and returns an immutable success-or-first-error result for the later documentation recognizer.

**Architecture:** Introduce a small package-private lexical domain model followed by one stateless state-machine lexer. The lexer emits exact-position semantic tokens, retains JSDoc as a distinct token, skips inert text, distinguishes regex from division using explicit expression-start context, owns nested template-interpolation braces, and fails closed at the first unsafe lexical position. It performs no file discovery, declaration recognition, or documentation-policy validation.

**Tech Stack:** Java 25, Java standard library, JUnit Jupiter, Gradle Kotlin DSL; no Node subprocess, npm package, third-party parser, source execution, or declaration-matching regular expression.

## Document Status

complete

## Objective

Implement Phase A of the approved JavaScript documentation scanner design in the existing isolated campaign worktree. The result must be a deterministic lexical boundary that Phase B can consume without re-reading JavaScript source or guessing through malformed syntax.

## Goals

- Represent token kinds, tokens, lexical errors, and success/failure results as validated immutable values.
- Tokenize repository-native ECMAScript module syntax without executing or importing it.
- Retain JSDoc tokens and exact-position ordinary-comment attachment barriers while making ordinary-comment contents, quoted-string content, regex bodies, and template raw text invisible to later declaration recognition.
- Preserve exact token spelling, one-based line and column, and zero-based start/exclusive-end UTF-16 offsets.
- Distinguish regex literals from division and division assignment using explicit lexical context.
- Support nested template literals and `${...}` interpolation without losing the brace owner.
- Return exactly one error anchored to the malformed unit's opening boundary, or to the first malformed internal character when more precise; a failed result never exposes an EOF token or any token owned by that incomplete unit.
- Prove behavior with isolated domain tests, lexical fixtures, repository-derived snippets, full validator tests, private Javadocs, and the root build.

## Inputs

- Approved design: `docs/specs/2026-07-29-javascript-documentation-scanner-design.md` in Builder.
- Campaign specification: `docs/specs/2026-07-29-christopherbell-dev-repository-wide-documentation-coverage.md` in Builder.
- Completed Java-checker phase base: spoke commit `d4a77e2e2a58906b968f61972ea964cdc10a8833`.
- The repository contains 96 first-party `.js` files, uses ESM plus the Node built-in test runner, and has no npm dependency workflow.
- Repository-derived lexical hazards include regex character classes, URLs/comment markers inside strings, multiline templates, nested interpolation, optional chaining, default/destructured parameters, and anonymous callbacks.
- The authoritative checkout status hash at the phase boundary is `C706E834EA40C9F523941C350570B68C5663FA4F3200528FA54D870A816E0CEB`.

## Branch

- Repository: `azurras/christopherbell.dev`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729`.
- Existing branch: `codex/repository-documentation-coverage`.
- Phase base: `d4a77e2e2a58906b968f61972ea964cdc10a8833`.
- Upstream integration target, deferred until the entire campaign is complete: refreshed `origin/main`.

## Global Constraints

- Work only in the isolated worktree. Do not edit, clean, stage, reset, switch, build, or otherwise mutate `A:\Projects\christopherbell.dev`.
- Recompute the authoritative checkout status hash before Task 1 and after final verification; require it to remain unchanged.
- Set `GRADLE_USER_HOME=A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage` for every Gradle command.
- Do not rebase, merge, pull, push, open a pull request, wire Gradle `check`, wire CI, remediate JavaScript documentation, update READMEs, or add the Phase B recognizer in this phase.
- Production code must use only the Java standard library. Do not invoke Node, a browser, application JavaScript, a parser dependency, or a JavaScript engine.
- Do not use regular expressions to identify declarations. The lexer may recognize regex-literal syntax only through character-by-character state transitions.
- Every new Java type, record component, constructor, method, private helper, field, enum constant, parameter, return value, and documented failure must have accurate Javadocs.
- Preserve UTF-16 Java `String` offsets exactly: `startOffset` is inclusive, `endOffset` is exclusive, and line/column are one-based. Treat `\r\n` as one line terminator while consuming two offsets; treat lone `\r`, `\n`, U+2028, and U+2029 as line terminators.
- Apply test-driven development separately for each task: add the named test first, run the exact focused command and record expected RED evidence, add the minimum production implementation, then rerun the identical command to GREEN.
- Each task receives independent spec-compliance and code-quality review. Final phase review must find no Critical or Important issue before the phase is accepted.

## Non-Goals

- No structural recognition of functions, arrows, classes, methods, object callables, parameters, returns, or throws.
- No module-purpose or declaration JSDoc enforcement and no JSDoc tag parsing.
- No repository discovery, UTF-8 file I/O, `DocumentationViolation` conversion, aggregation, command-line entry point, reporting, Gradle lifecycle wiring, or CI workflow changes.
- No complete ECMAScript parser, automatic semicolon insertion analysis, scope resolution, identifier binding, or semantic evaluation.
- No TypeScript, JSX, CommonJS, `.mjs`, `.cjs`, import-attribute semantics, or browser runtime support.
- No recovery after malformed lexical input; one deterministic failure is the entire result.

## Assumptions

- Java 25 sealed interfaces, records, switch expressions, `List.copyOf`, and Unicode identifier helpers are available.
- The Phase B recognizer needs semantic code tokens, template boundaries, and ordinary-comment attachment barriers, but not string contents, regex bodies, ordinary-comment semantics, or template raw chunks as code tokens.
- Exact source spelling is useful for identifiers, keywords, numbers, strings, regex literals, punctuators, JSDoc, ordinary-comment barriers, and template boundary tokens; raw template text can be skipped because interpolation boundaries and contained code remain explicit.
- The repository-native syntax and the deliberately forward-compatible private/accessor/generator punctuation can be represented by the token kinds and punctuator set below.
- Lexical uncertainty is safer as an explicit failure than as a partial successful stream.

## Open Questions

None. The user selected and approved the Java-standard-library tokenizer architecture. The recognizer and policy layer are intentionally deferred to a separate reviewed plan.

## Task Breakdown

### Task 1 - Add immutable lexical domain values

Sequence / dependencies:

- Runs first against spoke commit `d4a77e2e2a58906b968f61972ea964cdc10a8833`.
- Creates the only value contracts Task 2 may consume; Task 2 must not weaken or duplicate their validation.
- Commit independently as `Add JavaScript lexical domain types` after focused tests and task review pass.

Expected files or modules:

- `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptTokenKind.java`
- `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptToken.java`
- `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexError.java`
- `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexResult.java`
- `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexicalDomainTest.java`

Implementation notes:

- Required skill: `write-chris-street-style-code` before any code edits. Invoke it and `superpowers:test-driven-development` before creating the test or production files.
- Before-Edit Brief:
  - Behavior: callers can construct only internally consistent tokens, errors, successes, and failures; all exposed token lists are immutable and source ordered.
  - Invariants: token offsets never go backward; EOF is empty and zero-width; non-EOF tokens are nonempty; successful results contain exactly one terminal EOF; failed results contain no EOF and only tokens ending at or before the error offset.
  - Boundary/API: all types remain package-private in `dev.christopherbell.tools.documentation`; Task 2 consumes them directly and no application module depends on them.
  - Effects and failures: constructors have no I/O and reject absent or contradictory state with `NullPointerException` or `IllegalArgumentException`; result construction makes success/failure ambiguity unrepresentable.
  - Tests and evidence: first compile `JavaScriptLexicalDomainTest` before production types exist and record missing-symbol RED; then prove every constructor invariant, result invariant, token ordering rule, and list immutability with the same command.
- Use descriptive exception messages so failed fixtures explain the violated invariant.
- Validate source ordering by nondecreasing `startOffset`, require each token `endOffset <= next.startOffset`, and reject any token that extends beyond a failure's `error.offset()`.
- Do not add a generic diagnostic interface, mutable builder, inheritance hierarchy, or convenience state that Task 2 does not require.

#### Code Edit 1.1

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexicalDomainTest.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base d4a77e2e2a58906b968f61972ea964cdc10a8833.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

/** Verifies that JavaScript lexical values cannot represent contradictory state. */
class JavaScriptLexicalDomainTest {
  /** Accepts a normal token and preserves its complete source identity. */
  @Test
  void acceptsValidToken() {
    var token = new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "value", 2, 3, 4, 9);

    assertEquals(JavaScriptTokenKind.IDENTIFIER, token.kind());
    assertEquals("value", token.text());
    assertEquals(2, token.line());
    assertEquals(3, token.column());
    assertEquals(4, token.startOffset());
    assertEquals(9, token.endOffset());
  }

  /** Rejects absent, blank, reversed, or positionally invalid token state. */
  @Test
  void rejectsInvalidTokenState() {
    assertThrows(NullPointerException.class,
        () -> new JavaScriptToken(null, "name", 1, 1, 0, 4));
    assertThrows(NullPointerException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, null, 1, 1, 0, 4));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "", 1, 1, 0, 0));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "name", 0, 1, 0, 4));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "name", 1, 0, 0, 4));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "name", 1, 1, -1, 4));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "name", 1, 1, 4, 3));
  }

  /** Allows only the empty zero-width EOF spelling. */
  @Test
  void enforcesEndOfFileTokenShape() {
    var eof = new JavaScriptToken(JavaScriptTokenKind.EOF, "", 1, 5, 4, 4);

    assertEquals(4, eof.endOffset());
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.EOF, "x", 1, 5, 4, 5));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptToken(JavaScriptTokenKind.EOF, "", 1, 5, 4, 5));
  }

  /** Rejects incomplete error state. */
  @Test
  void rejectsInvalidErrorState() {
    assertThrows(NullPointerException.class,
        () -> new JavaScriptLexError(1, 1, 0, null));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexError(0, 1, 0, "error"));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexError(1, 0, 0, "error"));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexError(1, 1, -1, "error"));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexError(1, 1, 0, " "));
  }

  /** Requires one terminal EOF in successful results and exposes an immutable list. */
  @Test
  void validatesSuccessfulResult() {
    var identifier = new JavaScriptToken(
        JavaScriptTokenKind.IDENTIFIER, "x", 1, 1, 0, 1);
    var eof = new JavaScriptToken(JavaScriptTokenKind.EOF, "", 1, 2, 1, 1);
    var mutable = new ArrayList<>(List.of(identifier, eof));
    var result = new JavaScriptLexResult.Success(mutable);
    mutable.clear();

    assertEquals(List.of(identifier, eof), result.tokens());
    assertThrows(UnsupportedOperationException.class, () -> result.tokens().add(eof));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexResult.Success(List.of()));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexResult.Success(List.of(identifier)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexResult.Success(List.of(eof, identifier, eof)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexResult.Success(List.of(
            new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "a", 1, 2, 1, 2),
            new JavaScriptToken(JavaScriptTokenKind.EOF, "", 1, 1, 0, 0))));
  }

  /** Forbids EOF and post-error tokens in failed results and exposes an immutable prefix. */
  @Test
  void validatesFailedResult() {
    var identifier = new JavaScriptToken(
        JavaScriptTokenKind.IDENTIFIER, "x", 1, 1, 0, 1);
    var error = new JavaScriptLexError(1, 2, 1, "unterminated string literal");
    var mutable = new ArrayList<>(List.of(identifier));
    var result = new JavaScriptLexResult.Failure(mutable, error);
    mutable.clear();

    assertEquals(List.of(identifier), result.tokens());
    assertEquals(error, result.error());
    assertThrows(UnsupportedOperationException.class, () -> result.tokens().add(identifier));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexResult.Failure(List.of(
            new JavaScriptToken(JavaScriptTokenKind.EOF, "", 1, 2, 1, 1)), error));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptLexResult.Failure(List.of(
            new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "later", 1, 3, 2, 7)), error));
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexicalDomainTest'
```

Expected RED: test compilation fails only because the four planned lexical domain types do not yet exist. Preserve the output in the task report before production edits.

#### Code Edit 1.2

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptTokenKind.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base d4a77e2e2a58906b968f61972ea964cdc10a8833.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

/** Identifies the lexical role of one emitted JavaScript token. */
enum JavaScriptTokenKind {
  /** A JavaScript identifier, including private names whose spelling begins with {@code #}. */
  IDENTIFIER,
  /** A reserved or contextual word recognized by the lexical policy. */
  KEYWORD,
  /** A complete numeric literal, including an optional BigInt suffix. */
  NUMBER,
  /** A complete single- or double-quoted string literal. */
  STRING,
  /** A complete regular-expression literal, including flags. */
  REGEX,
  /** An operator, delimiter, separator, or other punctuation token. */
  PUNCTUATOR,
  /** A complete documentation block whose source spelling begins with two asterisks. */
  JAVADOC,
  /** The opening backtick of a template literal. */
  TEMPLATE_START,
  /** The dollar-sign and opening-brace boundary of a template interpolation. */
  TEMPLATE_EXPRESSION_START,
  /** The interpolation-owning closing brace of a template interpolation. */
  TEMPLATE_EXPRESSION_END,
  /** The closing backtick of a template literal. */
  TEMPLATE_END,
  /** The zero-width terminal marker in a successful token stream. */
  EOF
}
```

Verification:

- The enum compiles package-private, and every constant has a distinct documented semantic role.

#### Code Edit 1.3

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptToken.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base d4a77e2e2a58906b968f61972ea964cdc10a8833.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.Objects;

/**
 * Preserves one semantic JavaScript token and its exact source position.
 *
 * @param kind lexical role
 * @param text exact source spelling, empty only for EOF
 * @param line one-based start line
 * @param column one-based start column
 * @param startOffset zero-based inclusive UTF-16 offset
 * @param endOffset zero-based exclusive UTF-16 offset
 */
record JavaScriptToken(
    JavaScriptTokenKind kind,
    String text,
    int line,
    int column,
    int startOffset,
    int endOffset) {
  /**
   * Rejects incomplete or contradictory token identity.
   *
   * @param kind lexical role
   * @param text exact source spelling, empty only for EOF
   * @param line one-based start line
   * @param column one-based start column
   * @param startOffset zero-based inclusive UTF-16 offset
   * @param endOffset zero-based exclusive UTF-16 offset
   * @throws NullPointerException when kind or text is absent
   * @throws IllegalArgumentException when a position or EOF/content invariant is invalid
   */
  JavaScriptToken {
    Objects.requireNonNull(kind);
    Objects.requireNonNull(text);
    if (line < 1 || column < 1 || startOffset < 0 || endOffset < startOffset) {
      throw new IllegalArgumentException("JavaScript token position is invalid");
    }
    if (kind == JavaScriptTokenKind.EOF) {
      if (!text.isEmpty() || startOffset != endOffset) {
        throw new IllegalArgumentException("EOF token must be empty and zero-width");
      }
    } else if (text.isEmpty() || startOffset == endOffset) {
      throw new IllegalArgumentException("Non-EOF token must have nonempty source text");
    }
  }
}
```

Verification:

- The focused domain test accepts one valid token and rejects every invalid shape without needing the lexer.

#### Code Edit 1.4

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexError.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base d4a77e2e2a58906b968f61972ea964cdc10a8833.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.Objects;

/**
 * Identifies the first JavaScript source position where lexical recovery is unsafe.
 *
 * @param line one-based source line
 * @param column one-based source column
 * @param offset zero-based UTF-16 source offset
 * @param message nonblank actionable explanation
 */
record JavaScriptLexError(int line, int column, int offset, String message) {
  /**
   * Rejects incomplete error identity.
   *
   * @param line one-based source line
   * @param column one-based source column
   * @param offset zero-based UTF-16 source offset
   * @param message nonblank actionable explanation
   * @throws NullPointerException when the message is absent
   * @throws IllegalArgumentException when the position is invalid or the message is blank
   */
  JavaScriptLexError {
    Objects.requireNonNull(message);
    if (line < 1 || column < 1 || offset < 0) {
      throw new IllegalArgumentException("JavaScript lexical error position is invalid");
    }
    if (message.isBlank()) {
      throw new IllegalArgumentException("JavaScript lexical error message must not be blank");
    }
  }
}
```

Verification:

- The focused domain test rejects null, blank, and nonpositive error identity.

#### Code Edit 1.5

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexResult.java`
- Lines: 1
- Action: add

Current:

```text
Absent at phase base d4a77e2e2a58906b968f61972ea964cdc10a8833.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Objects;

/** Represents either a complete JavaScript token stream or its first lexical failure. */
sealed interface JavaScriptLexResult
    permits JavaScriptLexResult.Success, JavaScriptLexResult.Failure {
  /**
   * Returns the immutable source-ordered tokens emitted by the lexer.
   *
   * @return complete successful stream or pre-error diagnostic prefix
   */
  List<JavaScriptToken> tokens();

  /**
   * Represents a complete stream ending in exactly one EOF token.
   *
   * @param tokens immutable source-ordered complete stream
   */
  record Success(List<JavaScriptToken> tokens) implements JavaScriptLexResult {
    /**
     * Copies and validates the complete stream.
     *
     * @param tokens source-ordered stream ending in EOF
     * @throws NullPointerException when the list or one token is absent
     * @throws IllegalArgumentException when ordering or EOF ownership is invalid
     */
    Success {
      tokens = List.copyOf(tokens);
      validateOrdering(tokens);
      if (tokens.isEmpty() || tokens.getLast().kind() != JavaScriptTokenKind.EOF) {
        throw new IllegalArgumentException("Successful token stream must end in EOF");
      }
      if (tokens.stream().limit(tokens.size() - 1L)
          .anyMatch(token -> token.kind() == JavaScriptTokenKind.EOF)) {
        throw new IllegalArgumentException("Successful token stream contains an early EOF");
      }
    }
  }

  /**
   * Represents an immutable token prefix and the first unsafe lexical position.
   *
   * @param tokens immutable source-ordered prefix without EOF
   * @param error first lexical failure
   */
  record Failure(List<JavaScriptToken> tokens, JavaScriptLexError error)
      implements JavaScriptLexResult {
    /**
     * Copies and validates the failed stream.
     *
     * @param tokens source-ordered prefix without EOF
     * @param error first lexical failure
     * @throws NullPointerException when the list, one token, or error is absent
     * @throws IllegalArgumentException when ordering, EOF ownership, or error position is invalid
     */
    Failure {
      tokens = List.copyOf(tokens);
      error = Objects.requireNonNull(error);
      validateOrdering(tokens);
      if (tokens.stream().anyMatch(token -> token.kind() == JavaScriptTokenKind.EOF)) {
        throw new IllegalArgumentException("Failed token stream must not contain EOF");
      }
      if (tokens.stream().anyMatch(token -> token.endOffset() > error.offset())) {
        throw new IllegalArgumentException("Failed token stream extends beyond its error");
      }
    }
  }

  /**
   * Validates that token extents are source ordered and nonoverlapping.
   *
   * @param tokens tokens to validate
   * @throws IllegalArgumentException when token extents overlap or move backward
   */
  private static void validateOrdering(List<JavaScriptToken> tokens) {
    for (var index = 1; index < tokens.size(); index++) {
      if (tokens.get(index - 1).endOffset() > tokens.get(index).startOffset()) {
        throw new IllegalArgumentException("JavaScript tokens must be source ordered");
      }
    }
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexicalDomainTest'
```

Expected GREEN: all lexical-domain fixtures pass with zero failures/errors. Run `git diff --check`, perform task review, and commit only the five Task 1 files.

### Task 2 - Add the pure JavaScript state-machine lexer

Sequence / dependencies:

- Runs only after Task 1 is committed and independently approved.
- Consumes the Task 1 contracts without changing their semantics unless a failing test proves an invariant defect and the task review explicitly approves the narrow correction.
- Commit independently as `Add JavaScript lexer foundation` after focused, module, private-Javadoc, root-build, and review gates pass.

Expected files or modules:

- `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexer.java`
- `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexerTest.java`

Implementation notes:

- Required skill: `write-chris-street-style-code` before any code edits. Invoke it and `superpowers:test-driven-development` before creating the test or production file.
- Before-Edit Brief:
  - Behavior: `lex(String)` returns a complete immutable token stream ending in EOF for valid source or one immutable failure at the first unsafe lexical position for invalid source.
  - Invariants: inert lexical regions never emit code-looking tokens; emitted extents never overlap; regex/division classification is deterministic; every `${` owns exactly one interpolation-end token; no failure contains EOF; the lexer has no I/O or mutable global state.
  - Boundary/API: one package-private final utility class exposes only `static JavaScriptLexResult lex(String source)`; all scanner policy and file ownership remain outside this phase.
  - Effects and failures: the method reads only the supplied `String`; null is rejected; malformed literals/comments/templates/numbers/escapes return typed failure rather than throwing or recovering; internal invariant defects may throw `IllegalStateException` and are test failures.
  - Tests and evidence: first add the complete fixture suite and record missing-symbol RED for `JavaScriptLexer`; then use the identical focused command to prove token identities, coordinates, lexical isolation, regex context, template ownership, first-error behavior, and real-source snippets.
- Implement a private per-call `Cursor` or equivalent mutable scanner object so the public lexical operation remains reentrant and stateless. Document every field and helper.
- Recognize identifier starts with `$`, `_`, and supported ECMAScript `ID_Start` code points, plus private-name `#` followed by a valid identifier start. Recognize parts with `$`, `_`, U+200C, U+200D, or supported `ID_Continue` code points. The JDK Unicode predicates may be used only after excluding Java identifier-ignorable controls/formats and JavaScript whitespace; U+FEFF must terminate an identifier as whitespace, while unsupported NUL/control input must reach the normal fail-closed unexpected-character path. Reject a backslash escape inside an identifier with `unsupported escaped identifier` at the backslash.
- Classify the fixed reserved/expression-leading word set in a private immutable `Set<String>`. Classify the exact `KEYWORDS` set in Code Edit 2.2, including literal words `true`, `false`, and `null`; other valid names are `IDENTIFIER`.
- Tokenize numeric literals without a regex: decimal integer/fraction/exponent, leading-dot decimals, `0x`, `0b`, `0o`, numeric separators between digits, and an optional BigInt `n` only on integer forms. Return a failure at the first malformed digit, separator, exponent, radix, or forbidden BigInt fraction/exponent.
- Tokenize the longest valid punctuator from an immutable longest-first list including current source and planned recognizer forms: `>>>=`, `===`, `!==`, `>>>`, `**=`, `&&=`, `||=`, `??=`, `=>`, `==`, `!=`, `<=`, `>=`, `++`, `--`, `&&`, `||`, `??`, `?.`, `**`, `<<`, `>>`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `|=`, `^=`, `...`, and all single-character JavaScript delimiters/operators used by owned source. Return `unexpected character` for a code character outside identifiers, numbers, quotes/templates, slash handling, or the punctuator set.
- Scan single/double strings through escapes and escaped line continuations. Reject unescaped line terminators and EOF before the closing quote. Validate `\xHH`, `\uHHHH`, and `\u{H...}` structure; allow standard single-character escapes and standalone `\0` only when no decimal digit follows; reject `\1` through `\9`, `\00`-style legacy octal escapes, non-octal decimal escapes such as `\08`, and truncated/malformed hexadecimal or Unicode escapes at the owning backslash.
- Detect `//`, `/*`, and `/**` before regex/division. Emit an exact-spelling `ORDINARY_COMMENT` attachment-barrier token for each complete line or ordinary block comment without changing significant-token expression context. Emit an exact-spelling `JAVADOC` token for every complete block beginning with `/**`, including an empty `/**/`; the later policy layer owns nonblank-content validation. Fail at the opening delimiter for an unterminated block or JSDoc.
- Determine whether `/` starts regex from the previous significant token plus a small delimiter/control context stack. Expression-start positions include beginning of input, a template-expression start boundary, opening `(` / `[` / `{`, comma, colon, semicolon, question mark, assignment/binary/unary operators, arrow, reserved expression-leading keywords `return`, `throw`, `case`, `delete`, `void`, `typeof`, `new`, `yield`, `await`, `else`, `do`, `in`, and `instanceof`, plus contextual `of` only after the current top-level `for` header proves the for-of operator role. Contextual IdentifierNames `async`, `from`, `get`, `set`, and ordinary identifier uses of `of` are value-ending. Value-ending positions also include identifier, number, string, regex, template end, `this`, `super`, `true`, `false`, `null`, closing `]`, postfix `++` / `--`, and a closing `)` known to close a value expression. Track `if`/`for`/`while`/`with`/`switch`/`catch` control parentheses so `/regex/` after their closing `)` is expression-start, while `call()/value/` remains division. Track a `for` header through initial, classic-after-semicolon, and for-of-RHS states so only the first proved operator-position `of` is expression-leading. A slash immediately after an ordinary `}` is lexically ambiguous without object-versus-block recognition; return `ambiguous slash after closing brace` at the slash instead of guessing. A slash after an unmatched `)` must use a distinct accurate ambiguity state and message. Owned syntax can be broadened only when Phase B supplies a proved brace context.
- Within regex, honor escapes and character classes; a line terminator or EOF before the closing slash is a failure at the opening slash. Consume flags using identifier-part rules and reject a backslash flag escape. Preserve the whole literal spelling as one `REGEX` token.
- Emit `TEMPLATE_START` for `` ` ``, skip raw template characters and valid escapes, emit `TEMPLATE_EXPRESSION_START` for `${`, tokenize interpolation code normally, emit `TEMPLATE_EXPRESSION_END` only when the interpolation-owned brace closes, and emit `TEMPLATE_END` for the matching backtick. Use explicit template/interpolation frames so nested object braces, blocks, templates, strings, comments, and regex literals cannot steal an owner. Each frame records the token-list size before its opening boundary. On an unterminated template or interpolation, truncate tokens back to that checkpoint before returning the failure, so no retained token extends past the opening-boundary error offset. Fail at the opening backtick for an unterminated template and at the owning `${` for an unterminated interpolation.
- Advance position in one private operation that handles CRLF, lone CR/LF, U+2028, U+2029, BMP code units, and supplementary code points consistently. Offsets remain UTF-16 indices; column advances once per Unicode code point.
- Always append an EOF token at the current line/column/source length on success. On failure, return the already emitted non-EOF prefix and no tokens from a partially consumed lexical unit.

#### Code Edit 2.1

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexerTest.java`
- Lines: 1
- Action: add

Current:

```text
Absent at Task 2 base after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

/** Exercises JavaScript lexical states without executing fixture source. */
class JavaScriptLexerTest {
  /** Emits a terminal zero-width EOF for empty source. */
  @Test
  void tokenizesEmptySource() {
    assertEquals(List.of(
        new JavaScriptToken(JavaScriptTokenKind.EOF, "", 1, 1, 0, 0)),
        success(""));
  }

  /** Emits exact semantic tokens and longest punctuation for normal module syntax. */
  @Test
  void tokenizesIdentifiersKeywordsNumbersAndPunctuation() {
    var source = "const $value = 0x2A + .5e+2; privateName ??= 1_000n; obj?.#field;";

    var tokens = success(source);

    assertEquals(List.of(
        "KEYWORD:const", "IDENTIFIER:$value", "PUNCTUATOR:=", "NUMBER:0x2A",
        "PUNCTUATOR:+", "NUMBER:.5e+2", "PUNCTUATOR:;",
        "IDENTIFIER:privateName", "PUNCTUATOR:??=", "NUMBER:1_000n",
        "PUNCTUATOR:;", "IDENTIFIER:obj", "PUNCTUATOR:?.",
        "IDENTIFIER:#field", "PUNCTUATOR:;", "EOF:"), identities(tokens));
  }

  /** Accepts the planned radix, separator, fraction, exponent, and BigInt forms. */
  @Test
  void tokenizesSupportedNumericForms() {
    var source = "0b1010 0o755 0xCA_FE 1_000 1.25 1e-3 12n";

    assertEquals(List.of(
        "NUMBER:0b1010", "NUMBER:0o755", "NUMBER:0xCA_FE", "NUMBER:1_000",
        "NUMBER:1.25", "NUMBER:1e-3", "NUMBER:12n", "EOF:"),
        identities(success(source)));
  }

  /** Classifies the complete planned word set and accepts Unicode/private identifiers. */
  @Test
  void tokenizesExactKeywordsAndUnicodeIdentifiers() {
    var keywords = List.of(
        "async", "await", "break", "case", "catch", "class", "const", "continue",
        "debugger", "default", "delete", "do", "else", "enum", "export", "extends",
        "false", "finally", "for", "from", "function", "get", "if", "implements",
        "import", "in", "instanceof", "interface", "let", "new", "null", "of",
        "package", "private", "protected", "public", "return", "set", "static",
        "super", "switch", "this", "throw", "true", "try", "typeof", "var", "void",
        "while", "with", "yield");
    var source = String.join(" ", keywords) + " café 变量 #私有";

    var tokens = success(source);

    assertEquals(keywords, tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.KEYWORD)
        .map(JavaScriptToken::text)
        .toList());
    assertEquals(List.of("café", "变量", "#私有"), tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.IDENTIFIER)
        .map(JavaScriptToken::text)
        .toList());
  }

  /**
   * Emits every planned punctuator with longest-match identity.
   *
   * @param source source chosen to place the punctuator in a valid lexical context
   * @param punctuator exact punctuator expected in the stream
   */
  @ParameterizedTest(name = "punctuator {1}")
  @MethodSource("punctuatorSources")
  void tokenizesEveryPlannedPunctuator(String source, String punctuator) {
    assertEquals(1, success(source).stream().filter(token ->
        token.kind() == JavaScriptTokenKind.PUNCTUATOR
            && token.text().equals(punctuator)).count());
  }

  /**
   * Supplies every planned punctuator in an unambiguous lexical context.
   *
   * @return source and expected punctuator fixtures
   */
  private static Stream<Arguments> punctuatorSources() {
    return Stream.of(
        Arguments.of("a >>>= b", ">>>="), Arguments.of("a === b", "==="),
        Arguments.of("a !== b", "!=="), Arguments.of("a >>> b", ">>>"),
        Arguments.of("a **= b", "**="), Arguments.of("a &&= b", "&&="),
        Arguments.of("a ||= b", "||="), Arguments.of("a ??= b", "??="),
        Arguments.of("a <<= b", "<<="), Arguments.of("a >>= b", ">>="),
        Arguments.of("(...a)", "..."), Arguments.of("a => b", "=>"),
        Arguments.of("a == b", "=="), Arguments.of("a != b", "!="),
        Arguments.of("a <= b", "<="), Arguments.of("a >= b", ">="),
        Arguments.of("a++", "++"), Arguments.of("a--", "--"),
        Arguments.of("a && b", "&&"), Arguments.of("a || b", "||"),
        Arguments.of("a ?? b", "??"), Arguments.of("a?.b", "?."),
        Arguments.of("a ** b", "**"), Arguments.of("a << b", "<<"),
        Arguments.of("a >> b", ">>"), Arguments.of("a += b", "+="),
        Arguments.of("a -= b", "-="), Arguments.of("a *= b", "*="),
        Arguments.of("a /= b", "/="), Arguments.of("a %= b", "%="),
        Arguments.of("a &= b", "&="), Arguments.of("a |= b", "|="),
        Arguments.of("a ^= b", "^="), Arguments.of("{", "{"),
        Arguments.of("}", "}"), Arguments.of("(", "("), Arguments.of(")", ")"),
        Arguments.of("[", "["), Arguments.of("]", "]"), Arguments.of(".", "."),
        Arguments.of(";", ";"), Arguments.of(",", ","), Arguments.of("<", "<"),
        Arguments.of(">", ">"), Arguments.of("+", "+"), Arguments.of("-", "-"),
        Arguments.of("*", "*"), Arguments.of("%", "%"), Arguments.of("&", "&"),
        Arguments.of("|", "|"), Arguments.of("^", "^"), Arguments.of("!", "!"),
        Arguments.of("~", "~"), Arguments.of("?", "?"), Arguments.of(":", ":"),
        Arguments.of("=", "="), Arguments.of("a / b", "/"));
  }

  /** Retains JSDoc while preventing ordinary comments and quoted text from becoming code. */
  @Test
  void isolatesCommentsAndQuotedStrings() {
    var source = "/** Module // purpose. */\n/* function hidden() {} */\n"
        + "const url = 'https://example.test/a/*b*/'; // class Hidden {}\n"
        + "const marker = \"// not a comment\";";

    assertEquals(List.of(
        "JAVADOC:/** Module // purpose. */", "KEYWORD:const", "IDENTIFIER:url",
        "PUNCTUATOR:=", "STRING:'https://example.test/a/*b*/'", "PUNCTUATOR:;",
        "KEYWORD:const", "IDENTIFIER:marker", "PUNCTUATOR:=",
        "STRING:\"// not a comment\"", "PUNCTUATOR:;", "EOF:"),
        identities(success(source)));
  }

  /** Retains an empty documentation block for later nonblank-content policy. */
  @Test
  void retainsEmptyJavadocToken() {
    assertEquals("JAVADOC:/**/", identity(success("/**/ const value = 1;").getFirst()));
  }

  /** Preserves valid string escapes and escaped line continuations as inert string text. */
  @Test
  void tokenizesValidStringEscapesAndContinuation() {
    var source = "const escaped = '\\x41\\u0042\\u{43}\\n'; const joined = 'a\\\r\nb';";

    assertEquals(List.of(
        "STRING:'\\x41\\u0042\\u{43}\\n'", "STRING:'a\\\r\nb'"),
        success(source).stream()
            .filter(token -> token.kind() == JavaScriptTokenKind.STRING)
            .map(JavaScriptLexerTest::identity)
            .toList());
  }

  /** Distinguishes repository-style regex literals from division and division assignment. */
  @Test
  void distinguishesRegexFromDivision() {
    var source = "const matcher = /https?:\\/\\/[a-z/]+/giu; value / 2; value /= 3; "
        + "if (ready) /x[\\/]y/.test(input); call() / other; return /done/;";

    assertEquals(List.of(
        "REGEX:/https?:\\/\\/[a-z/]+/giu", "PUNCTUATOR:/", "PUNCTUATOR:/=",
        "REGEX:/x[\\/]y/", "PUNCTUATOR:/", "REGEX:/done/"),
        success(source).stream()
            .filter(token -> token.kind() == JavaScriptTokenKind.REGEX
                || token.text().equals("/") || token.text().equals("/="))
            .map(JavaScriptLexerTest::identity)
            .toList());
  }

  /**
   * Starts a regex after every explicitly supported expression-leading keyword.
   *
   * @param keyword expression-leading keyword under test
   */
  @ParameterizedTest(name = "regex after {0}")
  @ValueSource(strings = {
      "await", "case", "delete", "do", "else", "in", "instanceof", "new", "of",
      "return", "throw", "typeof", "void", "yield"
  })
  void startsRegexAfterEveryExpressionLeadingKeyword(String keyword) {
    assertEquals(1, success(keyword + " /x/;").stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.REGEX)
        .count());
  }

  /**
   * Starts a regex after each supported control-header closing parenthesis.
   *
   * @param source control header followed by a regex statement
   */
  @ParameterizedTest(name = "control regex {index}")
  @ValueSource(strings = {
      "if (ready) /x/;", "for (;;) /x/;", "while (ready) /x/;",
      "with (value) /x/;", "switch (value) /x/;", "catch (error) /x/;"
  })
  void startsRegexAfterEveryControlParenthesis(String source) {
    assertEquals(1, success(source).stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.REGEX)
        .count());
  }

  /** Preserves nested interpolation ownership while skipping every raw template fragment. */
  @Test
  void tokenizesNestedTemplateInterpolation() {
    var source = "`raw function fake() {} ${ {value: `nested ${/x/.test(name)}`} } tail`";

    assertEquals(List.of(
        "TEMPLATE_START:`", "TEMPLATE_EXPRESSION_START:${", "PUNCTUATOR:{",
        "IDENTIFIER:value", "PUNCTUATOR::", "TEMPLATE_START:`",
        "TEMPLATE_EXPRESSION_START:${", "REGEX:/x/", "PUNCTUATOR:.",
        "IDENTIFIER:test", "PUNCTUATOR:(", "IDENTIFIER:name", "PUNCTUATOR:)",
        "TEMPLATE_EXPRESSION_END:}", "TEMPLATE_END:`", "PUNCTUATOR:}",
        "TEMPLATE_EXPRESSION_END:}", "TEMPLATE_END:`", "EOF:"),
        identities(success(source)));
  }

  /** Keeps template escapes, strings, and comments from closing an interpolation owner. */
  @Test
  void isolatesNestedTemplateStringsCommentsAndEscapes() {
    var source = "`raw \\` ${ \"}\" /* } */ `nested ${value}` } tail`";

    var tokens = success(source);

    assertEquals(2, tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.TEMPLATE_START).count());
    assertEquals(2, tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.TEMPLATE_EXPRESSION_START).count());
    assertEquals(2, tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.TEMPLATE_EXPRESSION_END).count());
    assertEquals(List.of("STRING:\"}\""), tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.STRING)
        .map(JavaScriptLexerTest::identity)
        .toList());
  }

  /** Reports exact line, column, and UTF-16 offsets across all supported line endings. */
  @Test
  void tracksCoordinatesAcrossLineEndingsAndUnicode() {
    var source = "const astral = '😀';\r\nconst next = 1;\u2028const last = 2;";

    var tokens = success(source);
    var next = tokens.stream().filter(token -> token.text().equals("next")).findFirst().orElseThrow();
    var last = tokens.stream().filter(token -> token.text().equals("last")).findFirst().orElseThrow();

    assertEquals(new JavaScriptToken(JavaScriptTokenKind.IDENTIFIER, "next", 2, 7, 28, 32), next);
    assertEquals(3, last.line());
    assertEquals(7, last.column());
    assertEquals(source.indexOf("last"), last.startOffset());
  }

  /** Advances same-line columns by code point while retaining UTF-16 offsets. */
  @Test
  void separatesUnicodeColumnsFromOffsets() {
    var source = "'😀' after";

    var after = success(source).stream()
        .filter(token -> token.text().equals("after"))
        .findFirst().orElseThrow();

    assertEquals(1, after.line());
    assertEquals(5, after.column());
    assertEquals(5, after.startOffset());
  }

  /**
   * Treats each supported JavaScript line terminator as one logical line boundary.
   *
   * @param terminator source line terminator under test
   * @param expectedOffset UTF-16 offset of the token after the terminator
   */
  @ParameterizedTest(name = "line terminator {index}")
  @MethodSource("lineTerminators")
  void tracksEverySupportedLineTerminator(String terminator, int expectedOffset) {
    var source = "a" + terminator + "b";

    var token = success(source).stream()
        .filter(candidate -> candidate.text().equals("b"))
        .findFirst().orElseThrow();

    assertEquals(2, token.line());
    assertEquals(1, token.column());
    assertEquals(expectedOffset, token.startOffset());
  }

  /**
   * Supplies LF, lone CR, CRLF, U+2028, and U+2029 line terminators.
   *
   * @return line terminator and expected following UTF-16 offset fixtures
   */
  private static Stream<Arguments> lineTerminators() {
    return Stream.of(
        Arguments.of("\n", 2),
        Arguments.of("\r", 2),
        Arguments.of("\r\n", 3),
        Arguments.of("\u2028", 2),
        Arguments.of("\u2029", 2));
  }

  /** Tokenizes representative regex and nested-template source copied from owned modules. */
  @Test
  void tokenizesRepositoryDerivedSnippets() {
    var source = "const price = /\\$([0-9]+(?:\\.[0-9]{2})?)/.exec(text);\n"
        + "const endpoint = `${baseUrl}/api/${encodeURIComponent(path)}`;";

    var tokens = success(source);

    assertEquals(1, tokens.stream().filter(token -> token.kind() == JavaScriptTokenKind.REGEX).count());
    assertEquals(2, tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.TEMPLATE_EXPRESSION_START)
        .count());
    assertEquals(2, tokens.stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.TEMPLATE_EXPRESSION_END)
        .count());
  }

  /** Rejects null source before creating scanner state. */
  @Test
  void rejectsNullSource() {
    assertThrows(NullPointerException.class, () -> JavaScriptLexer.lex(null));
  }

  /** Removes tokens owned by an unterminated template frame before returning failure. */
  @Test
  void rollsBackTokensFromUnterminatedTemplateOwner() {
    var source = "const before = 1; `open ${value";

    var failure = assertInstanceOf(
        JavaScriptLexResult.Failure.class, JavaScriptLexer.lex(source));

    assertEquals(List.of(
        "KEYWORD:const", "IDENTIFIER:before", "PUNCTUATOR:=", "NUMBER:1",
        "PUNCTUATOR:;", "TEMPLATE_START:`"), identities(failure.tokens()));
    assertEquals(new JavaScriptLexError(
        1, 25, 24, "unterminated template interpolation"), failure.error());
  }

  /** Removes a partial malformed number while preserving only completed prefix tokens. */
  @Test
  void doesNotRetainPartialMalformedNumber() {
    var failure = assertInstanceOf(JavaScriptLexResult.Failure.class,
        JavaScriptLexer.lex("const before = 1; 2e+"));

    assertEquals(List.of(
        "KEYWORD:const", "IDENTIFIER:before", "PUNCTUATOR:=", "NUMBER:1",
        "PUNCTUATOR:;"), identities(failure.tokens()));
    assertEquals(new JavaScriptLexError(
        1, 20, 19, "malformed numeric exponent"), failure.error());
  }

  /**
   * Returns one stable failure and no partial lexical-unit token for malformed source.
   *
   * @param name fixture identity used by the parameterized display name
   * @param source malformed source text
   * @param line expected one-based error line
   * @param column expected one-based error column
   * @param offset expected zero-based UTF-16 error offset
   * @param message expected stable error explanation
   */
  @ParameterizedTest(name = "{0}")
  @MethodSource("malformedSources")
  void failsClosedOnMalformedSource(
      String name, String source, int line, int column, int offset, String message) {
    var failure = assertInstanceOf(JavaScriptLexResult.Failure.class,
        JavaScriptLexer.lex(source), name);

    assertEquals(new JavaScriptLexError(line, column, offset, message), failure.error());
    assertEquals(0, failure.tokens().stream()
        .filter(token -> token.kind() == JavaScriptTokenKind.EOF).count());
    assertThrows(UnsupportedOperationException.class,
        () -> failure.tokens().add(new JavaScriptToken(
            JavaScriptTokenKind.EOF, "", 1, 1, 0, 0)));
  }

  /**
   * Supplies one exact first-error fixture for every unsafe lexical state.
   *
   * @return malformed source and expected error fixtures
   */
  private static Stream<Arguments> malformedSources() {
    return Stream.of(
        Arguments.of("block comment", "/* open", 1, 1, 0, "unterminated block comment"),
        Arguments.of("JSDoc", "/** open", 1, 1, 0, "unterminated JSDoc"),
        Arguments.of("single string", "'open", 1, 1, 0, "unterminated string literal"),
        Arguments.of("double string line", "\"open\n", 1, 1, 0, "unescaped line terminator in string literal"),
        Arguments.of("hex escape", "'\\xG0'", 1, 2, 1, "malformed hexadecimal escape"),
        Arguments.of("Unicode escape", "'\\u{}'", 1, 2, 1, "malformed Unicode escape"),
        Arguments.of("regex", "const x = /open", 1, 11, 10, "unterminated regular expression literal"),
        Arguments.of("regex class", "const x = /[abc/", 1, 11, 10, "unterminated regular expression character class"),
        Arguments.of("regex flag escape", "const x = /x/\\u0067", 1, 14, 13,
            "unsupported regular expression flag escape"),
        Arguments.of("template", "`open", 1, 1, 0, "unterminated template literal"),
        Arguments.of("interpolation", "`open ${value", 1, 7, 6, "unterminated template interpolation"),
        Arguments.of("radix", "0x", 1, 1, 0, "malformed hexadecimal literal"),
        Arguments.of("separator", "1__0", 1, 2, 1, "malformed numeric separator"),
        Arguments.of("exponent", "1e+", 1, 2, 1, "malformed numeric exponent"),
        Arguments.of("binary digit", "0b102", 1, 5, 4, "malformed binary literal"),
        Arguments.of("octal digit", "0o758", 1, 5, 4, "malformed octal literal"),
        Arguments.of("BigInt fraction", "1.0n", 1, 4, 3, "BigInt literal must be an integer"),
        Arguments.of("BigInt exponent", "1e2n", 1, 4, 3, "BigInt literal must be an integer"),
        Arguments.of("identifier escape", "const \\u0061 = 1", 1, 7, 6, "unsupported escaped identifier"),
        Arguments.of("ambiguous slash", "{} /x/", 1, 4, 3, "ambiguous slash after closing brace"),
        Arguments.of("unexpected", "@", 1, 1, 0, "unexpected character '@'"));
  }

  /**
   * Extracts a successful result or lets the assertion identify an unexpected failure.
   *
   * @param source valid JavaScript source
   * @return immutable complete token stream
   */
  private static List<JavaScriptToken> success(String source) {
    return assertInstanceOf(JavaScriptLexResult.Success.class, JavaScriptLexer.lex(source)).tokens();
  }

  /**
   * Renders token kinds and exact spellings for compact fixture assertions.
   *
   * @param tokens tokens to render
   * @return immutable rendered identities in token order
   */
  private static List<String> identities(List<JavaScriptToken> tokens) {
    return tokens.stream().map(JavaScriptLexerTest::identity).toList();
  }

  /**
   * Renders one token kind and exact spelling.
   *
   * @param token token to render
   * @return rendered kind and source spelling
   */
  private static String identity(JavaScriptToken token) {
    return token.kind() + ":" + token.text();
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexerTest'
```

Expected RED: test compilation fails only because `JavaScriptLexer` does not exist. Preserve the output in the task report before production edits.

The implementing worker must verify the two hard-coded coordinate expectations against Java's UTF-16 indexing while completing the fixture. If the literal's calculated offsets differ, correct the expected integers in the test before production implementation and record the calculation; do not distort lexer behavior to satisfy an arithmetic typo.

#### Code Edit 2.2

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexer.java`
- Lines: 1
- Action: add

Current:

```text
Absent at Task 2 base after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.Objects;

/** Tokenizes repository-owned JavaScript without executing or semantically parsing it. */
final class JavaScriptLexer {
  /** Prevents utility-class construction. */
  private JavaScriptLexer() {}

  /**
   * Tokenizes one complete JavaScript source value.
   *
   * @param source complete JavaScript source text
   * @return immutable complete stream or first lexical failure
   * @throws NullPointerException when source is absent
   */
  static JavaScriptLexResult lex(String source) {
    return new Cursor(Objects.requireNonNull(source)).scan();
  }
}
```

The excerpt above is the exact package boundary; implement the private `Cursor` and nested value types inside the same file with this fixed control-flow contract, not a different error protocol:

1. `Cursor` owns final `source`, mutable `tokens`, `templateFrames`, and `parenthesisContexts`; integer `offset`, `line = 1`, and `column = 1`; nullable `previousToken`; nullable `ParenthesisContext lastClosedParenthesisContext`; and nullable `JavaScriptLexError error`. The last-closed field has a field Javadoc stating that it classifies `previousToken` only when that token is `)`. No other mutable state is static.
2. `Cursor(String source)` assigns the already nonnull source. Its Javadoc includes `@param source complete JavaScript source text`.
3. `scan()` returns `JavaScriptLexResult`. While `offset < source.length()` and `error == null`, it dispatches exactly one complete unit based on template state and the current code point. Each scanner helper returns `void`: it either advances/emits/skips a whole unit or calls `recordFailure(...)` exactly once and returns. After every dispatch, `scan()` immediately returns `new Failure(tokens, error)` when error is nonnull. At clean EOF it diagnoses the top unclosed template/interpolation frame first; otherwise it emits EOF and returns `new Success(tokens)`. Its Javadoc includes `@return immutable complete stream or first lexical failure`.
4. `recordFailure(int errorLine, int errorColumn, int errorOffset, int tokenCheckpoint, String message)` returns `void`, ignores later calls after the first, removes tokens from the end until `tokens.size() == tokenCheckpoint`, and assigns the validated error. Its Javadoc documents all five parameters. This is the only malformed-source state transition.
5. Every unit scanner captures `start`, `startLine`, `startColumn`, and `tokenCheckpoint = tokens.size()` before consuming. Identifiers, numbers, strings, comments/JSDoc, regexes, template raw text, and punctuators use distinct private `void` helpers. Their Javadocs document each input parameter; they have no `@return` because they return `void`.
6. `emit(JavaScriptTokenKind kind, int start, int startLine, int startColumn)` returns `void`, constructs exact text with `source.substring(start, offset)`, adds one token, and updates `previousToken` for semantic code tokens, `TEMPLATE_EXPRESSION_START`, and `TEMPLATE_END`. Before any such update to a token other than `)`, it resets `lastClosedParenthesisContext` to null. JSDoc, `ORDINARY_COMMENT`, `TEMPLATE_START`, and `TEMPLATE_EXPRESSION_END` do not overwrite the separately established expression context. `canStartExpression()` treats `TEMPLATE_EXPRESSION_START` as expression-leading and `TEMPLATE_END` as value-ending. Its Javadoc documents all four parameters.
7. `advance()` returns `void` and is the only helper that mutates offset/line/column. It consumes CRLF together; consumes lone CR, LF, U+2028, or U+2029 as one line boundary; otherwise advances offset by `Character.charCount(codePoint)` and column by one. Its Javadoc states that positional effect.
8. `canStartExpression()` returns `SlashContext`, not `boolean`. `SlashContext` is a documented private enum with documented constants `REGEX`, `DIVISION`, `AMBIGUOUS_AFTER_BRACE`, and `AMBIGUOUS_AFTER_PARENTHESIS`. The slash dispatcher records an accurate message for each ambiguity, calls `scanRegex` for regex, and emits `/` or `/=` for division. This makes every fail-closed branch explicit rather than encoding ambiguity as a guess.
9. `TemplateFrame` is a private documented record with documented components `state`, `openingLine`, `openingColumn`, `openingOffset`, `braceDepth`, and `tokenCheckpoint`. `TemplateState` is a private documented enum with documented constants `TEMPLATE_RAW` and `TEMPLATE_EXPRESSION`. Updating brace depth replaces the top immutable frame; no frame is shared across calls.
10. `ParenthesisContext` is a private documented enum with documented constants `VALUE`, `CONTROL`, `FOR_HEAD`, `FOR_CLASSIC`, and `FOR_OF_RHS`. The lexer pushes `FOR_HEAD` when `(` follows `for`, `CONTROL` when `(` follows `if`, `while`, `with`, `switch`, or `catch`, and `VALUE` otherwise. A top-level semicolon changes `FOR_HEAD` to `FOR_CLASSIC`. In `FOR_HEAD`, an `of` following a proved assignment-target/value role becomes the for-of operator and changes the frame to `FOR_OF_RHS`; member/property-name, declaration-name, and expression-leading positions keep `of` as a contextual identifier. A closing-brace predecessor makes contextual `of` fail closed at its own boundary because brace-pattern ownership belongs to Phase B. When a matching `)` is scanned, pop the context, emit `)`, and assign its control-versus-value meaning to `lastClosedParenthesisContext`; an unmatched `)` emits normally and leaves that field null because unmatched delimiters remain Phase B recognizer concerns. When `previousToken` is `)`, `canStartExpression()` returns regex only for a nonnull control context, division for `VALUE`, and the distinct unmatched-parenthesis ambiguity for null. Whitespace, JSDoc, and ordinary-comment barriers do not reset the field; the next emitted significant token does as specified in item 6.
11. Declare exact immutable static values: `KEYWORDS = Set.of("async", "await", "break", "case", "catch", "class", "const", "continue", "debugger", "default", "delete", "do", "else", "enum", "export", "extends", "false", "finally", "for", "from", "function", "get", "if", "implements", "import", "in", "instanceof", "interface", "let", "new", "null", "of", "package", "private", "protected", "public", "return", "set", "static", "super", "switch", "this", "throw", "true", "try", "typeof", "var", "void", "while", "with", "yield")`; `CONTEXTUAL_IDENTIFIER_KEYWORDS = Set.of("async", "from", "get", "of", "set")`; `EXPRESSION_LEADING_KEYWORDS = Set.of("await", "case", "delete", "do", "else", "in", "instanceof", "new", "return", "throw", "typeof", "void", "yield")`; and longest-first `PUNCTUATORS = List.of(">>>=", "===", "!==", ">>>", "**=", "&&=", "||=", "??=", "<<=", ">>=", "...", "=>", "==", "!=", "<=", ">=", "++", "--", "&&", "||", "??", "?.", "**", "<<", ">>", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "{", "}", "(", ")", "[", "]", ".", ";", ",", "<", ">", "+", "-", "*", "%", "&", "|", "^", "!", "~", "?", ":", "=", "/")`.
12. Every private helper must have a descriptive Javadoc plus applicable `@param`, `@return`, and `@throws` tags. Every private field, nested type, record component, and enum constant must have semantic Javadocs. The Task 2 reviewer must inspect these tags directly because this phase does not yet route the new source through the aggregate Java checker.

No `UnsupportedOperationException`, nullable helper return, comment-only body, TODO, silent unsupported branch, catch-and-continue recovery, alternate error field, or partial-token emission is permitted.

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexerTest'
.\gradlew.bat --no-daemon :documentation-validator:test
$sourceFiles = Get-ChildItem -Recurse -Filter '*.java' 'documentation-validator\src\main\java'
& javadoc -private -quiet -d 'documentation-validator\build\reports\private-javadocs-javascript-lexer' $sourceFiles.FullName
.\gradlew.bat --no-daemon build
git diff --check
git status --short
```

Expected GREEN: focused lexer tests and all validator tests pass with zero failures/errors; established platform skips are allowed. Private Javadocs exit 0 without warnings, the root build exits 0, `git diff --check` exits 0, and the only uncommitted Task 2 files are the two planned additions.

After task review, stage only the two Task 2 files and commit:

```powershell
git add -- documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexer.java documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexerTest.java
git commit -m "Add JavaScript lexer foundation"
```

#### Corrective review amendment — Task 2 fix round 2

The first whole-phase review at `e496fe48a3b269c8baaf042bae3b5db9bd72e213` found four Important Phase B-readiness defects and one Minor diagnostic defect. Correct them together under TDD, then repeat Task 2 review before restarting Task 3. No other behavior or scope may change.

##### Code Edit 2.3

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptTokenKind.java`
- Lines: 4-29
- Action: modify

Current:

```java
/** A complete documentation block whose source spelling begins with {@code /**}. */
JAVADOC,
/** The opening backtick of a template literal. */
TEMPLATE_START,
```

Proposed:

```java
/** A complete ordinary line or block comment retained only as an attachment barrier. */
ORDINARY_COMMENT,
/** A complete documentation block whose source spelling begins with {@code /**}. */
JAVADOC,
/** The opening backtick of a template literal. */
TEMPLATE_START,
```

##### Code Edit 2.4

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexerTest.java`
- Lines: 51-568
- Action: modify

Current:

```java
@ValueSource(strings = {
    "await", "case", "delete", "do", "else", "in", "instanceof", "new", "of",
    "return", "throw", "typeof", "void", "yield"
})
```

Proposed:

```java
@ValueSource(strings = {
    "await", "case", "delete", "do", "else", "in", "instanceof", "new",
    "return", "throw", "typeof", "void", "yield"
})
```

Add focused fixtures that fail at the reviewed head and prove all of the following exact boundaries:

- Equal-width `/** docs */      function f(){}` and `/** docs *//*x*/ function f(){}` inputs produce distinct streams because the latter contains one exact-position `ORDINARY_COMMENT` token; line and block barriers never replace `previousToken` or change slash role.
- `function\uFEFFf(){}` emits `KEYWORD:function` then `IDENTIFIER:f`; `$`, `_`, U+200C, U+200D, a supplementary `ID_Start`, and a supplementary `ID_Continue` remain supported; NUL and another Java identifier-ignorable control produce an exact unexpected-character failure rather than entering an identifier.
- `const of = 8, x = 2; of / x / 2;` and equivalent `async`, `get`, `set`, and `from` bindings retain two division punctuators; `for (const item of /x/) {}` emits a regex only after the proved for-of operator; `for (const of of /x/) {}` distinguishes the binding name from the operator; `for (; of / 2; ) {}` treats `of` as a value in the classic header. `for (obj.of / 2; ; ) {}` and its optional-chain equivalent prove that member/property-name `of` is never promoted to the operator. `for (const {value} of /x/) {}` fails at the ambiguous `of` with exact coordinates because Phase A does not own brace-pattern recognition.
- Strings and template raw text accept standalone `\\0` plus one permitted non-escape character, while `\\1`, `\\8`, `\\9`, `\\01`, and `\\08` fail at the owning backslash and return stable line/column/offset/message evidence. String failures roll back to the string-unit checkpoint. Template failures, including nested-template failures after completed interpolations, roll back to the active `TEMPLATE_RAW` frame's owner checkpoint so no token owned by the incomplete template remains; exact failure-prefix assertions pin both cases.
- `) /x/` fails with an unmatched-parenthesis ambiguity message and never mentions a brace.

##### Code Edit 2.5

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexer.java`
- Lines: 13-1359
- Action: modify

Current:

```java
private static final Set<String> EXPRESSION_LEADING_KEYWORDS = Set.of(
    "await", "case", "delete", "do", "else", "in", "instanceof", "new", "of",
    "return", "throw", "typeof", "void", "yield");
```

Proposed:

```java
private static final Set<String> CONTEXTUAL_IDENTIFIER_KEYWORDS =
    Set.of("async", "from", "get", "of", "set");
private static final Set<String> EXPRESSION_LEADING_KEYWORDS = Set.of(
    "await", "case", "delete", "do", "else", "in", "instanceof", "new",
    "return", "throw", "typeof", "void", "yield");
```

Implement the following fixed behavior without adding source rereads, parser dependencies, shared mutable state, or recovery:

1. `scanLineComment` and complete non-JSDoc `scanBlockComment` calls emit `ORDINARY_COMMENT`; `emit` retains the token but excludes it from significant-token, update-role, parenthesis, and slash-context mutation. Unterminated comments still fail and emit no partial barrier.
2. Identifier start/part predicates exclude JavaScript whitespace and `Character.isIdentifierIgnorable` code points before applying the JDK Unicode predicate, except that U+200C and U+200D remain explicit valid continuation characters. This makes U+FEFF a separator and leaves unsupported controls for the fail-closed dispatcher.
3. `scanEscape` rejects every decimal escape except `\\0` with a non-decimal lookahead. The error is anchored at the owning backslash and uses one stable message such as `legacy numeric escape is not permitted in a module`. String callers pass their unit-local checkpoint. A template-raw caller must pass, or explicitly roll back to, the active `TEMPLATE_RAW` frame's `tokenCheckpoint`, not the current segment's `tokens.size()`, so an invalid escape removes `TEMPLATE_START`, completed interpolation tokens, and nested-template tokens owned by that still-incomplete template. The nested-template fixture must prove that outer completed tokens remain while every token owned by the invalid inner template is removed.
4. Treat `async`, `from`, `get`, `set`, and identifier-position `of` as value-ending for slash purposes even though their exact spellings remain recognizer-visible. Extend the documented parenthesis context with `FOR_HEAD`, `FOR_CLASSIC`, and `FOR_OF_RHS`: enter `FOR_HEAD` after `for (`; change it to `FOR_CLASSIC` at its first top-level semicolon; recognize `of` as the for-of operator only in `FOR_HEAD` after a proved assignment-target/value role, then change to `FOR_OF_RHS`. A current member-name role after `.` or `?.`, a declaration-name position, or another expression-leading predecessor proves identifier use and must not promote `of`. A closing-brace predecessor is structurally ambiguous because Phase A cannot distinguish an object/destructuring pattern from a block/object expression; fail at that `of` with stable `ambiguous contextual 'of' after closing brace in for header` coordinates instead of choosing a slash goal. Nested value parentheses do not consume or mutate the owning `for` state.
5. Add a distinct documented unmatched-parenthesis slash ambiguity state and accurate diagnostic; do not route it through `AMBIGUOUS_AFTER_BRACE`.
6. Update every affected field/helper/nested-type/enum-constant Javadoc, including the new token's attachment-only semantics and every changed failure contract.

Fix-round RED must be assertion failures from the new fixtures, not compilation failure. After GREEN, rerun focused lexer tests, the complete validator module, direct private Javadocs, the root build, `git diff --check`, the 96-file corpus probe, and authoritative-checkout status hashing. Commit only the three files above with message `Preserve JavaScript lexical boundary semantics`, then repeat the Task 2 scoped review against all five final-review findings.

### Task 3 - Run phase review and freeze the Phase B input boundary

Sequence / dependencies:

- Runs after both implementation commits and their task-specific reviews are complete.
- Makes no planned source edits. If review finds a Critical or Important issue, return to the owning task with a failing regression test, make a narrow fix commit, and repeat both task and final review.

Implementation notes:

- Required skill: `write-chris-street-style-code` before any corrective code edits. Invoke it and `superpowers:test-driven-development` if review produces a change.
- Before-Edit Brief:
  - Behavior: the committed lexical boundary is independently shown to be deterministic, fail-closed, fully documented, and sufficient for the later recognizer.
  - Invariants: no application/runtime behavior, file discovery, policy enforcement, Gradle lifecycle, CI, README, or authoritative-checkout state changes.
  - Boundary/API: Phase B receives only `JavaScriptLexResult` and its tokens/errors; it must reject `Failure` without consuming its token prefix.
  - Effects and failures: review is read-only unless a proven defect triggers the explicit RED/fix/re-review loop; no push or integration occurs.
  - Tests and evidence: rerun focused/domain/module/root/private-Javadoc checks from clean commits and retain review verdicts plus authoritative status hashes.

Task-level verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexicalDomainTest'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexerTest'
.\gradlew.bat --no-daemon :documentation-validator:test
$sourceFiles = Get-ChildItem -Recurse -Filter '*.java' 'documentation-validator\src\main\java'
& javadoc -private -quiet -d 'documentation-validator\build\reports\private-javadocs-javascript-lexer' $sourceFiles.FullName
.\gradlew.bat --no-daemon build
git diff --check
git status --short --branch
```

Require a clean isolated worktree, zero test failures/errors, no private-Javadoc warnings, no whitespace errors, unchanged authoritative checkout status hash, and a final review verdict with no Critical or Important finding.

## Code Changes

- Add `JavaScriptTokenKind.java`: documented stable token taxonomy.
- Add `JavaScriptToken.java`: validated exact-spelling and exact-position token value.
- Add `JavaScriptLexError.java`: validated first-unsafe-position value.
- Add `JavaScriptLexResult.java`: sealed immutable success/failure boundary with stream invariants.
- Add `JavaScriptLexer.java`: pure per-call state-machine tokenizer.
- Add `JavaScriptLexicalDomainTest.java`: constructor, ordering, EOF, failure, and immutability fixtures.
- Add `JavaScriptLexerTest.java`: lexical isolation, coordinates, regex/division, nested template, malformed-state, and repository-derived fixtures.

No existing application, discovery, checker, Gradle, workflow, README, or JavaScript file changes in this phase.

## Files and Modules

Only the `documentation-validator` module changes. Expected final phase diff from `d4a77e2e2a58906b968f61972ea964cdc10a8833`: seven new Java files. Build outputs under `documentation-validator/build/` remain untracked.

## Unit Testing

Task 1 RED/GREEN:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexicalDomainTest'
```

Task 2 RED/GREEN:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptLexerTest'
```

Complete module:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test
```

The test suite must cover valid and invalid values, immutable result lists, keyword/name/numeric/punctuator tokenization, JSDoc retention, comment/string isolation, regex/division context, regex character classes and escapes, nested template ownership, UTF-16 coordinates, all supported line endings, malformed escapes/literals/comments/templates, first-error semantics, and representative owned-source snippets.

## Local Testing

No Spring application launch, browser session, Node process, service restart, or production listener action is required because this phase changes only an isolated build-time tokenizer that is not wired into the lifecycle. Local confidence comes from direct private-Javadoc generation and the repository root build:

```powershell
$sourceFiles = Get-ChildItem -Recurse -Filter '*.java' 'documentation-validator\src\main\java'
& javadoc -private -quiet -d 'documentation-validator\build\reports\private-javadocs-javascript-lexer' $sourceFiles.FullName
.\gradlew.bat --no-daemon build
```

## Validation

- Task 1 shows expected missing-symbol RED before domain implementation and GREEN afterward.
- Task 2 shows expected missing-symbol RED before lexer implementation and GREEN afterward.
- A successful empty source produces only EOF at line 1, column 1, offsets 0-0.
- A failed source produces one `Failure`, no EOF, and no token from the partial malformed lexical unit. Template/interpolation failure rolls the emitted list back to the owning frame checkpoint before constructing that result.
- Ordinary comments, quoted contents, regex bodies, and template raw text cannot surface declaration-looking tokens.
- JSDoc, interpolation boundaries, interpolation code, and nested template boundaries remain explicit.
- Regex/division fixtures include expression-leading keywords, control-parenthesis closure, call closure, division assignment, escaped slash, and slash inside a character class.
- Domain and lexer tests, the complete validator suite, private Javadocs, root build, and `git diff --check` pass.
- Only seven planned files exist in the phase diff; the isolated worktree is clean after commits.
- Independent task and final reviews report no Critical or Important issue.
- The authoritative checkout status hash is unchanged.

## Execution Evidence

- Phase base: `d4a77e2e2a58906b968f61972ea964cdc10a8833`; completed head: `affed13149c07ec5c024e20325a0333c2efd374f`.
- Commits: `2a019769a029acb61b5780d5683a66978d35cab7`, `a84cca2299bbdb507ddfe5d917ed116e969d9da0`, `16b6b08da2459b1eb912d996472b43ded6ad4055`, `e496fe48a3b269c8baaf042bae3b5db9bd72e213`, and `affed13149c07ec5c024e20325a0333c2efd374f`.
- Task 1 captured missing-symbol RED, then passed 7 domain tests; its independent fix re-review approved all findings.
- Task 2 initial RED was missing only `JavaScriptLexer`; fix round 1 captured 11 assertion failures across 132 tests, and fix round 2 captured 24 assertion failures across 155 compile-clean tests before production changes.
- Final GREEN: 155 lexer tests and 7 domain tests passed; the complete validator suite passed 234 tests with zero failures/errors and one established Windows skip; direct private Javadocs exited 0 without warnings.
- Final repository root `build` exited 0 in 2m16s with 22 actionable tasks, 8 executed and 14 up-to-date.
- A reflective final-head probe lexed all 96 first-party JavaScript files successfully with zero failures.
- The complete diff contains exactly the seven planned Java files; `git diff --check` passed and the isolated worktree was clean.
- The scoped fix-round review approved all five whole-phase findings with no new issue. The fresh final whole-phase re-review returned `APPROVED` with 0 Critical, 0 Important, and 0 Minor findings.
- The authoritative dirty checkout status hash remained `C706E834EA40C9F523941C350570B68C5663FA4F3200528FA54D870A816E0CEB`.
- No rebase, pull, push, pull request, merge, application launch, production listener action, or authoritative-checkout mutation occurred in this phase.

## Rollback or Recovery

- Revert only the isolated branch's Task 2 commit to remove the lexer while preserving the domain contract, or revert Task 2 then Task 1 to remove the entire phase.
- Do not reset or clean either checkout. Preserve task reports, RED/GREEN output, and review findings long enough to diagnose any failed gate.
- If a malformed-source test exposes ambiguous desired behavior, stop at the failed test and amend this Builder plan/design through the normal review/checkpoint workflow before broadening syntax support.
- If Gradle locks occur, use only the isolated `GRADLE_USER_HOME`; stop only the daemon proven to own the isolated lock and retry once.

## Risks

- **Regex versus division ambiguity:** mitigate with explicit expression-start/value-end categories, control-parenthesis context, paired positive/negative fixtures, and fail-closed behavior for unhandled characters.
- **Template owner corruption:** mitigate with explicit nested template/interpolation frames and fixtures combining object braces, nested templates, regex, strings, and comments.
- **Position drift around CRLF or astral characters:** offsets are UTF-16, columns advance by code point, and exact mixed-line-ending fixtures pin both dimensions.
- **Numeric grammar gaps:** support the bounded standard forms explicitly and reject malformed separators/radices/exponents instead of splitting them into misleading valid tokens.
- **False confidence from synthetic fixtures:** include short source snippets copied from owned modules while keeping tests hermetic and independent of mutable application files.
- **Private helper complexity:** keep one mutable cursor per call, small single-purpose documented helpers, no shared mutable state, and task/final quality review.
- **Future JavaScript syntax expansion:** Phase B or later source changes receive a deterministic lexical or unsupported-syntax failure; broaden only with new RED fixtures and reviewed design updates.
- **Branch drift from `origin/main`:** integration is deliberately deferred; do not hide drift with a rebase during this phase.

## Completion Criteria

- All seven planned Java files exist on the isolated branch in independently reviewed commits.
- The value model rejects every contradictory EOF, order, position, error, and mutability state in the plan.
- The lexer is JDK-only, pure, reentrant, non-executing, and character-state based.
- Every demonstrated lexical hazard is isolated or tokenized with exact identity and position.
- Malformed lexical input returns exactly one deterministic failure and never a successful partial stream.
- Every new Java declaration, private helper, field, enum constant, parameter, return value, and failure contract has accurate Javadocs.
- Focused tests, full validator tests, direct private Javadocs, root build, and whitespace validation pass from clean commits.
- Task-level and final reviews find no remaining Critical or Important issue.
- The authoritative dirty checkout is unchanged, and no integration/push/PR action has occurred.
- The exact immutable lexical boundary is ready for a separately planned Phase B structural recognizer and documentation-rule implementation.
