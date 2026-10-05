# JavaScript Structural Recognizer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. Every code task must also invoke `chris-street-style` and `superpowers:test-driven-development` before editing production or test code.
>
> **Review gate:** Approved for execution on 2026-08-01 after an independent full-plan review returned 0 Critical, 0 Important, and 0 Minor findings. Any later API or accepted-inventory change returns the plan to `ready-for-review` before spoke edits continue.

**Goal:** Implement Phase B1 as a pure, JDK-only structural recognizer that accepts only a completed `JavaScriptLexResult.Success` and returns immutable JavaScript declaration data or one deterministic structural error for every repository-native named callable and stable class value.

**Architecture:** Keep the completed lexer as an immutable trust boundary. Add a validated structural domain, then focused delimiter, documentation-attachment, formal-parameter, and callable-body helpers, and finally a context-owned declaration scanner behind one package-private facade. The scanner records structure and exact preceding JSDoc/barrier ownership but performs no JSDoc content or tag policy, file discovery, source reread, violation conversion, or build integration.

**Tech Stack:** Java 25, Java standard library, JUnit Jupiter, Gradle Kotlin DSL; no npm, Node subprocess, browser, JavaScript execution, parser dependency, source-declaration regular expression, or application runtime.

## Document Status

ready-for-execution

Independent review: `READY` on 2026-08-01 with no Critical, Important, or Minor findings after the empty-range, enum/API consistency, caller-visible throw, SDD/TDD sequencing, formal-rest, Javadoc, failure-prefix, contextual-member, optional-chain, default-export owner, and private-constructor corrections were incorporated.

## Objective

Implement only Phase B1 of the approved JavaScript scanner design at spoke head `affed13149c07ec5c024e20325a0333c2efd374f`. The completed phase must turn a successful immutable lexical stream into a source-ordered immutable module-documentation fact plus every documentable callable/class declaration, or fail closed at the first structural uncertainty.

Phase B1 must preserve enough syntax facts for Phase B2 without enforcing Phase B2 policy: exact declaration identity and position, exact directly attached JSDoc or blocking token, formal positions and object-pattern leaves, modifiers, and direct value-return/direct-throw/caller-visible-throw facts.

## Goals

- Accept only `JavaScriptLexResult.Success`; make it impossible for B1 to inspect a failed lexical prefix.
- Represent structural success and first structural failure as a sealed immutable result.
- Preserve binding, assigned-identifier, property-path, source-named-expression, and default-export identities as distinct immutable cases.
- Recognize all 1,259 current documentable declarations: 1,240 callables/members, 13 class declarations, five anonymous class expressions with stable binding/member/property targets, and one returned source-named class expression.
- Recognize the complete current callable inventory: 676 function declarations, 52 named arrow bindings, 33 stable identifier/member assignment arrows, one source-named returned function expression, 102 class members, 70 object shorthand methods, one object getter, and 305 arrow-valued object properties.
- Preserve 1,135 formal positions, including 38 object-destructured positions with 152 leaf bindings and the one rest parameter, without inventing a parameter name for a destructuring pattern.
- Record direct syntactic value-return facts for 793 callables and direct syntactic throw facts for 74 callables while excluding nested callable/class bodies from their owners' facts; additionally distinguish the caller-visible subset so a caught throw does not create an inaccurate B2 `@throws` requirement.
- Exempt anonymous function/arrow expressions used directly as any call or constructor argument because they have no stable declaration identity; the current corpus contains 784 call-argument and 21 constructor-argument exemptions, including 270 Node test callbacks.
- Continue traversing exempt callback bodies so named nested helpers remain declarations.
- Recognize every source-named class expression, including the returned `DefaultFileReader` expression, and every anonymous class expression assigned to a stable binding, member, or named object property.
- Fail closed on unmatched delimiters, malformed supported declaration heads, unsupported formal patterns, and callable-looking computed class/object/member keys.
- Prove the boundary with unit fixtures, an exact current-corpus probe, complete validator tests, private-Javadoc generation, root build, and independent task/final review.

## Inputs

- Approved design: `C:\Users\Christopher\Developer\builder\docs\specs\2026-07-29-javascript-documentation-scanner-design.md`.
- Campaign specification: `C:\Users\Christopher\Developer\builder\docs\specs\2026-07-29-christopherbell-dev-repository-wide-documentation-coverage.md`.
- Completed lexical plan: `C:\Users\Christopher\Developer\builder\docs\implementation-plans\2026-07-29-javascript-lexical-foundation.md`.
- Spoke worktree: `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729`.
- Phase base/head: `affed13149c07ec5c024e20325a0333c2efd374f` on `codex/repository-documentation-coverage`.
- Immutable lexer boundary:
  - `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptTokenKind.java:1-31`
  - `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptToken.java:1-51`
  - `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexResult.java:1-86`
  - `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptLexer.java:1-1505`
- Existing lexical tests:
  - `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexicalDomainTest.java:1-136`
  - `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptLexerTest.java:1-821`
- Accepted head inventory: 96 first-party JavaScript files, 59 application/resource files and 37 Node test files, totaling 18,830 lines. All 96 lex successfully at the phase base.
- Stable-bound anonymous classes are:
  - `website/src/test/js/nav-messages-link.test.js:4` (`globalThis.HTMLElement`)
  - `website/src/test/js/public-content.test.js:6` (`globalThis.HTMLElement`)
  - `website/src/test/js/site-media-player-component.test.js:6` (`globalThis.HTMLElement`)
  - `website/src/test/js/site-media-player-component.test.js:216` (`globalThis.MediaMetadata`)
  - `website/src/test/js/site-media-player-component.test.js:250` (`context.XMLHttpRequest` through the named object property)
- The returned source-named class is `website/src/test/js/site-media-player.test.js:662` (`DefaultFileReader`).
- The returned source-named function is `website/src/main/resources/static/js/lib/feed-context.js:13` (`fetchRoot`).

## Branch

- Repository: `azurras/christopherbell.dev`.
- Isolated worktree: `A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729`.
- Existing branch: `codex/repository-documentation-coverage`.
- Phase base: `affed13149c07ec5c024e20325a0333c2efd374f`.
- Upstream integration target, outside this plan: refreshed `origin/main` after the documentation campaign is ready to integrate.

## Global Constraints

- Work only in the isolated spoke worktree. Do not edit, clean, stage, reset, switch, build, or otherwise mutate `A:\Projects\christopherbell.dev`.
- Recompute the authoritative checkout status hash before Task 1 and after final verification; require it to remain `C706E834EA40C9F523941C350570B68C5663FA4F3200528FA54D870A816E0CEB` unless the user explicitly establishes a new baseline.
  Run this exact read-only PowerShell sequence from `A:\Projects\christopherbell.dev` so encoding and trailing-newline normalization match the accepted Phase A baseline:

  ```powershell
  $statusText = (git status --porcelain=v1 | Out-String)
  $statusBytes = [Text.Encoding]::UTF8.GetBytes($statusText)
  [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($statusBytes))
  ```
- Set `GRADLE_USER_HOME=A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage` for every Gradle command.
- Production B1 code accepts only `JavaScriptLexResult.Success`. Do not add an overload accepting `JavaScriptLexResult`, a `String`, a path, a stream, or a `RepositoryFile`.
- B1 must not re-read JavaScript source. Exact spelling and position come only from the immutable tokens.
- Production code uses only the Java standard library. Do not invoke Node, a browser, a JavaScript engine, Git, the filesystem, the network, or application code.
- Do not use regular expressions to identify declarations, formal parameters, bodies, return/throw facts, or attachment.
- Do not modify the seven completed lexical files or weaken their validation. A lexical defect discovered during execution stops this plan and returns to a separately reviewed Phase A correction.
- Emit declarations in ascending anchor-token offset with no duplicates. A failed result may retain only fully recognized declarations anchored before the first structural error and is never eligible for B2 policy evaluation; the scanner appends a candidate only after its complete owned syntax is proved.
- Resolve module/declaration JSDoc ownership from token adjacency. Whitespace is absent from the stream; `ORDINARY_COMMENT`, a semantic token, or an already-claimed JSDoc is an explicit non-attachment fact. One JSDoc cannot satisfy the module and a declaration, or two declarations.
- Treat anonymous direct call/new function or arrow arguments generically; do not maintain a callee-name allowlist. A source-named function/class expression remains a declaration even when returned or passed as an argument.
- A stable `const`/`let`/`var` binding, bare identifier assignment, dotted member assignment, or named object-property target makes its arrow/function/class value documentable. Preserve the target category and full static property path.
- Anonymous class expressions without a stable target do not produce a class-value declaration, but their named members are traversed and remain callable declarations.
- A callable-looking computed key such as `[name]() {}`, `[name]: () => {}`, or `target[name] = () => {}` is a structural error at `[`; do not guess a stable identity. Non-callable computed reads/writes remain ordinary expressions.
- Direct value-return and direct-throw facts include nested control blocks owned by the callable but exclude every nested function, arrow, and class/member body. Caller-visible throw is a separately recorded subset: a throw protected by an enclosing same-callable `try` with a `catch` is not caller-visible, while a throw or rethrow in a `catch`/`finally` remains visible unless an outer same-callable caught `try` protects it. A concise arrow has a direct value return. A bare `return;` does not.
- Object-destructuring in a `for ... of` header remains an accepted lexical failure from Phase A and never reaches B1. Do not add B1 recovery or source lookahead for it.
- Every new Java type, record component, constructor, method, private helper, field, enum constant, parameter, return value, and documented failure must have accurate Javadocs.
- Apply TDD independently for each implementation task: add the planned test first, run the exact focused command and inspect the expected RED, add minimum production code, then rerun the identical command to GREEN before refactoring.
- Each implementer commits only its task-owned files after focused verification and self-review. The subsequent independent task review gates task completion and any fix round produces additional implementer-owned commits. Do not rebase, merge, pull, push, open a pull request, wire Gradle/CI, or integrate mainline in this plan.
- Final B1 review must find no Critical or Important issue before the phase is accepted or B2 planning begins.

## Non-Goals

- No parsing, normalization, or validation of JSDoc descriptions, `@param`, `@return`/`@returns`, `@throws`, async, effect, mutation, cancellation, ownership, DOM, network, storage, or rejection documentation.
- No conversion to `DocumentationRule` or `DocumentationViolation` and no changes to either existing type.
- No module-purpose policy decision beyond recording its exact attachment state.
- No repository discovery, UTF-8 file reading, path ownership, aggregation, reporting, command-line entry point, or process execution in production B1 code.
- No Gradle task/lifecycle wiring, CI workflow wiring, npm workflow, JavaScript remediation, README work, or aggregate Java/JavaScript ordering.
- No complete ECMAScript parser, binding resolution, type inference, control-flow proof, automatic-semicolon-insertion engine, JSX, TypeScript, CommonJS, decorators, or import-attribute support.
- No syntax expansion beyond forms required by the approved design or demonstrated current corpus. Unsupported callable-looking syntax fails visibly.
- No change to application/runtime behavior or JavaScript source.

## Assumptions

- Java 25 sealed interfaces, records, pattern matching, `List.copyOf`, `Set.copyOf`, and `List.getFirst/getLast` are available.
- `JavaScriptLexResult.Success` already guarantees one terminal EOF, exact nonoverlapping token ranges, and no malformed lexical unit.
- The accepted inventory's 1,240 callable count includes all current class members, including the constructor inside the stable-bound `globalThis.MediaMetadata` class expression, and excludes class-value declarations themselves.
- The exact current documentable total is therefore `1,240 + 13 + 5 + 1 = 1,259`, not 1,254.
- Current documentable formal destructuring uses supported object patterns. Array formal patterns occur only in anonymous direct call-argument callbacks, whose callable declaration and formal model are exempt; a documentable callable with an array formal fails closed until an approved syntax expansion supplies fixtures and a reviewed contract.
- Static property identity consists of identifier/private-name, keyword-as-IdentifierName, string-literal, or numeric-literal segments. Computed segments are not stable identities in B1.
- Token adjacency is sufficient to distinguish attached JSDoc from whitespace, ordinary-comment barriers, semantic barriers, and an already claimed module/declaration JSDoc.
- The current branch remains isolated; the phase does not need to resolve its reported ahead/behind relationship with `origin/main`.

## Open Questions

None. The stable-bound anonymous class count and resulting 1,259-declaration total are resolved inputs, and the complete plan has passed its independent execution-readiness review.

## Files and Modules

Only the spoke's `documentation-validator` module changes. The implementation adds focused package-private Java types and tests under the existing package:

- Structural domain:
  - `JavaScriptDocumentationAttachment.java`
  - `JavaScriptDeclarationName.java`
  - `JavaScriptFormalParameter.java`
  - `JavaScriptCallableBodyFacts.java`
  - `JavaScriptDeclaration.java`
  - `JavaScriptStructuralError.java`
  - `JavaScriptStructuralResult.java`
  - `JavaScriptStructuralDomainTest.java`
- Structural support:
  - `JavaScriptTokenRange.java`
  - `JavaScriptDelimiterIndex.java`
  - `JavaScriptDocumentationResolver.java`
  - `JavaScriptFormalParameterParser.java`
  - `JavaScriptBodyFactsAnalyzer.java`
  - `JavaScriptStructuralSupportTest.java`
- Declaration recognition:
  - `JavaScriptStructuralRecognizer.java`
  - `JavaScriptDeclarationScanner.java`
  - `JavaScriptStructuralRecognizerTest.java`

No existing production source, test, Gradle, workflow, application JavaScript, or documentation file changes in the spoke are planned.

## Execution and Review Protocol

- Execute Tasks 1 through 3 sequentially through `superpowers:subagent-driven-development`; shared files and task dependencies prohibit concurrent implementation edits.
- For each task, dispatch one fresh implementation subagent with only that task's generated brief, phase boundaries, exact worktree, required skills, and report path. Record the task BASE first. The implementer performs RED/GREEN, self-review, stages only task-owned files, commits, and writes the complete report before returning.
- The controller personally inspects the report and BASE/HEAD, generates the SDD review package from that exact range, and dispatches one fresh task reviewer with the brief, report, package, and binding global constraints.
- The task reviewer must return both required verdicts: specification compliance and task quality. Its quality review covers correctness, invariants, error ownership, immutability, Javadocs including private helpers and enum constants, test quality, and repository style.
- Any failed specification verdict or Critical/Important quality finding enters the skill's bounded fix loop. The original implementer owns rounds 1-3, a fresh more-capable implementer owns rounds 4-5, every behavior correction begins with a failing regression fixture, every fix is committed, and every round receives a scoped re-review package.
- The controller independently runs the task's full listed verification after review approval, inspects the committed diff, and records exact BASE/HEAD, RED/GREEN, commit, review, fix-round, and completion evidence in the plan-specific SDD ledger before dispatching the next task. Implementer self-review never replaces the independent task reviewer.
- Task 4 uses a fresh most-capable whole-phase reviewer over the complete review package. Critical or Important findings receive the skill's single final fix dispatch and scoped re-review; residual load-bearing findings stop the phase.
- After a clean Task 4 review, remove only this plan's resolved SDD workspace and invoke `superpowers:finishing-a-development-branch`. The binding campaign constraint selects keeping the existing isolated branch/worktree for the separately planned B2 phase; no merge, rebase, push, pull request, or branch deletion is authorized by B1.

### TDD micro-cycle protocol

- The complete proposed test files below are accumulated end states, not instructions to paste a broad suite before production exists. Add one named behavior at a time, run the focused test command, and require a JUnit assertion failure with the expected message; compilation errors never count as RED.
- For the first new type of each task, use a temporary reflection bootstrap fixture that catches `ClassNotFoundException`/`ReflectiveOperationException` and returns a value asserted by JUnit. The absent or behaviorally incomplete boundary must therefore produce an assertion failure, not a test error. Add only the minimum production type/behavior needed to make that fixture pass. Once an equivalent strongly typed regression compiles, fails for the next missing behavior, and then passes, replace the reflection bootstrap with that stronger permanent test; preserve the bootstrap RED/GREEN output in the implementer report rather than retaining redundant reflection code in the final test file.
- Repeat RED → inspect expected assertion failure → minimum GREEN → inspect pristine pass → refactor while green for each subsequent behavior. When a strongly typed test would not compile until a new sibling type exists, bootstrap that sibling through the same reflection pattern before adding its strongly typed cases.
- The implementer report lists every micro-cycle's test name, failing assertion, production behavior added, and identical GREEN command. Type-level compiler failures may be retained as supplemental Jane-style evidence but never replace behavioral RED.

## Task Breakdown

### Task 1 - Add the immutable structural domain

Sequence / dependencies:

- Runs first against exact spoke head `affed13149c07ec5c024e20325a0333c2efd374f` after confirming a clean isolated worktree and unchanged authoritative-checkout status hash.
- Fixes the only result, identity, parameter, attachment, declaration, and error types later tasks may expose.
- The implementer commits independently as `Add JavaScript structural domain` after RED/GREEN, private-Javadoc, diff, and self-review; the generated commit range then enters the independent task-review gate.

Expected files or modules:

- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDocumentationAttachment.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclarationName.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptFormalParameter.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptCallableBodyFacts.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclaration.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralError.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralResult.java`.
- Create `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralDomainTest.java`.

Interfaces:

- Consumes: completed `JavaScriptToken` values only for exact anchors, JSDoc tokens, and barriers.
- Produces: `JavaScriptStructuralResult.Success(moduleDocumentation, declarations)` or `Failure(moduleDocumentation, declarations, error)`; sealed `JavaScriptDeclaration.Callable` and `ClassValue`; sealed declaration-name, parameter-pattern, and documentation-attachment cases.

Implementation notes:

- Required skill: `chris-street-style` before any code edits. Invoke it and `superpowers:test-driven-development` before creating the test or production files.
- Before-Edit Brief:
  - Behavior: callers can represent only complete source-positioned declaration data, exact documentation ownership, supported formal patterns, direct body facts, or one first structural failure.
  - Invariants: every collection is copied; declaration anchors are semantic non-EOF tokens; declaration order is strictly increasing; failure prefixes stop before their error; attachment variants carry only tokens of the promised role; parameter positions are one-based; property/binding names are nonblank; callable-only state cannot appear on a class value.
  - Boundary/API: every type remains package-private in `dev.christopherbell.tools.documentation`; Tasks 2 and 3 consume the exact signatures below, and no application module imports them.
  - Effects and failures: constructors perform no I/O or mutation beyond defensive copies; absent values fail with `NullPointerException`, contradictory domain states fail with `IllegalArgumentException`, and expected structural source failure is represented by `JavaScriptStructuralError` rather than thrown.
  - Tests and evidence: bootstrap each of the seven domain boundaries through an assertion-failing reflection fixture, then add the strongly typed valid/invalid behavior cases one at a time. Use the identical focused command for each RED/GREEN cycle and finish with every variant, invalid-state rejection, ordering rule, prefix bound, and collection immutability green.
- Keep the structural domain independent from `DocumentationRule`, `DocumentationViolation`, `RepositoryFile`, source text, and file paths.
- Use distinct name variants for a declared binding, bare assigned identifier, full static property path, source-named expression, and anonymous default export. Do not collapse them into one display string.
- Use nested enums/records inside `JavaScriptDeclaration` and `JavaScriptFormalParameter` where they are owned solely by that domain, reducing file count without weakening Javadocs.
- A `Blocked` attachment preserves the exact closest token that prevented direct attachment. `AlreadyClaimed` preserves the exact JSDoc already owned by the module or an earlier declaration.

#### Code Edit 1.1

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralDomainTest.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

/** Proves that JavaScript structural values cannot represent contradictory state. */
class JavaScriptStructuralDomainTest {
  /** Accepts every exact documentation-attachment ownership case. */
  @Test
  void representsExactDocumentationOwnership() {
    var javadoc = token(JavaScriptTokenKind.JAVADOC, "/** docs */", 0);
    var barrier = token(JavaScriptTokenKind.ORDINARY_COMMENT, "/* barrier */", 12);

    assertEquals(javadoc,
        new JavaScriptDocumentationAttachment.Attached(javadoc).javadoc());
    assertEquals(barrier,
        new JavaScriptDocumentationAttachment.Blocked(barrier).barrier());
    assertEquals(javadoc,
        new JavaScriptDocumentationAttachment.AlreadyClaimed(javadoc).javadoc());
    assertEquals(new JavaScriptDocumentationAttachment.Absent(),
        new JavaScriptDocumentationAttachment.Absent());
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDocumentationAttachment.Attached(barrier));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDocumentationAttachment.Blocked(javadoc));
  }

  /** Preserves distinct stable name categories and immutable property segments. */
  @Test
  void representsDeclarationNameCategories() {
    var segments = new ArrayList<>(List.of("globalThis", "MediaMetadata"));
    var path = new JavaScriptDeclarationName.PropertyPath(segments);
    segments.clear();

    assertEquals("binding", new JavaScriptDeclarationName.BoundIdentifier("binding").displayName());
    assertEquals("assigned", new JavaScriptDeclarationName.AssignedIdentifier("assigned").displayName());
    assertEquals("fetchRoot",
        new JavaScriptDeclarationName.SourceNamedExpression("fetchRoot").displayName());
    assertEquals("default export", new JavaScriptDeclarationName.DefaultExport().displayName());
    assertEquals(List.of("globalThis", "MediaMetadata"), path.segments());
    assertEquals("globalThis.MediaMetadata", path.displayName());
    assertThrows(UnsupportedOperationException.class, () -> path.segments().add("later"));
  }

  /** Preserves object-pattern property paths separately from their bound identifiers. */
  @Test
  void representsFormalPositionsAndObjectLeaves() {
    var leaf = new JavaScriptFormalParameter.ObjectBinding(
        List.of("request", "account", "id"), "accountId", false, true);
    var formal = new JavaScriptFormalParameter(
        2, new JavaScriptFormalParameter.ObjectPattern(List.of(leaf)), false, true);

    assertEquals(2, formal.position());
    assertEquals(List.of("request", "account", "id"), leaf.propertyPath());
    assertEquals("accountId", leaf.boundIdentifier());
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptFormalParameter(0,
            new JavaScriptFormalParameter.IdentifierPattern("value"), false, false));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptFormalParameter.ObjectPattern(List.of()));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptFormalParameter(
            1,
            new JavaScriptFormalParameter.ObjectPattern(List.of(
                new JavaScriptFormalParameter.ObjectBinding(
                    List.of("value"), "value", false, false))),
            true,
            false));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptFormalParameter.ObjectPattern(List.of(
            new JavaScriptFormalParameter.ObjectBinding(
                List.of("options", "remaining"), "remaining", true, false),
            new JavaScriptFormalParameter.ObjectBinding(
                List.of("options", "later"), "later", false, false))));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptFormalParameter.ObjectBinding(
            List.of("options", "sourceName"), "remaining", true, false));
    assertEquals(2, new JavaScriptFormalParameter.ObjectPattern(List.of(
        new JavaScriptFormalParameter.ObjectBinding(
            List.of("nested", "remaining"), "remaining", true, false),
        new JavaScriptFormalParameter.ObjectBinding(
            List.of("outer"), "outer", false, false))).bindings().size());
  }

  /** Copies callable collections and rejects callable-kind contradictions. */
  @Test
  void validatesCallableDeclarationState() {
    var anchor = token(JavaScriptTokenKind.KEYWORD, "function", 0);
    var parameters = new ArrayList<>(List.of(new JavaScriptFormalParameter(
        1, new JavaScriptFormalParameter.IdentifierPattern("value"), false, false)));
    var modifiers = new LinkedHashSet<>(Set.of(JavaScriptDeclaration.Modifier.ASYNC));
    var callable = new JavaScriptDeclaration.Callable(
        JavaScriptDeclaration.CallableKind.FUNCTION_DECLARATION,
        new JavaScriptDeclarationName.BoundIdentifier("load"),
        anchor,
        new JavaScriptDocumentationAttachment.Absent(),
        modifiers,
        parameters,
        new JavaScriptCallableBodyFacts(true, true, true));
    parameters.clear();
    modifiers.clear();

    assertEquals(1, callable.parameters().size());
    assertEquals(Set.of(JavaScriptDeclaration.Modifier.ASYNC), callable.modifiers());
    assertThrows(UnsupportedOperationException.class,
        () -> callable.parameters().add(new JavaScriptFormalParameter(
            2, new JavaScriptFormalParameter.IdentifierPattern("later"), false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.CONSTRUCTOR,
            new JavaScriptDeclarationName.PropertyPath(List.of("Type", "constructor")),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(JavaScriptDeclaration.Modifier.ASYNC),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptCallableBodyFacts(false, false, true));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.CONSTRUCTOR,
            new JavaScriptDeclarationName.PropertyPath(List.of("Type", "play")),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.CLASS_METHOD,
            new JavaScriptDeclarationName.PropertyPath(List.of("Type", "#play")),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.CLASS_METHOD,
            new JavaScriptDeclarationName.PropertyPath(List.of("Type", "#constructor")),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(JavaScriptDeclaration.Modifier.PRIVATE),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.CLASS_GETTER,
            new JavaScriptDeclarationName.PropertyPath(List.of("Type", "constructor")),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.CLASS_METHOD,
            new JavaScriptDeclarationName.PropertyPath(List.of("Type", "play")),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(JavaScriptDeclaration.Modifier.PRIVATE),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.CLASS_METHOD,
            new JavaScriptDeclarationName.PropertyPath(List.of("Type", "constructor")),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.ARROW_FUNCTION,
            new JavaScriptDeclarationName.SourceNamedExpression("impossibleArrow"),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(),
            List.of(),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.Callable(
            JavaScriptDeclaration.CallableKind.FUNCTION_DECLARATION,
            new JavaScriptDeclarationName.BoundIdentifier("misnumbered"),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(),
            List.of(new JavaScriptFormalParameter(
                2, new JavaScriptFormalParameter.IdentifierPattern("value"), false, false)),
            new JavaScriptCallableBodyFacts(false, false, false)));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptDeclaration.ClassValue(
            JavaScriptDeclaration.ClassKind.CLASS_EXPRESSION,
            new JavaScriptDeclarationName.BoundIdentifier("Value"),
            anchor,
            new JavaScriptDocumentationAttachment.Absent(),
            Set.of(JavaScriptDeclaration.Modifier.EXPORTED)));
  }

  /** Copies ordered declaration results and bounds a completed failed prefix by anchor. */
  @Test
  void validatesStructuralResultState() {
    var first = classValue("First", 0);
    var second = classValue("Second", 10);
    var declarations = new ArrayList<JavaScriptDeclaration>(List.of(first, second));
    var success = new JavaScriptStructuralResult.Success(
        new JavaScriptDocumentationAttachment.Absent(), declarations);
    declarations.clear();

    assertEquals(List.of(first, second), success.declarations());
    assertThrows(UnsupportedOperationException.class, () -> success.declarations().add(first));
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptStructuralResult.Success(
            new JavaScriptDocumentationAttachment.Absent(), List.of(second, first)));

    var errorToken = token(JavaScriptTokenKind.PUNCTUATOR, "[", 8);
    var error = new JavaScriptStructuralError(errorToken, "unsupported computed callable key");
    assertThrows(IllegalArgumentException.class,
        () -> new JavaScriptStructuralResult.Failure(
            new JavaScriptDocumentationAttachment.Absent(), List.of(second), error));
    assertEquals(List.of(first), new JavaScriptStructuralResult.Failure(
        new JavaScriptDocumentationAttachment.Absent(), List.of(first), error).declarations());
  }

  /**
   * Creates one class declaration fixture at an exact offset.
   *
   * @param name stable class name
   * @param offset zero-based anchor offset
   * @return immutable class-value fixture
   */
  private static JavaScriptDeclaration classValue(String name, int offset) {
    return new JavaScriptDeclaration.ClassValue(
        JavaScriptDeclaration.ClassKind.CLASS_DECLARATION,
        new JavaScriptDeclarationName.BoundIdentifier(name),
        token(JavaScriptTokenKind.KEYWORD, "class", offset),
        new JavaScriptDocumentationAttachment.Absent(),
        Set.of());
  }

  /**
   * Creates one exact-width token fixture.
   *
   * @param kind token lexical role
   * @param text exact source spelling
   * @param offset zero-based source offset
   * @return exact-position token fixture
   */
  private static JavaScriptToken token(
      JavaScriptTokenKind kind, String text, int offset) {
    return new JavaScriptToken(kind, text, 1, offset + 1, offset, offset + text.length());
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralDomainTest'
```

Expected first RED: the first reflection bootstrap test compiles and fails a JUnit assertion because its domain boundary is absent. Bootstrap and complete the seven domain types sequentially under the TDD micro-cycle protocol; missing-symbol compiler output is supplemental only and never accepted as RED.

#### Code Edit 1.2

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDocumentationAttachment.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.Objects;

/** Records why one module or declaration does or does not own directly preceding JSDoc. */
sealed interface JavaScriptDocumentationAttachment
    permits JavaScriptDocumentationAttachment.Absent,
        JavaScriptDocumentationAttachment.Attached,
        JavaScriptDocumentationAttachment.Blocked,
        JavaScriptDocumentationAttachment.AlreadyClaimed {
  /** Represents a source boundary with no preceding emitted token. */
  record Absent() implements JavaScriptDocumentationAttachment {}

  /**
   * Records one directly attached, newly claimed JSDoc token.
   *
   * @param javadoc exact JSDoc token owned by this module or declaration
   */
  record Attached(JavaScriptToken javadoc) implements JavaScriptDocumentationAttachment {
    /**
     * Requires an exact JSDoc token.
     *
     * @param javadoc exact JSDoc token
     * @throws NullPointerException when the token is absent
     * @throws IllegalArgumentException when the token is not JSDoc
     */
    public Attached {
      Objects.requireNonNull(javadoc);
      if (javadoc.kind() != JavaScriptTokenKind.JAVADOC) {
        throw new IllegalArgumentException("Attached documentation must be a JSDoc token");
      }
    }
  }

  /**
   * Records the exact ordinary-comment or semantic token that blocks direct attachment.
   *
   * @param barrier closest emitted token before the declaration head
   */
  record Blocked(JavaScriptToken barrier) implements JavaScriptDocumentationAttachment {
    /**
     * Rejects a token that represents attached or terminal state instead of a barrier.
     *
     * @param barrier closest emitted blocking token
     * @throws NullPointerException when the token is absent
     * @throws IllegalArgumentException when the token is JSDoc or EOF
     */
    public Blocked {
      Objects.requireNonNull(barrier);
      if (barrier.kind() == JavaScriptTokenKind.JAVADOC
          || barrier.kind() == JavaScriptTokenKind.EOF) {
        throw new IllegalArgumentException("Documentation barrier must be ordinary or semantic");
      }
    }
  }

  /**
   * Records a directly preceding JSDoc already owned by an earlier eligible target.
   *
   * @param javadoc exact previously claimed JSDoc token
   */
  record AlreadyClaimed(JavaScriptToken javadoc) implements JavaScriptDocumentationAttachment {
    /**
     * Requires an exact JSDoc token.
     *
     * @param javadoc exact previously claimed JSDoc token
     * @throws NullPointerException when the token is absent
     * @throws IllegalArgumentException when the token is not JSDoc
     */
    public AlreadyClaimed {
      Objects.requireNonNull(javadoc);
      if (javadoc.kind() != JavaScriptTokenKind.JAVADOC) {
        throw new IllegalArgumentException("Claimed documentation must be a JSDoc token");
      }
    }
  }
}
```

Verification:

- Domain tests distinguish attached, blocked, already-claimed, and absent cases and reject token-kind contradictions.

#### Code Edit 1.3

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclarationName.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Objects;

/** Preserves the source category and stable display identity of one declaration. */
sealed interface JavaScriptDeclarationName
    permits JavaScriptDeclarationName.BoundIdentifier,
        JavaScriptDeclarationName.AssignedIdentifier,
        JavaScriptDeclarationName.PropertyPath,
        JavaScriptDeclarationName.SourceNamedExpression,
        JavaScriptDeclarationName.DefaultExport {
  /**
   * Returns the stable human-readable identity without erasing its source category.
   *
   * @return stable display identity
   */
  String displayName();

  /**
   * Represents an identifier introduced by a declaration or lexical binding.
   *
   * @param identifier exact declared or bound identifier
   */
  record BoundIdentifier(String identifier) implements JavaScriptDeclarationName {
    /**
     * Validates the nonblank bound identifier.
     *
     * @param identifier exact declared or bound identifier
     * @throws NullPointerException when the identifier is absent
     * @throws IllegalArgumentException when the identifier is blank
     */
    public BoundIdentifier { identifier = requireName(identifier); }
    /**
     * Returns the bound identifier.
     *
     * @return exact bound identifier
     */
    @Override public String displayName() { return identifier; }
  }

  /**
   * Represents an existing bare identifier used as an assignment target.
   *
   * @param identifier exact assigned identifier
   */
  record AssignedIdentifier(String identifier) implements JavaScriptDeclarationName {
    /**
     * Validates the nonblank assigned identifier.
     *
     * @param identifier exact assigned identifier
     * @throws NullPointerException when the identifier is absent
     * @throws IllegalArgumentException when the identifier is blank
     */
    public AssignedIdentifier { identifier = requireName(identifier); }
    /**
     * Returns the assigned identifier.
     *
     * @return exact assigned identifier
     */
    @Override public String displayName() { return identifier; }
  }

  /**
   * Represents a static member, class-member, or named object-property path.
   *
   * @param segments nonempty static source path segments
   */
  record PropertyPath(List<String> segments) implements JavaScriptDeclarationName {
    /**
     * Copies and validates every static path segment.
     *
     * @param segments nonempty static source path segments
     * @throws NullPointerException when the list or a segment is absent
     * @throws IllegalArgumentException when the path is empty or a segment is blank
     */
    public PropertyPath {
      segments = List.copyOf(segments);
      if (segments.isEmpty()) {
        throw new IllegalArgumentException("Property path must contain at least one segment");
      }
      segments.forEach(JavaScriptDeclarationName::requireName);
    }
    /**
     * Returns the dot-separated source property path.
     *
     * @return dot-separated source path
     */
    @Override public String displayName() { return String.join(".", segments); }
  }

  /**
   * Represents a function/class expression whose own source name provides its identity.
   *
   * @param identifier exact expression name
   */
  record SourceNamedExpression(String identifier) implements JavaScriptDeclarationName {
    /**
     * Validates the nonblank source name.
     *
     * @param identifier exact expression name
     * @throws NullPointerException when the identifier is absent
     * @throws IllegalArgumentException when the identifier is blank
     */
    public SourceNamedExpression { identifier = requireName(identifier); }
    /**
     * Returns the source expression name.
     *
     * @return exact source expression name
     */
    @Override public String displayName() { return identifier; }
  }

  /** Represents an anonymous default export with an approved stable module identity. */
  record DefaultExport() implements JavaScriptDeclarationName {
    /**
     * Returns the approved default-export identity.
     *
     * @return stable default-export display identity
     */
    @Override public String displayName() { return "default export"; }
  }

  /**
   * Validates one lexer-proved static name spelling.
   *
   * @param name lexer-proved source name
   * @return the validated name
   * @throws NullPointerException when the name is absent
   * @throws IllegalArgumentException when the name is blank
   */
  private static String requireName(String name) {
    Objects.requireNonNull(name);
    if (name.isBlank()) {
      throw new IllegalArgumentException("JavaScript declaration name must not be blank");
    }
    return name;
  }
}
```

Verification:

- Domain tests prove that property paths remain immutable and never collapse into bound identifiers.

#### Code Edit 1.4

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptFormalParameter.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Objects;

/**
 * Preserves one source-order callable formal without inventing a destructuring name.
 *
 * @param position one-based formal position
 * @param pattern identifier or object-pattern structure
 * @param rest whether the formal has the outer rest wrapper
 * @param defaulted whether the formal has an outer default value
 */
record JavaScriptFormalParameter(
    int position, Pattern pattern, boolean rest, boolean defaulted) {
  /**
   * Validates the formal position and pattern.
   *
   * @param position one-based formal position
   * @param pattern identifier or object-pattern structure
   * @param rest whether the formal has the outer rest wrapper
   * @param defaulted whether the formal has an outer default value
   * @throws NullPointerException when the pattern is absent
   * @throws IllegalArgumentException when position or wrapper state is contradictory
   */
  JavaScriptFormalParameter {
    Objects.requireNonNull(pattern);
    if (position < 1) {
      throw new IllegalArgumentException("Formal parameter position must be positive");
    }
    if (rest && defaulted) {
      throw new IllegalArgumentException("A rest formal cannot have a default value");
    }
    if (rest && !(pattern instanceof IdentifierPattern)) {
      throw new IllegalArgumentException("An outer rest formal requires an identifier binding");
    }
  }

  /** Identifies the supported immutable formal-pattern cases. */
  sealed interface Pattern permits IdentifierPattern, ObjectPattern {}

  /**
   * Represents one ordinary bound identifier.
   *
   * @param boundIdentifier exact source binding
   */
  record IdentifierPattern(String boundIdentifier) implements Pattern {
    /**
     * Rejects an absent or blank identifier.
     *
     * @param boundIdentifier exact source binding
     * @throws NullPointerException when the identifier is absent
     * @throws IllegalArgumentException when the identifier is blank
     */
    public IdentifierPattern {
      Objects.requireNonNull(boundIdentifier);
      if (boundIdentifier.isBlank()) {
        throw new IllegalArgumentException("Formal binding must not be blank");
      }
    }
  }

  /**
   * Represents one object-destructured formal through its source-order leaf bindings.
   *
   * @param bindings nonempty immutable leaf bindings
   */
  record ObjectPattern(List<ObjectBinding> bindings) implements Pattern {
    /**
     * Copies and validates a nonempty source-order leaf list.
     *
     * @param bindings nonempty source-order leaf bindings
     * @throws NullPointerException when the list or a binding is absent
     * @throws IllegalArgumentException when the list is empty or object rest is non-final
     */
    public ObjectPattern {
      bindings = List.copyOf(bindings);
      if (bindings.isEmpty()) {
        throw new IllegalArgumentException("Object formal must expose at least one leaf binding");
      }
      for (var index = 0; index < bindings.size(); index++) {
        var binding = bindings.get(index);
        if (!binding.rest()) {
          continue;
        }
        var ownerPath = binding.propertyPath().subList(0, binding.propertyPath().size() - 1);
        for (var laterIndex = index + 1; laterIndex < bindings.size(); laterIndex++) {
          if (startsWith(bindings.get(laterIndex).propertyPath(), ownerPath)) {
            throw new IllegalArgumentException("Object rest binding must be final in its owner");
          }
        }
      }
    }

    /**
     * Reports whether one property path begins with an exact owner-path prefix.
     *
     * @param propertyPath complete property path
     * @param ownerPath candidate owner prefix
     * @return whether every owner segment begins the property path
     */
    private static boolean startsWith(List<String> propertyPath, List<String> ownerPath) {
      return propertyPath.size() >= ownerPath.size()
          && propertyPath.subList(0, ownerPath.size()).equals(ownerPath);
    }
  }

  /**
   * Preserves one object-pattern property path and its distinct local binding.
   *
   * @param propertyPath nonempty static source property path
   * @param boundIdentifier local leaf binding
   * @param rest whether this is an object rest leaf
   * @param defaulted whether this leaf has a default value
   */
  record ObjectBinding(
      List<String> propertyPath, String boundIdentifier, boolean rest, boolean defaulted) {
    /**
     * Copies and validates one object-pattern leaf.
     *
     * @param propertyPath nonempty static source property path
     * @param boundIdentifier local leaf binding
     * @param rest whether this is an object rest leaf
     * @param defaulted whether this leaf has a default value
     * @throws NullPointerException when a path, segment, or binding is absent
     * @throws IllegalArgumentException when names or rest/default state are contradictory
     */
    public ObjectBinding {
      propertyPath = List.copyOf(propertyPath);
      Objects.requireNonNull(boundIdentifier);
      if (propertyPath.isEmpty() || propertyPath.stream().anyMatch(String::isBlank)) {
        throw new IllegalArgumentException("Object binding property path must be nonblank");
      }
      if (boundIdentifier.isBlank()) {
        throw new IllegalArgumentException("Object binding identifier must not be blank");
      }
      if (rest && defaulted) {
        throw new IllegalArgumentException("An object rest binding cannot have a default value");
      }
      if (rest && !propertyPath.getLast().equals(boundIdentifier)) {
        throw new IllegalArgumentException(
            "Object rest path must end with its bound identifier");
      }
    }
  }
}
```

Verification:

- Domain tests prove one-based positions, immutable paths/leaves, distinct property and local names, identifier-only outer rest, object-rest owner/finality, and rest/default contradictions.

#### Code Edit 1.5

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptCallableBodyFacts.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

/**
 * Records syntax facts owned directly by one callable body.
 *
 * @param hasDirectValueReturn whether a concise arrow or direct non-bare return yields a value
 * @param hasDirectThrow whether a throw statement occurs outside every nested callable/class body
 * @param hasCallerVisibleThrow whether such a throw can escape same-callable caught try regions
 */
record JavaScriptCallableBodyFacts(
    boolean hasDirectValueReturn,
    boolean hasDirectThrow,
    boolean hasCallerVisibleThrow) {
  /**
   * Rejects caller-visible state without a direct throw owned by this callable.
   *
   * @param hasDirectValueReturn whether the callable directly returns a value
   * @param hasDirectThrow whether the callable owns a direct throw
   * @param hasCallerVisibleThrow whether a direct throw can escape to its caller
   * @throws IllegalArgumentException when caller-visible state lacks a direct throw
   */
  JavaScriptCallableBodyFacts {
    if (hasCallerVisibleThrow && !hasDirectThrow) {
      throw new IllegalArgumentException("A caller-visible throw must be a direct throw");
    }
  }
}
```

Verification:

- Domain construction is trivial; Task 2 behavior tests prove the ownership semantics.

#### Code Edit 1.6

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclaration.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Objects;
import java.util.Set;

/** Represents one immutable documentable JavaScript callable or stable class value. */
sealed interface JavaScriptDeclaration
    permits JavaScriptDeclaration.Callable, JavaScriptDeclaration.ClassValue {
  /**
   * Returns the stable source-category-aware declaration identity.
   *
   * @return immutable stable declaration identity
   */
  JavaScriptDeclarationName name();
  /**
   * Returns the semantic token that anchors the declaration head.
   *
   * @return exact declaration-head anchor token
   */
  JavaScriptToken anchor();
  /**
   * Returns exact preceding documentation ownership.
   *
   * @return immutable attachment state
   */
  JavaScriptDocumentationAttachment documentation();

  /** Distinguishes callable grammar forms with different structural contracts. */
  enum CallableKind {
    /** Named function declaration at module or nested scope. */ FUNCTION_DECLARATION,
    /** Function expression with a stable target or source name. */ FUNCTION_EXPRESSION,
    /** Arrow expression with a stable target. */ ARROW_FUNCTION,
    /** Constructor declared inside a class body. */ CONSTRUCTOR,
    /** Ordinary named class method. */ CLASS_METHOD,
    /** Class getter accessor. */ CLASS_GETTER,
    /** Class setter accessor. */ CLASS_SETTER,
    /** Object-literal shorthand method. */ OBJECT_METHOD,
    /** Object-literal getter accessor. */ OBJECT_GETTER,
    /** Object-literal setter accessor. */ OBJECT_SETTER
  }

  /** Distinguishes statement/binding class declarations from class expressions. */
  enum ClassKind {
    /** Named or approved anonymous default class declaration. */ CLASS_DECLARATION,
    /** Stable-target or source-named class expression. */ CLASS_EXPRESSION
  }

  /** Preserves declaration modifiers needed by B2 and diagnostics. */
  enum Modifier {
    /** Callable is declared async. */ ASYNC,
    /** Callable is a generator. */ GENERATOR,
    /** Class member is static. */ STATIC,
    /** Declaration is exported. */ EXPORTED,
    /** Declaration is the module default export. */ DEFAULT_EXPORTED,
    /** Static property/member name is private. */ PRIVATE
  }

  /**
   * Represents one callable declaration and its B2-relevant syntax facts.
   *
   * @param kind callable grammar form
   * @param name stable declaration identity
   * @param anchor declaration-head token
   * @param documentation exact attachment state
   * @param modifiers immutable modifier set
   * @param parameters immutable source-order formals
   * @param bodyFacts direct return/throw and caller-visible-throw facts
   */
  record Callable(
      CallableKind kind,
      JavaScriptDeclarationName name,
      JavaScriptToken anchor,
      JavaScriptDocumentationAttachment documentation,
      Set<Modifier> modifiers,
      List<JavaScriptFormalParameter> parameters,
      JavaScriptCallableBodyFacts bodyFacts) implements JavaScriptDeclaration {
    /**
     * Copies and validates complete callable state.
     *
     * @param kind callable grammar form
     * @param name stable declaration identity
     * @param anchor declaration-head token
     * @param documentation exact attachment state
     * @param modifiers callable modifier set
     * @param parameters source-order formals
     * @param bodyFacts direct callable-body facts
     * @throws NullPointerException when required state or a collection element is absent
     * @throws IllegalArgumentException when identity, modifiers, formals, or kind conflict
     */
    public Callable {
      Objects.requireNonNull(kind);
      Objects.requireNonNull(name);
      requireAnchor(anchor);
      Objects.requireNonNull(documentation);
      modifiers = Set.copyOf(modifiers);
      parameters = List.copyOf(parameters);
      Objects.requireNonNull(bodyFacts);
      validateCallableIdentityAndModifiers(kind, name, modifiers);
      validateParameterSequence(parameters);
      if (kind == CallableKind.CLASS_GETTER || kind == CallableKind.OBJECT_GETTER) {
        if (!parameters.isEmpty()) {
          throw new IllegalArgumentException("Getter cannot declare formal parameters");
        }
      }
      if ((kind == CallableKind.CLASS_SETTER || kind == CallableKind.OBJECT_SETTER)
          && parameters.size() != 1) {
        throw new IllegalArgumentException("Setter must declare exactly one formal parameter");
      }
      if ((kind == CallableKind.CLASS_SETTER || kind == CallableKind.OBJECT_SETTER)
          && parameters.getFirst().rest()) {
        throw new IllegalArgumentException("Setter parameter cannot be rest");
      }
    }
  }

  /**
   * Represents one documentable class declaration or stable class expression value.
   *
   * @param kind declaration or expression form
   * @param name stable declaration identity
   * @param anchor class/declaration-head token
   * @param documentation exact attachment state
   * @param modifiers immutable modifier set
   */
  record ClassValue(
      ClassKind kind,
      JavaScriptDeclarationName name,
      JavaScriptToken anchor,
      JavaScriptDocumentationAttachment documentation,
      Set<Modifier> modifiers) implements JavaScriptDeclaration {
    /**
     * Copies and validates complete class-value state.
     *
     * @param kind declaration or expression form
     * @param name stable declaration identity
     * @param anchor class/declaration-head token
     * @param documentation exact attachment state
     * @param modifiers class-value modifier set
     * @throws NullPointerException when required state or a modifier is absent
     * @throws IllegalArgumentException when identity, modifiers, or kind conflict
     */
    public ClassValue {
      Objects.requireNonNull(kind);
      Objects.requireNonNull(name);
      requireAnchor(anchor);
      Objects.requireNonNull(documentation);
      modifiers = Set.copyOf(modifiers);
      validateClassIdentityAndModifiers(kind, name, modifiers);
    }
  }

  /**
   * Validates source identity and the exact modifier subset allowed by one callable kind.
   *
   * @param kind callable grammar form
   * @param name stable declaration identity
   * @param modifiers immutable modifier set
   * @throws IllegalArgumentException when the identity or modifiers contradict the kind
   */
  private static void validateCallableIdentityAndModifiers(
      CallableKind kind, JavaScriptDeclarationName name, Set<Modifier> modifiers) {
    var allowed = switch (kind) {
      case FUNCTION_DECLARATION ->
          Set.of(Modifier.ASYNC, Modifier.GENERATOR, Modifier.EXPORTED,
              Modifier.DEFAULT_EXPORTED);
      case FUNCTION_EXPRESSION -> Set.of(Modifier.ASYNC, Modifier.GENERATOR);
      case ARROW_FUNCTION -> Set.of(Modifier.ASYNC);
      case CONSTRUCTOR -> Set.<Modifier>of();
      case CLASS_METHOD ->
          Set.of(Modifier.ASYNC, Modifier.GENERATOR, Modifier.STATIC, Modifier.PRIVATE);
      case CLASS_GETTER, CLASS_SETTER -> Set.of(Modifier.STATIC, Modifier.PRIVATE);
      case OBJECT_METHOD -> Set.of(Modifier.ASYNC, Modifier.GENERATOR);
      case OBJECT_GETTER, OBJECT_SETTER -> Set.<Modifier>of();
    };
    if (!allowed.containsAll(modifiers)) {
      throw new IllegalArgumentException("Callable kind has unsupported modifiers");
    }
    validateExportModifiers(modifiers);
    var member = switch (kind) {
      case CONSTRUCTOR, CLASS_METHOD, CLASS_GETTER, CLASS_SETTER,
          OBJECT_METHOD, OBJECT_GETTER, OBJECT_SETTER -> true;
      default -> false;
    };
    if (member && !(name instanceof JavaScriptDeclarationName.PropertyPath)) {
      throw new IllegalArgumentException("Callable identity does not match its grammar kind");
    }
    if (member) {
      validateMemberIdentity(
          kind, (JavaScriptDeclarationName.PropertyPath) name, modifiers);
    }
    if (kind == CallableKind.FUNCTION_DECLARATION
        && !(name instanceof JavaScriptDeclarationName.BoundIdentifier)
        && !(name instanceof JavaScriptDeclarationName.DefaultExport)) {
      throw new IllegalArgumentException("Function declaration requires a declared identity");
    }
    if (kind == CallableKind.ARROW_FUNCTION
        && !(name instanceof JavaScriptDeclarationName.BoundIdentifier)
        && !(name instanceof JavaScriptDeclarationName.AssignedIdentifier)
        && !(name instanceof JavaScriptDeclarationName.PropertyPath)) {
      throw new IllegalArgumentException("Arrow requires a stable target identity");
    }
    if (kind == CallableKind.FUNCTION_EXPRESSION
        && !(name instanceof JavaScriptDeclarationName.BoundIdentifier)
        && !(name instanceof JavaScriptDeclarationName.AssignedIdentifier)
        && !(name instanceof JavaScriptDeclarationName.PropertyPath)
        && !(name instanceof JavaScriptDeclarationName.SourceNamedExpression)) {
      throw new IllegalArgumentException("Function expression requires target or source identity");
    }
    if (name instanceof JavaScriptDeclarationName.DefaultExport
        && !modifiers.contains(Modifier.DEFAULT_EXPORTED)) {
      throw new IllegalArgumentException("Default-export identity requires its modifier");
    }
  }

  /**
   * Ties constructor and private-member syntax to the terminal property-path segment.
   *
   * @param kind class/object member grammar kind
   * @param name exact member property path
   * @param modifiers immutable member modifier set
   * @throws IllegalArgumentException when constructor or private identity is contradictory
   */
  private static void validateMemberIdentity(
      CallableKind kind,
      JavaScriptDeclarationName.PropertyPath name,
      Set<Modifier> modifiers) {
    var terminal = name.segments().getLast();
    var classMember = switch (kind) {
      case CONSTRUCTOR, CLASS_METHOD, CLASS_GETTER, CLASS_SETTER -> true;
      default -> false;
    };
    if (kind == CallableKind.CONSTRUCTOR && !terminal.equals("constructor")) {
      throw new IllegalArgumentException("Constructor identity must end with constructor");
    }
    if (classMember && kind != CallableKind.CONSTRUCTOR && terminal.equals("constructor")
        && !modifiers.contains(Modifier.STATIC)) {
      throw new IllegalArgumentException("Non-static constructor name requires constructor kind");
    }
    if (classMember && terminal.equals("#constructor")) {
      throw new IllegalArgumentException("Private member cannot be named #constructor");
    }
    var privateName = terminal.startsWith("#");
    if (classMember && kind != CallableKind.CONSTRUCTOR
        && privateName != modifiers.contains(Modifier.PRIVATE)) {
      throw new IllegalArgumentException("Private modifier must match the class member name");
    }
    if (!classMember && privateName) {
      throw new IllegalArgumentException("Object member cannot use a private name");
    }
  }

  /**
   * Requires contiguous one-based positions and a final-only outer rest formal.
   *
   * @param parameters immutable source-order formal list
   * @throws IllegalArgumentException when positions or rest placement are contradictory
   */
  private static void validateParameterSequence(List<JavaScriptFormalParameter> parameters) {
    for (var index = 0; index < parameters.size(); index++) {
      var parameter = parameters.get(index);
      if (parameter.position() != index + 1) {
        throw new IllegalArgumentException("Callable formal positions must be contiguous");
      }
      if (parameter.rest() && index != parameters.size() - 1) {
        throw new IllegalArgumentException("Rest formal must be final");
      }
    }
  }

  /**
   * Validates source identity and modifiers for a declaration or class expression.
   *
   * @param kind declaration or expression form
   * @param name stable class identity
   * @param modifiers immutable modifier set
   * @throws IllegalArgumentException when identity or modifiers contradict the kind
   */
  private static void validateClassIdentityAndModifiers(
      ClassKind kind, JavaScriptDeclarationName name, Set<Modifier> modifiers) {
    var allowed = kind == ClassKind.CLASS_DECLARATION
        ? Set.of(Modifier.EXPORTED, Modifier.DEFAULT_EXPORTED)
        : Set.<Modifier>of();
    if (!allowed.containsAll(modifiers)) {
      throw new IllegalArgumentException("Class kind has unsupported modifiers");
    }
    validateExportModifiers(modifiers);
    if (kind == ClassKind.CLASS_DECLARATION
        && !(name instanceof JavaScriptDeclarationName.BoundIdentifier)
        && !(name instanceof JavaScriptDeclarationName.DefaultExport)) {
      throw new IllegalArgumentException("Class declaration requires a declared identity");
    }
    if (kind == ClassKind.CLASS_EXPRESSION
        && !(name instanceof JavaScriptDeclarationName.BoundIdentifier)
        && !(name instanceof JavaScriptDeclarationName.AssignedIdentifier)
        && !(name instanceof JavaScriptDeclarationName.PropertyPath)
        && !(name instanceof JavaScriptDeclarationName.SourceNamedExpression)) {
      throw new IllegalArgumentException("Class expression requires target or source identity");
    }
    if (name instanceof JavaScriptDeclarationName.DefaultExport
        && !modifiers.contains(Modifier.DEFAULT_EXPORTED)) {
      throw new IllegalArgumentException("Default-export identity requires its modifier");
    }
  }

  /**
   * Requires every default-export modifier to carry the ordinary exported modifier too.
   *
   * @param modifiers immutable declaration modifier set
   * @throws IllegalArgumentException when default export lacks ordinary export
   */
  private static void validateExportModifiers(Set<Modifier> modifiers) {
    if (modifiers.contains(Modifier.DEFAULT_EXPORTED)
        && !modifiers.contains(Modifier.EXPORTED)) {
      throw new IllegalArgumentException("Default export must also be exported");
    }
  }

  /**
   * Rejects comment and terminal tokens as declaration anchors.
   *
   * @param anchor candidate semantic declaration anchor
   * @throws NullPointerException when the anchor is absent
   * @throws IllegalArgumentException when the anchor is a comment or EOF token
   */
  private static void requireAnchor(JavaScriptToken anchor) {
    Objects.requireNonNull(anchor);
    if (anchor.kind() == JavaScriptTokenKind.ORDINARY_COMMENT
        || anchor.kind() == JavaScriptTokenKind.JAVADOC
        || anchor.kind() == JavaScriptTokenKind.EOF) {
      throw new IllegalArgumentException("Declaration anchor must be semantic");
    }
  }
}
```

Verification:

- Domain tests prove defensive copies, exact grammar-kind/name/modifier compatibility, export/default-export consistency, and constructor/getter/setter formal invariants.

#### Code Edit 1.7

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralError.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.Objects;

/**
 * Identifies the first token where structural recognition cannot continue safely.
 *
 * @param token exact source-positioned token
 * @param message nonblank actionable explanation
 */
record JavaScriptStructuralError(JavaScriptToken token, String message) {
  /**
   * Rejects incomplete structural error identity.
   *
   * @param token exact source-positioned token
   * @param message nonblank actionable explanation
   * @throws NullPointerException when token or message is absent
   * @throws IllegalArgumentException when the message is blank
   */
  JavaScriptStructuralError {
    Objects.requireNonNull(token);
    Objects.requireNonNull(message);
    if (message.isBlank()) {
      throw new IllegalArgumentException("Structural error message must not be blank");
    }
  }
}
```

Verification:

- Domain tests reject absent/blank error state and use the token's exact line/column/offset.

#### Code Edit 1.8

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralResult.java`
- Lines: 1
- Action: add

Current:

```text
Absent at spoke head affed13149c07ec5c024e20325a0333c2efd374f.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Objects;

/** Represents either complete JavaScript structure or the first fail-closed structural error. */
sealed interface JavaScriptStructuralResult
    permits JavaScriptStructuralResult.Success, JavaScriptStructuralResult.Failure {
  /**
   * Returns the module-purpose documentation attachment fact.
   *
   * @return exact module attachment state
   */
  JavaScriptDocumentationAttachment moduleDocumentation();
  /**
   * Returns immutable source-ordered declarations or a diagnostic prefix.
   *
   * @return complete declarations or fully recognized diagnostic prefix
   */
  List<JavaScriptDeclaration> declarations();

  /**
   * Represents a complete structural scan.
   *
   * @param moduleDocumentation exact module attachment state
   * @param declarations complete source-ordered declarations
   */
  record Success(
      JavaScriptDocumentationAttachment moduleDocumentation,
      List<JavaScriptDeclaration> declarations) implements JavaScriptStructuralResult {
    /**
     * Copies and validates a complete structural result.
     *
     * @param moduleDocumentation exact module attachment state
     * @param declarations complete source-ordered declarations
     * @throws NullPointerException when required state or a declaration is absent
     * @throws IllegalArgumentException when declarations are not strictly source ordered
     */
    public Success {
      Objects.requireNonNull(moduleDocumentation);
      declarations = List.copyOf(declarations);
      validateOrdering(declarations);
    }
  }

  /**
   * Represents a declaration prefix and first structural error.
   *
   * @param moduleDocumentation exact module attachment state
   * @param declarations fully recognized source-ordered declarations anchored before the error
   * @param error first structural failure
   */
  record Failure(
      JavaScriptDocumentationAttachment moduleDocumentation,
      List<JavaScriptDeclaration> declarations,
      JavaScriptStructuralError error) implements JavaScriptStructuralResult {
    /**
     * Copies and validates a failed structural result.
     *
     * @param moduleDocumentation exact module attachment state
     * @param declarations fully recognized source-ordered declarations anchored before the error
     * @param error first structural failure
     * @throws NullPointerException when required state or a declaration is absent
     * @throws IllegalArgumentException when ordering or prefix bounds are invalid
     */
    public Failure {
      Objects.requireNonNull(moduleDocumentation);
      declarations = List.copyOf(declarations);
      Objects.requireNonNull(error);
      validateOrdering(declarations);
      if (declarations.stream().anyMatch(declaration ->
          declaration.anchor().startOffset() >= error.token().startOffset())) {
        throw new IllegalArgumentException("Structural prefix reaches or passes its first error");
      }
    }
  }

  /**
   * Validates strictly increasing declaration anchor offsets.
   *
   * @param declarations immutable declarations to validate
   * @throws IllegalArgumentException when anchors are not strictly increasing
   */
  private static void validateOrdering(List<JavaScriptDeclaration> declarations) {
    for (var index = 1; index < declarations.size(); index++) {
      if (declarations.get(index - 1).anchor().startOffset()
          >= declarations.get(index).anchor().startOffset()) {
        throw new IllegalArgumentException("Declarations must be strictly source ordered");
      }
    }
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralDomainTest'
git diff --check
```

Expected GREEN: every domain fixture passes, lists/sets are immutable, invalid state is rejected at construction, and no existing test changes. The implementer self-reviews, stages only the eight Task 1 files, and commits before the controller generates the Task 1 review package:

```powershell
git add -- documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDocumentationAttachment.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclarationName.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptFormalParameter.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptCallableBodyFacts.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclaration.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralError.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralResult.java documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralDomainTest.java
git commit -m "Add JavaScript structural domain"
```

### Task 2 - Add delimiter, attachment, formal, and direct-body support

Sequence / dependencies:

- Runs only after Task 1 is committed and independently approved.
- Supplies four narrow responsibilities to Task 3; Task 3 must not duplicate delimiter matching, JSDoc claiming, formal parsing, or direct-body analysis.
- The implementer commits independently as `Add JavaScript structural parsing support` after RED/GREEN and self-review; the generated commit range then enters the independent task-review gate.

Expected files or modules:

- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptTokenRange.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDelimiterIndex.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDocumentationResolver.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptFormalParameterParser.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptBodyFactsAnalyzer.java`.
- Create `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralSupportTest.java`.

Interfaces:

- Consumes: `List<JavaScriptToken>` from one `JavaScriptLexResult.Success` and immutable token-index ranges.
- Produces:
  - `JavaScriptDelimiterIndex.BuildResult` with matched `()`, `[]`, `{}`, and template-expression boundaries or one structural error.
  - stateful single-scan `JavaScriptDocumentationResolver.resolveModule()` / `resolveBefore(int)` attachment ownership.
  - `JavaScriptFormalParameterParser.ParseResult` with immutable formals or one structural error.
  - `JavaScriptBodyFactsAnalyzer.analyzeBlock(...)` / `analyzeConciseArrow(...)` facts.

Implementation notes:

- Required skill: `chris-street-style` before any code edits. Invoke it and `superpowers:test-driven-development` before creating the test or production files.
- Before-Edit Brief:
  - Behavior: a successful lexical stream gains exact delimiter partners, one-use JSDoc ownership, supported formal structure, and direct body facts without declaration policy or source rereads.
  - Invariants: every index/range is within the immutable token list; delimiter pairs are symmetric and type-correct; the first unmatched/mismatched boundary wins; one JSDoc index is claimed once; object leaves retain property path and local binding; nested callable/class ranges never contribute return/throw facts to an owner.
  - Boundary/API: all helpers remain package-private and accept only token lists/ranges; Task 3 owns traversal and supplies declaration heads and nested-body ranges.
  - Effects and failures: helpers perform no I/O; delimiter/formal source failures return typed error variants; attachment claiming is mutable only inside one resolver instance owned by one scan; invalid trusted indices throw `IllegalArgumentException`/`IllegalStateException` as programmer errors.
  - Tests and evidence: bootstrap delimiter, token-range, attachment, formal, and body-fact boundaries sequentially through assertion-failing reflection fixtures, then add one strongly typed behavioral fixture at a time. Prove every delimiter partition, attachment ownership state, formal wrapper/pattern case, unsupported computed/array pattern, and direct-body ownership boundary with the identical focused command.
- `JavaScriptTokenRange` uses `startInclusive` and `endExclusive` token indices, permits zero-width ranges for empty function/class/object interiors, and rejects only negative or reversed bounds.
- Delimiter indexing treats lexer-owned `TEMPLATE_EXPRESSION_START`/`TEMPLATE_EXPRESSION_END` as a distinct matching pair and never conflates them with ordinary braces.
- Documentation resolution uses the earliest declaration-head token (`export`, `async`, `function`, `class`, binding keyword, assignment target, class modifier/accessor/name, or object key). It examines the immediately preceding emitted token because whitespace is not emitted.
- `resolveModule()` claims token zero only when it is JSDoc. If token zero is ordinary/semantic it returns `Blocked`; if token zero is EOF it returns `Absent`. `resolveBefore` returns `AlreadyClaimed` when the same immediate JSDoc already belongs to the module or an earlier declaration.
- Formal parsing supports:
  - zero parameters;
  - identifier and contextual-IdentifierName bindings accepted by the lexer;
  - outer defaults with a delimiter-aware expression skip;
  - final outer `...identifier` rest;
  - object patterns with shorthand, alias, nested static property paths, leaf defaults, and final object rest;
  - commas only at the owning formal/object depth.
- Formal parsing fails at the first `[` for an array formal, at a computed object key, at an object method, at a missing binding, at a non-final rest, or at a rest/default combination. These are unsupported structural errors, not partial parameters.
- Body analysis accepts already proved body ranges. A block scan counts `return` with a following same-statement value and every direct `throw` through nested control/object blocks, skips the outermost nonoverlapping nested callable/class body ranges owned relative to that callable, and stops a `return` at `;`, `}`, EOF, or a line terminator inferred from the next token's line. It also proves which direct throws are caller-visible by indexing same-callable caught `try` body interiors; caught throws are not caller-visible, while catch/finally throws and rethrows remain visible unless protected by an outer caught `try`. Concise arrows always set `hasDirectValueReturn=true` and both throw facts false.

#### Code Edit 2.1

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralSupportTest.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

/** Exercises structural support boundaries independently from declaration recognition. */
class JavaScriptStructuralSupportTest {
  /** Preserves empty interiors while rejecting negative or reversed token ranges. */
  @Test
  void validatesPossiblyEmptyTokenRanges() {
    assertEquals(new JavaScriptTokenRange(2, 2), new JavaScriptTokenRange(2, 2));
    assertThrows(IllegalArgumentException.class, () -> new JavaScriptTokenRange(-1, 0));
    assertThrows(IllegalArgumentException.class, () -> new JavaScriptTokenRange(3, 2));
  }

  /** Rejects absent success and failure payloads in structural support results. */
  @Test
  void rejectsAbsentSupportResultPayloads() {
    assertThrows(NullPointerException.class,
        () -> new JavaScriptDelimiterIndex.BuildResult.Success(null));
    assertThrows(NullPointerException.class,
        () -> new JavaScriptDelimiterIndex.BuildResult.Failure(null));
    assertThrows(NullPointerException.class,
        () -> new JavaScriptFormalParameterParser.ParseResult.Failure(null));
    assertThrows(NullPointerException.class,
        () -> new JavaScriptFormalParameterParser.ParseResult.Success(null));
  }

  /** Matches every ordinary and template delimiter without crossing owners. */
  @Test
  void indexesNestedOrdinaryAndTemplateDelimiters() {
    var tokens = tokens("function f({value}) { return `${items.map(x => ({x}))}`; }");
    var result = assertInstanceOf(
        JavaScriptDelimiterIndex.BuildResult.Success.class,
        JavaScriptDelimiterIndex.build(tokens));

    for (var opening : List.of("(", "{", "[", "${")) {
      var index = firstIndex(tokens, opening);
      assertEquals(index, result.index().matchingIndex(result.index().matchingIndex(index)));
    }
  }

  /** Returns the first exact mismatched or unterminated delimiter as structural failure. */
  @Test
  void failsClosedOnDelimiterMismatchAndEndOfFile() {
    var mismatched = tokens("function f(] {}");
    var mismatch = assertInstanceOf(
        JavaScriptDelimiterIndex.BuildResult.Failure.class,
        JavaScriptDelimiterIndex.build(mismatched));
    assertEquals("]", mismatch.error().token().text());

    var unterminated = tokens("function f() {");
    var end = assertInstanceOf(
        JavaScriptDelimiterIndex.BuildResult.Failure.class,
        JavaScriptDelimiterIndex.build(unterminated));
    assertEquals("", end.error().token().text());
    assertEquals("unclosed '{' delimiter", end.error().message());
  }

  /** Claims module JSDoc once and distinguishes whitespace, comments, and semantic barriers. */
  @Test
  void resolvesExactSingleUseDocumentationAttachment() {
    var direct = tokens("/** module */ function f() {}");
    var resolver = new JavaScriptDocumentationResolver(direct);

    assertInstanceOf(JavaScriptDocumentationAttachment.Attached.class,
        resolver.resolveModule());
    assertInstanceOf(JavaScriptDocumentationAttachment.AlreadyClaimed.class,
        resolver.resolveModule());
    assertInstanceOf(JavaScriptDocumentationAttachment.AlreadyClaimed.class,
        resolver.resolveBefore(firstIndex(direct, "function")));

    var blocked = tokens("/** docs */ /* barrier */ function f() {}");
    var blockedResolver = new JavaScriptDocumentationResolver(blocked);
    var attachment = assertInstanceOf(JavaScriptDocumentationAttachment.Blocked.class,
        blockedResolver.resolveBefore(firstIndex(blocked, "function")));
    assertEquals("/* barrier */", attachment.barrier().text());
  }

  /** Parses ordinary, default, rest, aliased, nested, and defaulted object leaves. */
  @Test
  void parsesSupportedFormalPatternsWithoutInventingNames() {
    var tokens = tokens("function f(value, options = {}, ...rest) {}");
    var delimiters = delimiterIndex(tokens);
    var parameters = assertInstanceOf(
        JavaScriptFormalParameterParser.ParseResult.Success.class,
        JavaScriptFormalParameterParser.parse(
            tokens, delimiters, firstIndex(tokens, "("), firstIndex(tokens, ")")))
        .parameters();

    assertEquals(List.of("value", "options", "rest"), parameters.stream()
        .map(parameter -> ((JavaScriptFormalParameter.IdentifierPattern) parameter.pattern())
            .boundIdentifier())
        .toList());
    assertEquals(List.of(false, true, false),
        parameters.stream().map(JavaScriptFormalParameter::defaulted).toList());
    assertEquals(List.of(false, false, true),
        parameters.stream().map(JavaScriptFormalParameter::rest).toList());

    var objectTokens = tokens(
        "function g({account: {id: accountId = null}, signal, ...other}) {}");
    var objectParameters = assertInstanceOf(
        JavaScriptFormalParameterParser.ParseResult.Success.class,
        JavaScriptFormalParameterParser.parse(
            objectTokens,
            delimiterIndex(objectTokens),
            firstIndex(objectTokens, "("),
            firstIndex(objectTokens, ")")))
        .parameters();
    var leaves = ((JavaScriptFormalParameter.ObjectPattern)
        objectParameters.getFirst().pattern()).bindings();
    assertEquals(List.of("account.id", "signal", "other"), leaves.stream()
        .map(binding -> String.join(".", binding.propertyPath())).toList());
    assertEquals(List.of("accountId", "signal", "other"),
        leaves.stream().map(JavaScriptFormalParameter.ObjectBinding::boundIdentifier).toList());
    assertEquals(List.of(true, false, false),
        leaves.stream().map(JavaScriptFormalParameter.ObjectBinding::defaulted).toList());
    assertEquals(List.of(false, false, true),
        leaves.stream().map(JavaScriptFormalParameter.ObjectBinding::rest).toList());
  }

  /** Accepts only the lexer's exact contextual-keyword subset as binding identifiers. */
  @Test
  void parsesContextualBindingsAndRejectsReservedOrPrivateBindings() {
    var accepted = tokens("function f(async, from, get, of, set) {}");
    var parameters = assertInstanceOf(
        JavaScriptFormalParameterParser.ParseResult.Success.class,
        JavaScriptFormalParameterParser.parse(
            accepted,
            delimiterIndex(accepted),
            firstIndex(accepted, "("),
            firstIndex(accepted, ")"))).parameters();
    assertEquals(List.of("async", "from", "get", "of", "set"), parameters.stream()
        .map(parameter -> ((JavaScriptFormalParameter.IdentifierPattern) parameter.pattern())
            .boundIdentifier())
        .toList());

    for (var source : List.of("function f(return) {}", "function f(#private) {}")) {
      var rejected = tokens(source);
      assertInstanceOf(JavaScriptFormalParameterParser.ParseResult.Failure.class,
          JavaScriptFormalParameterParser.parse(
              rejected,
              delimiterIndex(rejected),
              firstIndex(rejected, "("),
              firstIndex(rejected, ")")),
          source);
    }
  }

  /** Fails closed on array, computed, method, and non-final rest formal syntax. */
  @Test
  void rejectsUnsupportedOrContradictoryFormalPatterns() {
    for (var source : List.of(
        "function f([first]) {}",
        "function f({[name]: value}) {}",
        "function f({method() {}}) {}",
        "function f(...rest, later) {}")) {
      var tokens = tokens(source);
      assertInstanceOf(JavaScriptFormalParameterParser.ParseResult.Failure.class,
          JavaScriptFormalParameterParser.parse(
              tokens, delimiterIndex(tokens), firstIndex(tokens, "("), firstIndex(tokens, ")")),
          source);
    }
  }

  /** Counts direct value returns and throws while excluding nested callable/class bodies. */
  @Test
  void analyzesOnlyDirectCallableBodyFacts() {
    var tokens = tokens("function outer() { if (ready) return value; "
        + "const nested = () => { throw new Error('nested'); }; "
        + "class Inner { method() { return hidden; } } throw failure; }");
    var delimiters = delimiterIndex(tokens);
    var outerOpen = nthIndex(tokens, "{", 1);
    var nestedOpen = nthIndex(tokens, "{", 2);
    var classOpen = nthIndex(tokens, "{", 3);
    var facts = JavaScriptBodyFactsAnalyzer.analyzeBlock(
        tokens,
        delimiters,
        new JavaScriptTokenRange(outerOpen + 1, delimiters.matchingIndex(outerOpen)),
        List.of(
            new JavaScriptTokenRange(nestedOpen, delimiters.matchingIndex(nestedOpen) + 1),
            new JavaScriptTokenRange(classOpen, delimiters.matchingIndex(classOpen) + 1)));

    assertEquals(new JavaScriptCallableBodyFacts(true, true, true), facts);
    assertEquals(new JavaScriptCallableBodyFacts(true, false, false),
        JavaScriptBodyFactsAnalyzer.analyzeConciseArrow());
  }

  /** Separates caught throws from rethrows that remain visible to the callable's caller. */
  @Test
  void distinguishesCaughtAndCallerVisibleThrows() {
    var source = "function caught() { try { throw hidden; } catch (error) { consume(error); } } "
        + "function rethrows() { try { risky(); } catch (error) { throw error; } } "
        + "function outerCatch() { try { try { risky(); } catch (error) { throw error; } } "
        + "catch (outer) { consume(outer); } }";
    var tokens = tokens(source);
    var delimiters = delimiterIndex(tokens);

    assertEquals(new JavaScriptCallableBodyFacts(false, true, false),
        analyzeNamedFunction(tokens, delimiters, "caught"));
    assertEquals(new JavaScriptCallableBodyFacts(false, true, true),
        analyzeNamedFunction(tokens, delimiters, "rethrows"));
    assertEquals(new JavaScriptCallableBodyFacts(false, true, false),
        analyzeNamedFunction(tokens, delimiters, "outerCatch"));
  }

  /**
   * Analyzes the first block body following one exact function name.
   *
   * @param tokens complete fixture token stream
   * @param delimiters complete fixture delimiter index
   * @param name exact function name
   * @return direct body facts for the named function
   */
  private static JavaScriptCallableBodyFacts analyzeNamedFunction(
      List<JavaScriptToken> tokens, JavaScriptDelimiterIndex delimiters, String name) {
    var nameIndex = firstIndex(tokens, name);
    var openingBrace = firstIndexAtOrAfter(tokens, "{", nameIndex + 1);
    return JavaScriptBodyFactsAnalyzer.analyzeBlock(
        tokens,
        delimiters,
        new JavaScriptTokenRange(openingBrace + 1, delimiters.matchingIndex(openingBrace)),
        List.of());
  }

  /**
   * Finds the first exact spelling at or after one token index.
   *
   * @param tokens complete fixture token stream
   * @param text exact token spelling
   * @param startInclusive first candidate token index
   * @return matching token index
   * @throws IllegalArgumentException when no token matches
   */
  private static int firstIndexAtOrAfter(
      List<JavaScriptToken> tokens, String text, int startInclusive) {
    for (var index = startInclusive; index < tokens.size(); index++) {
      if (tokens.get(index).text().equals(text)) {
        return index;
      }
    }
    throw new IllegalArgumentException("Fixture token was not found: " + text);
  }

  /**
   * Lexes a fixture through the completed immutable boundary.
   *
   * @param source complete JavaScript fixture
   * @return complete immutable token stream
   */
  private static List<JavaScriptToken> tokens(String source) {
    return assertInstanceOf(JavaScriptLexResult.Success.class, JavaScriptLexer.lex(source)).tokens();
  }

  /**
   * Builds a successful delimiter index for a fixture.
   *
   * @param tokens complete fixture token stream
   * @return complete delimiter index
   */
  private static JavaScriptDelimiterIndex delimiterIndex(List<JavaScriptToken> tokens) {
    return assertInstanceOf(JavaScriptDelimiterIndex.BuildResult.Success.class,
        JavaScriptDelimiterIndex.build(tokens)).index();
  }

  /**
   * Finds the first token with one exact spelling.
   *
   * @param tokens complete fixture token stream
   * @param text exact token spelling
   * @return first matching token index
   */
  private static int firstIndex(List<JavaScriptToken> tokens, String text) {
    return nthIndex(tokens, text, 1);
  }

  /**
   * Finds one one-based occurrence of an exact token spelling.
   *
   * @param tokens complete fixture token stream
   * @param text exact token spelling
   * @param occurrence one-based matching occurrence
   * @return matching token index
   * @throws AssertionError when the fixture lacks the requested occurrence
   */
  private static int nthIndex(List<JavaScriptToken> tokens, String text, int occurrence) {
    var seen = 0;
    for (var index = 0; index < tokens.size(); index++) {
      if (tokens.get(index).text().equals(text) && ++seen == occurrence) {
        return index;
      }
    }
    throw new AssertionError("Missing token occurrence " + occurrence + " for " + text);
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralSupportTest'
```

Expected first RED: the first support reflection bootstrap compiles and fails a JUnit assertion because the selected helper/behavior is absent. Bootstrap the five support types sequentially, then add each typed delimiter/attachment/formal/body behavior through its own assertion-failing RED; compiler errors are supplemental only.

#### Code Edit 2.2

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptTokenRange.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

/**
 * Identifies one possibly empty half-open range in a JavaScript token list.
 *
 * @param startInclusive first owned token index
 * @param endExclusive first token index after the range
 */
record JavaScriptTokenRange(int startInclusive, int endExclusive) {
  /**
   * Rejects negative or reversed token ranges while preserving valid empty interiors.
   *
   * @param startInclusive first owned token index
   * @param endExclusive first token index after the range
   * @throws IllegalArgumentException when either bound is negative or order is reversed
   */
  JavaScriptTokenRange {
    if (startInclusive < 0 || endExclusive < startInclusive) {
      throw new IllegalArgumentException("JavaScript token range must be nonnegative and ordered");
    }
  }

  /**
   * Reports whether one token index is owned by this range.
   *
   * @param index candidate token index
   * @return whether the index lies within the half-open range
   */
  boolean contains(int index) {
    return index >= startInclusive && index < endExclusive;
  }
}
```

Verification:

- Focused support tests use exact half-open nested body ranges, accept an empty body interior, and reject negative/reversed construction in added constructor assertions.

#### Code Edit 2.3

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDelimiterIndex.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Map;
import java.util.Objects;

/** Provides immutable symmetric delimiter partners for one successful lexical stream. */
final class JavaScriptDelimiterIndex {
  /** Symmetric immutable token-index partner map. */
  private final Map<Integer, Integer> partners;

  /**
   * Stores one already validated immutable partner map.
   *
   * @param partners symmetric delimiter partner map
   * @throws NullPointerException when the map or an entry is absent
   */
  private JavaScriptDelimiterIndex(Map<Integer, Integer> partners) {
    this.partners = Map.copyOf(partners);
  }

  /**
   * Builds exact delimiter ownership or returns the first structural failure.
   *
   * @param tokens complete successful lexical stream
   * @return complete delimiter index or first source failure
   * @throws NullPointerException when the list or a token is absent
   */
  static BuildResult build(List<JavaScriptToken> tokens) {
    return new Builder(List.copyOf(tokens)).build();
  }

  /**
   * Returns the matching delimiter index for a validated opening or closing index.
   *
   * @param delimiterIndex validated opening or closing token index
   * @return partner token index
   * @throws IllegalArgumentException when the index does not identify a matched delimiter
   */
  int matchingIndex(int delimiterIndex) {
    var partner = partners.get(delimiterIndex);
    if (partner == null) {
      throw new IllegalArgumentException("Token index does not identify a matched delimiter");
    }
    return partner;
  }

  /** Represents delimiter-index construction success or first source failure. */
  sealed interface BuildResult permits BuildResult.Success, BuildResult.Failure {
    /**
     * Carries one complete delimiter index.
     *
     * @param index complete immutable delimiter index
     */
    record Success(JavaScriptDelimiterIndex index) implements BuildResult {
      /**
       * Rejects an absent delimiter index.
       *
       * @param index complete immutable delimiter index
       * @throws NullPointerException when the index is absent
       */
      public Success { Objects.requireNonNull(index); }
    }
    /**
     * Carries the first mismatched or unclosed delimiter.
     *
     * @param error first delimiter failure
     */
    record Failure(JavaScriptStructuralError error) implements BuildResult {
      /**
       * Rejects an absent delimiter failure.
       *
       * @param error first delimiter failure
       * @throws NullPointerException when the error is absent
       */
      public Failure { Objects.requireNonNull(error); }
    }
  }
}
```

Implement the private documented `Builder` in the same file with this fixed contract:

1. It copies the nonnull token list, requires terminal EOF, and owns a local stack of documented `OpeningDelimiter` records.
2. It recognizes ordinary `(` / `)`, `[` / `]`, `{` / `}`, and lexer-owned `TEMPLATE_EXPRESSION_START` / `TEMPLATE_EXPRESSION_END` as four distinct pair categories.
3. It adds both directions to one mutable map only after a correct pair closes.
4. On an unexpected closer or mismatched category, it returns `Failure` anchored to that closer with an exact message naming expected and actual spelling.
5. At EOF with an unclosed stack, it reports the innermost opening category at EOF; it does not report a successful partial index.
6. Every field, nested record/component, enum constant, constructor, and private helper has accurate Javadocs. No helper returns null and no error is thrown for untrusted delimiter syntax.

Verification:

- Focused tests prove symmetric ownership, template separation, first mismatch, and EOF-anchored unclosed failure.

#### Code Edit 2.4

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDocumentationResolver.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/** Owns single-use JSDoc claims for one source-ordered structural scan. */
final class JavaScriptDocumentationResolver {
  /** Immutable successful lexical stream. */
  private final List<JavaScriptToken> tokens;
  /** JSDoc token indices already owned by the module or a declaration. */
  private final Set<Integer> claimedJavadocs = new HashSet<>();

  /**
   * Creates one scan-local resolver over a nonempty stream with terminal EOF.
   *
   * @param tokens complete successful lexical stream
   * @throws NullPointerException when the list or a token is absent
   * @throws IllegalArgumentException when the stream is empty or lacks terminal EOF
   */
  JavaScriptDocumentationResolver(List<JavaScriptToken> tokens) {
    this.tokens = List.copyOf(tokens);
    if (this.tokens.isEmpty()
        || this.tokens.getLast().kind() != JavaScriptTokenKind.EOF) {
      throw new IllegalArgumentException("Documentation tokens must end with EOF");
    }
  }

  /**
   * Resolves and, when present, claims the first token as module documentation.
   *
   * @return exact module attachment state
   */
  JavaScriptDocumentationAttachment resolveModule() {
    var first = tokens.getFirst();
    if (first.kind() == JavaScriptTokenKind.EOF) {
      return new JavaScriptDocumentationAttachment.Absent();
    }
    if (first.kind() == JavaScriptTokenKind.JAVADOC) {
      if (!claimedJavadocs.add(0)) {
        return new JavaScriptDocumentationAttachment.AlreadyClaimed(first);
      }
      return new JavaScriptDocumentationAttachment.Attached(first);
    }
    return new JavaScriptDocumentationAttachment.Blocked(first);
  }

  /**
   * Resolves and claims documentation immediately before one declaration-head index.
   *
   * @param declarationIndex semantic declaration-head token index
   * @return exact declaration attachment state
   * @throws IllegalArgumentException when the index is out of range or nonsemantic
   */
  JavaScriptDocumentationAttachment resolveBefore(int declarationIndex) {
    if (declarationIndex < 0 || declarationIndex >= tokens.size()) {
      throw new IllegalArgumentException("Declaration index is outside the token stream");
    }
    var declaration = tokens.get(declarationIndex);
    if (declaration.kind() == JavaScriptTokenKind.ORDINARY_COMMENT
        || declaration.kind() == JavaScriptTokenKind.JAVADOC
        || declaration.kind() == JavaScriptTokenKind.EOF) {
      throw new IllegalArgumentException("Declaration index must identify semantic syntax");
    }
    if (declarationIndex == 0) {
      return new JavaScriptDocumentationAttachment.Absent();
    }
    var precedingIndex = declarationIndex - 1;
    var preceding = tokens.get(precedingIndex);
    if (preceding.kind() != JavaScriptTokenKind.JAVADOC) {
      return new JavaScriptDocumentationAttachment.Blocked(preceding);
    }
    if (!claimedJavadocs.add(precedingIndex)) {
      return new JavaScriptDocumentationAttachment.AlreadyClaimed(preceding);
    }
    return new JavaScriptDocumentationAttachment.Attached(preceding);
  }
}
```

Verification:

- Focused tests prove module claim, declaration claim, already-claimed reuse prevention, exact ordinary-comment barrier, semantic barrier, and BOF absence.

#### Code Edit 2.5

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptFormalParameterParser.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Objects;

/** Parses the bounded formal-parameter grammar demonstrated by repository-owned JavaScript. */
final class JavaScriptFormalParameterParser {
  /** Prevents construction of the stateless parser. */
  private JavaScriptFormalParameterParser() {}

  /**
   * Parses tokens strictly between one proved parameter-list pair.
   *
   * @param tokens complete successful lexical stream
   * @param delimiters complete delimiter index for the stream
   * @param openingParenthesisIndex opening formal-list parenthesis index
   * @param closingParenthesisIndex matching closing parenthesis index
   * @return complete formals or first unsupported/malformed token
   * @throws NullPointerException when trusted inputs are absent
   * @throws IllegalArgumentException when supplied indices are not the proved pair
   */
  static ParseResult parse(
      List<JavaScriptToken> tokens,
      JavaScriptDelimiterIndex delimiters,
      int openingParenthesisIndex,
      int closingParenthesisIndex) {
    return new Cursor(
        List.copyOf(tokens), delimiters, openingParenthesisIndex, closingParenthesisIndex).parse();
  }

  /** Represents complete formal parsing or the first unsupported/malformed formal token. */
  sealed interface ParseResult permits ParseResult.Success, ParseResult.Failure {
    /**
     * Carries complete source-order formal parameters.
     *
     * @param parameters complete source-order formals
     */
    record Success(List<JavaScriptFormalParameter> parameters) implements ParseResult {
      /**
       * Copies the complete parameter list.
       *
       * @param parameters complete source-order formals
       * @throws NullPointerException when the list or a parameter is absent
       */
      public Success { parameters = List.copyOf(parameters); }
    }
    /**
     * Carries the first formal-structure failure.
     *
     * @param error first unsupported or malformed formal token
     */
    record Failure(JavaScriptStructuralError error) implements ParseResult {
      /**
       * Rejects an absent formal-structure failure.
       *
       * @param error first unsupported or malformed formal token
       * @throws NullPointerException when the error is absent
       */
      public Failure { Objects.requireNonNull(error); }
    }
  }
}
```

Implement the private documented `Cursor` in the same file with this exact grammar contract:

1. Validate that the supplied indices name a matched `(` / `)` pair and that no token access crosses the close.
2. Split formals only on commas at the parameter-list owner depth; use `JavaScriptDelimiterIndex` to skip nested object/default expression delimiters.
3. Parse an optional outer `...`, then either one lexer-proved binding identifier or one `{...}` object pattern, then an optional outer `= expression`. A binding identifier is an `IDENTIFIER` token whose text does not begin `#`, or a `KEYWORD` token with exactly one of `async`, `from`, `get`, `of`, or `set`; keep that documented set local to this parser because the lexer's set is intentionally private. Reject every other `KEYWORD` and private name at its exact token.
4. Require outer rest to be final and forbid its default.
5. Recursively flatten an object pattern in source order. Accept static identifier/keyword/string/number property names, shorthand, `property: local`, `property: {nested}`, leaf defaults, and final `...local` object rest. Outer formal rest accepts only an identifier binding, never an object pattern.
6. Preserve every nested static property segment and the actual bound identifier in `ObjectBinding`; never synthesize a name for the owning formal. For object rest, append its bound identifier as the final path segment under the current object owner so the immutable domain can prove rest ownership and finality.
7. Reject `[` array patterns, computed object keys, object methods/accessors, absent values, duplicate separators, non-final rest, rest defaults, and a nested value that is neither a supported identifier nor object pattern. Anchor the first error to the exact uncertain token.
8. Copy every returned list and document every field/helper/component/parameter/return/failure. Do not catch an internal invariant failure and translate it to an empty parameter list.

Verification:

- Focused tests prove empty, identifier, default, rest, nested object, alias, shorthand, leaf default, object rest, delimiter-aware default expressions, and every fail-closed partition above.

#### Code Edit 2.6

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptBodyFactsAnalyzer.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 1 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.Comparator;
import java.util.List;

/** Derives direct return, direct throw, and caller-visible throw facts from proved ranges. */
final class JavaScriptBodyFactsAnalyzer {
  /** Prevents construction of the stateless analyzer. */
  private JavaScriptBodyFactsAnalyzer() {}

  /**
   * Analyzes one block-body interior while skipping complete nested callable/class ranges.
   *
   * @param tokens complete successful lexical stream
   * @param delimiters complete delimiter index for the stream
   * @param bodyInterior possibly empty block-body interior
   * @param nestedBodies outermost nested callable/class exclusions
   * @return immutable direct return/throw facts
   * @throws NullPointerException when trusted inputs or elements are absent
   * @throws IllegalArgumentException when ranges are invalid, overlapping, or out of bounds
   */
  static JavaScriptCallableBodyFacts analyzeBlock(
      List<JavaScriptToken> tokens,
      JavaScriptDelimiterIndex delimiters,
      JavaScriptTokenRange bodyInterior,
      List<JavaScriptTokenRange> nestedBodies) {
    var immutableTokens = List.copyOf(tokens);
    var orderedNestedBodies = nestedBodies.stream()
        .sorted(Comparator.comparingInt(JavaScriptTokenRange::startInclusive))
        .toList();
    return analyze(immutableTokens, delimiters, bodyInterior, orderedNestedBodies);
  }

  /**
   * Returns the fixed direct-value fact for a concise arrow expression.
   *
   * @return value-return true with both throw facts false
   */
  static JavaScriptCallableBodyFacts analyzeConciseArrow() {
    return new JavaScriptCallableBodyFacts(true, false, false);
  }
}
```

Implement the private documented `analyze` and its focused helpers in the same file:

1. Validate that ranges are in bounds, ordered, nonoverlapping, and contained by the owner body.
2. Require the supplied exclusions to be the outermost nonoverlapping nested callable/class ranges relative to this owner, then advance over each entire range before inspecting its tokens. A class-body exclusion subsumes its method bodies for the surrounding owner; those methods are analyzed independently for their own candidates.
3. Treat `throw` at any non-skipped owner depth as direct. Before the fact scan, identify every syntactically complete `try` body in the owner that has an associated same-callable `catch`; record only that protected try-body interior, not its catch or finally body.
4. Treat `return` as value-bearing only when its next non-comment/JSDoc token occurs on the same line and is not `;`, `}`, `TEMPLATE_EXPRESSION_END`, or EOF. Ordinary/JSDoc comments after `return` do not create a value and a line change ends the statement.
5. Use delimiter partners only to advance safely; do not skip ordinary nested control/object blocks because their return/throw statements belong to the callable.
6. Set `hasCallerVisibleThrow` when at least one direct throw is outside every protected caught-try interior. A throw in a catch or finally is therefore visible unless it lies inside an outer protected caught-try interior; a rethrow follows the same rule. Fail with a programmer-facing invariant error if a structurally incomplete try/catch range reaches this already-proved helper.
7. Never infer exception types, promise rejection, unreachable flow, or documentation policy. B2 receives only the three syntax booleans and uses caller-visible throw rather than raw direct throw for `@throws` policy.
8. Document every helper and reject programmer-supplied invalid ranges rather than returning false facts.

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralSupportTest'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralDomainTest'
git diff --check
```

Expected GREEN: all support and domain fixtures pass with zero failures/errors. The implementer self-reviews, stages only the six Task 2 files, and commits before the controller generates the Task 2 review package:

```powershell
git add -- documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptTokenRange.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDelimiterIndex.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDocumentationResolver.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptFormalParameterParser.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptBodyFactsAnalyzer.java documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralSupportTest.java
git commit -m "Add JavaScript structural parsing support"
```

### Task 3 - Recognize repository-native declarations and exemptions

Sequence / dependencies:

- Runs only after Tasks 1 and 2 are committed and independently approved.
- Uses the completed lexer and Task 2 helpers without changing either boundary.
- Produces the complete B1 feature. The implementer commits independently as `Recognize JavaScript declarations` after focused, module, corpus, private-Javadoc, root-build, and self-review gates pass; the generated commit range then enters the independent task-review gate.

Expected files or modules:

- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralRecognizer.java`.
- Create `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclarationScanner.java`.
- Create `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralRecognizerTest.java`.

Interfaces:

- Consumes: exactly `JavaScriptLexResult.Success` through `JavaScriptStructuralRecognizer.recognize(JavaScriptLexResult.Success)`.
- Produces: one `JavaScriptStructuralResult`; `Success` exposes module attachment plus all declarations, while `Failure` exposes only a safe prefix and first structural error.
- Delegates: delimiter pairing, attachment ownership, formal parsing, and direct-body fact derivation only to Task 2 helpers.

Implementation notes:

- Required skill: `chris-street-style` before any code edits. Invoke it and `superpowers:test-driven-development` before creating the test or production files.
- Before-Edit Brief:
  - Behavior: every approved/current stable JavaScript callable or class value is emitted exactly once in source order; truly anonymous direct call/new callbacks are exempt; unsupported callable-looking syntax and malformed structure fail at the first uncertain token.
  - Invariants: input is lexical success; scan state is per call; contexts and owner paths are explicit; declaration names preserve source category; class/object/function bodies are traversed once; nested helpers are retained; direct facts exclude nested bodies; no partial failed candidate is emitted.
  - Boundary/API: one package-private facade method is the complete B1 entry point; one focused scanner owns grammar/context traversal; supporting responsibilities remain in Task 2 files; B2, discovery, violation, Gradle, and application modules have no dependency here.
  - Effects and failures: recognition is deterministic in-memory work over immutable tokens; source uncertainty returns `Failure`; null/trusted-invariant defects throw specific programmer errors; there is no I/O, logging, execution, concurrency, global mutation, or recovery.
  - Tests and evidence: bootstrap the facade/scanner through one reflection-invoked declaration fixture that catches reflection failures and fails by assertion, implement the minimum single declaration to GREEN, then add every structural grammar fixture one behavior at a time before its production branch. Finish with the complete module, exact corpus probe, direct private Javadocs, and root build.
- The scanner owns one documented mutable per-call cursor and explicit context frames. Do not split shared traversal ownership across independent rescans, and do not put parameter, body-fact, delimiter, or attachment algorithms back into the scanner.
- Recognize these declaration heads:
  - `function name`, `async function name`, generator `function * name`, and `export` / `export default` combinations at any nesting depth;
  - anonymous default-exported function declarations through `DefaultExport` identity;
  - `const` / `let` / `var` binding initialized to a function expression or arrow;
  - bare identifier and dotted static member assignment to a function expression or arrow;
  - named object property initialized to a function expression or arrow, including nested named object paths;
  - source-named function expressions even without a stable outer target, including returned/passed forms;
  - class declarations, anonymous default-exported class declarations, stable binding/identifier/member/object-property class expressions, and any source-named class expression;
  - constructors and static/async/accessor/private/generator class methods;
  - object shorthand methods and accessors;
  - all named members inside anonymous classes even when the class expression itself lacks a stable target.
- Recognize both synchronous and `async` arrows in single-parameter and parenthesized forms, and preserve `ASYNC` on their callable declarations.
- Preserve stable identity precedence: assignment/binding/property target first; otherwise a source expression name; otherwise approved anonymous default export; otherwise no class/callable declaration. Still traverse bodies when no outer declaration is emitted.
- For class/member owner paths, append static member names to the class's stable path. For an unbound anonymous class, use only the declared member's property segment and do not invent an anonymous-class name.
- For named object paths, carry a static parent path only when the object literal itself has a stable binding/member/property owner. A named property in an unbound object still receives its own source property path without a synthetic parent.
- Recognize direct anonymous argument exemption from syntactic context, not callee spelling:
  - arrow/function expression is the direct element of a `CallArguments` or `NewArguments` frame;
  - expression has no source name and no binding/member/property target;
  - scanner emits no declaration for that callback but recursively scans its parameter defaults and body for named nested declarations;
  - named function/class expressions and named properties nested inside an argument are not exempt.
- Object-versus-block classification must be explicit from the owning context: class body, function/control block, arrow block, object initializer/value, returned object, array element, call/new argument value, or template interpolation expression. If a callable-looking sequence depends on an unproved brace role, return an unsupported-syntax error.
- A computed key becomes an error only when lookahead proves callable/class-value shape. Ordinary computed reads, writes of non-callable values, and array indexing remain expressions.
- Scan once in source order and claim each declaration anchor once. The scanner may collect internal immutable candidates before body-fact materialization, but the result list must be source ordered and duplicate-free.

#### Code Edit 3.1

- File: `documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralRecognizerTest.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 2 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

/** Proves B1 declaration recognition against approved and repository-native forms. */
class JavaScriptStructuralRecognizerTest {
  /** Recognizes exported, async, generator, nested, bound, assigned, and returned functions. */
  @Test
  void recognizesFunctionAndArrowIdentityForms() {
    var result = success("""
        /** module */
        /** exported */ export async function load(value) { return value; }
        /** generator */ function * values() { yield 1; }
        /** bound */ const normalize = ({value}) => value;
        /** assigned */ handler = item => { throw item; };
        /** member */ player.sync = async () => true;
        function factory() { return function namedInner(input) { return input; }; }
        """);

    assertEquals(List.of(
        "load", "values", "normalize", "handler", "player.sync", "factory", "namedInner"),
        names(result));
    assertEquals(List.of(
        JavaScriptDeclaration.CallableKind.FUNCTION_DECLARATION,
        JavaScriptDeclaration.CallableKind.FUNCTION_DECLARATION,
        JavaScriptDeclaration.CallableKind.ARROW_FUNCTION,
        JavaScriptDeclaration.CallableKind.ARROW_FUNCTION,
        JavaScriptDeclaration.CallableKind.ARROW_FUNCTION,
        JavaScriptDeclaration.CallableKind.FUNCTION_DECLARATION,
        JavaScriptDeclaration.CallableKind.FUNCTION_EXPRESSION),
        callables(result).stream().map(JavaScriptDeclaration.Callable::kind).toList());
    assertInstanceOf(JavaScriptDeclarationName.BoundIdentifier.class,
        result.declarations().get(2).name());
    assertInstanceOf(JavaScriptDeclarationName.AssignedIdentifier.class,
        result.declarations().get(3).name());
    assertInstanceOf(JavaScriptDeclarationName.PropertyPath.class,
        result.declarations().get(4).name());
    assertInstanceOf(JavaScriptDeclarationName.SourceNamedExpression.class,
        result.declarations().get(6).name());
  }

  /** Distinguishes contextual async parameter identity from the async arrow modifier. */
  @Test
  void distinguishesContextualAsyncArrowForms() {
    var result = success("""
        /** module */
        const contextual = async => async;
        const asynchronous = async value => value;
        """);

    assertEquals(List.of(Set.of(), Set.of(JavaScriptDeclaration.Modifier.ASYNC)),
        callables(result).stream().map(JavaScriptDeclaration.Callable::modifiers).toList());
    assertEquals(List.of("async", "value"), callables(result).stream()
        .map(callable -> ((JavaScriptFormalParameter.IdentifierPattern)
            callable.parameters().getFirst().pattern()).boundIdentifier())
        .toList());
  }

  /** Recognizes named, stable-bound anonymous, and returned source-named classes plus members. */
  @Test
  void recognizesEveryStableClassValueAndNamedMember() {
    var result = success("""
        /** module */
        /** declared */ export class Player {
          /** ctor */ constructor(value) { this.value = value; }
          /** method */ async play() { return this.value; }
          /** private */ static * #items() { yield 1; }
        }
        /** bound */ globalThis.MediaMetadata = class {
          /** ctor */ constructor(details) { Object.assign(this, details); }
        };
        function reader() {
          /** returned */ return class DefaultFileReader {
            /** load */ loadRange(range) { return range; }
          };
        }
        """);

    assertEquals(List.of(
        "Player", "Player.constructor", "Player.play", "Player.#items",
        "globalThis.MediaMetadata", "globalThis.MediaMetadata.constructor",
        "reader", "DefaultFileReader", "DefaultFileReader.loadRange"), names(result));
    assertEquals(3, result.declarations().stream()
        .filter(JavaScriptDeclaration.ClassValue.class::isInstance).count());
    assertEquals(Set.of(
        JavaScriptDeclaration.Modifier.STATIC,
        JavaScriptDeclaration.Modifier.GENERATOR,
        JavaScriptDeclaration.Modifier.PRIVATE),
        callables(result).stream()
            .filter(callable -> callable.name().displayName().equals("Player.#items"))
            .findFirst().orElseThrow().modifiers());
  }

  /** Gives anonymous default-exported classes and their members one explicit stable owner path. */
  @Test
  void recognizesAnonymousDefaultExportClassMemberIdentity() {
    var result = success("""
        /** module */
        /** class */ export default class {
          /** ctor */ constructor() {}
          /** method */ load() { return true; }
        }
        """);

    assertEquals(List.of(
        "default export", "default export.constructor", "default export.load"), names(result));
    assertInstanceOf(JavaScriptDeclarationName.DefaultExport.class,
        result.declarations().getFirst().name());
    result.declarations().forEach(declaration ->
        assertInstanceOf(JavaScriptDocumentationAttachment.Attached.class,
            declaration.documentation()));
  }

  /** Recognizes object shorthand/accessor/property callables and stable class properties. */
  @Test
  void recognizesNamedObjectCallableAndClassProperties() {
    var result = success("""
        /** module */
        const context = {
          /** method */ parse(value) { return value; },
          /** getter */ get ready() { return true; },
          nested: {
            /** arrow */ fetch: async ({id: accountId}) => accountId,
            /** function */ save: function saveValue(value) { return value; },
          },
          /** class */ XMLHttpRequest: class {},
        };
        """);

    assertEquals(List.of(
        "context.parse", "context.ready", "context.nested.fetch",
        "context.nested.save", "context.XMLHttpRequest"), names(result));
    var fetch = callables(result).stream()
        .filter(callable -> callable.name().displayName().equals("context.nested.fetch"))
        .findFirst().orElseThrow();
    var leaf = ((JavaScriptFormalParameter.ObjectPattern)
        fetch.parameters().getFirst().pattern()).bindings().getFirst();
    assertEquals(List.of("id"), leaf.propertyPath());
    assertEquals("accountId", leaf.boundIdentifier());
  }

  /** Distinguishes contextual member names from actual modifiers and accessors. */
  @Test
  void distinguishesContextualGetSetAsyncAndStaticMemberNames() {
    var result = success("""
        /** module */
        class Contextual {
          get(name) {}
          get value() { return true; }
          set(name) {}
          set value(next) {}
          async() {}
          async load() {}
          static() {}
          static get ready() { return true; }
          static get constructor() { return Contextual; }
        }
        const object = {
          get(name) {}, get value() { return true; },
          set(name) {}, set value(next) {},
          async() {}, async load() {}, static() {},
        };
        """);

    assertEquals(List.of(
        JavaScriptDeclaration.CallableKind.CLASS_METHOD,
        JavaScriptDeclaration.CallableKind.CLASS_GETTER,
        JavaScriptDeclaration.CallableKind.CLASS_METHOD,
        JavaScriptDeclaration.CallableKind.CLASS_SETTER,
        JavaScriptDeclaration.CallableKind.CLASS_METHOD,
        JavaScriptDeclaration.CallableKind.CLASS_METHOD,
        JavaScriptDeclaration.CallableKind.CLASS_METHOD,
        JavaScriptDeclaration.CallableKind.CLASS_GETTER,
        JavaScriptDeclaration.CallableKind.CLASS_GETTER,
        JavaScriptDeclaration.CallableKind.OBJECT_METHOD,
        JavaScriptDeclaration.CallableKind.OBJECT_GETTER,
        JavaScriptDeclaration.CallableKind.OBJECT_METHOD,
        JavaScriptDeclaration.CallableKind.OBJECT_SETTER,
        JavaScriptDeclaration.CallableKind.OBJECT_METHOD,
        JavaScriptDeclaration.CallableKind.OBJECT_METHOD,
        JavaScriptDeclaration.CallableKind.OBJECT_METHOD),
        callables(result).stream().map(JavaScriptDeclaration.Callable::kind).toList());
    assertEquals(Set.of(JavaScriptDeclaration.Modifier.ASYNC),
        callables(result).stream()
            .filter(callable -> callable.name().displayName().equals("Contextual.load"))
            .findFirst().orElseThrow().modifiers());
    assertEquals(Set.of(JavaScriptDeclaration.Modifier.STATIC),
        callables(result).stream()
            .filter(callable -> callable.name().displayName().equals("Contextual.ready"))
            .findFirst().orElseThrow().modifiers());
  }

  /** Exempts only anonymous direct call/new arguments while retaining named nested helpers. */
  @Test
  void exemptsAnonymousDirectArgumentsWithoutDroppingNestedDeclarations() {
    var result = success("""
        /** module */
        test('case', async () => {
          /** nested */ function helper() { return true; }
        });
        new Promise(resolve => {
          /** nested arrow */ const finish = () => resolve();
          finish();
        });
        register(function namedCallback(value) { return value; });
        """);

    assertEquals(List.of("helper", "finish", "namedCallback"), names(result));
  }

  /** Claims module/declaration JSDoc once and preserves exact comment/semantic barriers. */
  @Test
  void preservesExactDocumentationOwnershipForB2() {
    var result = success("""
        /** module */
        function missingOwnBlock() {}
        /** blocked */ /* barrier */ function blocked() {}
        /** attached */ function attached() {}
        """);

    assertInstanceOf(JavaScriptDocumentationAttachment.Attached.class,
        result.moduleDocumentation());
    assertInstanceOf(JavaScriptDocumentationAttachment.AlreadyClaimed.class,
        result.declarations().get(0).documentation());
    var blocked = assertInstanceOf(JavaScriptDocumentationAttachment.Blocked.class,
        result.declarations().get(1).documentation());
    assertEquals("/* barrier */", blocked.barrier().text());
    assertInstanceOf(JavaScriptDocumentationAttachment.Attached.class,
        result.declarations().get(2).documentation());
  }

  /** Records direct facts for each owner and excludes nested callable/class bodies. */
  @Test
  void recordsOnlyDirectCallableBodyFacts() {
    var result = success("""
        /** module */
        function outer(flag) {
          if (flag) return value;
          const nested = () => { throw hidden; };
          class Inner { method() { return hidden; } }
          throw visible;
        }
        const bare = () => { return; };
        const concise = value => value;
        """);

    assertEquals(List.of(
        new JavaScriptCallableBodyFacts(true, true, true),
        new JavaScriptCallableBodyFacts(false, true, true),
        new JavaScriptCallableBodyFacts(true, false, false),
        new JavaScriptCallableBodyFacts(false, false, false),
        new JavaScriptCallableBodyFacts(true, false, false)),
        callables(result).stream().map(JavaScriptDeclaration.Callable::bodyFacts).toList());
  }

  /** Distinguishes caught throws, visible rethrows, and rethrows caught by an outer try. */
  @Test
  void recordsCallerVisibleThrowFacts() {
    var result = success("""
        /** module */
        function caught() { try { throw hidden; } catch (error) { consume(error); } }
        function rethrows() { try { risky(); } catch (error) { throw error; } }
        function outerCatch() {
          try { try { risky(); } catch (error) { throw error; } }
          catch (outer) { consume(outer); }
        }
        """);

    assertEquals(List.of(
        new JavaScriptCallableBodyFacts(false, true, false),
        new JavaScriptCallableBodyFacts(false, true, true),
        new JavaScriptCallableBodyFacts(false, true, false)),
        callables(result).stream().map(JavaScriptDeclaration.Callable::bodyFacts).toList());
  }

  /** Fails closed at callable-looking computed keys and returns no uncertain declaration. */
  @Test
  void rejectsComputedCallableKeysAndTargets() {
    for (var source : List.of(
        "const value = { [name]() {} };",
        "const value = { [name]: () => true };",
        "class Value { [name]() {} }",
        "target[name] = () => true;")) {
      var failure = assertInstanceOf(JavaScriptStructuralResult.Failure.class,
          recognize(source), source);
      assertEquals("[", failure.error().token().text());
      assertEquals("unsupported computed callable key", failure.error().message());
    }
  }

  /** Rejects an optional chain as a callable assignment target at its first invalid token. */
  @Test
  void rejectsOptionalChainCallableAssignmentTarget() {
    var failure = assertInstanceOf(JavaScriptStructuralResult.Failure.class,
        recognize("target?.handler = () => true;"));

    assertEquals("?.", failure.error().token().text());
    assertEquals("unsupported optional-chain assignment target", failure.error().message());
    assertEquals(List.of(), failure.declarations());
  }

  /** Rejects non-static constructor accessors while retaining static constructor properties. */
  @Test
  void rejectsReservedNonStaticConstructorAccessor() {
    var failure = assertInstanceOf(JavaScriptStructuralResult.Failure.class,
        recognize("class Value { get constructor() {} }"));

    assertEquals("constructor", failure.error().token().text());
    assertEquals("non-static constructor cannot be an accessor", failure.error().message());
  }

  /** Rejects the ECMAScript-reserved private constructor name at its exact token. */
  @Test
  void rejectsPrivateConstructorMemberName() {
    var failure = assertInstanceOf(JavaScriptStructuralResult.Failure.class,
        recognize("class Value { #constructor() {} }"));

    assertEquals("#constructor", failure.error().token().text());
    assertEquals("private member cannot be named #constructor", failure.error().message());
  }

  /** Retains only completed candidates and never leaks a malformed head into failure prefix. */
  @Test
  void returnsOnlyFullyRecognizedFailurePrefix() {
    var unsupportedFormal = assertInstanceOf(JavaScriptStructuralResult.Failure.class,
        recognize("function good() {} const bad = ([first]) => first;"));
    assertEquals(List.of("good"), unsupportedFormal.declarations().stream()
        .map(declaration -> declaration.name().displayName()).toList());
    assertEquals("[", unsupportedFormal.error().token().text());

    var delimiterFailure = assertInstanceOf(JavaScriptStructuralResult.Failure.class,
        recognize("function good() {} function broken(] {}"));
    assertEquals(List.of(), delimiterFailure.declarations());
    assertEquals("]", delimiterFailure.error().token().text());
  }

  /** Rejects absent input while exposing no API for lexical failure or source text. */
  @Test
  void acceptsOnlySuccessfulLexicalInput() {
    assertThrows(NullPointerException.class, () -> JavaScriptStructuralRecognizer.recognize(null));
  }

  /**
   * Returns complete structure for one valid source fixture.
   *
   * @param source complete valid JavaScript fixture
   * @return successful immutable structure
   */
  private static JavaScriptStructuralResult.Success success(String source) {
    return assertInstanceOf(JavaScriptStructuralResult.Success.class, recognize(source));
  }

  /**
   * Lexes then recognizes one valid fixture through the two explicit boundaries.
   *
   * @param source complete JavaScript fixture
   * @return structural success or first failure
   */
  private static JavaScriptStructuralResult recognize(String source) {
    var lexical = assertInstanceOf(JavaScriptLexResult.Success.class, JavaScriptLexer.lex(source));
    return JavaScriptStructuralRecognizer.recognize(lexical);
  }

  /**
   * Returns every declaration's stable display identity in source order.
   *
   * @param result successful structural result
   * @return source-order declaration display names
   */
  private static List<String> names(JavaScriptStructuralResult.Success result) {
    return result.declarations().stream().map(declaration -> declaration.name().displayName()).toList();
  }

  /**
   * Returns only callable declarations in source order.
   *
   * @param result successful structural result
   * @return source-order callable declarations
   */
  private static List<JavaScriptDeclaration.Callable> callables(
      JavaScriptStructuralResult.Success result) {
    return result.declarations().stream()
        .filter(JavaScriptDeclaration.Callable.class::isInstance)
        .map(JavaScriptDeclaration.Callable.class::cast)
        .toList();
  }
}
```

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralRecognizerTest'
```

Expected first RED: a reflection bootstrap fixture lexes one simple named function, attempts to invoke the absent recognizer, catches reflection absence, and fails an exact JUnit assertion that one declaration was expected. Add only the facade/scanner path for that declaration to GREEN, replace the bootstrap after the equivalent strongly typed simple-function fixture proves its own RED/GREEN, and then follow the micro-cycle protocol for every remaining grammar partition; compiler errors never count as RED.

Accumulate this exact test file through individually observed RED/GREEN micro-cycles for every approved/current partition not fully shown in the compact examples above; do not add the list as one broad pre-production batch:

- plain/exported/default-exported/async/generator function declarations and anonymous default function identity;
- function expression targets for lexical binding, assigned identifier, member path, object property, source-named return, and anonymous return exclusion;
- synchronous/async arrows with single, parenthesized, multiline, default, object-destructured, and rest formals plus concise/object/block bodies;
- anonymous function/arrow/class values used as parameter defaults remain non-declarations, while source-named expressions and named properties nested inside those defaults remain declarations;
- all five stable-bound anonymous class shapes from the current corpus and the returned named class shape;
- class constructor, async/static/private/generator methods, getter, setter, nested class, and unbound anonymous-class member traversal;
- nested synchronous/async/generator object methods, getter/setter, function property, arrow property, and stable class property;
- ordinary/optional-call/new anonymous exemptions, an exempt array-destructured callback, named direct argument expressions, named property inside an argument object, and named nested helper inside each exempt parameter-default/body range;
- module/decl JSDoc across whitespace, ordinary comment, semantic barrier, and already-claimed ownership;
- direct bare/value returns, ASI line break, concise arrows, nested control blocks, nested callables/classes, direct/nested throws, caught throws, visible rethrows, and rethrows protected by an outer caught try;
- mismatched/unclosed delimiters, unsupported array formal, unsupported computed callable keys, and ambiguous callable-looking brace ownership;
- exact declaration anchor line/column/offset, deterministic ordering, immutable result lists, and duplicate-free nested traversal.

Each added test must contain literal hand-derived expected names/kinds/facts and must be observed failing for the missing recognizer behavior before that production branch is added.

#### Code Edit 3.2

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralRecognizer.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 2 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.List;
import java.util.Objects;

/** Converts one complete lexical stream into immutable repository-native JavaScript structure. */
final class JavaScriptStructuralRecognizer {
  /** Prevents construction of the stateless recognizer boundary. */
  private JavaScriptStructuralRecognizer() {}

  /**
   * Recognizes complete structure from an already successful lexical result.
   *
   * @param lexicalResult complete immutable lexer success
   * @return complete immutable structure or first fail-closed structural error
   * @throws NullPointerException when the lexical success is absent
   */
  static JavaScriptStructuralResult recognize(JavaScriptLexResult.Success lexicalResult) {
    var tokens = List.copyOf(Objects.requireNonNull(lexicalResult).tokens());
    var documentation = new JavaScriptDocumentationResolver(tokens);
    var moduleDocumentation = documentation.resolveModule();
    return switch (JavaScriptDelimiterIndex.build(tokens)) {
      case JavaScriptDelimiterIndex.BuildResult.Failure failure ->
          new JavaScriptStructuralResult.Failure(
              moduleDocumentation, List.of(), failure.error());
      case JavaScriptDelimiterIndex.BuildResult.Success success ->
          new JavaScriptDeclarationScanner(
              tokens, success.index(), documentation, moduleDocumentation).scan();
    };
  }
}
```

Verification:

- The package has exactly one B1 entry point and the Java type system prevents a lexical failure from reaching it.

#### Code Edit 3.3

- File: `documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclarationScanner.java`
- Lines: 1
- Action: add

Current:

```text
Absent after the independently approved Task 2 commit.
```

Proposed:

```java
package dev.christopherbell.tools.documentation;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Owns one source-ordered context traversal over a complete JavaScript token stream. */
final class JavaScriptDeclarationScanner {
  /** Complete immutable lexical tokens. */
  private final List<JavaScriptToken> tokens;
  /** Complete immutable delimiter ownership. */
  private final JavaScriptDelimiterIndex delimiters;
  /** Single-use documentation owner for this traversal. */
  private final JavaScriptDocumentationResolver documentation;
  /** Module documentation fact copied into every result variant. */
  private final JavaScriptDocumentationAttachment moduleDocumentation;
  /** Completed internal candidates in source order. */
  private final List<Candidate> candidates = new ArrayList<>();
  /** First structural failure, or null while recognition remains safe. */
  private JavaScriptStructuralError error;

  /**
   * Creates one per-call scanner over already validated support boundaries.
   *
   * @param tokens complete successful lexical stream
   * @param delimiters complete delimiter ownership
   * @param documentation scan-local documentation resolver
   * @param moduleDocumentation exact module attachment state
   * @throws NullPointerException when required state or a token is absent
   * @throws IllegalArgumentException when the token stream is empty or lacks terminal EOF
   */
  JavaScriptDeclarationScanner(
      List<JavaScriptToken> tokens,
      JavaScriptDelimiterIndex delimiters,
      JavaScriptDocumentationResolver documentation,
      JavaScriptDocumentationAttachment moduleDocumentation) {
    this.tokens = List.copyOf(tokens);
    if (this.tokens.isEmpty() || this.tokens.getLast().kind() != JavaScriptTokenKind.EOF) {
      throw new IllegalArgumentException("Scanner tokens must end with EOF");
    }
    this.delimiters = Objects.requireNonNull(delimiters);
    this.documentation = Objects.requireNonNull(documentation);
    this.moduleDocumentation = Objects.requireNonNull(moduleDocumentation);
  }

  /**
   * Traverses each token exactly once by owner and materializes immutable declarations.
   *
   * @return complete immutable structure or the first structural failure
   */
  JavaScriptStructuralResult scan() {
    scanRange(new JavaScriptTokenRange(0, tokens.size()), Context.MODULE, List.of());
    return materializeResult();
  }
}
```

Implement the rest of this file through focused documented private types/helpers with the following fixed ownership contract. This is deliberately one traversal owner; do not absorb the already separated Task 2 algorithms into it.

1. `Context` is a documented private enum with documented constants `MODULE`, `BLOCK`, `FUNCTION_BODY`, `CLASS_BODY`, `OBJECT_LITERAL`, `ARRAY_LITERAL`, `CALL_ARGUMENTS`, `NEW_ARGUMENTS`, `PARAMETER_DEFAULT`, and `TEMPLATE_EXPRESSION`.
2. `Candidate` is a documented private immutable record containing declaration kind, stable name, anchor/head index, attachment, modifier set, parsed formals, body range or concise-arrow marker, and the outermost nonoverlapping nested callable/class ranges relative to that body. Its compact constructor copies collections and rejects incomplete combinations. No candidate escapes the scanner.
3. `scanRange(JavaScriptTokenRange range, Context context, List<String> ownerPath)` advances monotonically. It dispatches declaration heads, proved object/class/function bodies, calls/new arguments, arrays, and template expressions; otherwise it advances one semantic unit by delimiter partner. It never rescans a completed owned body from its parent.
4. A declaration-head recognizer returns a documented immutable `Recognition` containing the exclusive next token index and every owned body range. Absence is represented by a documented `NotRecognized` case; source uncertainty calls `fail(JavaScriptToken, String)` once and returns a `Failed` case. Do not use nullable indices or exceptions for expected grammar rejection.
5. Export modifiers are consumed only as part of a proved function/class declaration head. `export default` anonymous function/class declarations use `DefaultExport`; named forms use `BoundIdentifier` plus `DEFAULT_EXPORTED`.
6. Lexical bindings claim only the individual declarator whose initializer is callable/class. A comma starts another declarator; its identity and attachment are resolved independently. Destructured variable targets used for callable/class assignment fail at the first pattern token because no single stable declaration identity exists.
7. Assignment targets accept a bare lexer-proved identifier or ordinary static dot-member chain without computed or optional-chain segments. Bare assignment uses `AssignedIdentifier`; member assignment uses `PropertyPath`. A callable-looking computed target fails at its opening bracket, and a callable-valued optional-chain assignment fails at `?.` with `unsupported optional-chain assignment target`; optional chains remain valid only for expression/call detection.
8. Function recognition handles optional `async`, `function`, optional `*`, optional source name, proved parameter pair, and proved block body. A missing required declaration name, missing parameter/body delimiter, or malformed formal returns the first structural error. A named expression without target uses `SourceNamedExpression`; an anonymous direct call/new argument emits no candidate; an unbound anonymous return emits no candidate; anonymous default export uses `DefaultExport`.
9. Arrow recognition uses lookahead and token lines before assigning contextual `async`: `async => value` is a synchronous single-parameter arrow whose binding is named `async`, while `async value => value` and `async (value) => value` carry `ASYNC` only with no line terminator after `async`. It then proves either a single approved binding identifier or a matched parenthesized list followed by `=>`, followed by a matched block or one delimiter-aware concise expression. The target rules in items 6-7/object properties provide identity. A direct anonymous call/new arrow emits no candidate; because it has no B1 formal model, the scanner does not invoke the fail-closed documentable-formal parser for that exempt head, but it still traverses its complete parameter/default range and body for nested named declarations.
10. Class recognition handles declaration/expression, optional source name, optional `extends` expression through the proved body opening brace, then scans the class body. Emit a class candidate when identity comes from declaration/binding/assignment/property/source name/default export. Derive the member-owner path without erasing identity: reuse `PropertyPath.segments()`, use the single identifier for bound/assigned/source-named identities, and use the literal single segment `default export` for `DefaultExport`; append each member segment to that path. Thus anonymous `export default class { load() {} }` yields class identity `DefaultExport` and member `PropertyPath(List.of("default export", "load"))`. Do not emit an unbound anonymous class candidate, but always scan its named members.
11. Class-member recognition uses delimiter-aware lookahead before treating contextual words as modifiers. `get`/`set`/`async`/`static` followed immediately by `(` are ordinary member names; `get` or `set` is an accessor modifier only when another static name is followed by the formal `(`; `async` is a modifier only with no intervening line terminator and another method name or `*`; `static` is a modifier only when another member head follows. After optional proved `static`, `async`, accessor, and `*` roles in grammar order, accept one static IdentifierName/private/string/number member name, a matched formal pair, and matched body. Non-static terminal `constructor` maps to `CONSTRUCTOR`; `static constructor()` remains `CLASS_METHOD`; a non-static getter/setter named `constructor` fails at that name with `non-static constructor cannot be an accessor`; static accessors named `constructor` remain allowed. Any private member/accessor token `#constructor` fails at that token with `private member cannot be named #constructor`. Other accessors map to getter/setter kinds and all remaining methods map to `CLASS_METHOD`. Enforce getter/setter/constructor/private invariants before domain construction and again in domain constructors.
12. Object classification is driven by the parent expression/declarator context. Object-member recognition applies the same `get`/`set`/`async` lookahead (`get(name)`, `set(name)`, and `async()` are ordinary method names), while `static()` is always an ordinary object method name because object members have no static modifier. It accepts static-name synchronous/`async`/generator shorthand methods and getters/setters, `key: function`, `key: arrow`, `key: class`, and nested `key: { ... }`. It records `ASYNC`/`GENERATOR` on shorthand object methods where present. Carry a stable parent path when one exists; otherwise begin the property path at the current static key. A spread property is traversed only as an expression and never invents a property identity.
13. When `[` begins a class/object/member key or assignment target, look through its matched `]`. If the following shape is `(`, `: function`, `: class`, `: <arrow head>`, or `= <arrow/function/class head>`, fail at `[` with exactly `unsupported computed callable key`. Otherwise treat it as an ordinary computed expression.
14. Ordinary and optional-call/new argument recognition uses the matched argument `(` and top-level commas, including current `target?.method?.(...)` and `callable?.(...)` forms. It passes `CALL_ARGUMENTS` or `NEW_ARGUMENTS` only to direct argument expressions; nested object properties and named expressions retain normal identity rules. For an exempt direct anonymous function/arrow, `scanExemptFormalRange` traverses the proved parameter tokens as expression/default syntax without creating `JavaScriptFormalParameter` values, so current array-destructured callbacks remain accepted and any named function/class/arrow nested in a default expression remains discoverable. The same array formal on any documentable callable still fails at `[`.
15. Every emitted candidate receives `documentation.resolveBefore(headIndex)` exactly once. Head index is the earliest token owned by that declaration (`export`, `async`, `function`, or `class` for declarations; the binding keyword for the first declarator and the bound identifier for each later comma-separated declarator; the assignment target; the first class modifier/name; or the object key). Comments inside a proved modifier/head sequence are syntactic trivia but cannot become that declaration's attachment because they are not immediately before its earliest head token.
16. After traversal succeeds, materialize candidate body facts with `JavaScriptBodyFactsAnalyzer`, create domain declarations, sort by anchor offset, and reject any duplicate anchor as an internal invariant failure. On source failure, materialize only candidates anchored before the error and return `Failure`.
17. Direct nested-body exclusions cover every function, arrow, and class body found inside the owner, whether or not that nested value emitted a declaration because of the callback/class exemption, but are normalized to the outermost nonoverlapping ranges relative to that owner. Therefore an outer callable excludes a nested class body once (which subsumes its methods), while each class method candidate separately excludes its own nested callable/class bodies.
18. Parameter-default traversal starts strictly after the formal's default `=` in `PARAMETER_DEFAULT` context. The formal binding and its `=` never become an assignment-target identity for an anonymous default function/arrow/class (including the current dependency-injection defaults); source-named expressions and named properties/classes inside the default expression are still recognized normally. Exempt formal traversal applies the same rule without constructing a formal model.
19. Every field, constructor, context constant, record component, helper parameter/return/failure, and private method has accurate Javadocs. No helper has a comment-only body, catches `Exception`, returns null, or silently skips callable-looking syntax.

Verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralRecognizerTest'
.\gradlew.bat --no-daemon :documentation-validator:test
$sourceFiles = Get-ChildItem -Recurse -Filter '*.java' 'documentation-validator\src\main\java'
& javadoc -private -quiet -d 'documentation-validator\build\reports\private-javadocs-javascript-structure' $sourceFiles.FullName
.\gradlew.bat --no-daemon build
git diff --check
git status --short
```

Expected GREEN: focused recognizer tests, all structural support/domain tests, and the complete validator suite pass with zero failures/errors; the established Windows discovery skip is allowed. Private Javadocs exit 0 without warnings, the root build exits 0, and `git diff --check` exits 0.

Run the following read-only corpus probe after compiling Task 3. It creates no source file and performs no production integration. The probe must report the fixed declaration, formal, and direct-body inventory: 96 lexical successes, 96 structural successes, 1,240 callable declarations, 19 class-value declarations, 1,259 total declarations, 1,135 formals, 38 object patterns, 152 object leaves, one rest formal, 793 value-return callables, and 74 direct-throw callables. It also reports the reviewed caller-visible-throw subset:

```powershell
$repo = 'A:\Projects\christopherbell.dev-worktrees\repository-documentation-coverage-20260729'
$classPath = Join-Path $repo 'documentation-validator\build\classes\java\main'
$probe = @'
import java.nio.file.*;
import java.util.*;
var root = Path.of("A:/Projects/christopherbell.dev-worktrees/repository-documentation-coverage-20260729");
var lexer = Class.forName("dev.christopherbell.tools.documentation.JavaScriptLexer");
var lex = lexer.getDeclaredMethod("lex", String.class);
lex.setAccessible(true);
var successType = Class.forName("dev.christopherbell.tools.documentation.JavaScriptLexResult$Success");
var recognizer = Class.forName("dev.christopherbell.tools.documentation.JavaScriptStructuralRecognizer");
var recognize = recognizer.getDeclaredMethod("recognize", successType);
recognize.setAccessible(true);
var callableType = Class.forName("dev.christopherbell.tools.documentation.JavaScriptDeclaration$Callable");
var classType = Class.forName("dev.christopherbell.tools.documentation.JavaScriptDeclaration$ClassValue");
var objectPatternType = Class.forName(
    "dev.christopherbell.tools.documentation.JavaScriptFormalParameter$ObjectPattern");
var parametersMethod = callableType.getDeclaredMethod("parameters");
var bodyFactsMethod = callableType.getDeclaredMethod("bodyFacts");
var patternMethod = Class.forName("dev.christopherbell.tools.documentation.JavaScriptFormalParameter")
    .getDeclaredMethod("pattern");
var restMethod = Class.forName("dev.christopherbell.tools.documentation.JavaScriptFormalParameter")
    .getDeclaredMethod("rest");
var bindingsMethod = objectPatternType.getDeclaredMethod("bindings");
var valueReturnMethod = Class.forName(
    "dev.christopherbell.tools.documentation.JavaScriptCallableBodyFacts")
    .getDeclaredMethod("hasDirectValueReturn");
var directThrowMethod = Class.forName(
    "dev.christopherbell.tools.documentation.JavaScriptCallableBodyFacts")
    .getDeclaredMethod("hasDirectThrow");
var visibleThrowMethod = Class.forName(
    "dev.christopherbell.tools.documentation.JavaScriptCallableBodyFacts")
    .getDeclaredMethod("hasCallerVisibleThrow");
for (var method : List.of(parametersMethod, bodyFactsMethod, patternMethod, restMethod,
    bindingsMethod, valueReturnMethod, directThrowMethod, visibleThrowMethod)) {
  method.setAccessible(true);
}
List<Path> files;
try (var paths = Files.walk(root)) {
  files = paths.filter(path -> path.toString().endsWith(".js"))
      .filter(path -> !path.toString().replace('\\', '/').contains("/build/"))
      .filter(path -> !path.toString().replace('\\', '/').contains("/static/vendor/"))
      .sorted().toList();
}
int lexicalSuccesses = 0;
int structuralSuccesses = 0;
int callables = 0;
int classes = 0;
int formals = 0;
int objectPatterns = 0;
int objectLeaves = 0;
int restFormals = 0;
int valueReturns = 0;
int directThrows = 0;
int callerVisibleThrows = 0;
for (var file : files) {
  var lexical = lex.invoke(null, Files.readString(file));
  if (!lexical.getClass().getSimpleName().equals("Success")) {
    throw new IllegalStateException("Lexical failure: " + root.relativize(file));
  }
  lexicalSuccesses++;
  var structure = recognize.invoke(null, lexical);
  if (!structure.getClass().getSimpleName().equals("Success")) {
    throw new IllegalStateException("Structural failure: " + root.relativize(file) + " " + structure);
  }
  structuralSuccesses++;
  var declarationsMethod = structure.getClass().getDeclaredMethod("declarations");
  declarationsMethod.setAccessible(true);
  var declarations = (List<?>) declarationsMethod.invoke(structure);
  for (var declaration : declarations) {
    if (callableType.isInstance(declaration)) {
      callables++;
      var parameters = (List<?>) parametersMethod.invoke(declaration);
      formals += parameters.size();
      for (var parameter : parameters) {
        if ((boolean) restMethod.invoke(parameter)) restFormals++;
        var pattern = patternMethod.invoke(parameter);
        if (objectPatternType.isInstance(pattern)) {
          objectPatterns++;
          objectLeaves += ((List<?>) bindingsMethod.invoke(pattern)).size();
        }
      }
      var facts = bodyFactsMethod.invoke(declaration);
      if ((boolean) valueReturnMethod.invoke(facts)) valueReturns++;
      if ((boolean) directThrowMethod.invoke(facts)) directThrows++;
      if ((boolean) visibleThrowMethod.invoke(facts)) callerVisibleThrows++;
    } else if (classType.isInstance(declaration)) {
      classes++;
    } else {
      throw new IllegalStateException("Unknown declaration type " + declaration.getClass());
    }
  }
}
System.out.println("files=" + files.size() + " lexical=" + lexicalSuccesses
    + " structural=" + structuralSuccesses + " callables=" + callables
    + " classes=" + classes + " total=" + (callables + classes)
    + " formals=" + formals + " objectPatterns=" + objectPatterns
    + " objectLeaves=" + objectLeaves + " restFormals=" + restFormals
    + " valueReturns=" + valueReturns + " directThrows=" + directThrows
    + " callerVisibleThrows=" + callerVisibleThrows);
/exit
'@
$probe | jshell --class-path $classPath
```

Expected final line:

```text
files=96 lexical=96 structural=96 callables=1240 classes=19 total=1259 formals=1135 objectPatterns=38 objectLeaves=152 restFormals=1 valueReturns=793 directThrows=74 callerVisibleThrows=N
```

All values before `callerVisibleThrows` are fixed accepted inventory and must match literally. `callerVisibleThrows` must be an integer from zero through 74, must be strictly lower than 74 if the current corpus contains any same-callable caught throw, and must be preserved as review evidence alongside named caught/rethrow spot checks; it is not pre-pinned because the approved inventory recorded raw direct throws only.

If the probe differs, stop. Inspect each delta against the fixed identity/exemption policy and either correct a recognizer bug under a new RED fixture or return the plan to review if accepted inventory evidence is wrong. Do not change the expected totals merely to make the probe green.

After the corpus probe and implementer self-review pass, stage only the three Task 3 files and commit; the controller then generates the Task 3 review package and dispatches its independent task reviewer:

```powershell
git add -- documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptStructuralRecognizer.java documentation-validator/src/main/java/dev/christopherbell/tools/documentation/JavaScriptDeclarationScanner.java documentation-validator/src/test/java/dev/christopherbell/tools/documentation/JavaScriptStructuralRecognizerTest.java
git commit -m "Recognize JavaScript declarations"
```

### Task 4 - Run whole-phase review and freeze the B2 input boundary

Sequence / dependencies:

- Runs after the three implementation commits and their task-level reviews are complete.
- Makes no planned source edit. A Critical or Important finding returns to the owning task with a new failing regression fixture, one narrow corrective commit, and repeated task/final review.

Expected files or modules:

- No planned file changes.
- Review the complete B1 diff from `affed13149c07ec5c024e20325a0333c2efd374f` through the Task 3 head.

Implementation notes:

- Required skill: `chris-street-style` before any corrective code edit. Invoke it and `superpowers:test-driven-development` if review identifies a required semantic change.
- Before-Edit Brief for any correction:
  - Behavior: correct only the proven structural misrecognition while preserving every already approved declaration/exemption and immutable boundary.
  - Invariants: lexical files, B2 policy, discovery, violations, build wiring, application JavaScript, and authoritative checkout remain unchanged.
  - Boundary/API: preserve `recognize(JavaScriptLexResult.Success)` and the reviewed domain signatures unless the plan is returned to `ready-for-review` for an API change.
  - Effects and failures: correction remains pure/in-memory and fail-closed; no integration or external mutation.
  - Tests and evidence: first capture the review counterexample as a failing focused fixture, then run the same fixture to GREEN and repeat all task/final gates.

Review checklist:

1. Confirm the facade has no lexical-failure/string/path/file overload and no source reread.
2. Trace all 1,259 corpus declarations to a stable identity category; specifically inspect the five stable-bound anonymous classes and returned named class.
3. Inspect representative examples from every inventory category and all 96 structural successes.
4. Prove generic direct call/new anonymous exemption and named nested-helper retention without a callee allowlist.
5. Prove property paths remain distinct from bound and assigned identifiers.
6. Prove module/declaration JSDoc single-use attachment across whitespace, comment barriers, semantic barriers, and already-claimed state.
7. Prove 1,135 formal positions, 38 object patterns, 152 object leaves, and one rest parameter are represented without invented names.
8. Prove 793 direct value-return and 74 direct-throw facts, inspect the caller-visible-throw subset, and prove counterexamples with caught throws, visible rethrows, outer catches, and nested callbacks/classes.
9. Prove computed callable-looking keys fail at `[` while ordinary computed expressions remain accepted.
10. Confirm every production/test type, field, constructor, method, helper, record component, parameter, return, failure, and enum constant has accurate Javadocs.
11. Confirm no B2 tag rule, violation conversion, discovery/file I/O, Gradle/CI wiring, remediation, README, or integration code entered the diff.

Task-level verification:

```powershell
$env:GRADLE_USER_HOME='A:\Projects\christopherbell.dev-worktrees\.gradle-documentation-coverage'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralDomainTest'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralSupportTest'
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralRecognizerTest'
.\gradlew.bat --no-daemon :documentation-validator:test
$sourceFiles = Get-ChildItem -Recurse -Filter '*.java' 'documentation-validator\src\main\java'
& javadoc -private -quiet -d 'documentation-validator\build\reports\private-javadocs-javascript-structure' $sourceFiles.FullName
.\gradlew.bat --no-daemon build
git diff --check affed13149c07ec5c024e20325a0333c2efd374f..HEAD
git status --short --branch
```

Also rerun the exact Task 3 corpus probe and the authoritative-checkout status hash. Require a clean isolated worktree, unchanged authoritative hash, exact fixed `96/96/1240/19/1259/1135/38/152/1/793/74` corpus output plus the reviewed caller-visible subset, zero test failures/errors, no private-Javadoc warnings, no whitespace errors, and a final review verdict with no Critical or Important finding.

## Code Changes

- Task 1, add `JavaScriptDocumentationAttachment.java`: exact attached/blocked/already-claimed/absent documentation ownership.
- Task 1, add `JavaScriptDeclarationName.java`: binding, assigned identifier, property path, source-named expression, and default-export identities.
- Task 1, add `JavaScriptFormalParameter.java`: one-based formals and object-pattern leaf bindings.
- Task 1, add `JavaScriptCallableBodyFacts.java`: direct syntactic value-return/throw facts plus the caller-visible throw subset.
- Task 1, add `JavaScriptDeclaration.java`: sealed callable/class-value declarations, kinds, and modifiers.
- Task 1, add `JavaScriptStructuralError.java`: exact first structural error token/message.
- Task 1, add `JavaScriptStructuralResult.java`: immutable complete or first-failure result.
- Task 1, add `JavaScriptStructuralDomainTest.java`: constructor and immutability contract tests.
- Task 2, add `JavaScriptTokenRange.java`: validated half-open token ranges.
- Task 2, add `JavaScriptDelimiterIndex.java`: matched ordinary/template delimiters and first error.
- Task 2, add `JavaScriptDocumentationResolver.java`: one-scan JSDoc claim ownership.
- Task 2, add `JavaScriptFormalParameterParser.java`: bounded current formal grammar.
- Task 2, add `JavaScriptBodyFactsAnalyzer.java`: direct return/throw analysis excluding nested bodies.
- Task 2, add `JavaScriptStructuralSupportTest.java`: focused delimiter/attachment/formal/body tests.
- Task 3, add `JavaScriptStructuralRecognizer.java`: sole B1 facade accepting lexical success.
- Task 3, add `JavaScriptDeclarationScanner.java`: context-owned declaration traversal.
- Task 3, add `JavaScriptStructuralRecognizerTest.java`: declaration, exemption, error, and attachment fixtures.

No existing file is modified by the planned B1 implementation.

## Unit Testing

Task 1 RED/GREEN:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralDomainTest'
```

Task 2 RED/GREEN:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralSupportTest'
```

Task 3 RED/GREEN:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test --tests '*JavaScriptStructuralRecognizerTest'
```

Complete validator regression:

```powershell
.\gradlew.bat --no-daemon :documentation-validator:test
```

The permanent fixture suite must prove domain validation/immutability; ordinary/template delimiter ownership; documentation single-use/barriers; supported/unsupported formals; direct body-fact ownership; all function/arrow/class/object forms; stable identities; anonymous call/new exemption; nested-helper retention; exact errors; exact coordinates; and deterministic order.

## Local Testing

No Spring application launch, browser session, MongoDB, service restart, or production listener action is required. B1 production code is an unwired pure build-time component and never launches Node; the mandatory root Gradle `build` does invoke the repository's existing `:website:jsTest` task and therefore uses the installed Node runtime as verification only.

Local evidence consists of:

- focused structural tests;
- complete validator tests;
- direct private-Javadoc generation;
- exact read-only 96-file corpus probe;
- existing Node JavaScript tests through the root build's `:website:jsTest` dependency;
- root Gradle build;
- `git diff --check`;
- clean isolated worktree after commits; and
- unchanged authoritative-checkout hash.

## Validation

- Task 1 shows assertion-failing reflection/behavior REDs and immutable-domain GREEN after each micro-cycle.
- Task 2 shows assertion-failing support-behavior REDs and delimiter/attachment/formal/body GREEN after each micro-cycle.
- Task 3 shows an assertion-failing reflection facade RED followed by one-behavior-at-a-time declaration-recognition RED/GREEN cycles.
- The facade accepts only `JavaScriptLexResult.Success`; lexical failure cannot be inspected or recovered.
- The current corpus reports exactly 96 lexical successes, 96 structural successes, 1,240 callables, 19 class values, and 1,259 total declarations.
- The five stable-bound anonymous class expressions and one returned source-named class expression are class declarations; anonymous unbound class expressions are not, while their named members remain declarations.
- Anonymous direct call/new callback counts remain exemptions (784 call, 21 constructor, including 270 Node test callbacks); named direct expressions/properties/nested helpers remain declarations.
- Current formal output totals 1,135 positions, 38 object patterns, 152 object leaves, and one rest parameter.
- Current body facts total 793 callables with direct value return and 74 with direct throw; caller-visible throw is a reviewed subset that excludes same-callable caught throws and drives later B2 `@throws` policy.
- Unsupported callable-looking computed keys fail at their first `[` and object-destructuring `for ... of` remains a lexical failure outside B1.
- Every result, list, set, property path, parameter leaf list, delimiter map, and error is immutable or scan-local with one owner.
- Full validator tests, private Javadocs, root build, corpus probe, whitespace check, and independent reviews pass.
- No B2 policy, discovery/file I/O, violation conversion, Gradle/CI wiring, remediation, README, application, or integration change exists.

## Rollback or Recovery

- Revert the Task 3 commit to remove declaration recognition while retaining reviewed structural support/domain values.
- Revert Task 2 after Task 3 to remove structural support while retaining the domain contract.
- Revert Task 1 last to remove the entire B1 phase.
- Do not reset or clean either checkout. Preserve RED/GREEN output, corpus totals, private-Javadoc output, and review findings until the phase is accepted.
- If a fixture exposes a contradiction in the approved grammar or count policy, stop at RED and return this Builder plan to `ready-for-review`; do not broaden the grammar or edit expected totals without approval.
- If Gradle registry/file locks occur, use only the isolated `GRADLE_USER_HOME`; stop only the daemon proven to own that isolated lock and retry once.
- A structural failure in one current file is not recoverable by skipping the file or declaration. Keep the first error and fix the recognizer contract under TDD or return the plan for review.

## Risks

- **Object versus block ambiguity:** explicit parent contexts and fail-closed callable-looking ambiguity prevent an object method from being silently skipped or a control block from becoming an object.
- **Duplicate traversal:** one monotonic owner scan, owned body ranges, and strict anchor ordering prevent class/object/nested callables from being emitted twice.
- **False callback exemptions:** syntactic direct argument frames plus source-name/target checks prevent a broad API allowlist from exempting named work.
- **Anonymous class undercount:** fixed tests and corpus totals cover all five stable-bound anonymous classes, the returned named class, and named members of unbound anonymous classes.
- **Attachment reuse:** a scan-local claimed-JSDoc set and exact `AlreadyClaimed` state prevent module documentation or one declaration block from satisfying a second target.
- **Destructuring name invention:** formal/object leaf types preserve property paths and local bindings separately and reject unsupported patterns.
- **Nested return/throw leakage:** explicit nested callable/class ranges prevent inner behavior from changing an owner's B2 facts.
- **Computed-name false identity:** callable-looking computed keys fail visibly instead of being rendered as unstable strings.
- **Core scanner size:** delimiter, documentation, formal, body, and immutable-domain responsibilities are separate files; the remaining scanner stays focused on context traversal because splitting that single ownership would invite rescans and duplicate claims.
- **Current-corpus drift:** the exact probe is pinned to head evidence; any delta stops execution for review rather than silently rewriting expected totals.
- **Branch drift from mainline:** integration is outside B1; do not hide it with a rebase or merge during this phase.

## Completion Criteria

- All 17 planned Java files exist in exactly three independently reviewed spoke commits; no existing file is changed.
- The plan has been reviewed and explicitly promoted from `ready-for-review` before any spoke edit begins.
- Structural domain constructors reject every contradictory attachment, name, formal, callable/class, ordering, prefix, and mutability state described above.
- Task 2 helpers own delimiter, JSDoc claim, formal, and direct-body behavior independently from declaration traversal, including caught-versus-caller-visible throw classification.
- `JavaScriptStructuralRecognizer.recognize(JavaScriptLexResult.Success)` is the only B1 entry point and is pure, deterministic, package-private, and JDK-only.
- All approved/current function, arrow, class, class-member, object-method, accessor, and named-property forms are emitted exactly once with exact identity, anchor, documentation fact, formals, modifiers, and body facts.
- Anonymous direct call/new functions/arrows are exempt only when they have no stable identity; nested named declarations are retained.
- The exact corpus probe reports `files=96 lexical=96 structural=96 callables=1240 classes=19 total=1259 formals=1135 objectPatterns=38 objectLeaves=152 restFormals=1 valueReturns=793 directThrows=74`, plus a reviewed integer caller-visible-throw subset.
- Focused tests, complete validator tests, direct private Javadocs, root build, and whitespace validation pass from clean commits.
- Task-level and final reviews find no remaining Critical or Important issue.
- The authoritative dirty checkout is unchanged, and no B2, discovery, violation, Gradle/CI, remediation, README, integration, push, PR, merge, application, or production action occurred.
- The immutable B1 success boundary is ready for a separately reviewed B2 JSDoc policy plan.
