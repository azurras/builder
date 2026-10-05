# Java

Use the repository's Java version, build, formatting and nullability conventions.
- Prefer records for immutable data, enums/sealed alternatives for closed states, and validated constructors for invariants. Do not default to factories or interfaces without a boundary.
- Distinguish Optional absence from domain rejection and exceptions. Preserve exception causes; avoid broad catch-and-continue.
- Keep constructor injection for stable dependencies; pass per-operation data explicitly. Avoid hidden static state.
- Use try-with-resources, explicit transaction boundaries and bounded executor/task ownership. Propagate interruption and cancellation.
- For persistence changes, test actual constraints, transaction behavior, query bounds and old/new data compatibility.
- Apply repository-native unit/integration tools; test public behavior rather than mocks or framework wiring already covered elsewhere.

## Implementation Recipe

1. Inspect the supported JDK, neighboring package/API style, nullability rules, and formatter. Use only supported language features.
2. Choose a record/value class for data whose invariants survive construction; use closed alternatives for genuinely distinct states. Validate the joint invariant in the constructor, not only at one caller.
3. Read each actual invocation as a sentence. Parameter names complement the method: `sendInvoiceTo(Invoice invoice, Recipient recipient)`. Give same-type inputs distinct role names; use enums or role types when accidental misuse is likely.
4. State whether each operation can be absent, rejected, or fail. Use Optional for documented absence, a domain result for an expected choice where native policy calls for it, and a specific exception for failure. Inspect public consumers before changing that contract.
5. Make resource and transaction boundaries explicit. Use try-with-resources, own executor/task lifetimes, and propagate cancellation/interruption according to the existing contract. Awaiting a future does not itself guarantee cancellation of its work.
6. Compile, apply native analysis, and test constructors, public outcomes, causes, cleanup, and real persistence constraints where relevant.

## Good and Bad Resource Ownership

Bad method fragment (imports and containing class omitted):

```java
long countLinesIn(Path filePath) throws IOException {
    return Files.lines(filePath).count();
}
```

The stream owns a file resource but has no guaranteed close.

Good method fragment with the same contract:

```java
long countLinesIn(Path filePath) throws IOException {
    try (Stream<String> lines = Files.lines(filePath)) {
        return lines.count();
    }
}
```

The scope owns cleanup even when processing fails. Use native imports from `java.nio.file`, `java.io`, and `java.util.stream`. Keep the IOException visible to the caller instead of converting unreadability into a zero-line file.

## Evidence and Review

Use the complete [TimeWindow example](good-and-bad-examples.md#3-model-an-invariant-instead-of-trusting-a-comment) for constructor-enforced invariants and sentence-like predicates. Review callers before renaming public methods or reflective properties. Test the actual boundary: database transaction/constraint behavior needs integration evidence; compile success alone does not prove it. New factories/interfaces need a present invariant, consumer, or effect seam.
